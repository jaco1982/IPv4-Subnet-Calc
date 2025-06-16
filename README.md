# IPv4 Subnet Calculator 🧮

A lightweight, educational IPv4 subnet calculator built in Python. This project is intended as a learning tool to explore core Python concepts like input validation, bitwise operations, and string manipulation.

There are any number of modules and functions available for interacting with IPv4, but I specifically wanted to avoid using any of these, as the specific goal of this project is to learn about using the Python language.

This is currently still very much a work in progress, so check back regularly or follow this project for updates.

## Features

Intended features:
- ✅ Validates IPv4 addresses and CIDR notation
- ✅ Calculates subnet masks, network address, broadcast address, host ranges
- ✅ CLI-based interaction
- ✅ Designed for readability and learning

## TODO
- ✅ Move binary calculator to helpers
- ✅ Calculate host count
- ✅ Move wildcard calculator to helpers
- ✅ Add wrapper function to perform all calculations in one step

## Installation and use
Reccomended installing with pipx. Since installing this is outside of the scope of this guide, Google is your friend. Install with the following command:

{
    pipx install git+https://github.com/jaco1982/IPv4-Subnet-Calc
    pipx ensurepath
}

Then restart your terminal of choice.

After installing you can run this with the following command:

{
    ipcalc CIDR_Address
}

Output should look similar to this:

{
    input:
        CIDR        :  192.168.0.0/24
        address     :  192.168.0.0
        mask        :  /24

    output:
        result      :  True
        message     :  Calculations completed

    network:
        network_id  :  192.168.0.0
        netmask     :  255.255.255.0
        broadcast   :  192.168.0.255
        wildcard    :  0.0.0.255

    hosts:
        first       :  192.168.0.1
        last        :  192.168.0.254
        total       :  254

    binary:
        network_id  :  11000000.10101000.00000000.00000000
        netmask     :  11111111.11111111.11111111.00000000
        broadcast   :  11000000.10101000.00000000.11111111
}


## IPv6

Please note that this module does not currently support IPv4, but this will be added in a future version

## Example Output

The intent is for this to use a wrapper function to output all values as a single JSON dictionary. See examples/output.json for an example.

