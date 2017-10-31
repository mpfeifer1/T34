from util import *



def run_instruction(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    upper = bits[12:14]

    # Whether to keep running after command
    running = True

    # Miscellaneous
    if upper == '00':
        running &= run_misc(memory, reg)

    # Memory
    if upper == '01':
        running &= run_memory(memory, reg)

    # ALU
    if upper == '10':
        running &= run_alu(memory, reg)

    # Jump
    if upper == '11':
        running &= run_jump(memory, reg)
    else:
        reg['pc'] += 1

    return running



def run_misc(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    lower = bits[14:18]

    # HALT
    if lower == '0000':
        print("Machine Halted - HALT instruction executed")
        return False

    # NOP
    if lower == '0001':
        return True

    # Unknown command
    print("Machine Halted - undefined opcode")
    return False



def run_memory(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    lower = bits[14:18]

    # Grab indexing mode
    indexmode = bits[18:22]
    indexreg  = bits[22:24]

    # LD
    if lower == '0000':
        print("Not implemented")
        return True

    # ST
    if lower == '0001':
        print("Not implemented")
        return True

    # EM
    if lower == '0010':
        print("Not implemented")
        return True

    # LDX
    if lower == '1000':
        print("Machine Halted - unimplemented opcode")
        return False

    # STX
    if lower == '1001':
        print("Machine Halted - unimplemented opcode")
        return False

    # EMX
    if lower == '1010':
        print("Machine Halted - unimplemented opcode")
        return False

    # Unknown command
    print("Machine Halted - undefined opcode")
    return False



def run_alu(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    lower = bits[14:18]

    # ADD
    if lower == '0000':
        print("Not implemented")
        return True

    # SUB
    if lower == '0001':
        print("Not implemented")
        return True

    # CLR
    if lower == '0010':
        print("Not implemented")
        return True

    # COM
    if lower == '0011':
        print("Not implemented")
        return True

    # AND
    if lower == '0100':
        print("Not implemented")
        return True

    # OR
    if lower == '0101':
        print("Not implemented")
        return True

    # XOR
    if lower == '0110':
        print("Not implemented")
        return True

    # ADDX
    if lower == '1000':
        print("Machine Halted - unimplemented opcode")
        return False

    # SUBX
    if lower == '1001':
        print("Machine Halted - unimplemented opcode")
        return False

    # CLRX
    if lower == '1010':
        print("Machine Halted - unimplemented opcode")
        return False

    # Unknown command
    print("Machine Halted - undefined opcode")
    return False



def run_jump(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    lower = bits[14:18]

    # J
    if lower == '0000':
        reg['pc'] += 1
        print("Not implemented, incrementing PC for fun")
        return True

    # JZ
    if lower == '0001':
        reg['pc'] += 1
        print("Not implemented, incrementing PC for fun")
        return True

    # JN
    if lower == '0010':
        reg['pc'] += 1
        print("Not implemented, incrementing PC for fun")
        return True

    # JP
    if lower == '0011':
        reg['pc'] += 1
        print("Not implemented, incrementing PC for fun")
        return True

    # Unknown command
    print("Machine Halted - undefined opcode")
    return False



def get_inst_name(instruction):
    # Get instruction in binary
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    upper = bits[12:14]
    lower = bits[14:18]

    # Find instruction name
    name = "????"
    if upper == '00':
        if lower == '0000':
            name = "HALT"
        if lower == '0001':
            name = "NOP"
    if upper == '01':
        if lower == '0000':
            name = "LD"
        if lower == '0001':
            name = "ST"
        if lower == '0010':
            name = "EM"
        if lower == '1000':
            name = "LDX"
        if lower == '1001':
            name = "STX"
        if lower == '1010':
            name = "EMX"
    if upper == '10':
        if lower == '0000':
            name = "ADD"
        if lower == '0001':
            name = "SUB"
        if lower == '0010':
            name = "CLR"
        if lower == '0011':
            name = "COM"
        if lower == '0100':
            name = "AND"
        if lower == '0101':
            name = "OR"
        if lower == '0110':
            name = "XOR"
        if lower == '1000':
            name = "ADDX"
        if lower == '1001':
            name = "SUBX"
        if lower == '1010':
            name = "CLRX"
    if upper == '11':
        if lower == '0000':
            name = "J"
        if lower == '0001':
            name = "JZ"
        if lower == '0010':
            name = "JN"
        if lower == '0011':
            name = "JP"

    return name
