from . import capacity
import re

_CAPACITY_PATTERN = re.compile(r"^([0-9\.]+)\s*\*?\s*(.+)$")

def _get_known_capacity(s):
    return capacity._KNOWN_CAPACITIES.get(s, None)

def from_string(s):
    if s in capacity._KNOWN_CAPACITIES:
        return capacity._KNOWN_CAPACITIES[s]
    match = _CAPACITY_PATTERN.match(s)
    if not match:
        raise ValueError(s)
    amount = float(match.group(1))
    unit = _get_known_capacity(match.group(2))
    if unit is None:
        raise ValueError(s)
    return amount * unit
