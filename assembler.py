import fileinput
from util import *

def goodreg(s):
    s = s[1]
    s = bin(int(s))[2:]
    if len(s) == 1:
        s = '0' + s
    return s

data = []
for line in fileinput.input():
    data.append(line)

print(0, len(data), end=' ')
for line in data:
    address = '000000000000'
    opcode = '000000'
    mode = '0000'
    reg = '00'

    line = line.split()
    if line[0] == 'halt':
        opcode = '000000'
    if line[0] == 'nop':
        opcode = '000001'

    if line[0] == 'ld':
        opcode = '010000'
    if line[0] == 'st':
        opcode = '010001'
    if line[0] == 'em':
        opcode = '010010'
    if line[0] == 'ldx':
        opcode = '011000'
    if line[0] == 'stx':
        opcode = '011001'
    if line[0] == 'emx':
        opcode = '011010'

    if line[0] == 'add':
        opcode = '100000'
    if line[0] == 'sub':
        opcode = '100001'
    if line[0] == 'clr':
        opcode = '100010'
    if line[0] == 'com':
        opcode = '100011'
    if line[0] == 'and':
        opcode = '100100'
    if line[0] == 'or':
        opcode = '100101'
    if line[0] == 'xor':
        opcode = '100110'
    if line[0] == 'addx':
        opcode = '101000'
    if line[0] == 'subx':
        opcode = '101001'
    if line[0] == 'clrx':
        opcode = '101010'

    if line[0] == 'j':
        opcode = '110000'
    if line[0] == 'jz':
        opcode = '110001'
    if line[0] == 'jn':
        opcode = '110010'
    if line[0] == 'jp':
        opcode = '0011'

    if line[0] in ['ld', 'st', 'em', 'ldx', 'stx', 'emx', 'add', 'sub', 'and', 'or', 'xor', 'addx', 'subx', 'j', 'jz', 'jn', 'jp']:
        if line[1] == 'dir':
            mode = '0000'
        if line[1] == 'imm':
            mode = '0001'
        if line[1] == 'idx':
            mode = '0010'
        if line[1] == 'idr':
            mode = '0100'
        if line[1] == 'xdr':
            mode = '0110'

        if line[1] == 'dir':
            address = to_printable(int(line[-1],16), 12, True)
        if line[1] == 'imm':
            address = to_printable(int(line[-1]   ), 12, True)

    if line[0] == 'clrx':
        reg = goodreg(line[1])

    if line[0] in ['ldx', 'stx', 'emx', 'addx', 'subx']:
        reg = goodreg(line[2])

    if line[0] in ['j', 'jz', 'jn', 'jp']:
        address = bin(int(line[2], 16))[2:]

    command = address + opcode + mode + reg

    if line[0] not in ['clr', 'com', 'halt', 'nop', 'clrx', 'ld', 'st', 'em', 'ldx', 'stx', 'emx', 'add', 'sub', 'and', 'or', 'xor', 'addx', 'subx', 'j', 'jz', 'jn', 'jp']:
        command = to_printable(int(line[0]), 24,True)

    command = int(command, 2)
    print(to_printable(command, 6), end=' ')

print()
print(0)
