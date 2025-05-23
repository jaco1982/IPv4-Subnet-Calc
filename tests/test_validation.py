import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from subnet_calc.helpers import valid_address, valid_ipv4

# @pytest.mark.parametrize(
#     "octet,expected",
#     [
#         ("0",    True),
#         ("255",  True),
#         ("256",  False),
#         ("-1",   False),
#         ("abc",  False),
#     ],
# )
# def test_valid_octet(octet, expected):
#     assert valid_ipv4(octet) is expected


# @pytest.mark.parametrize(
#     "ip,expected",
#     [
#         ("192.168.1.1",    True),
#         ("10.0.0.0",       True),
#         ("300.1.1.1",      False),
#         ("192.168.1",      False),
#         ("192.168.1.1.1",  False),
#     ],
# )
# def test_valid_ip_part(ip, expected):
#     assert valid_ip_part(ip) is expected


@pytest.mark.parametrize(
    "cidr,expected",
    [
        ("192.168.1.1/24",    True),
        ("10.0.0.0/8",        True),
        ("192.168.1.1/33",    False),   # mask too large
        ("192.168.1.1/",      False),   # missing mask
        ("192.168.1/24",      False),   # bad IP format
        ("10.0.0.0/0",        False),   # fringe case you haven’t built yet
    ],
)


def test_valid_ipv4(cidr, expected):
    assert valid_ipv4(cidr) is expected

