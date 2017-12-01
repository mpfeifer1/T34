import sys
from alu import *
from util import *



# This is the main program - it sets up the memory, imports the object file, and processes the user input
def main(infile):
    # Open the input file
    try:
        f = open(infile)
    except:
        print("Please pass in a valid file")
        return

    # Build data, check not empty
    f = f.read().splitlines()
    if len(f) == 0:
        print("Error - This object file is empty")
        return

    # Process object file
    data = []
    for line in f:
        # Split line
        line = line.split()

        # Cast to int from hex/int
        for i in range(len(line)):
            if i == 0 or i > 1:
                line[i] = int(line[i], 16)
            else:
                line[i] = int(line[i])

        # Toss it into data
        data.append(line)

    # Create memory - memory only holds decimal ints
    memory = [0] * 4096

    # Add the object to memory
    for line in data[:-1]:
        location = line[0]
        for i in range(line[1]):
            memory[location] = line[2+i]
            location += 1

    # Check PC is on its own line
    if len(data[-1]) > 1:
        print("Error - PC is not on its own line")
        return

    # Set up registers
    reg = {}
    reg['pc'] = data[-1][0]
    reg['ac'] = 0
    reg['x0'] = 0
    reg['x1'] = 0
    reg['x2'] = 0
    reg['x3'] = 0

    # Print a menu for the user - disabled
    while True:
        sel = menu(memory, reg)
        if sel in ['q', 'Q']:
            break
        print()

    # Terminate the emulator
    return



# Executes a line of code, and returns true if the emulator should be halted
def execute(memory, reg):
    # Run command
    print_trace(memory, reg)
    ret = run_instruction(memory, reg)
    print_result(memory, reg)

    # Check termination
    if len(ret) > 1:
        print(ret[1])
    return ret[0]



def print_trace(memory, reg):
    # Grab current instruction
    pc = reg['pc']
    instruction = memory[pc]

    # Get name, and pad with spaces to 4 chars
    name = get_inst_name(instruction).ljust(4)
    addr = to_printable(pc, 3)
    inst = to_printable(instruction, 6)

    # Get data necessary for indexing mode
    bits = to_printable(instruction, 24, True)
    addridx = bits[18:22]
    upper = bits[12:14]
    lower = bits[14:18]

    # Get indexing mode (EA)
    temp1, ea, temp2 = indexing_mode(memory, reg)
    mode = to_printable(ea, 3)

    # Get indexing mode
    if addridx == '0001':
        mode = "IMM"
    if upper == '00':
        mode = "   "
    if upper == '10' and lower == '1010':
        mode = "   "
    if upper == '10' and lower == '0010':
        mode = "   "
    if upper == '10' and lower == '0011':
        mode = "   "

    # Check if indexing mode is illegal
    if addridx not in ['0000', '0001', '0010', '0100', '0110']:
        mode = "???"

    print(addr + ":", inst, name, mode, sep='  ', end='  ')

    return



def print_result(memory, reg):
    # Get other registers
    ac = 'AC[' + to_printable(reg['ac'], 6) + ']'
    x1 = 'X0[' + to_printable(reg['x0'], 3) + ']'
    x2 = 'X1[' + to_printable(reg['x1'], 3) + ']'
    x3 = 'X2[' + to_printable(reg['x2'], 3) + ']'
    x4 = 'X3[' + to_printable(reg['x3'], 3) + ']'
    print(ac, x1, x2, x3, x4, sep='  ')

    return



# Checks that the given location is in memory
def menu(memory, reg):
    # Print the menu
    print("T-34 Emulator ~~~ Enter a command")
    print("P: Parse memory")
    print("D: Dump memory")
    print("C: Print Program Counter")
    print("E: Emulate Object")
    print("Q: Quit")

    # Get the user's selction
    sel = get_selection(memory, reg)

    return sel



# Gets the user's mode selection, and launches it
def get_selection(memory, reg):
    # Try to get selection
    print("Selection: ", end='')
    selection = input()
    selection = selection.upper()

    # While selection isn't valid, keep asking
    while len(selection) != 1 or selection not in ['P', 'D', 'C', 'Q', 'E']:
        print("Please enter a single valid character")
        print("Selection: ", end='')
        selection = input()
        selection = selection.upper()

    # Parse a val in memory
    if selection == 'P':
        location = get_mem_location()
        count    = get_count()
        print()
        parse(memory, location, count)
        print()

    # Print all the vals in memory
    if selection == 'D':
        print()
        memdump(memory)
        print()

    # Get the program counter
    if selection == 'C':
        print()
        print("PC:", reg['pc'])

    if selection == 'E':
        print()
        # Emulate the program
        running = True
        while running:
            running = execute(memory, reg)

    return selection



# This function repeatedly asks the user for a positive number
def get_count():
    # Ask for a count
    print("How many values would you like")

    # Try to get selection
    print("Selection: ", end='')
    selection = input()

    # Cast selection to an int
    try:
        selection = int(selection)
    except:
        pass

    # While selection isn't valid, keep asking
    while selection < 0:
        print("How many values would you like")
        print("Selection: ", end='')
        selection = input()

        # Cast selection to an int
        try:
            selection = int(selection)
        except:
            pass

    return selection



# This function repeatedly asks the user for a valid memory location
def get_mem_location():
    # Ask for a memory location
    print("Please enter a valid memory location in hex")

    # Try to get selection
    print("Selection: ", end='')
    selection = input()

    # Cast selection to an int
    try:
        selection = int(selection, 16)
    except:
        pass

    # While selection isn't valid, keep asking
    while not in_memory(selection):
        print("Please enter a valid memory location in hex")
        print("Selection: ", end='')
        selection = input()

        # Cast selection to an int
        try:
            selection = int(selection, 16)
        except:
            pass

    return selection



# Checks that the given location is in memory
def in_memory(location):
    return (location >= 0 and location < 4096)



# Shows the values of the next count values in memory,
# starting from location
def parse(memory, location, count):
    # Print the first line
    print("     ADDR         OP     AM")

    # For each memory address
    while count > 0:
        # Check the location is in memory
        if not in_memory(location):
            break

        # Prepare the value and location to print
        value = memory[location]
        value = to_printable(value, 24, True)
        templocation = to_printable(location, 3)

        # Print the address and value
        value = value[:12] + ' ' + value[12:18] + " " + value[18:]
        print(templocation, ": ", value, sep='')

        # Start the next one
        location += 1
        count -= 1
    return



# Prints all locations in memory that aren't equal to 0
def memdump(memory):
    # Print the data
    for i in range(len(memory)):
        if memory[i] != 0:
            # Get value and address to print
            val = to_printable(memory[i], 6)
            address = to_printable(i, 3)

            # Print
            address += ":"
            print(address, val)
    return



# Launches the program after confirming an object file was given
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please include an object file")
    else:
        main(sys.argv[1])
