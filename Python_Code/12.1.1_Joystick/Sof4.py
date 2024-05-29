# 
aout = 0
for a in range(0, 2):
    aout = aout + 1
    print("a is ", a)
    v = ((a+1) & 0x03)
    print(v, aout)
    print(f" a is {a}, bin(v) is {bin(v)} ")
print("hex40 is ", bin(0x40))
print (f"0x03 is {bin(0x03)}")
print(bin(0xff))
    