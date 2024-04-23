import galoisfield as gf
from galoisfield import GaloisElement as ge

import numpy as np


gf.set_base(7)

print(ge(3))
print([ge(3)])

print("4 + 5 = ",ge(4)+ge(5))
print("4 - 5 = ",ge(4)-ge(5))
print("-5 = ",-ge(5))
print("-5+5 = ",-ge(5)+ge(5))
print("4 * 5 = ",ge(4)*ge(5))
print("4 / 5 = ",ge(4)/ge(5))
print("4 ** 5 = ",ge(4)**5)
print("4 == 5 = ",ge(4)==ge(5))
print("5 == '5' = ",ge(5) == 5)
print("4 != 5 = ",ge(4)!=ge(5))
print("4 < 5 = ",ge(4)<ge(5))
print("4 <= 5 = ",ge(4)<=ge(5))
print("4 > 5 = ",ge(4)>ge(5))
print("log(4,primitive) = ",ge(4).log_primitive())
print("log(5,primitive) = ",ge(5).log_primitive())
print("log(6,primitive) = ",ge(6).log_primitive())
print("order(4) = ",ge(4).order())
print("order(5) = ",ge(5).order())
print("6^^-2: ", ge(1)/(ge(6)*ge(6)))
print("6**-2",ge(6)**-2)


print(f"Primitive element for base {gf.get_base()} is {gf.get_primitive_element()}")
print("Primitive table: ",gf.get_primitive_table())

#transformed = gf.transform(gf.to_GaloisElement([3,4,2,5,1]))
to_transform = [3,4,2,5,1]
transformed = gf.inverse_transform(to_transform)
#print([x.value for x in transformed])
#print(transformed)
print("a(x) of A(x)=3+4x+2*x^2+5x^3+x^4 is {}+{}x+{}x^2+{}x^3+{}x^4+{}x^5".format(*transformed))

inverse_transformed = gf.inverse_transform(transformed)
#print([x.value for x in inverse_transformed])
print("transformed back: A(x) = {}+{}x+{}x^2+{}x^3+{}x^4+{}x^5".format(*inverse_transformed))


transformed2 = gf.inverse_transform([3,4,2,5,1])

print([x for x in to_transform])
print([x.value for x in transformed])
print([x.value for x in gf.direct_transform(transformed)])
print("equal: ",gf.to_GaloisElement(to_transform) == gf.direct_transform(transformed)[:len(to_transform)])


gf.set_base(31)

print(f"Primitive element for base {gf.get_base()} is {gf.get_primitive_element()}")

to_transform2 = [3,4,2,5,1,6,7,8,9,10,11,12,13,0,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,14]
transformed2 = gf.inverse_transform(to_transform2)
inverse_transformed2 = gf.direct_transform(transformed2)

print([x for x in to_transform2])
print([x.value for x in transformed2])
print([x.value for x in inverse_transformed2])
print("equal: ",gf.to_GaloisElement(to_transform2) == inverse_transformed2[:len(to_transform2)])


gf.set_base(7)

A=[3,4,2,5,1,0]
B=[2,5,1,3,0,0]

C=np.convolve(A,B)

print(C)

A = gf.to_GaloisElement(A)
B = gf.to_GaloisElement(B)

C = np.convolve(A,B)

print([n.value for n in C])

print("A(x)B(x)= D(x) =")

D=[0]*(gf.get_base()-1)
for i in range(len(C)):
    D[i%(gf.get_base()-1)] += C[i]

print([n.value for n in D])

E=[]

for i in range(len(A)):
    sum=0
    for j in range(len(B)):
        sum += A[j]*B[-j+i]
    E.append(sum.value)

print(E)

A_trans = gf.inverse_transform(A)
B_trans = gf.inverse_transform(B)

F_trans = [A_trans[i]*B_trans[i] for i in range(len(A))]

F = gf.direct_transform(F_trans)

print([n.value for n in F])


G = gf.convolve(A,B)

print([n.value for n in G])



print("A(x),a_i",[n.value for n in A],[n.value for n in gf.inverse_transform(A)])
print("B(x),b_i",[n.value for n in B],[n.value for n in gf.inverse_transform(B)])
print("D(x),d_i",[n.value for n in D],[n.value for n in gf.inverse_transform(D)])
