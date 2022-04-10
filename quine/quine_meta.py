code = "7101\n7208\n7305\n7420\n7511\n76C0\n5662\n7714\n7851\n1967\n1A68\n99FF\nE500\n1553\n7B7E\n5BB2\n1BBE\n9BFF\n7B7F\n5BB2\n1BBF\n9BFF\n9AFF\n5EE2\n1EEF\n9EFF\n1773\n1B67\n9BFF\n2441\nD450\n0000\n".split()

def prnt(s):
    global p
    print(ith(p) + ": " + s)
    p += 1

def ith(n):
    j = hex(n)[2:]
    if len(j) == 1:
        return ("0"+j).upper()
    assert len(j) == 2
    return j.upper()

p = 16

prnt("C014")
jj = 25
for i in range(32):
    c = code[i]
    prnt("7E" + c[:2])
    prnt("7F" + c[2:])
    prnt("C051")
    prnt(c)
    prnt("C0"+ith(jj))
    jj += 5