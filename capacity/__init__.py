__version__ = "0.0.1"
import operator

class Capacity(object):
    def __init__(self, bits):
        super(Capacity, self).__init__()
        self.bits = bits
    def __hash__(self):
        return hash(self.bits)
    ## Equality and comparison, python 3 style. We don't rely on __cmp__ or cmp.
    def _compare(self, other):
        return (self - other).bits
    def __eq__(self, other):
        try:
            return self._compare(other) == 0
        except TypeError:
            return False
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        return self._compare(other) < 0
    def __gt__(self, other):
        return self._compare(other) > 0
    def __le__(self, other):
        return self._compare(other) <= 0
    def __ge__(self, other):
        return self._compare(other) >= 0
    ## Arithmetic
    def __neg__(self):
        return Capacity(-self.bits)
    def __mul__(self, other):
        if isinstance(other, Capacity):
            raise TypeError("Cannot multiply Capacity by Capacity")
        return self._arithmetic_to_capacity(operator.mul, other,
                                            allow_nonzero_ints=True)
    __rmul__ = __mul__
    def __add__(self, other):
        return self._arithmetic_to_capacity(operator.add, other)
    __radd__ = __add__
    def __sub__(self, other):
        return self._arithmetic_to_capacity(operator.sub, other)
    def __rsub__(self, other):
        return (-self) + other
    def __div__(self, other):
        if isinstance(other, Capacity):
            return self._arithmetic_to_number(operator.div, other)
        return self._arithmetic_to_capacity(operator.div, other, allow_nonzero_ints=True)
    def __rdiv__(self, other):
        if other == 0:
            return 0
        raise TypeError("Attempt to divide %r object by Capacity" % (other,))
    __rfloordiv__ = __rdiv__
    def __floordiv__(self, other):
        return self._arithmetic_to_number(operator.floordiv, other, allow_nonzero_ints=True)
    def __mod__(self, other):
        return self._arithmetic_to_capacity(operator.mod, other)
    def __rmod__(self, other):
        if other == 0:
            return self
        raise TypeError("Attempt to perform modulo of %r object by Capacity" % (other,))
    def roundup(self, boundary):
        returned = (self // boundary) * boundary
        if self % boundary != 0:
            returned += boundary
        return returned
    def rounddown(self, boundary):
        return (self // boundary) * boundary
    def _arithmetic_to_number(self, operator, operand, allow_nonzero_ints=False):
        if not isinstance(operand, Capacity):
            if not allow_nonzero_ints and operand != 0:
                raise TypeError("Attempt to perform %s operation between capacity and %r object" % (operator.__name__, operand))
            operand = Capacity(operand)
        return operator(self.bits, operand.bits)
    def _arithmetic_to_capacity(self, *args, **kwargs):
        return Capacity(self._arithmetic_to_number(*args, **kwargs))
    ## Representation
    def __str__(self):
        return '{0} bit'.format(self.bits)
    def __repr__(self):
        return str(self)

KNOWN_CAPACITIES = {}

__all__ = ['Capacity']

def _add_known_capacity(name, capacity):
    KNOWN_CAPACITIES[name] = capacity
    globals()[name] = capacity
    __all__.append(name)

_add_known_capacity('bit', Capacity(1))
_add_known_capacity('byte', 8 * bit)

for multiplier, chain in [
    (1024, ['KiB', 'MiB', 'GiB', 'TiB', 'XiB']),
    (1000, ['KB', 'MB', 'GB', 'TB', 'XB']),
    ]:
    current = multiplier * byte
    for name in chain:
        _add_known_capacity(name, current)
        current *= multiplier
