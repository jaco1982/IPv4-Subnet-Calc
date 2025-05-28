import os

cidr_mask = ''
cidr_address = ''
netmask = ''

def valid_address(address: str):
    """
    Validate that an address is indeed a valid IPv4 address with four octets, with each octet in the range 0-255

    :param address: The address to check
    :type address: str
    returns: Returns True/False whether this is a valid octet
    """
    # TODO: Add exception catching

    octets = address.split('.')

    # First, let's check if there are four octets
    if len(octets) == 4:
        for octet in octets:
            # Validate the octet
            if not 0 <= int(octet) <= 255:
                return False
    
    return True

def valid_cidr(address: str):
    """
    Validate the user's input is indeed in valid CIDR format and conforms to the general IPv4 spec as per RFC 791, 950 and 4632.

    :param address: The IP Address to validate. This would usually be the direct input from the user.
    :type address: str
    :returns: Returns True/False whether this is a valid CIDR IPv4 address
    """

    try:
        # First we need to check that the CIDR mask is valid
        # Start by splitting the entered address and then checking if the list length is == 2
        cidr_split = address.split('/')
        if len(cidr_split) == 2:
            cidr_address = cidr_split[0]
            cidr_mask = cidr_split[1]

        # If this list length is indeed correct we can proceed to the next step, which is to check if the mask is numeric
        # If the mask is numeric we can check if the mask is in the valid range of 1-32 (For now we will not be handling fringe cases as indicated below)
        # TODO: Add support for /0
            if cidr_mask.isnumeric():
                if 1 <= int(cidr_mask) <=32:
                    # Now we can check that the address portion is valid. use the return from valid_address, since if it passes everything at this point it is a valid address
                    return valid_address(cidr_address)
    except ValueError:
        return False
    
    # Return False by default
    return False

def calc_netmask(address: str):
    """
    Calculate the proper netmask from the provided address such that it complies with the relevant IPv4 spec as per RFC 791, 950 and 4632.

    :param address: The IP Address to validate. This would usually be the direct input from the user.
    :type address: str
    :returns: Returns a string containing the valid netmask for this address in the correct four octet format where each octec is in the range 0-255
    """

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
