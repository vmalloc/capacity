import pytest
from capacity import *
from numbers import Integral
from operator import truediv


def test_truth():
    assert byte
    assert GiB
    assert not (0 * byte)


def test_bits_attribute():
    assert (666 * bit).bits == 666


def test_hashability():
    assert hash(MiB) == hash(MiB.bits)


def test_equality():
    small = Capacity(666)
    great = Capacity(667)
    assert small == small
    assert great == great
    assert small != great
    assert great != small
    assert great > small
    assert small > (- small)
    assert great > (- great)
    assert 0 > (- small)
    assert 0 < small
    assert (- small) < 0
    assert great >= small
    assert small < great
    assert small <= great
    # negative tests
    assert not (small > great)
    assert not (small < -small)
    assert not (small >= great)
    assert not (great < small)
    assert not (great <= small)
    assert not (small != small)
    assert not (great != great)
    assert not (great == small)
    assert not (small == great)


def test_equality_to_other_objects():
    for obj in ("some_string", "", 2.0, 2, True, False):
        assert MiB != obj
        assert not (MiB == obj)


def test_multiplication_by_zero():
    assert isinstance(0 * MiB, Capacity)


def test_equality_to_zero():
    assert not (MiB == 0)
    assert MiB != 0
    assert not (0 * MiB != 0)
    assert 0 * MiB == 0


def test_new_style_formatting():
    assert "{0}".format(3 * GiB) == str(3 * GiB)
    assert "{0!r}".format(3 * GiB) == repr(3 * GiB)
    assert "{0:GiB}".format(3 * GiB) == "3"
    with pytest.raises(ValueError):
        assert "{0:kjdkj}".format(3 * GiB)
    assert u"{0:byte}".format(100 * byte) == u"100"


def test_new_style_with_specifiers():
    assert "{0:<5MiB}".format(MiB) == "1    "
    assert "{0:>5MiB}".format(MiB) == "    1"
    assert "{0:^5MiB}".format(MiB) == "  1  "
    assert "{0:05MiB}".format(MiB) == "00001"


def test_new_style_with_unit():
    assert "{0:<5MiB!}".format(MiB) == "1MiB "


def test_simple_textual_representation():
    _assert_str_repr_equals(bit, '1*bit', '1*bit')
    _assert_str_repr_equals(bit, '1*bit', '1*bit')


def test_representation():
    _assert_str_repr_equals(0.5 * MiB, '0.5*MiB', '512*KiB')
    _assert_str_repr_equals(
        0.5 * MiB + bit, '0.5*MiB', '{0}*bit'.format(int((0.5 * MiB).bits + 1)))
    _assert_str_repr_equals(
        0.5 * MiB - bit, '0.5*MiB', '{0}*bit'.format(int((0.5 * MiB).bits - 1)))
    _assert_str_repr_equals(2 * MiB, '2*MiB', '2*MiB')
    _assert_str_repr_equals(
        GiB - bit, '1*GiB', '{0}*bit'.format(GiB.bits - 1))
    _assert_str_repr_equals(
        GiB - 0.5 * bit, '1*GiB', '{0}*bit'.format(GiB.bits - 0.5))

    # fractions with two decimal places
    _assert_str_repr_equals(
        0.99 * KiB, '0.99*KiB', '{0}*bit'.format(0.99 * 1024 * 8))
    _assert_str_repr_equals(
        0.59 * MiB, '0.59*MiB', '{0}*bit'.format(0.59 * 1024 * 1024 * 8))
    # fractions with multiple decimal places
    _assert_str_repr_equals(9122 * byte, '8.91*KiB', '9122*byte')
    _assert_str_repr_equals(
        23124232 * byte, '22.05*MiB', '23124232*byte')
    _assert_str_repr_equals(
        58918694226 * byte, '54.87*GiB', '58918694226*byte')
    _assert_str_repr_equals(
        213124232 * byte, '0.2*GiB', '213124232*byte')
    # test *B instead of only *iB
    _assert_str_repr_equals(
        0.5 * MB - bit, '0.5*MB', '{0}*bit'.format(int((0.5 * MB).bits - 1)))
    _assert_str_repr_equals(0.5 * MB, '0.5*MB', '500*KB')
    _assert_str_repr_equals(2 * MB, '2*MB', '2*MB')

    _assert_str_repr_equals(0 * bit, '0*bit', '0*bit')


def _assert_str_repr_equals(obj, str_value, repr_value):
    assert str(obj) == str_value
    assert repr(obj) == repr_value


def test_add():
    assert (MiB + MiB) == Capacity((MiB.bits * 2))
    assert (MiB + 0) == MiB
    assert (0 + MiB) == MiB


def test_iadd():
    a = MiB
    a += MiB
    assert a == (2 * MiB)


def test_abs():
    assert abs((- MiB)) == MiB
    assert abs(MiB) == MiB


def test_sub():
    assert (MiB - bit) == Capacity((MiB.bits - 1))
    assert (0 - bit) == (- bit)
    assert (bit - 0) == bit


def test_isub():
    a = 2 * MiB
    a -= MiB
    assert a == MiB


def test_neg():
    assert (- MiB).bits == (- MiB.bits)
    assert (MiB + (- MiB)) == 0
    assert ((- MiB) + (2 * MiB)) == MiB


def test_mul():
    assert (2 * MiB) == Capacity((MiB.bits * 2))
    assert (0 * MiB) == Capacity(0)


def test_div():
    assert (MiB / 2) == (0.5 * MiB)
    assert (GB / 10) == (100 * MB)
    assert ((2 * MiB) / 2) == MiB
    assert ((1.5 * MiB) / MiB) == 1.5
    assert ((2 * MiB) / MiB) == 2
    assert (0 / MiB) == 0
    assert ((2 * MiB) / MiB) == 2


def test_truediv():
    assert truediv(MiB, 2) == (0.5 * MiB)
    assert truediv((2 * MiB), 2) == MiB
    assert truediv((1.5 * MiB), MiB) == 1.5
    assert truediv((2 * MiB), MiB) == 2
    assert truediv(0, MiB) == 0
    assert truediv((2 * MiB), MiB) == 2


def test_mod():
    assert (((2 * MiB) + bit) % MiB) == bit
    assert (0 % MiB) == MiB
    assert ((0.5 * MiB) % (0.5 * MiB)) == 0


def test_floordiv():
    assert (((2 * MiB) + bit) // MiB) == 2
    assert isinstance((((2 * MiB) + bit) // MiB), Integral)
    assert ((2 * MiB) // 2) == MiB
    assert ((2 * MiB) // MiB) == 2
    assert isinstance(((2 * MiB) // MiB), Integral)
    assert ((2.001 * MiB) // 2) == (8392802 * bit)
    assert (0 // MiB) == 0


def test_roundup():
    assert MiB.roundup(MiB) == MiB
    assert (MiB + bit).roundup(MiB) == (2 * MiB)


def test_rounddown():
    assert MiB.rounddown(MiB) == MiB
    assert (MiB - bit).rounddown(MiB) == 0
    assert ((3 * MiB) - bit).rounddown(MiB) == (2 * MiB)


def test_invalid_arithmetic():
    size = 668 * bit

    with pytest.raises(TypeError):
        size * size
    with pytest.raises(TypeError):
        size + 3
    with pytest.raises(TypeError):
        3 / size
    with pytest.raises(TypeError):
        3 % size
    with pytest.raises(TypeError):
        size % 3
    with pytest.raises(TypeError):
        size < 2
    with pytest.raises(TypeError):
        size > 2
    with pytest.raises(ZeroDivisionError):
        size / 0
    with pytest.raises(ZeroDivisionError):
        size % 0


def test_from_string_construction():
    assert Capacity('20*GiB') == (20 * GiB)


def test_from_string_fractions():
    assert Capacity('1119.63 * TB') == (1119630 * GB)


def test_from_string():
    check = _assert_from_string_equals
    check("GiB", GiB)
    check("MiB", MiB)
    for variant in ("2*GiB", "2GiB", "2* GiB", "2 *GiB"):
        check(variant, 2 * GiB)


def test_invalid_patterns():
    check = _assert_value_error
    check("2")
    check("bla")
    check("GIB")
    check("1*GiB*bla")
    check("1+2")
    check("1*2")


def _assert_from_string_equals(s, value):
    assert from_string(s) == value


def _assert_value_error(s):
    with pytest.raises(ValueError):
        from_string(s)
