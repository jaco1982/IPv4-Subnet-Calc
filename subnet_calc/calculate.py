from . import validation

_cidr_mask = ''
_cidr_address = ''
_netmask = ''

def calc_ipv4_mask(address: str):
    """
    Calculate the proper netmask from the provided address such that it complies with the relevant IPv4 spec as per RFC 791, 950 and 4632.

    :param address: The IP Address in CIDR notation used for this calculation.
    :type address: str
    :returns: Returns a string containing the valid netmask for this address in the correct four octet format where each octec is in the range 0-255
    """

    # Let's first validate that the provided address is valid
    if not validation.valid_cidr(address):
        raise ValueError(f'Invalid CIDR Address: {address}')

    cidr_split = address.split('/')
    _cidr_mask = int(cidr_split[1])
    _full_mask: list[str] = []

    if _cidr_mask == 0: # Handle a /0 mask quickly as the value is explicitly known
        _full_mask = ['0','0','0','0']
    elif _cidr_mask == 32: # Handle a /32 mask quickly as the value is explicitly known
        _full_mask = ['255','255','255','255']
    else:
        # In order to calculate the mask we need to do some modulo maths to calculate the number of full octets and the number of borrowed bits
    
        _full_octets = _cidr_mask // 8 
        _borrowed_bits = _cidr_mask % 8
        
        # Now we can calculate the full mask
        
        if _full_octets == 0: # First we set the first octet if the prefix is < 8
            _full_mask.append(str(255 - ((1 << (8-_borrowed_bits)) - 1)))
        else:
            for i in range(_full_octets): # Let's deal with the full octets
                _full_mask.append('255')
            if _borrowed_bits != 0:
                borrowed_octet = str(255 - ((1 << (8-_borrowed_bits)) - 1))
                _full_mask.append(borrowed_octet)

        while(len(_full_mask) <= 3):
            _full_mask.append('0')
        
    _netmask = '.'.join(_full_mask)
    return _netmask

# def ipv4_bin(address: str):
#     """
#     Calculate the binary representation of the provided address

#     :param address: The address to calculate in dot decimal format
#     :type address: str
#     :returns: Returns a string containing the binary representation of the provided addesss
#     """

#     binary_address = []

#     # First check that the provided address is valid. If not, raise an exception
#     print(f'Checking {address} is valid')
#     if not validation.valid_address(address):
#         raise ValueError(f'Invalid address: {address}')
    
#    # Now we can split the address into octets, convert each octet into binary and return the entire thing in dot binary format
#     split_address = address.split('.')
#     for octet in split_address:
#         octet = octet.replace(' ','')
#         binary_address.append(format(int(octet), f'0{8}b'))

#     return '.'.join(binary_address)

def ipv4_net_id(address: str):
    """
    Calculate the proper network ID from the provided address such that it complies with the relevant IPv4 spec as per RFC 791, 950 and 4632.
    
    :param address: The IP Address to use as a basis for the calculation in CIDR format. 
    :type address: str
    :returns: Returns a string containing the calcualted network ID
    """
    _net_id: list[str] = []

    # Let's first validate that the provided address is valid
    if not validation.valid_cidr(address):
        raise ValueError(f'Invalid CIDR Address: {address}')

    # First we need to split the input string to get the address portion
    _cidr_split = address.split('/')
    #_cidr_mask = int(cidr_split[1])
    _address_split = _cidr_split[0].split('.')

    # Let's handle the fringe cases /0 and /32, as these are quick and easy and requires no calculations
    if int(_cidr_split[1]) == 32:
        return _cidr_split[0]
    elif int(_cidr_split[1]) == 0:
        return '0.0.0.0'

    # Now we need to get the calculated _netmask
    _netmask = calc_ipv4_mask(address)
    _netmask_split = _netmask.split('.')

    # Now we can calculate the network ID, where all the host bits are 0
    # Take the provided address, and calculated mask and do a bitwise AND to get the resulting address. This should be the network ID
    for i in range(4):
        _net_id.append(str(int(_netmask_split[i]) & int(_address_split[i])))

    return '.'.join(_net_id)

def ipv4_broadcast(address: str):
    """
    Calculate the proper broadcast address from the provided address such that it complies with the relevant IPv4 spec as per RFC 791, 950 and 4632.

    :param address: The IP Address to use as a basis for the calculation in CIDR format. 
    :type address: str
    :returns: Returns a string containing the calculated broadcast address
    """

    _broadcast_address: list[str] = []

    # Let's first validate that the provided address is valid
    if not validation.valid_cidr(address):
        raise ValueError(f'Invalid CIDR Address: {address}')
    
    # First we need to split the input string to get the address portion
    _cidr_split = address.split('/')
    #_cidr_mask = int(cidr_split[1])
    _address_split = _cidr_split[0].split('.')

    # Now we need to get the calculated _netmask
    _netmask = calc_ipv4_mask(address)
    _netmask_split = _netmask.split('.')

    # Calculate the network ID
    _network_id = ipv4_net_id(address)
    _network_id_split = _network_id.split('.')

    # Do a bitwise OR on each octet, using the network ID and the inverse of the _netmask
    for i in range(4):
        octet = int(_network_id_split[i]) | (~int(_netmask_split[i]) &  0xFF)
        _broadcast_address.append(str(octet))

    # Convert the result back to a valid IP Address

    return '.'.join(_broadcast_address)
    
def ipv4_edge(address: str, first: bool):
    """
    Calculate the first or last usable address from the provided address such that it complies with the relevant IPv4 spec as per RFC 791, 950 and 4632.

    :param address: The IP Address to use as a basis for the calculation in CIDR format. 
    :param first: Calculate the first or last address. True == first, False == last
    :type address: str
    :type first: bool
    :returns: Returns a string containing the calculated address
    """

    return_address = []

    # Let's first validate that the provided address is valid
    if not validation.valid_cidr(address):
        raise ValueError(f'Invalid CIDR Address: {address}')
    
    # TODO: Handle the edge cases for things like /0, /31 and /32 for now we will just reject it as invalid
    cidr_split = address.split('/')
    match int(cidr_split[1]):
        case 0:
            raise ValueError('Cannot currently handle /0')
        case 31:
            raise ValueError('Cannot currently handle /31')
        case 32:
            raise ValueError('Cannot currently handle /32')

    # Calculate the first address or last address
    match first:
        case True:
            # Calculate the network ID
            # Add 1 to the network ID to get the first address
            network_id = ipv4_net_id(address).split('.')
            network_id[3] = str(int(network_id[3]) + 1)
            return_address = network_id
        case False:
            # Calculate the broadcast address
            # Subtract 1 from the broadcast address to get the last address
            broadcast = ipv4_broadcast(address).split('.')
            broadcast[3] = str(int(broadcast[3]) - 1)
            return_address = broadcast
    
    return '.'.join(return_address)


