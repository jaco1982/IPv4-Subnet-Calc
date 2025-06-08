import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from subnet_calc.validation import valid_address, valid_cidr, valid_mask

@pytest.mark.parametrize(
    'ip,expected',
    [
        ('192.168.1.1',    True),
        ('10.0.0.0',       True),
        ('300.1.1.1',      False),
        ('192.168.1',      False),
        ('192.168.1.1.1',  False),
    ],
)
def test_valid_address(ip: str, expected: bool):
    assert valid_address(ip) is expected

@pytest.mark.parametrize(
    'cidr,expected',
    [
        ('192.168.1.1/24',    True),
        ('10.0.0.0/8',        True),
        ('192.168.1.1/33',    False),   # mask too large
        ('192.168.1.1/',      False),   # missing mask
        ('192.168.1/24',      False),   # bad IP format
        ('10.0.0.0/0',        False),   # fringe case you haven’t built yet
    ],
)
def test_valid_cidr(cidr: str, expected: bool):
    assert valid_cidr(cidr) is expected

@pytest.mark.parametrize(
    'mask,expected',
    [
        ('255.0.0.0',     True),   # Valid class A mask
        ('255.255.0.0',   True),   # Valid class B mask
        ('255.255.255.0', True),   # Valid class C mask
        ('255.255.254.0', True),   # Valid subnet mask with non-/24 boundary
        ('255.255.255.255', True), # Valid /32 mask
        ('255.0.255.0',   False),  # Invalid: discontiguous mask
        ('255.255.0.255', False),  # Invalid: discontiguous mask
        ('255.255.256.0', False),  # Invalid: octet out of range
        ('255.255',        False), # Invalid: too few octets
        ('255.255.255.0.0', False),# Invalid: too many octets
        ('255.255.255.foo', False),# Invalid: non-numeric octet
        ('128.0.0.0',      True),  # Valid /1 mask
        ('254.0.0.0',      True),  # Valid /7 mask
        ('255.255.255.128', True), # Valid mask with host bits
        ('255.255.255.127', False) # Invalid: host bits set after network bits
    ],
)
def test_valid_mask(mask: str, expected: bool):
    assert valid_mask(mask) is expected