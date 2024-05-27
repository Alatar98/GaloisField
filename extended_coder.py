import galois
from functools import partial

irreducible_poly = "x^4 + x + 1"

GF = galois.GF(2**4, irreducible_poly=irreducible_poly)
GP = partial(galois.Poly, field=GF)


print(GF.properties)


syndrome_positions = [12, 13, 14, 0, 1, 2]

generator = GF([1])
for pos in syndrome_positions:

    mul = GF("a")**-pos
    
    generator = generator * GP([1,mul])
print("g= ",generator)


i = [10,0,6,5,2,12,1,2,7]

i = GP(i)
print("i= ",i)


a = i * generator
print("a= ",a)


f = [10,0,0,0,0,0,0,0,0,0,14,0,0,0,0]

f = GP(f)
print("f= ",f)


r = a + f
print("r= ",r)


S = []
for pos in syndrome_positions:
    mul = GF("a")**-pos
    S.append(r(mul))
S.reverse()
S=GP(S)
print("S= ",S)


from extended_euclid import extended_euclid as ext_eu

C ,T = ext_eu(S,3,GF)
print("C= ",C)
print("T= ",T)

nlst = []
for pos in range(a.degree+1):
    p = GF("a")**pos
    if C(p) == 0:
        nlst.append(pos)
print("nlst= ", nlst)

correction = []
for pos in nlst:
    a=((GF("a")**pos)**syndrome_positions[0])*GF(GF.degree)*((GF("a")**-1)**pos)
    N=-T(pos)
    C_=C.derivative()(pos)
    cor =a*N/C_
    correction.append(cor)

print("WRONG")
print("correction= ",correction)