from __future__ import division
import decimal
import math
import re
import operator
from numbers import Number


class Capacity(object):

    def __init__(self, bits):
        super(Capacity, self).__init__()
        if isinstance(bits, str):
            bits = from_string(bits).bits
        self.bits = bits

    def __nonzero__(self):
        return bool(self.bits)

    def __bool__(self):
        return self.__nonzero__()

    def __hash__(self):
        return hash(self.bits)
    # Equality and comparison, python 3 style. We don't rely on __cmp__ or cmp.

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
    # Arithmetic

    def __abs__(self):
        return Capacity(abs(self.bits))

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
        if self == 0:
            return 0
        return self._arithmetic_to_capacity(operator.mod, other)

    def __rmod__(self, other):
        if other == 0:
            return 0
        raise TypeError("Attempt to perform modulo of %r by Capacity" %
                        (other,))

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
                raise TypeError(
                    "Attempt to perform %s operation between capacity and %r" %
                    (operator.__name__, operand))
            operand = Capacity(operand)
        return operator(self.bits, operand.bits)

    def _arithmetic_to_capacity(self, *args, **kwargs):
        return Capacity(self._arithmetic_to_number(*args, **kwargs))
    # Representation

    def __str__(self):
        if self < byte:
            return self._format_as_number_of_bits()
        result = None
        for name, unit in reversed(_SORTED_CAPACITIES):
            if unit * 0.1 > self:
                continue
            unit_fraction = self / unit
            # use at most 2 precision points
            rounded_fraction = round(unit_fraction, 2)
            # whole numbers should still be whole
            rounded_fraction = int(
                rounded_fraction) if rounded_fraction.is_integer() else rounded_fraction
            current_result = '{0}*{1}'.format(rounded_fraction, name)
            if result is not None:
                # switch to current result if it is more compact (e.g. 0.5MB <
                # 0.49MiB)
                return result if len(result.split("*")[0]) <= len(current_result.split("*")[0]) else current_result
            # continue with result to next iteration to check for better
            # representation
            result = current_result
        if result is not None:
            return result
        return self._format_as_number_of_bits()

    def _format_as_number_of_bits(self):
        bits = self.bits
        if isinstance(bits, float) and bits.is_integer():
            bits = int(bits)
        return '{0}*bit'.format(bits)

    def __format__(self, capacity):
        if not capacity:
            return str(self)
        formatter, value = self._get_new_style_formatter_and_value(capacity)
        returned = formatter(value)
        return returned

    def _get_new_style_formatter_and_value(self, specifier):
        include_unit = specifier.endswith("!")
        if include_unit:
            specifier = specifier[:-1]
        unit_name = specifier
        unit = _KNOWN_CAPACITIES.get(specifier)
        formatter = str
        if unit is None:
            for unit_name in _KNOWN_CAPACITIES:
                if specifier.endswith(unit_name):
                    unit = _KNOWN_CAPACITIES[unit_name]
                    formatter = "{{0:{0}}}".format(specifier[:-len(unit_name)]).format
                    break
            else:
                raise ValueError("Unknown specifier: {0}".format(specifier))
        value = self // unit
        if include_unit:
            value = "{0}{1}".format(value, unit_name)
        return formatter, value

    def __repr__(self):
        if self.bits == 0:
            return self._format_as_number_of_bits()
        for name, unit in reversed(_SORTED_CAPACITIES):
            if self % unit == 0:
                return '{0}*{1}'.format(self // unit, name)
        return self._format_as_number_of_bits()

_KNOWN_CAPACITIES = {}

__all__ = ['Capacity']


def _add_known_capacity(name, capacity):
    _KNOWN_CAPACITIES[name] = capacity
    globals()[name] = capacity
    __all__.append(name)

_add_known_capacity('bit', Capacity(1))
_add_known_capacity('byte', 8 * bit)
_add_known_capacity('b', byte)

for multiplier, chain in [
    (1024, ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB']),
    (1000, ['KB', 'MB', 'GB', 'TB', 'PB', 'EB']),
]:
    current = multiplier * byte
    for name in chain:
        _add_known_capacity(name, current)
        current *= multiplier
_SORTED_CAPACITIES = sorted(
    _KNOWN_CAPACITIES.items(), key=lambda pair: pair[1])

# parsing

_CAPACITY_PATTERN = re.compile(r"^([0-9\.]+)\s*\*?\s*(.+)$")


def _get_known_capacity(s):
    return _KNOWN_CAPACITIES.get(s, None)


def from_string(s):
    if s in _KNOWN_CAPACITIES:
        return _KNOWN_CAPACITIES[s]
    match = _CAPACITY_PATTERN.match(s)
    if not match:
        raise ValueError(s)
    amount = decimal.Decimal(match.group(1))
    unit = _get_known_capacity(match.group(2))
    if unit is None:
        raise ValueError(s)
    num_bits = amount * unit.bits
    if num_bits.to_integral() == num_bits:
        num_bits = int(num_bits)
    else:
        num_bits = float(num_bits)
    return Capacity(num_bits)
