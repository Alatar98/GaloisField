import galoisfield as gf
from galoisfield import GaloisElement as ge
from galoisfield import GaloisPolynomial as gp

import numpy as np

def calc_generator_poly(k, n):
    g = gp([1])
    for i in range(k, n):
        g=g*gp([-gf.get_primitive_element()**-i,ge(1)])
    return g

class coder:
    def __init__(self, n, d, coder_type="systematic"):
        self.n = n
        self.d = d
        self.k = n-d+1

        self.coder_type = coder_type

        if coder_type == "systematic":
            self.generator = calc_generator_poly(0, self.n-self.k)
        else:
            self.generator = calc_generator_poly(self.k, self.n)

    def encode(self, data):
        if len(data) != self.k:
            raise ValueError("Data length must be equal to k")

        data = gp(data[::-1])

        if self.coder_type == "systematic":
            mul = [1 if i == self.n-self.k else 0 for i in range(self.n)]
            data = gp(data)*gp(mul)
            q,r = data/self.generator
            data = data - r
        else:
            raise NotImplementedError("Only systematic encoding is implemented")


        return data
    
    def calc_syndrome(self, data):

        if self.coder_type == "systematic":
            syndrome = gf.direct_transform(data)
            syndrome = syndrome[0:self.n-self.k]
        else:
            raise NotImplementedError("Only systematic encoding is implemented")

        return syndrome
    
    def calc_c(self, syndrome, f_max):
        if self.coder_type == "systematic":
            
            a = gp([1 if i == self.n-self.k else 0 for i in range(self.n)])
            b = gp(syndrome)
            q,r = a/b
            v_old = gp([1])
            v_cur = gp([0])
            w_old = gp([0])
            w_cur = gp([1])

            v_new = v_old - q*v_cur
            w_new = w_old - q*w_cur
            while r.degree() >=2:
                a = b
                b = r
                q,r = a/b

                [v_old,v_cur] = [v_cur,v_new]
                [w_old,w_cur] = [w_cur,w_new]

                v_new = v_old - q*v_cur
                w_new = w_old - q*w_cur
            
            c = gp([1])-q*w_cur
            
        else:
            raise NotImplementedError("Only systematic encoding is implemented")

        return c
    
    
        