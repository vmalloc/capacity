from unittest import TestCase
from numbers import Integral
from capacity import *

class CapacityTest(TestCase):
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
        #negative tests
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
        self._assert_str_of_equals(bit, '1 bit')
        self._assert_repr_of_equals(bit, '1 bit')
    def _assert_str_of_equals(self, obj, value):
        self.assertEquals(str(obj), value)
    def _assert_repr_of_equals(self, obj, value):
        self.assertEquals(repr(obj), value)

class CapacityArithmeticTest(TestCase):
    def test__add(self):
        self.assertEquals(MiB + MiB, Capacity(MiB.bits * 2))
        self.assertEquals(MiB + 0, MiB)
        self.assertEquals(0 + MiB, MiB)
    def test__iadd(self):
        a = MiB
        a += MiB
        self.assertEquals(a, 2 * MiB)
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
        self.assertEquals((2 * MiB) / 2, MiB)
        self.assertEquals((1.5 * MiB) / MiB, 1.5)
        self.assertEquals((2 * MiB) / MiB, 2)
        self.assertEquals(0/MiB, 0)
    def test__mod(self):
        self.assertEquals(((2 * MiB) + bit) % MiB, bit)
        self.assertEquals(0 % MiB, MiB)
    def test__floordiv(self):
        self.assertEquals(((2 * MiB)+bit) // MiB, 2)
        self.assertEquals(0 // MiB, 0)
    def test__roundup(self):
        self.assertEquals(MiB.roundup(MiB), MiB)
        self.assertEquals((MiB + bit).roundup(MiB), 2 * MiB)
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
