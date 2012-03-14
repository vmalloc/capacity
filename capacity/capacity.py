from __future__ import division
from .__version__ import __version__
import math
import operator
from numbers import Number

class Capacity(object):
    def __init__(self, bits):
        super(Capacity, self).__init__()
        self.bits = bits
    def __nonzero__(self):
        return bool(self.bits)
    def __bool__(self):
        return self.__nonzero__()
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
    def __truediv__(self, other):
        if isinstance(other, Capacity):
            return self._arithmetic_to_number(operator.truediv, other)
        return self._arithmetic_to_capacity(operator.truediv, other, allow_nonzero_ints=True)
    def __rdiv__(self, other):
        if other == 0:
            return 0
        raise TypeError("Attempt to divide %r by Capacity" % (other,))
    __rtruediv__ = __rdiv__
    __rfloordiv__ = __rdiv__
    def __floordiv__(self, other):
        returned = self / other
        if isinstance(other, Capacity):
            returned = math.floor(returned)
        else:
            returned.bits = math.floor(returned.bits)
        if isinstance(returned, Number):
            returned = int(returned)
        return returned
    def __mod__(self, other):
        return self._arithmetic_to_capacity(operator.mod, other)
    def __rmod__(self, other):
        if other == 0:
            return self
        raise TypeError("Attempt to perform modulo of %r by Capacity" % (other,))
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
                raise TypeError("Attempt to perform %s operation between capacity and %r" % (operator.__name__, operand))
            operand = Capacity(operand)
        return operator(self.bits, operand.bits)
    def _arithmetic_to_capacity(self, *args, **kwargs):
        return Capacity(self._arithmetic_to_number(*args, **kwargs))
    ## Representation
    def __str__(self):
        if self < byte:
            return self._format_as_number_of_bits()
        for name, unit in reversed(_SORTED_CAPACITIES):
            if self % unit == 0:
                return '{0}*{1}'.format(int(self // unit), name)
            if unit * 0.1 < self < unit * 0.9:
                return '{0:.1}*{1}'.format(self/unit, name)
        return self._format_as_number_of_bits()
    def _format_as_number_of_bits(self):
        return '{0}*bit'.format(self.bits)
    def __repr__(self):
        return str(self)

_KNOWN_CAPACITIES = {}

__all__ = ['Capacity']

def _add_known_capacity(name, capacity):
    _KNOWN_CAPACITIES[name] = capacity
    globals()[name] = capacity
    __all__.append(name)

_add_known_capacity('bit', Capacity(1))
_add_known_capacity('byte', 8 * bit)

for multiplier, chain in [
    (1024, ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB']),
    (1000, ['KB', 'MB', 'GB', 'TB', 'PB', 'EB']),
    ]:
    current = multiplier * byte
    for name in chain:
        _add_known_capacity(name, current)
        current *= multiplier
_SORTED_CAPACITIES = sorted(_KNOWN_CAPACITIES.items(), key=lambda pair: pair[1])
