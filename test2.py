import reedsolomon as rs
from galoisfield import GaloisPolynomial as gp
import galoisfield as gf

coder = rs.coder(6, 5)

print(coder.generator)


encoded = coder.encode([5,3])

print(encoded)

fehler = gp([0,0,3,0,1,0])

recieved = encoded + fehler

print(recieved)


print(coder.calc_syndrome(recieved))

print("c")
syndrome = gp([3,0,4,3])

print(coder.calc_c(syndrome,2))


print("wrong bits")

print(gf.inverse_transform(coder.calc_c(syndrome,2)))

