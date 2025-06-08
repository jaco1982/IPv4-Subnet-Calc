import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from subnet_calc.calculate import ipv4_bin,ipv4_mask_bin, ipv4_net_id

@pytest.mark.parametrize(
    'mask,bin_mask',
    [
        # Valid masks
        ('255.0.0.0',         '11111111.00000000.00000000.00000000'),  # /8
        ('255.255.0.0',       '11111111.11111111.00000000.00000000'),  # /16
        ('255.255.255.0',     '11111111.11111111.11111111.00000000'),  # /24
        ('255.255.255.128',   '11111111.11111111.11111111.10000000'),  # /25
        ('255.255.255.192',   '11111111.11111111.11111111.11000000'),  # /26
        ('255.255.255.224',   '11111111.11111111.11111111.11100000'),  # /27
        ('255.255.255.240',   '11111111.11111111.11111111.11110000'),  # /28
        ('255.255.255.252',   '11111111.11111111.11111111.11111100'),  # /30
        ('255.255.255.254',   '11111111.11111111.11111111.11111110'),  # /31
        ('255.255.255.255',   '11111111.11111111.11111111.11111111'),  # /32
        ('128.0.0.0',         '10000000.00000000.00000000.00000000'),  # /1
        ('254.0.0.0',         '11111110.00000000.00000000.00000000'),  # /7
        ('0.0.0.0',           '00000000.00000000.00000000.00000000'),  # All-hosts mask

        # Malformed or invalid masks
        ('255.0.255.0',       pytest.raises(ValueError)),  # Discontiguous
        ('255.255.0.255',     pytest.raises(ValueError)),  # Discontiguous
        ('255.255',           pytest.raises(ValueError)),  # Too few octets
        ('255.255.255.0.0',   pytest.raises(ValueError)),  # Too many octets
        ('255.255.256.0',     pytest.raises(ValueError)),  # Octet out of range
        ('255.255.255.foo',   pytest.raises(ValueError)),  # Non-numeric octet
        ('255.255.255.127',   pytest.raises(ValueError)),  # Host bits set after network bits
        ('255.255.255.-1',    pytest.raises(ValueError))  # Negative octet
    ],
)
def test_calc_mask_bin(mask: str, bin_mask: str):
    if isinstance(bin_mask, str):
        assert ipv4_mask_bin(mask) == bin_mask
    else:
        with bin_mask:
            ipv4_mask_bin(mask)

@pytest.mark.parametrize(
    'ip_addr,expected',
    [
        # Valid inputs
        ('0.0.0.0',        '00000000.00000000.00000000.00000000'),
        ('255.255.255.255','11111111.11111111.11111111.11111111'),
        ('192.168.1.1',    '11000000.10101000.00000001.00000001'),
        ('10.0.0.1',       '00001010.00000000.00000000.00000001'),
        ('127.0.0.1',      '01111111.00000000.00000000.00000001'),

        # Invalid inputs
        ('256.0.0.1',         pytest.raises(ValueError)),
        ('192.168.1',         pytest.raises(ValueError)),
        ('192.168.1.1.1',     pytest.raises(ValueError)),
        ('192.168.one.1',     pytest.raises(ValueError)),
        ('192.168.1.-1',      pytest.raises(ValueError)),
    ]
)
def test_ipv4_to_bin(ip_addr, expected):
    if isinstance(expected, str):
        assert ipv4_bin(ip_addr) == expected
    else:
        with expected:
            ipv4_bin(ip_addr)

@pytest.mark.parametrize(
    'cidr,expected',
    [
        # Valid inputs
        ('192.168.0.10/24',        '192.168.0.0'),
        ('192.168.0.10/16',        '192.168.0.0'),
        ('192.168.0.10/8',         '192.0.0.0'),
        ('10.0.5.25/32',           '10.0.5.25'),     # /32 means host address is the network
        ('10.0.5.25/0',            '0.0.0.0'),       # /0 means all IPs in one block
        ('172.16.5.10/20',         '172.16.0.0'),
        ('172.16.5.10/21',         '172.16.0.0'),
        ('172.16.5.10/22',         '172.16.4.0'),
        ('172.16.5.10/23',         '172.16.4.0'),
        ('172.16.5.10/25',         '172.16.5.0'),
        ('172.16.5.10/26',         '172.16.5.0'),
        ('172.16.5.10/27',         '172.16.5.0'),
        ('172.16.5.10/28',         '172.16.5.0'),
        ('172.16.5.10/29',         '172.16.5.8'),
        ('172.16.5.10/30',         '172.16.5.8'),
        ('172.16.5.10/31',         '172.16.5.10'),
        ('172.16.5.10/32',         '172.16.5.10'),

        # Edge-case IPs
        ('0.0.0.0/0',              '0.0.0.0'),
        ('255.255.255.255/32',     '255.255.255.255'),
        ('1.2.3.4/1',              '0.0.0.0'),
        ('1.2.3.4/2',              '0.0.0.0'),
        ('1.2.3.4/3',              '0.0.0.0'),
        ('1.2.3.4/4',              '0.0.0.0'),

        # Malformed or invalid IPs
        ('192.168.1/24',          pytest.raises(ValueError)),  # Too few octets
        ('192.168.1.1.1/24',      pytest.raises(ValueError)),  # Too many octets
        ('192.168.256.1/24',      pytest.raises(ValueError)),  # Octet out of range
        ('192.168.-1.1/24',       pytest.raises(ValueError)),  # Negative octet
        ('192.168.foo.1/24',      pytest.raises(ValueError)),  # Non-numeric octet
        ('192.168.1.1/33',        pytest.raises(ValueError)),  # Invalid CIDR prefix (too high)
        ('192.168.1.1/-1',        pytest.raises(ValueError)),  # Invalid CIDR prefix (negative)
        ('192.168.1.1/',          pytest.raises(ValueError)),  # Missing prefix
        ('/24',                   pytest.raises(ValueError)),  # Missing IP
        ('',                      pytest.raises(ValueError)),  # Empty string
        ('192.168.1.1/abc',       pytest.raises(ValueError)),  # Non-numeric prefix
        ('192.168.1.1/ 24',       pytest.raises(ValueError)),  # Leading space in prefix
    ]
)
def test_ipv4_network_id(cidr: str, expected: str):
    if isinstance(expected, str):
        assert ipv4_net_id(cidr) == expected
    else:
        with expected:
            ipv4_net_id(cidr)