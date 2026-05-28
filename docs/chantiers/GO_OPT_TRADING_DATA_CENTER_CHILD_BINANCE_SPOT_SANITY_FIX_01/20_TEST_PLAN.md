# Test Plan

1. `python3 -m pytest modules/collector_binance_spot/tests -q`
2. `python3 -m pytest tests/data_center/test_binance_spot_dc_runtime.py modules/data_center/tests/test_spot_snapshot_dc_writer.py -q`
