#!/usr/bin/env node
/**
 * bot_vision_headless — capture_headless.js
 *
 * Headless browser capture using Playwright + Chromium.
 * Produces screen_*.png + sidecar JSON into vision_inbox with atomic write.
 * Classifies captures as ready / blocked / invalid_visual.
 *
 * Usage:
 *   node capture_headless.js --profile profiles.example.json --once
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ── Config ──────────────────────────────────────────────
const TMP_DIR = process.env.BOT_VISION_TMP || '/tmp/bot_vision_headless';
const OUT_DIR = process.env.BOT_VISION_OUT || '/srv/sftp/shared_files/shared/vision_inbox';
const VIEWPORT = { width: 1920, height: 1080 };
const PAGE_TIMEOUT = 30000;
const POST_LOAD_WAIT_MS = 3000;
const WAIT_UNTIL = 'networkidle';
const SCREENSHOT_MODE = 'viewport';
const MIN_FILE_SIZE = 1024; // 1 KB minimum

// Status constants
const STATUS_READY = 'ready';
const STATUS_BLOCKED = 'blocked';
const STATUS_INVALID_VISUAL = 'invalid_visual';

// Blocked reasons
const BLOCKED_PAGE_GOTO_TIMEOUT = 'PAGE_GOTO_TIMEOUT';
const BLOCKED_PAGE_GOTO_ERROR = 'PAGE_GOTO_ERROR';
const BLOCKED_SCREENSHOT_ERROR = 'SCREENSHOT_ERROR';
const BLOCKED_OUTPUT_WRITE_ERROR = 'OUTPUT_WRITE_ERROR';

// Visual status values
const VISUAL_UNCHECKED = 'unchecked';
const VISUAL_PASS = 'pass';
const VISUAL_POSSIBLE_SPINNER = 'possible_spinner';
const VISUAL_BLANK_OR_UNIFORM = 'blank_or_uniform';
const VISUAL_TOO_SMALL = 'too_small';
const VISUAL_LOADING_STATE_DETECTED = 'loading_state_detected';

// Detection defaults
const DEFAULT_LOADING_SELECTORS = ['loading', 'spinner', 'please wait', 'loader', 'progress'];
const BLANK_PNG_SIZE_THRESHOLD = 15360; // 15 KB heuristic for uniform/blank image
const VISUAL_CHECK_ENABLED = true;

const VALID_WAIT_UNTIL = new Set(['networkidle', 'domcontentloaded', 'load']);
const VALID_SCREENSHOT_MODE = new Set(['viewport']);

// ── Parse args ──────────────────────────────────────────
const args = process.argv.slice(2);
let profilePath = null;
let once = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--profile' && args[i + 1]) { profilePath = args[++i]; }
  if (args[i] === '--once') { once = true; }
}

if (!profilePath) {
  console.error('Usage: capture_headless.js --profile <file> [--once]');
  process.exit(1);
}

if (!fs.existsSync(profilePath)) {
  console.error(`Profile not found: ${profilePath}`);
  process.exit(1);
}

const profiles = JSON.parse(fs.readFileSync(profilePath, 'utf-8'));

// ── Helpers ─────────────────────────────────────────────
function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function ts() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}_${pad(d.getHours())}-${pad(d.getMinutes())}-${pad(d.getSeconds())}`;
}

function atomicWrite(destDir, baseName, content, isJson = false) {
  const data = isJson ? JSON.stringify(content, null, 2) : content;
  const tmpSuffix = '.uploading';
  const finalName = path.join(destDir, baseName);
  const tmpName = finalName + tmpSuffix;

  // Clean stale .uploading > 5 min
  cleanupStaleUploads(destDir);

  fs.writeFileSync(tmpName, data);
  const stat = fs.statSync(tmpName);

  if (stat.size < MIN_FILE_SIZE && !isJson) {
    fs.unlinkSync(tmpName);
    console.error(`WARN: file too small (${stat.size}B), removed: ${tmpName}`);
    return null;
  }

  if (stat.size === 0) {
    fs.unlinkSync(tmpName);
    console.error(`WARN: empty file, removed: ${tmpName}`);
    return null;
  }

  fs.renameSync(tmpName, finalName);
  console.log(`OK: ${finalName} (${stat.size}B)`);
  return finalName;
}

function cleanupStaleUploads(dir) {
  if (!fs.existsSync(dir)) return;
  const files = fs.readdirSync(dir);
  const now = Date.now();
  for (const f of files) {
    if (!f.endsWith('.uploading')) continue;
    const fp = path.join(dir, f);
    const st = fs.statSync(fp);
    if (now - st.mtimeMs > 5 * 60 * 1000) {
      fs.unlinkSync(fp);
      console.log(`CLEANUP: removed stale ${fp}`);
    }
  }
}

function numberOption(value, defaultValue, name, { min = 0 } = {}) {
  if (value === undefined || value === null) return defaultValue;
  const n = Number(value);
  if (!Number.isFinite(n) || n < min) {
    throw new Error(`Invalid ${name}: ${value}`);
  }
  return Math.trunc(n);
}

function profileOptions(profile) {
  const waitUntil = profile.wait_until || WAIT_UNTIL;
  if (!VALID_WAIT_UNTIL.has(waitUntil)) {
    throw new Error(`Invalid wait_until: ${waitUntil}`);
  }

  const screenshotMode = profile.screenshot_mode || SCREENSHOT_MODE;
  if (!VALID_SCREENSHOT_MODE.has(screenshotMode)) {
    throw new Error(`Invalid screenshot_mode: ${screenshotMode}`);
  }

  return {
    waitUntil,
    timeoutMs: numberOption(profile.timeout_ms, PAGE_TIMEOUT, 'timeout_ms', { min: 1 }),
    postLoadWaitMs: numberOption(profile.post_load_wait_ms, POST_LOAD_WAIT_MS, 'post_load_wait_ms'),
    screenshotMode,
    visualCheckEnabled: profile.visual_check_enabled !== undefined ? !!profile.visual_check_enabled : VISUAL_CHECK_ENABLED,
    domLoadingSelectors: Array.isArray(profile.dom_loading_selectors) ? profile.dom_loading_selectors : DEFAULT_LOADING_SELECTORS
  };
}

// ── Visual classification ───────────────────────────────
async function classifyVisual(pngPath, page, loadingSelectors) {
  // 1. File size check
  const stat = fs.statSync(pngPath);
  if (stat.size < MIN_FILE_SIZE) {
    return { visualStatus: VISUAL_TOO_SMALL, status: STATUS_INVALID_VISUAL };
  }

  // 2. Blank/uniform heuristic: very small PNG at viewport resolution
  if (stat.size < BLANK_PNG_SIZE_THRESHOLD) {
    return { visualStatus: VISUAL_BLANK_OR_UNIFORM, status: STATUS_INVALID_VISUAL };
  }

  // 3. DOM loading text detection
  try {
    const loadingDetected = await page.evaluate((selectors) => {
      const bodyText = (document.body && document.body.innerText) || '';
      return selectors.some(s => bodyText.toLowerCase().includes(s.toLowerCase()));
    }, loadingSelectors);

    if (loadingDetected) {
      return { visualStatus: VISUAL_LOADING_STATE_DETECTED, status: STATUS_INVALID_VISUAL };
    }
  } catch (_) {
    // DOM not accessible; proceed
  }

  // 4. Document readyState check
  try {
    const readyState = await page.evaluate(() => document.readyState);
    if (readyState !== 'complete') {
      return { visualStatus: VISUAL_POSSIBLE_SPINNER, status: STATUS_INVALID_VISUAL };
    }
  } catch (_) {
    // DOM not accessible; proceed
  }

  return { visualStatus: VISUAL_PASS, status: STATUS_READY };
}

// ── Blocked sidecar writer ──────────────────────────────
function writeBlockedSidecar(baseJson, profile, options, blockedReason, errorMessage) {
  const { source, symbol, timeframe, url, page_id } = profile;
  const sidecar = {
    producer: 'bot_vision_headless',
    capture_mode: 'playwright_chromium',
    page_id: page_id || null,
    source,
    symbol: symbol || 'dashboard',
    timeframe: timeframe || 'H1',
    url,
    status: STATUS_BLOCKED,
    blocked_reason: blockedReason,
    capture_error: errorMessage,
    wait_until: options.waitUntil,
    timeout_ms: options.timeoutMs,
    post_load_wait_ms: options.postLoadWaitMs,
    created_at_utc: new Date().toISOString()
  };

  const result = atomicWrite(OUT_DIR, baseJson, sidecar, true);
  if (result) {
    console.log(`BLOCKED: ${source} ${symbol || ''} -> ${baseJson} (${blockedReason})`);
  } else {
    console.error(`FAIL: could not write blocked sidecar for ${source}`);
  }
}

// ── Capture ─────────────────────────────────────────────
async function captureOne(profile) {
  const { page_id: pageId, source, symbol, timeframe, url } = profile;
  if (!source || !url) {
    console.error(`Invalid profile (missing source/url): ${JSON.stringify(profile)}`);
    return;
  }

  let options;
  try {
    options = profileOptions(profile);
  } catch (err) {
    console.error(`Invalid profile options for ${source} ${symbol || ''}: ${err.message}`);
    return;
  }

  const tsStr = ts();
  const basePng = `screen_${source}_${symbol || 'dashboard'}_${timeframe || 'H1'}_${tsStr}.png`;
  const baseJson = basePng.replace('.png', '.json');

  console.log(`\n[${tsStr}] Capturing: ${source} ${symbol || ''} (${url})`);
  console.log(`LOAD: wait_until=${options.waitUntil} timeout_ms=${options.timeoutMs} post_load_wait_ms=${options.postLoadWaitMs} screenshot_mode=${options.screenshotMode}`);

  ensureDir(TMP_DIR);
  ensureDir(OUT_DIR);

  let browser;
  let page;
  try {
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({
      viewport: VIEWPORT,
      userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    });

    page = await context.newPage();
    page.setDefaultTimeout(options.timeoutMs);

    // ── Page navigation ──────────────────────────────
    let gotoError = null;
    try {
      await page.goto(url, { waitUntil: options.waitUntil, timeout: options.timeoutMs });
    } catch (err) {
      gotoError = err;
    }

    if (gotoError) {
      const reason = gotoError.name === 'TimeoutError' ? BLOCKED_PAGE_GOTO_TIMEOUT : BLOCKED_PAGE_GOTO_ERROR;
      writeBlockedSidecar(baseJson, profile, options, reason, gotoError.message);
      console.error(`BLOCKED: ${source} goto failed: ${gotoError.message}`);
      return;
    }

    // ── Post-load wait ───────────────────────────────
    if (options.postLoadWaitMs > 0) {
      await page.waitForTimeout(options.postLoadWaitMs);
    }

    // ── Screenshot ───────────────────────────────────
    let pngBuffer;
    let screenshotError = null;
    try {
      pngBuffer = await page.screenshot({ type: 'png', fullPage: false });
    } catch (err) {
      screenshotError = err;
    }

    if (screenshotError) {
      writeBlockedSidecar(baseJson, profile, options, BLOCKED_SCREENSHOT_ERROR, screenshotError.message);
      console.error(`BLOCKED: ${source} screenshot failed: ${screenshotError.message}`);
      return;
    }

    // ── Write PNG ────────────────────────────────────
    let pngPath = null;
    try {
      pngPath = atomicWrite(OUT_DIR, basePng, pngBuffer);
    } catch (err) {
      writeBlockedSidecar(baseJson, profile, options, BLOCKED_OUTPUT_WRITE_ERROR, err.message);
      console.error(`BLOCKED: ${source} PNG write failed: ${err.message}`);
      return;
    }

    if (!pngPath) {
      // atomicWrite returned null (too small); treat as invalid_visual
      const sidecar = {
        producer: 'bot_vision_headless',
        capture_mode: 'playwright_chromium',
        page_id: pageId || null,
        source,
        symbol: symbol || 'dashboard',
        timeframe: timeframe || 'H1',
        url,
        status: STATUS_INVALID_VISUAL,
        visual_status: VISUAL_TOO_SMALL,
        wait_until: options.waitUntil,
        timeout_ms: options.timeoutMs,
        post_load_wait_ms: options.postLoadWaitMs,
        screenshot_mode: options.screenshotMode,
        viewport: VIEWPORT,
        created_at_utc: new Date().toISOString()
      };
      atomicWrite(OUT_DIR, baseJson, sidecar, true);
      console.error(`INVALID_VISUAL: ${source} PNG too small`);
      return;
    }

    // ── Visual classification ─────────────────────────
    let visualStatus = VISUAL_UNCHECKED;
    let captureStatus = STATUS_READY;

    if (options.visualCheckEnabled) {
      try {
        const result = await classifyVisual(pngPath, page, options.domLoadingSelectors);
        visualStatus = result.visualStatus;
        captureStatus = result.status;
      } catch (err) {
        console.error(`VISUAL CHECK ERROR: ${err.message}`);
        visualStatus = VISUAL_UNCHECKED;
        captureStatus = STATUS_READY;
      }
    } else {
      visualStatus = VISUAL_UNCHECKED;
    }

    // ── Write sidecar JSON ────────────────────────────
    const sidecar = {
      producer: 'bot_vision_headless',
      capture_mode: 'playwright_chromium',
      page_id: pageId || null,
      source,
      symbol: symbol || 'dashboard',
      timeframe: timeframe || 'H1',
      url,
      status: captureStatus,
      visual_status: visualStatus,
      wait_until: options.waitUntil,
      timeout_ms: options.timeoutMs,
      post_load_wait_ms: options.postLoadWaitMs,
      screenshot_mode: options.screenshotMode,
      viewport: VIEWPORT,
      created_at_utc: new Date().toISOString(),
      output_png: basePng,
      output_json: baseJson
    };

    atomicWrite(OUT_DIR, baseJson, sidecar, true);

    if (captureStatus === STATUS_INVALID_VISUAL) {
      console.log(`INVALID_VISUAL: ${source} -> ${basePng} (${visualStatus})`);
    } else {
      console.log(`DONE: ${source} -> ${basePng}`);
    }
  } catch (err) {
    // Unexpected error (browser launch, context creation, etc.)
    console.error(`ERROR capturing ${source}: ${err.message}`);
    try {
      writeBlockedSidecar(baseJson, profile, options || {
        waitUntil: WAIT_UNTIL,
        timeoutMs: PAGE_TIMEOUT,
        postLoadWaitMs: POST_LOAD_WAIT_MS
      }, BLOCKED_PAGE_GOTO_ERROR, err.message);
    } catch (_) {
      // Best-effort sidecar
    }
  } finally {
    if (browser) await browser.close();
  }
}

// ── Main ────────────────────────────────────────────────
(async () => {
  cleanupStaleUploads(OUT_DIR);

  const list = Array.isArray(profiles) ? profiles : [profiles];

  for (const profile of list) {
    await captureOne(profile);
  }

  console.log('\nCapture cycle complete.');
})();
