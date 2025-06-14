import json, sys
from subnet_calc.wrapper import calc_subnet

address = ''
argument_list = sys.argv[1:] # Retrieve arguments

if len(argument_list) != 0:
    address = argument_list[0]

if address == '': # If no CLI address is specified
    address = input('Enter an IP Address in CIDR notation: ') 
    if address == '': # If no address is specified
        print('Address cannot be blank')

raw_results = calc_subnet(address)
results = json.loads(raw_results)

for key, value in results.items():
    print(f'{key}:')
    for sub_key, sub_value in value.items():
        print(f'   {sub_key:<12}:  {sub_value}')
    print()

