__version__ = "0.0.1"
from numbers import Number
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
    def __mul__(self, other):
        if not isinstance(other, Number):
            raise TypeError("Cannot multiply capacity by %r" % (other,))
        return self._arithmetic_to_capacity(operator.mul, other)
    __rmul__ = __mul__
    def __add__(self, other):
        if not isinstance(other, Capacity):
            raise TypeError("Cannot add Capacity and %r objects" % (other,))
        return self._arithmetic_to_capacity(operator.add, other)
    def __iadd__(self, other):
        self.bits = (self + other).bits
    def __sub__(self, other):
        if not isinstance(other, Capacity):
            raise TypeError("Cannot subtract %r objects from Capacity" % (other,))
        return self._arithmetic_to_capacity(operator.sub, other)
    def __isub__(self, other):
        self.bits = (self - other).bits
    def __div__(self, other):
        if isinstance(other, Capacity):
            return self._arithmetic_to_number(operator.div, other)
        return self._arithmetic_to_capacity(operator.div, other)
    def __mod__(self, other):
        if isinstance(other, Capacity):
            return self._arithmetic_to_capacity(operator.mod, other)
        return self._arithmetic_to_number(operator.mod, other)
    def _arithmetic_to_number(self, operator, operand):
        return operator(self.bits, operand.bits if isinstance(operand, Capacity) else operand)
    def _arithmetic_to_capacity(self, operator, operand):
        return Capacity(self._arithmetic_to_number(operator, operand))
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
