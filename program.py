from subnet_calc.calculate import ipv4_net_id
CIDR = '10.0.5.25/0'

print(f'Starting the program with {CIDR}')
print(ipv4_net_id(CIDR))