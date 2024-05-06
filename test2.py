import reedsolomon as rs
from galoisfield import GaloisPolynomial as gp
import galoisfield as gf

coder = rs.coder(6, 5)

print(coder.generator)


encoded = coder.encode([3,1])

print(encoded)

fehler = gp([0,0,0,-1,0,1])

recieved = encoded + fehler

print(recieved)


print(coder.calc_syndrome(recieved))



