#!/usr/bin/env node
/**
 * bot_vision_headless — capture_headless.js
 *
 * Headless browser capture using Playwright + Chromium.
 * Produces screen_*.png + sidecar JSON into vision_inbox with atomic write.
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
const MIN_FILE_SIZE = 1024; // 1 KB minimum

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

// ── Capture ─────────────────────────────────────────────
async function captureOne(profile) {
  const { source, symbol, timeframe, url } = profile;
  if (!source || !url) {
    console.error(`Invalid profile (missing source/url): ${JSON.stringify(profile)}`);
    return;
  }

  const tsStr = ts();
  const basePng = `screen_${source}_${symbol || 'dashboard'}_${timeframe || 'H1'}_${tsStr}.png`;
  const baseJson = basePng.replace('.png', '.json');

  console.log(`\n[${tsStr}] Capturing: ${source} ${symbol || ''} (${url})`);

  ensureDir(TMP_DIR);
  ensureDir(OUT_DIR);

  let browser;
  try {
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({
      viewport: VIEWPORT,
      userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    });

    const page = await context.newPage();
    page.setDefaultTimeout(PAGE_TIMEOUT);

    await page.goto(url, { waitUntil: 'networkidle', timeout: PAGE_TIMEOUT });

    // Extra wait for charts to render
    await page.waitForTimeout(3000);

    const pngBuffer = await page.screenshot({ type: 'png', fullPage: false });

    // Write PNG
    const pngPath = atomicWrite(OUT_DIR, basePng, pngBuffer);
    if (!pngPath) {
      console.error(`FAIL: screenshot produced no valid output for ${source}`);
      return;
    }

    // Write sidecar JSON
    const sidecar = {
      producer: 'bot_vision_headless',
      capture_mode: 'playwright_chromium',
      source,
      symbol: symbol || 'dashboard',
      timeframe: timeframe || 'H1',
      url,
      viewport: VIEWPORT,
      created_at_utc: new Date().toISOString(),
      output_png: basePng,
      output_json: baseJson,
      status: 'ready'
    };

    atomicWrite(OUT_DIR, baseJson, sidecar, true);

    console.log(`DONE: ${source} -> ${basePng}`);
  } catch (err) {
    console.error(`ERROR capturing ${source}: ${err.message}`);
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
