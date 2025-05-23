import os

cidr_mask = ""
cidr_address = ""

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

def valid_ipv4(address: str):
    """
    Validate the user's input is indeed in valid CIDR format and conforms to the general IPv4 spec as per RFC 791,950 and 4632.

    :param address: The IP Address to validate. This would usually be the direct input from the user.
    :type address: str
    :returns: Returns True/False whether this is a valid CIDR IPv4 address
    """
    # TODO: Add exception catching

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

#function calculate_address(ip_address):


# #Clear the screen
# os.system('cls' if os.name == 'nt' else 'clear')

# #First we need to get an input address in CIDR notation
# print('Enter an IP Address in CIDR notation:')
# cidr_input = input()
# print('You entered ', cidr_input)

# # Check if the supplied address is a valid CIDR address
# if valid_ipv4(cidr_input):
#     print('Valid address')
# else:
#     print("Error!")