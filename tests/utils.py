import pytest

from capacity import from_string


def assert_value_error(s):
    with pytest.raises(ValueError):
        from_string(s)
