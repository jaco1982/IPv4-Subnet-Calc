
# Module constants
VALID_MASK_OCTETS = {0, 128, 192, 224, 240, 248, 252, 254, 255}

def valid_address(address: str):
    """
    Validate that an address is indeed a valid IPv4 address with four octets, with each octet in the range 0-255. Each octet needs to be numeric. Ignores spaces.

    :param address: The address to check
    :type address: str
    returns: Returns True/False whether this is a valid octet
    """

    octets = address.split('.')

    # First, let's check if there are four octets
    if len(octets) == 4:
        for octet in octets:
            # Validate the octet
            octet = octet.replace(' ','')
            if not octet.isnumeric:
                return False
            if not 0 <= int(octet) <= 255:
                return False
    else:
        return False
    
    return True

def valid_cidr(address: str):
    """
    Validate the user's input is indeed in valid CIDR format and conforms to the general IPv4 spec as per RFC 791, 950 and 4632.

    :param address: The IP Address to validate. This would usually be the direct input from the user.
    :type address: str
    :returns: Returns True/False whether this is a valid CIDR IPv4 address
    """

    #print(f'This is line 40 in validation.py. Value address is value {address} and is of type {type(address)}')

    try:
        # First we need to check that the CIDR mask is valid
        # Start by splitting the entered address and then checking if the list length is == 2
        
        cidr_split = address.split('/')
        if len(cidr_split) == 2:
            cidr_address = cidr_split[0]
            cidr_mask = cidr_split[1]

            # If this list length is indeed correct we can proceed to the next step, which is to check if the mask is numeric
            # If the mask is numeric we can check if the mask is in the valid range of 0-32
            if cidr_mask.isnumeric():
                if 0 <= int(cidr_mask) <=32:
                    # Now we can check that the address portion is valid. use the return from valid_address, since if it passes everything at this point it is a valid address
                    return valid_address(cidr_address)
    except ValueError:
        return False
    
    # Return False by default
    return False

def valid_mask(mask: str):
    """
    Validate the provided mask is valid

    :param mask: The mask to validate in Dotted-Decimal format
    :type mask: str
    returns: True/False whether this is a valid netmask
    """

    # First, split the mask into octets
    mask_octets = mask.split(".")
    # Now check that the correct number of octets is present
    if not len(mask_octets) == 4: 
        return False

    # Now check that each octet in turn is valid by simply checking that each is one of the acceptable values

    # Now finally do some logic validation to confirm that the octets are in the correct sequence - eg there are no smaller octets before larger octets
    prev_octet = 512 # Need to initialise this with an artificially high value, otherwise the next test fails. TODO: Fix this
    for i in range(len(mask_octets)): 
        if not mask_octets[i].isnumeric(): # Check that the value is numeric
            return False
        if int(mask_octets[i]) < 0: # Test if octet is negative
            return False
        if not int(mask_octets[i]) in VALID_MASK_OCTETS: # Check if the octet is in the acceptable list
            return False
        if i > 0: # We are dealing with the second or higher octet
            if prev_octet < int(mask_octets[i]):
                return False
        prev_octet = int(mask_octets[i])

    return True
