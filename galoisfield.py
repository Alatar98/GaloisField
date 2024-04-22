
__base = 7

def get_base():
    return __base

class GaloisElement:
    def __init__(self, value, base=None):
        if base is not None:
            self.base = base
        else:
            self.base = get_base()
        self.value = value % self.base

    def __add__(self, other):
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement((self.value + other.value) % self.base)

    def __sub__(self, other):
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement((self.value - other.value) % self.base)

    def __mul__(self, other):
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement((self.value * other.value) % self.base)

    def __truediv__(self, other):
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return GaloisElement(self.value * pow(other.value, self.base - 2, self.base))

    def __pow__(self, power):
        return GaloisElement(pow(self.value, power, self.base))

    def __eq__(self, other):
        return self.value == other.value and self.base == other.base
    
    def __ne__(self, other):
        return self.value != other.value or self.base != other.base
    
    def __lt__(self, other):
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return self.value < other.value
    
    def __le__(self, other):
        if self.base != other.base:
            raise ValueError("Base mismatch")
        return self.value <= other.value
    
    def log_primitive(self):
        return GaloisElement(logarithm_primitive_element(self.value, self.base))
    
    def order(self):
        for i in range(1, self.base):
            if pow(self.value, i, self.base) == 1:
                return i
        return None

    def inverse(self):
        return self**-1
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"GaliosElement({self.value}, base={self.base})"
    




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

def set_base(base):
    global __base, __primitive_element
    __base = base
    __primitive_element = calculate_primitive_element()



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
    return [GaloisElement(x) for x in value]
    

def transform(A):
    if not all(isinstance(x, GaloisElement) for x in A):
        A = to_GaloisElement(A)
    a = []
    for k in range(0,__base-2):
        sum = GaloisElement(0)
        for i in range(len(A)):
            sum += A[i] * (__primitive_element**k)**i
        a.append(sum)
    return a


def inverse_transform(a):
    if not all(isinstance(x, GaloisElement) for x in a):
        a = to_GaloisElement(A)
    A = []
    for i in range(len(a)):
        sum = GaloisElement(0)
        for k in range(0,__base-2):
            sum += a[k] * (__primitive_element**-i)**k
        A.append(sum / GaloisElement(__base-1))
    return A