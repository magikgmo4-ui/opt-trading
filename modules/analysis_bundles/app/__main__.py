"""Entry point: python -m modules.analysis_bundles.app"""
from modules.analysis_bundles.app.btc_core_producer import produce_btc_core
from modules.analysis_bundles.app.macro_producer import produce_macro
from modules.analysis_bundles.app.verdict_consumer import produce_verdict
import json


def main():
    print("=== BTC Core Bundle ===")
    btc = produce_btc_core()
    btc_dict = btc.to_dict()
    print(json.dumps(btc_dict, indent=2, default=str))

    print("\n=== Macro Bundle ===")
    macro = produce_macro()
    macro_dict = macro.to_dict()
    print(json.dumps(macro_dict, indent=2, default=str))

    print("\n=== Analysis Verdict ===")
    verdict = produce_verdict(btc_bundle=btc_dict, macro_bundle=macro_dict)
    print(json.dumps(verdict.to_dict(), indent=2, default=str))


if __name__ == "__main__":
    main()
