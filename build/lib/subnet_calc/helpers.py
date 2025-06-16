from . import validation, calculate

def ipv4_host_count(address: str):
    """
    Calculate the number of usable IPs in a given subnet.

    :param address: The prefix to use as a basis for the calculation in CIDR format. 
    :type address: str
    :returns: Returns an int containing the number of usable addresses in a given prefix/subnet
    """

    # Initialise internal variables
    _host_count = 0
    
    # Now do the validation
    if not validation.valid_cidr(address):
        raise ValueError(f'Invalid CIDR Address: {address}')

    # Split the address as per usual
    _host_bits =  32 - int(address.split('/')[1])

    # The formula is simple enough 2**h - 2, where h is the number of host bits
    _host_count = 2**_host_bits - 2

    return _host_count

def ipv4_bin(mask: str):
    """
    Calculate the binary equivalent of the provided netmask

    :param: mask: The netmask to calculate in dot decimal format
    :type mask: str
    : returns: Returns a string containing the calculated binary netmask
    """

    _binary_mask: list[str] = []
    
    # First, check if the provided mask is valid. If not, throw an exception
    # if not validation.valid_mask(mask):
    #     raise ValueError(f'Invalid mask: {mask}')

    # Split the provided mask into a list and then run the binary calculation on each octet
    _split_mask = mask.split('.')

    # Finally we can take the list and return it as a string in dot binary format
    for octet in _split_mask:
        _binary_mask.append(format(int(octet), f'0{8}b'))
    
    return '.'.join(_binary_mask)

def ipv4_wildcard(address: str):
    """
    Calculate the subnet wildcard from the provided address such that it complies with the relevant IPv4 spec as per RFC 791, 950 and 4632.

    :param address: The IP Address to use as a basis for the calculation in CIDR format. 
    :type address: str
    :returns: Returns a string containing the calculated wildcard
    """
    wildcard = []

    # Let's first validate that the provided address is valid
    if not validation.valid_cidr(address):
        raise ValueError(f'Invalid CIDR Address: {address}')

    # Now get the mask
    netmask_split = calculate.calc_ipv4_mask(address).split('.')

    # And now simply calculate the bitwise inverse
    for i in range(4):
        wildcard.append(str(~int(netmask_split[i]) &  0xFF))

    return '.'.join(wildcard)
