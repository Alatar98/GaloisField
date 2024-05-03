import numbers
from typing import Any


__base = 7

def get_base():
    return __base

class GaloisElement:
    def __init__(self, value, base=None):
        if not isinstance(value, numbers.Number):
            raise TypeError(f"Value must be a whole number, not '{type(value).__name__}'")
        if value % 1 != 0:
            raise ValueError("Value must be a whole number")
        if base is not None:
            self.base = base
        else:
            self.base = get_base()
        self.value = value % self.base

    def __add__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'+' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement((self.value + other.value) % self.base)
    
    def __iadd__(self, other):
        return self + other
    
    def __radd__(self, other):
        if other == 0:
            other = GaloisElement(0)
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'+' not supported between instances of '{type(other).__name__}' and '{type(self).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return self + other
    
    def __neg__(self):
        return GaloisElement(-self.value)

    def __sub__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'-' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement((self.value - other.value) % self.base)

    def __mul__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'*' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement((self.value * other.value) % self.base)

    def __truediv__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'/' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement(self.value * other.inverse().value)

    def __pow__(self, power):
        if not isinstance(power, numbers.Integral):
            raise TypeError(
                            f"'**' not supported between instances of '{type(self).__name__}' and noninteger('{type(power).__name__}')"
                            )
        power = power % (self.base-1)
        return GaloisElement(pow(self.value, power, self.base))
        

    def __eq__(self, other):
        if not isinstance(other, GaloisElement):
            return False
        return self.value == other.value and self.base == other.base
    
    def __ne__(self, other):
        if not isinstance(other, GaloisElement):
            return True
        return self.value != other.value or self.base != other.base
    
    def __lt__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return self.value < other.value
    
    def __le__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'<=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return self.value <= other.value
    
    def __gt__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'>' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return self.value > other.value
    
    def __ge__(self, other):
        if not isinstance(other, GaloisElement):
            raise TypeError(
                f"'>=' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return self.value >= other.value
    
    def __bool__(self):
        return self.value != 0
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"GaliosElement({self.value}, base={self.base})"
       
    
    def log_primitive(self):
        return GaloisElement(logarithm_primitive_element(self.value, self.base))
    
    def order(self):
        for i in range(1, self.base):
            if pow(self.value, i, self.base) == 1:
                return i
        return None

    def inverse(self):
        return self**-1
    


def __is_primitive_element(element):
    is_in_power = [False] * (__base - 1)
    for i in range(1, __base):
        is_in_power[pow(element, i, __base)-1] = True

    if False in is_in_power:
        return False
    return True

def calculate_primitive_element():
    for i in range(2, __base):
        if __is_primitive_element(i):
            return GaloisElement(i)
    raise ValueError("No primitive element found for base " + str(__base))

__primitive_element = calculate_primitive_element()



def get_primitive_element():
    return __primitive_element

def __isprime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

def set_base(base):
    if not isinstance(base, numbers.Number):
        raise TypeError(f"Base must be a whole number, not '{type(base).__name__}'")
    if base % 1 != 0:
        raise ValueError("Base must be a whole number")
    global __base, __primitive_element
    if not __isprime(base):
        print("Warning: Base is not a prime number!")
    __base = base
    __primitive_element = calculate_primitive_element()

def get_primitive_table():
    primitive_table = {0:0}
    for i in range(1, __base):
        primitive_table[(__primitive_element**i).value]=i
    return dict(sorted(primitive_table.items()))

def logarithm_primitive_element(element,base=__base):
    if base != __base:
        primitive_element = calculate_primitive_element()
    else:
        primitive_element = __primitive_element

    if element == 0:
        return element
    if element == 1:
        return 0
    if element == primitive_element.value:
        return element
    for i in range(2, base):
        if (primitive_element**i).value == element:
            return i
    raise ValueError("Element is not a power of the primitive element")


def to_GaloisElement(value):
    if hasattr(value, "__len__"):
        if all(isinstance(x, GaloisElement) for x in value):
            return value
        return [GaloisElement(x) for x in value]
    if isinstance(value, GaloisElement):
        return value
    return GaloisElement(value)
    

def inverse_transform(A):
    if not all(isinstance(x, GaloisElement) for x in A):
        A = to_GaloisElement(A)
    a = []
    for k in range(0,__base-1):
        sum = 0     #this does not have to be a GaloisElement because radd with integers works if the integer is 0
        for i in range(len(A)):
            sum += A[i] * (__primitive_element**k)**i
        a.append(sum)
    return a


def direct_transform(a):
    if not all(isinstance(x, GaloisElement) for x in a):
        a = to_GaloisElement(a)
    A = []
    for i in range(0,__base-1):
        sum = 0     #this does not have to be a GaloisElement because radd with integers works if the integer is 0
        for k in range(len(a)):
            sum += a[k] * (__primitive_element**-i)**k
        A.append(sum / GaloisElement(__base-1))
    return A

def convolve(A,B):
    if not all(isinstance(x, GaloisElement) for x in A):
        A = to_GaloisElement(A)
    if not all(isinstance(x, GaloisElement) for x in B):
        B = to_GaloisElement(B)
    base = A[0].base

    if len(A)!=base-1:
        print("Warning in convolve: A is not of length base-1. Assuming 0 for the rest of the elements")
        while len(A) < base-1:
            A.append(GaloisElement(0))
    if len(B)!=base-1:
        print("Warning in convolve: B is not of length base-1. Assuming 0 for the rest of the elements")
        while len(B) < base-1:
            B.append(GaloisElement(0))

    C = []
    for i in range(base-1):
        sum=0
        for j in range(base-1):
            sum += A[j]*B[-j+i]
        C.append(sum)
    return C


class  GaloisPolynomial:
    def __init__(self, coefficients):
        if not hasattr(coefficients, "__len__"):
            raise TypeError(f"coefficients must be a list, not '{type(coefficients).__name__}'")
        if not all(isinstance(x, GaloisElement) for x in coefficients):
            coefficients = to_GaloisElement(coefficients)
        if len(coefficients) > get_base()-1:
            raise ValueError(f"Length of coefficients must be smaller than {get_base()-1}, not {len(coefficients)}")
        while len(coefficients) < get_base()-1:
            coefficients.append(GaloisElement(0))

        self.coefficients = coefficients
        self.base = coefficients[0].base

    def __add__(self, other):
        if isinstance(other, GaloisElement):
            other = GaloisPolynomial([other])
        if not isinstance(other, GaloisPolynomial):
            raise TypeError(
                f"'+' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisPolynomial([self[i] + other[i] for i in range(len(self))])
    
    def __sub__(self, other):
        if not isinstance(other, GaloisPolynomial):
            raise TypeError(
                f"'-' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisPolynomial([self[i] - other[i] for i in range(len(self))])
    
    
    def __mul__(self, other):
        if isinstance(other, GaloisElement):
            other = GaloisPolynomial([other])
        if not isinstance(other, GaloisPolynomial):
            raise TypeError(
                f"'*' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        C = []
        for i in range(self.base-1):
            sum = 0
            for j in range(self.base-1):
                sum += self[j]*other[-j+i]
            C.append(sum)
        return GaloisPolynomial(C)
    
    
    def __truediv__(self, other):
        if not isinstance(other, GaloisPolynomial):
            raise TypeError(
                f"'/' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'"
                )
        if self.base != other.base:
            raise ValueError("Base mismatch")
        
        if other.degree() > self.degree():
            return GaloisPolynomial([GaloisElement(0)]), self.copy()
        
        quotient = []
        remainder = self.copy()

        self_deg = self.degree()
        deg_diff = self.degree()-other.degree()

        for i in range(deg_diff + 1):
            quotient.insert(0,remainder[self_deg-i] / other[self_deg-deg_diff])
            remainder -= ((other**(deg_diff-i))*quotient[0])


        return GaloisPolynomial(quotient), remainder
    
    def __pow__(self, power):
        if not isinstance(power, numbers.Integral):
            raise TypeError(
                            f"'**' not supported between instances of '{type(self).__name__}' and noninteger('{type(power).__name__}'"
                            )
        tmp = GaloisPolynomial([0])
        for i in range(self.base-1):
            tmp[(i+power)%(self.base-1)] = self[i]
        return tmp
    
    def degree(self):
        for i in range(self.base-2, 0, -1):
            if self[i] != GaloisElement(0):
                return i
        return 0

    def __str__(self):
        return str([n.value for n in self])
    
    def __len__(self):
        return len(self.coefficients)

    def __getitem__(self, index):
        return self.coefficients[index]
    
    def __setitem__(self, index, value):
        if not isinstance(value, GaloisElement):
            raise TypeError(f"Value must be a GaloisElement, not '{type(value).__name__}'")
        self.coefficients[index] = value

    def copy(self):
        return GaloisPolynomial(self.coefficients.copy())