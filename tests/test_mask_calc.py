import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from subnet_calc.helpers import calc_netmask

@pytest.mark.parametrize(
    'cidr,expected',
    [
        ('192.168.1.1/24',      '255.255.255.0'),     # Class C typical subnet
        ('10.0.0.0/8',          '255.0.0.0'),         # Class A typical subnet
        ('172.16.5.4/16',       '255.255.0.0'),       # Class B typical subnet
        ('192.0.2.128/25',      '255.255.255.128'),   # 25-bit mask
        ('203.0.113.0/30',      '255.255.255.252'),   # Very small subnet (4 IPs)
        ('198.51.100.7/32',     '255.255.255.255'),   # Host-only subnet
        ('0.0.0.0/0',           '0.0.0.0'),           # Default route
        ('192.168.100.5/23',    '255.255.254.0'),     # Spans two /24 networks
        ('10.1.2.3/12',         '255.240.0.0'),       # Class A with non-default mask
        ('172.31.255.255/22',   '255.255.252.0'),     # Network bleeding into adjacent blocks
        ('192.0.2.128/4',       '240.0.0.0')
    ]
)

def test_mask_calc(cidr: str, expected: str):
    assert calc_netmask(cidr) == expected

