nop
ld   dir     0c4
st   idx
em   xdr
ldx  imm x1  12
stx  dir x2  0c4
emx  dir x3  0c4
add  idx
sub  xdr
clr
com
and  dir     0c4
or   xdr
xor  imm     57
addx dir x1  0c4
subx imm x0  345
clrx     x1
j    dir 0c4 0c4
jz   idx 0c4
jn   idr 0c4
jp   xdr 0c4
halt
100
1000
10000
