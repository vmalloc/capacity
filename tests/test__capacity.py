import platform
if platform.python_version() >= '2.7':
    from unittest import TestCase
else:
    from unittest2 import TestCase
from capacity import *
from numbers import Integral
from operator import truediv

class CapacityTest(TestCase):

    def test__truth(self):
        self.assertTrue(bool(byte))
        self.assertTrue(bool(GiB))
        self.assertFalse(bool(0 * byte))

    def test__bits_attribute(self):
        self.assertEquals((666 * bit).bits, 666)

    def test__hashability(self):
        self.assertEquals(hash(MiB), hash(MiB.bits))

    def test__equality(self):
        small = Capacity(666)
        great = Capacity(667)
        self.assertEquals(small, small)
        self.assertEquals(great, great)
        # assertNotEqual uses == :-(
        self.assertTrue(small != great)
        self.assertTrue(great != small)
        self.assertGreater(great, small)
        self.assertGreater(small, -small)
        self.assertGreater(great, -great)
        self.assertGreater(0, -small)
        self.assertLess(0, small)
        self.assertLess(-small, 0)
        self.assertGreaterEqual(great, small)
        self.assertLess(small, great)
        self.assertLessEqual(small, great)
        # negative tests
        self.assertFalse(small > great)
        self.assertFalse(small < -small)
        self.assertFalse(small >= great)
        self.assertFalse(great < small)
        self.assertFalse(great <= small)
        self.assertFalse(small != small)
        self.assertFalse(great != great)
        self.assertFalse(great == small)
        self.assertFalse(small == great)

    def test__equality_to_other_objects(self):
        for obj in ("some_string", "", 2.0, 2, True, False):
            self.assertTrue(MiB != obj)
            self.assertFalse(MiB == obj)

    def test__multiplication_by_zero(self):
        self.assertIsInstance(0 * MiB, Capacity)

    def test__equality_to_zero(self):
        self.assertFalse(MiB == 0)
        self.assertTrue(MiB != 0)
        self.assertFalse(0 * MiB != 0)
        self.assertTrue(0 * MiB == 0)


class RepresentationTest(TestCase):

    def test__simple_textual_representation(self):
        self._assert_str_repr_equals(bit, '1*bit', '1*bit')
        self._assert_str_repr_equals(bit, '1*bit', '1*bit')

    def test__representation(self):
        self._assert_str_repr_equals(0.5 * MiB, '0.5*MiB', '512*KiB')
        self._assert_str_repr_equals(
            0.5 * MiB + bit, '0.5*MiB', '{0}*bit'.format(int((0.5 * MiB).bits + 1)))
        self._assert_str_repr_equals(
            0.5 * MiB - bit, '0.5*MiB', '{0}*bit'.format(int((0.5 * MiB).bits - 1)))
        self._assert_str_repr_equals(2 * MiB, '2*MiB', '2*MiB')
        self._assert_str_repr_equals(
            GiB - bit, '1*GiB', '{0}*bit'.format(GiB.bits - 1))
        self._assert_str_repr_equals(
            GiB - 0.5 * bit, '1*GiB', '{0}*bit'.format(GiB.bits - 0.5))

        # fractions with two decimal places
        self._assert_str_repr_equals(
            0.99 * KiB, '0.99*KiB', '{0}*bit'.format(0.99 * 1024 * 8))
        self._assert_str_repr_equals(
            0.59 * MiB, '0.59*MiB', '{0}*bit'.format(0.59 * 1024 * 1024 * 8))
        # fractions with multiple decimal places
        self._assert_str_repr_equals(9122 * byte, '8.91*KiB', '9122*byte')
        self._assert_str_repr_equals(
            23124232 * byte, '22.05*MiB', '23124232*byte')
        self._assert_str_repr_equals(
            58918694226 * byte, '54.87*GiB', '58918694226*byte')
        self._assert_str_repr_equals(
            213124232 * byte, '0.2*GiB', '213124232*byte')
        # test *B instead of only *iB
        self._assert_str_repr_equals(
            0.5 * MB - bit, '0.5*MB', '{0}*bit'.format(int((0.5 * MB).bits - 1)))
        self._assert_str_repr_equals(0.5 * MB, '0.5*MB', '500*KB')
        self._assert_str_repr_equals(2 * MB, '2*MB', '2*MB')

        self._assert_str_repr_equals(0 * bit, '0*bit', '0*bit')

    def _assert_str_repr_equals(self, obj, str_value, repr_value):
        self.assertEquals(str(obj), str_value)
        self.assertEquals(repr(obj), repr_value)


class CapacityArithmeticTest(TestCase):

    def test__add(self):
        self.assertEquals(MiB + MiB, Capacity(MiB.bits * 2))
        self.assertEquals(MiB + 0, MiB)
        self.assertEquals(0 + MiB, MiB)

    def test__iadd(self):
        a = MiB
        a += MiB
        self.assertEquals(a, 2 * MiB)

    def test__abs(self):
        self.assertEquals(abs(-MiB), MiB)
        self.assertEquals(abs(MiB), MiB)

    def test__sub(self):
        self.assertEquals(MiB - bit, Capacity(MiB.bits - 1))
        self.assertEquals(0 - bit, -bit)
        self.assertEquals(bit - 0, bit)

    def test__isub(self):
        a = 2 * MiB
        a -= MiB
        self.assertEquals(a, MiB)

    def test__neg(self):
        self.assertEquals((-MiB).bits, -(MiB.bits))
        self.assertEquals(MiB + (-MiB), 0)
        self.assertEquals(-MiB + (2 * MiB), MiB)

    def test__mul(self):
        self.assertEquals(2 * MiB, Capacity(MiB.bits * 2))
        self.assertEquals(0 * MiB, Capacity(0))

    def test__div(self):
        self.assertEquals(MiB / 2, 0.5 * MiB)
        self.assertEquals(GB / 10, 100 * MB)
        self.assertEquals((2 * MiB) / 2, MiB)
        self.assertEquals((1.5 * MiB) / MiB, 1.5)
        self.assertEquals((2 * MiB) / MiB, 2)
        self.assertEquals(0 / MiB, 0)
        self.assertEquals((2 * MiB) / MiB, 2)

    def test__truediv(self):
        self.assertEquals(truediv(MiB, 2), 0.5 * MiB)
        self.assertEquals(truediv(2 * MiB, 2), MiB)
        self.assertEquals(truediv(1.5 * MiB, MiB), 1.5)
        self.assertEquals(truediv(2 * MiB, MiB), 2)
        self.assertEquals(truediv(0, MiB), 0)
        self.assertEquals(truediv(2 * MiB, MiB), 2)

    def test__mod(self):
        self.assertEquals(((2 * MiB) + bit) % MiB, bit)
        self.assertEquals(0 % MiB, MiB)
        self.assertEquals(((0.5 * MiB) % (0.5 * MiB)), 0)

    def test__floordiv(self):
        self.assertEquals(((2 * MiB) + bit) // MiB, 2)
        self.assertIsInstance(((2 * MiB) + bit) // MiB, Integral)
        self.assertEquals((2 * MiB) // 2, MiB)
        self.assertEquals((2 * MiB) // MiB, 2)
        self.assertIsInstance((2 * MiB) // MiB, Integral)
        self.assertEquals((2.001 * MiB) // 2, 8392802 * bit)
        self.assertEquals(0 // MiB, 0)

    def test__roundup(self):
        self.assertEquals(MiB.roundup(MiB), MiB)
        self.assertEquals((MiB + bit).roundup(MiB), 2 * MiB)

    def test__rounddown(self):
        self.assertEquals(MiB.rounddown(MiB), MiB)
        self.assertEquals((MiB - bit).rounddown(MiB), 0)
        self.assertEquals((3 * MiB - bit).rounddown(MiB), 2 * MiB)


class InvalidArithmeticTest(TestCase):

    def test__invalid_arithmetic(self):
        size = 668 * bit

        with self.assertRaises(TypeError):
            size * size
        with self.assertRaises(TypeError):
            size + 3
        with self.assertRaises(TypeError):
            3 / size
        with self.assertRaises(TypeError):
            3 % size
        with self.assertRaises(TypeError):
            size % 3
        with self.assertRaises(TypeError):
            size < 2
        with self.assertRaises(TypeError):
            size > 2
        with self.assertRaises(ZeroDivisionError):
            size / 0
        with self.assertRaises(ZeroDivisionError):
            size % 0


class FromStringTest(TestCase):

    def test__from_string_construction(self):
        self.assertEquals(Capacity("20*GiB"), 20 * GiB)

    def test__from_string(self):
        check = self._assert_from_string_equals
        check("GiB", GiB)
        check("MiB", MiB)
        for variant in ("2*GiB", "2GiB", "2* GiB", "2 *GiB"):
            check(variant, 2 * GiB)

    def test__invalid_patterns(self):
        check = self._assert_value_error
        check("2")
        check("bla")
        check("GIB")
        check("1*GiB*bla")
        check("1+2")
        check("1*2")

    def _assert_from_string_equals(self, s, value):
        self.assertEquals(from_string(s), value)

    def _assert_value_error(self, s):
        with self.assertRaises(ValueError):
            from_string(s)
