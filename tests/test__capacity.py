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
        self.assertGreaterEqual(great, small)
        self.assertLess(small, great)
        self.assertLessEqual(small, great)
        #negative tests
        self.assertFalse(small > great)
        self.assertFalse(small >= great)
        self.assertFalse(great < small)
        self.assertFalse(great <= small)
        self.assertFalse(small != small)
        self.assertFalse(great != great)
        self.assertFalse(great == small)
        self.assertFalse(small == great)


class RepresentationTest(TestCase):
    def test__simple_textual_representation(self):
        self._assert_str_of_equals(bit, '1 bit')
        self._assert_repr_of_equals(bit, '1 bit')
    def _assert_str_of_equals(self, obj, value):
        self.assertEquals(str(obj), value)
    def _assert_repr_of_equals(self, obj, value):
        self.assertEquals(repr(obj), value)

class CapacityArithmeticTest(TestCase):
    def test__mul(self):
        self.assertEquals(2 * MiB, Capacity(MiB.bits * 2))
    def test__div(self):
        self.assertEquals((2 * MiB) / 2, MiB)
    def test__mod(self):
        self.assertEquals(((2 * MiB) + bit) % MiB, bit)

class InvalidArithmeticTest(TestCase):
    def test__invalid_arithmetic(self):
        size = 668 * bit

        with self.assertRaises(TypeError):
            size * size
        with self.assertRaises(TypeError):
            size + 3
        with self.assertRaises(TypeError):
            3 / size
