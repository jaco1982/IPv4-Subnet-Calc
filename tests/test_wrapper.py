import sys
import os
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from subnet_calc.wrapper import calc_subnet

@pytest.mark.parametrize("input_address, expected_result", [
    # Valid inputs
    ("192.168.1.1/24", True),
    ("10.0.0.1/8", True),
    ("172.16.5.10/16", True),
    ("192.0.2.100/26", True),
    ("203.0.113.45/30", True),
    ("100.64.0.1/10", True),

    # Invalid inputs
    ("192.168.1.1/33", False),
    ("10.0.0.1/-1", False),
    ("172.16.300.10/16", False),
    ("256.0.0.1/24", False),
    ("192.168.1.1/abc", False),
    ("10.0.0/24", False),  # missing octet
    ("8.8.8.8/32", False),
    ("", False),
])
def test_cidr_result_only(input_address, expected_result):
    result_raw = calc_subnet(input_address)  # This returns JSON string
    result_dict = json.loads(result_raw)          # Parse JSON string to dict
    actual_result = result_dict.get('result', None)
    assert actual_result is expected_result

