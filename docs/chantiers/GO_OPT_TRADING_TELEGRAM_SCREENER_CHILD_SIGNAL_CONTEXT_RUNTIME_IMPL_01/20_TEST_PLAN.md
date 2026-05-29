# Test Plan

1. `python3 -m pytest tests/test_telegram_screener_signal_context_reader.py -q`
2. `python3 -m pytest modules/data_center/tests/test_contract_tests.py -q`
3. `bash modules/telegram_screener/scripts/sanity_check.sh`
