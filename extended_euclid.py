import galois
from functools import partial



def extended_euclid(syndrome, f_max, GF):

    GP = partial(galois.Poly, field=GF)
        
    a = GP([1 if i == 0 else 0 for i in range(syndrome.degree+2)])
    if not isinstance(syndrome, galois.Poly):
        b = GP(syndrome)
    else:
        b = syndrome
    q,r = a//b, a%b
    v_old = GP([1])
    v_cur = GP([0])
    w_old = GP([0])
    w_cur = GP([1])

    v_new = v_old - q*v_cur
    w_new = w_old - q*w_cur

    while r.degree >=f_max:
        a = b
        b = r
        q,r = a//b, a%b

        [v_old,v_cur] = [v_cur,v_new]
        [w_old,w_cur] = [w_cur,w_new]

        v_new = v_old - q*v_cur
        w_new = w_old - q*w_cur
    
    c = GP([1])-q*w_cur

    return c , r