import numbers


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
        a = to_GaloisElement(A)
    A = []
    for i in range(0,__base-1):
        sum = 0     #this does not have to be a GaloisElement because radd with integers works if the integer is 0
        for k in range(len(a)):
            sum += a[k] * (__primitive_element**-i)**k
        A.append(sum / GaloisElement(__base-1))
    return A