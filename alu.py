from util import *



def indexing_mode(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab indexing mode
    indexmode = bits[18:22]

    # Find indexing register
    indexreg  = bits[22:24]
    if indexreg == '00':
        indexreg = 'x0'
    if indexreg == '01':
        indexreg = 'x1'
    if indexreg == '10':
        indexreg = 'x2'
    if indexreg == '11':
        indexreg = 'x3'

    # Find corresponding EA
    ea = None

    # Direct
    if indexmode == '0000':
        ea = memory[int(bits[0:12], 2)]

    # Immediate
    if indexmode == '0001':
        ea = int(bits[0:12], 2)

    # Indexed
    if indexmode == '0010':
        pass

    # Indirect
    if indexmode == '0100':
        pass

    # Indexed Indirect
    if indexmode == '0110':
        pass

    # Return
    return indexmode, ea



def run_instruction(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    upper = bits[12:14]

    # Get indexing mode (EA)
    ea = indexing_mode(memory, reg)

    # Whether to keep running after command
    running = (True, )

    # Miscellaneous
    if upper == '00':
        running = run_misc(memory, reg)

    # Memory
    if upper == '01':
        running = run_memory(memory, reg)

    # ALU
    if upper == '10':
        running = run_alu(memory, reg)

    # Jump
    if upper == '11':
        running = run_jump(memory, reg)
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
        return (False, "Machine Halted - HALT instruction executed")

    # NOP
    if lower == '0001':
        return (True, )

    # Unknown command
    return (False, "Machine Halted - undefined opcode")



def run_memory(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    lower = bits[14:18]

    # Get the indexing mode
    mode, val = indexing_mode(memory, reg)

    # LD
    if lower == '0000':
        if mode in ['0000', '0001']:
            reg['ac'] = val
            return (True, )
        elif mode in ['0010', '0100', '0110']:
            return (False, "Machine Halted - unimplemented addressing mode")
        else:
            return (False, "Machine Halted - illegal addressing mode")

    # ST
    if lower == '0001':
        if mode in ['0000', '0001']:
            memory[val] = reg['ac']
            return (True, )
        elif mode in ['0010', '0100', '0110']:
            return (False, "Machine Halted - unimplemented addressing mode")
        else:
            return (False, "Machine Halted - illegal addressing mode")

    # EM
    if lower == '0010':
        if mode in ['0000', '0001']:
            memory[val], reg['ac'] = reg['ac'], memory[val]
            return (True, )
        elif mode in ['0010', '0100', '0110']:
            return (False, "Machine Halted - unimplemented addressing mode")
        else:
            return (False, "Machine Halted - illegal addressing mode")

    # LDX
    if lower == '1000':
        return (False, "Machine Halted - unimplemented opcode")

    # STX
    if lower == '1001':
        return (False, "Machine Halted - unimplemented opcode")

    # EMX
    if lower == '1010':
        return (False, "Machine Halted - unimplemented opcode")

    # Unknown command
    return (False, "Machine Halted - undefined opcode")



def run_alu(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    lower = bits[14:18]

    # Get the indexing mode
    mode, val = indexing_mode(memory, reg)

    # ADD
    if lower == '0000':
        if mode in ['0000', '0001']:
            reg['ac'] += val
            return (True, )
        elif mode in ['0010', '0100', '0110']:
            return (False, "Machine Halted - unimplemented addressing mode")
        else:
            return (False, "Machine Halted - illegal addressing mode")

    # SUB
    if lower == '0001':
        if mode in ['0000', '0001']:
            reg['ac'] -= val
            return (True, )
        elif mode in ['0010', '0100', '0110']:
            return (False, "Machine Halted - unimplemented addressing mode")
        else:
            return (False, "Machine Halted - illegal addressing mode")

    # CLR
    if lower == '0010':
        return (True, "Not implemented")

    # COM
    if lower == '0011':
        return (True, "Not implemented")

    # AND
    if lower == '0100':
        return (True, "Not implemented")

    # OR
    if lower == '0101':
        return (True, "Not implemented")

    # XOR
    if lower == '0110':
        return (True, "Not implemented")

    # ADDX
    if lower == '1000':
        return (False, "Machine Halted - unimplemented opcode")

    # SUBX
    if lower == '1001':
        return (False, "Machine Halted - unimplemented opcode")

    # CLRX
    if lower == '1010':
        return (False, "Machine Halted - unimplemented opcode")

    # Unknown command
    return (False, "Machine Halted - undefined opcode")



def run_jump(memory, reg):
    # Get instruction in binary
    instruction = memory[reg['pc']]
    bits = to_printable(instruction, 24, True)

    # Grab instructions
    lower = bits[14:18]

    # Get the indexing mode
    mode, val = indexing_mode(memory, reg)

    # J
    if lower == '0000':
        if mode in ['0000', '0001']:
            reg['pc'] = val
            return (True, )
        else:
            return (False, "Machine Halted - illegal addressing mode")

    # JZ
    if lower == '0001':
        reg['pc'] += 1
        return (True, "Not implemented, incrementing PC for fun")

    # JN
    if lower == '0010':
        reg['pc'] += 1
        return (True, "Not implemented, incrementing PC for fun")

    # JP
    if lower == '0011':
        reg['pc'] += 1
        return (True, "Not implemented, incrementing PC for fun")

    # Unknown command
    return (False, "Machine Halted - undefined opcode")



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
