import galoisfield as gf
from galoisfield import GaloisElement as ge
from galoisfield import GaloisPolynomial as gp
import reedsolomon as rs

import numpy as np


gf.set_base(7)

def calc_generator_poly(n):
    g = gp([1])
    for i in range(n):
        g=g*gp([-gf.get_primitive_element()**-i,ge(1)])
    return g


print("Generator for (6,5): ",calc_generator_poly(6-5))

def is_primitive_poly(p):
    for i in range(1, p.base):
        if p**i == gp([1]):
            return False
    return True

poly = gp([1,1,0,1,0,0])

print("Is primitive: ",is_primitive_poly(poly))