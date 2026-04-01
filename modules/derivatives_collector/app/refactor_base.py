import sys
import re

collector_file = "modules/derivatives_collector/app/derivatives_collector.py"
binance_file = "modules/derivatives_collector/app/binance_adapter.py"
bitget_file = "modules/derivatives_collector/app/bitget_adapter.py"

# 1. Update derivatives_collector.py
with open(collector_file, "r") as f:
    text = f.read()

text = text.replace("import random\n", "import random\nimport time\nimport urllib.request\nimport urllib.error\nimport concurrent.futures\n")

base_adapter_old = """class BaseAdapter:
    def collect(self, symbols):
        raise NotImplementedError"""

base_adapter_new = """class BaseAdapter:
    def __init__(self, max_workers=5):
        self.max_workers = max_workers

    def _fetch(self, url, retries=3, backoff_factor=1.0):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    return json.loads(response.read().decode('utf-8'))
            except Exception as e:
                wait_time = backoff_factor * (2 ** attempt)
                error_msg = str(e)
                
                if isinstance(e, urllib.error.HTTPError):
                    if e.code == 429:
                        error_msg = "Rate limit exceeded (429)"
                        wait_time = max(wait_time, 2.0)
                    elif e.code == 418:
                        error_msg = "IP auto-banned (418)"
                        print(f"[{self.__class__.__name__.replace('Adapter', '').upper()}][FATAL] {error_msg} for {url}. Aborting.", file=sys.stderr)
                        return None
                    else:
                        error_msg = f"HTTP {e.code}"
                elif isinstance(e, urllib.error.URLError):
                    error_msg = f"Network/Timeout ({e.reason})"

                if attempt == retries - 1:
                    print(f"[{self.__class__.__name__.replace('Adapter', '').upper()}][ERROR] Final fetch failure for {url} after {retries} attempts: {error_msg}", file=sys.stderr)
                    return None
                    
                print(f"[{self.__class__.__name__.replace('Adapter', '').upper()}][WARN] Fetch failed for {url} (attempt {attempt+1}/{retries}): {error_msg}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)

    def _collect_symbol(self, symbol, batch_timestamp):
        raise NotImplementedError

    def collect(self, symbols):
        data = []
        batch_timestamp = datetime.now(timezone.utc).isoformat()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(lambda sym: self._collect_symbol(sym, batch_timestamp), symbols)
            for row in results:
                data.append(row)
                
        return data"""

text = text.replace(base_adapter_old, base_adapter_new)

with open(collector_file, "w") as f:
    f.write(text)

# 2. Update child adapters
def trim_child(filepath, class_name):
    with open(filepath, "r") as f:
        content = f.read()
    
    # Inject imports
    if "from .derivatives_collector import BaseAdapter" not in content:
        content = content.replace("import sys\n", "import sys\nfrom .derivatives_collector import BaseAdapter\n")
    
    # Change class signature
    content = content.replace(f"class {class_name}:", f"class {class_name}(BaseAdapter):")
    
    # Cut out _fetch and collect
    # We find where `def _collect_symbol` starts and slice before `def _fetch`
    fetch_idx = content.find("    def _fetch(")
    collect_sym_idx = content.find("    def _collect_symbol(")
    
    if fetch_idx != -1 and collect_sym_idx != -1:
        content = content[:fetch_idx] + content[collect_sym_idx:]
        
    collect_idx = content.find("    def collect(")
    if collect_idx != -1:
        content = content[:collect_idx]
        
    with open(filepath, "w") as f:
        f.write(content.strip() + "\n")

trim_child(binance_file, "BinanceAdapter")
trim_child(bitget_file, "BitgetAdapter")

print("Refactor script complete.")
