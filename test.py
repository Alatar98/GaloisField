import galoisfield as gf
from galoisfield import GaloisElement as ge


gf.set_base(7)

print(ge(3))
print([ge(3)])

print("4 + 5 = ",ge(4)+ge(5))
print("4 - 5 = ",ge(4)-ge(5))
print("4 * 5 = ",ge(4)*ge(5))
print("4 / 5 = ",ge(4)/ge(5))
print("4 ** 5 = ",ge(4)**5)
print("4 == 5 = ",ge(4)==ge(5))
print("4 != 5 = ",ge(4)!=ge(5))
print("4 < 5 = ",ge(4)<ge(5))
print("4 <= 5 = ",ge(4)<=ge(5))
print("4 > 5 = ",ge(4)>ge(5))
print("log(4,primitive) = ",ge(4).log_primitive())
print("log(5,primitive) = ",ge(5).log_primitive())
print("log(6,primitive) = ",ge(6).log_primitive())
print("order(4) = ",ge(4).order())
print("order(5) = ",ge(5).order())
print("inverse(5) = ",ge(5).inverse())



print(f"Primitive element for base {gf.get_base()} is {gf.get_primitive_element()}")

#transformed = gf.transform(gf.to_GaloisElement([3,4,2,5,1]))
transformed = gf.transform([3,4,2,5,1])
#print(transformed)
print("a(x) of A(x)=3+4x+2*x^2+5x^3+x^4 is {}+{}x+{}x^2+{}x^3+{}x^4".format(*transformed))

inverse_transformed = gf.inverse_transform(transformed)
print("transformed back: A(x) = {}+{}x+{}x^2+{}x^3+{}x^4".format(*inverse_transformed))


