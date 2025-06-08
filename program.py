from subnet_calc.calculate import ipv4_edge
CIDR = '192.168.1.0/32'

# print(f'Starting the program with {CIDR}')
print(f'{ipv4_edge(CIDR,True)} and {ipv4_edge(CIDR,False)}')