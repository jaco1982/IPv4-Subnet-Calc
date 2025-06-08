from subnet_calc import validation

cidr_mask = ''
cidr_address = ''
netmask = ''

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
    cidr_mask = int(cidr_split[1])
    full_mask = []

    if cidr_mask == 0: # Handle a /0 mask quickly as the value is explicitly known
        full_mask = ['0','0','0','0']
    elif cidr_mask == 32: # Handle a /32 mask quickly as the value is explicitly known
        full_mask = ['255','255','255','255']
    else:
        # In order to calculate the mask we need to do some modulo maths to calculate the number of full octets and the number of borrowed bits
    
        full_octets = cidr_mask // 8 
        borrowed_bits = cidr_mask % 8
        
        # Now we can calculate the full mask
        
        if full_octets == 0: # First we set the first octet if the prefix is < 8
            full_mask.append(str(255 - ((1 << (8-borrowed_bits)) - 1)))
        else:
            for i in range(full_octets): # Let's deal with the full octets
                full_mask.append('255')
            if borrowed_bits != 0:
                borrowed_octet = str(255 - ((1 << (8-borrowed_bits)) - 1))
                full_mask.append(borrowed_octet)

        while(len(full_mask) <= 3):
            full_mask.append('0')
        
    netmask = '.'.join(full_mask)
    return netmask

def ipv4_mask_bin(mask: str):
    """
    Calculate the binary equivalent of the provided netmask

    :param: mask: The netmask to calculate in dot decimal format
    :type mask: str
    : returns: Returns a string containing the calculated binary netmask
    """

    binary_mask = []
    
    # First, check if the provided mask is valid. If not, throw an exception
    if not validation.valid_mask(mask):
        raise ValueError(f'Invalid mask: {mask}')

    # Split the provided mask into a list and then run the binary calculation on each octet
    split_mask = mask.split('.')

    # Finally we can take the list and return it as a string in dot binary format
    for octet in split_mask:
        binary_mask.append(format(int(octet), f'0{8}b'))
    
    return '.'.join(binary_mask)

def ipv4_bin(address: str):
    """
    Calculate the binary representation of the provided address

    :param address: The address to calculate in dot decimal format
    :type address: str
    :returns: Returns a string containing the binary representation of the provided addesss
    """

    binary_address = []

    # First check that the provided address is valid. If not, raise an exception
    print(f'Checking {address} is valid')
    if not validation.valid_address(address):
        raise ValueError(f'Invalid address: {address}')
    
   # Now we can split the address into octets, convert each octet into binary and return the entire thing in dot binary format
    split_address = address.split('.')
    for octet in split_address:
        octet = octet.replace(' ','')
        binary_address.append(format(int(octet), f'0{8}b'))

    return '.'.join(binary_address)

def ipv4_net_id(address: str):
    """
    Calculate the proper network ID from the provided address such that it complies with the relevant IPv4 spec as per RFC 791, 950 and 4632.
    
    :param address: The IP Address to use as a basis for the calculation in CIDR format. 
    :type address: str
    :returns: Returns a string containing the calcualted network ID
    """
    net_id = []

    # Let's first validate that the provided address is valid
    if not validation.valid_cidr(address):
        raise ValueError(f'Invalid CIDR Address: {address}')

    # First we need to split the input string to get the address portion
    cidr_split = address.split('/')
    #cidr_mask = int(cidr_split[1])
    address_split = cidr_split[0].split('.')

    # Let's handle the fringe cases /0 and /32, as these are quick and easy and requires no calculations
    if cidr_split[1] == 32:
        return cidr_split[0]
    elif cidr_split[1] == 0:
        return '0.0.0.0'

    # Now we need to get the calculated netmask
    netmask = calc_ipv4_mask(address)
    netmask_split = netmask.split('.')

    # Now we can calculate the network ID, where all the host bits are 0
    # Take the provided address, and calculated mask and do a bitwise AND to get the resulting address. This should be the network ID
    for i in range(4):
        net_id.append(str(int(netmask_split[i]) & int(address_split[i])))

    return '.'.join(net_id)

# def calc_broadcast(address: str):

    
# def calc_start(address: str):


# def calc_end(address: str):


# def calc_min(address: str):


# def calc_max(address: str):
