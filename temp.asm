nop
ld   dir     018
st   idx     018
em   xdr     018
ldx  imm x1  12
stx  dir x2  018
emx  dir x3  018
add  idx     018
sub  xdr     018
clr
com
and  dir     018
or   xdr     018
xor  imm     57
addx dir x1  017
subx imm x0  345
clrx     x1
j    dir 015 018
jz   idx 0c4 018
jn   idr 0c4 018
jp   xdr 0c4 018
halt
100
1000
10000
