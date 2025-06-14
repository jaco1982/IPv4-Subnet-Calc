import json
from . import calculate
from . import helpers
from . import validation

_subnet_values = {
    'input'     :   {
                        'CIDR'          :   '',
                        'address'       :   '',
                        'mask'          :   ''
                    },
    'output'    :   {
                        'result'        :   False,
                        'message'       :   ''
                    },
    'network'   :   {
                        'network_id'    :   '',
                        'netmask'       :   '',
                        'broadcask'     :   '',
                        'wildcard'      :   ''
                    },
    'hosts'     :   {
                        'first'         :   '',
                        'last'          :   '',
                        'total'         :   ''
                    },
    'binary'    :   {
                        'network_id'    :   '',
                        'netmask'       :   '',
                        'broadcast'     :   ''
                    }
}

def calc_subnet(address:str):
    """A wrapper to perform all the required calculations on a single subnet
    
    :param address: The address to calculate in CIDR notation
    :type address: str
    :returns: A JSON dictionary containing the results of the various calculations
    """

    if validation.valid_cidr(address): # Only perform the calculations if the input is valid

        try:

            ip, cidr = address.split('/')

            _subnet_values['input'] = {
                'CIDR': address,
                'address': ip,
                'mask': f'/{cidr}'
            }

            _subnet_values['network'] = {
                'network_id': calculate.ipv4_net_id(address),
                'netmask': calculate.calc_ipv4_mask(address),
                'broadcast': calculate.ipv4_broadcast(address),
                'wildcard': helpers.ipv4_wildcard(address)
            }

            _subnet_values['hosts'] = {
                'first': calculate.ipv4_edge(address, True),
                'last': calculate.ipv4_edge(address, False),
                'total': helpers.ipv4_host_count(address)
            }

            _subnet_values['binary'] = {
                'network_id': helpers.ipv4_bin(_subnet_values['network']['network_id']),
                'netmask': helpers.ipv4_bin(_subnet_values['network']['netmask']),
                'broadcast': helpers.ipv4_bin(_subnet_values['network']['broadcast'])
            }

            _subnet_values['output'] = {
                'result': True,
                'message': 'Calculations completed'
            }

        except Exception as e:
            for key in _subnet_values:
                _subnet_values.pop(key, None)

            _subnet_values['output'] = {
                'result': False,
                'message': f'Exception: {str(e)}'
            }

    return json.dumps(_subnet_values, indent = 4)
