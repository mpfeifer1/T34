# Converts a hex or binary number to a printable form
def to_printable(num, digits, binary=False):
    # Convert (Defaults to hex, can also do binary)
    if binary:
        num = bin(num)
    else:
        num = hex(num)

    # Strip beginning
    num = str(num)[2:]

    # Pad beginning with desired number of 0's
    while(len(num) < digits):
        num = '0' + num

    # Return
    return num
