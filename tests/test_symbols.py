"""
Tests for the symbols module
"""

from functools import cmp_to_key
import unittest

from clothesline.algebra.symbols import PlusInf, MinusInf
from clothesline.algebra.symbols import is_symbol
from clothesline.algebra.symbols import x_equals, x_gt, x_lt, x_ge, x_le, x_cmp, x_sum, x_subtract

#
from clothesline.exceptions import IndeterminateFormError


class TestSymbols(unittest.TestCase):
    """
    Tests for +/- infinities and their extension's behaviour
    """

    def test_symbols(self):
        """equalities and the like"""
        plusInf = PlusInf
        self.assertIs(PlusInf, plusInf)
        self.assertIsNot(PlusInf, MinusInf)

        pi_instance = PlusInf()
        self.assertIsNot(PlusInf, pi_instance)

    def test_is_symbol(self):
        """the is_symbol function"""
        plusInf = PlusInf
        pi_instance = PlusInf()
        self.assertTrue(is_symbol(PlusInf))
        self.assertTrue(is_symbol(plusInf))
        self.assertFalse(is_symbol(pi_instance))
        self.assertFalse(is_symbol(0.0))

    def test_comparisons(self):
        """equalities and inequalities"""
        self.assertTrue(x_equals(0.0, 0.0))
        self.assertTrue(x_equals(MinusInf, MinusInf))
        self.assertFalse(x_equals(0.0, 1.0))
        self.assertFalse(x_equals(0.0, PlusInf))

        #
        self.assertTrue(x_gt(1.0, 0.0))
        self.assertTrue(x_gt(PlusInf, 0.0))
        self.assertTrue(x_gt(0.0, MinusInf))
        self.assertTrue(x_gt(PlusInf, MinusInf))

        self.assertFalse(x_lt(1.0, 0.0))
        self.assertFalse(x_lt(PlusInf, 0.0))
        self.assertFalse(x_lt(0.0, MinusInf))
        self.assertFalse(x_lt(PlusInf, MinusInf))

        self.assertFalse(x_gt(0.0, 1.0))
        self.assertFalse(x_gt(0.0, PlusInf))
        self.assertFalse(x_gt(MinusInf, 0.0))
        self.assertFalse(x_gt(MinusInf, PlusInf))

        self.assertTrue(x_lt(0.0, 1.0))
        self.assertTrue(x_lt(0.0, PlusInf))
        self.assertTrue(x_lt(MinusInf, 0.0))
        self.assertTrue(x_lt(MinusInf, PlusInf))

        self.assertFalse(x_gt(MinusInf, MinusInf))
        self.assertFalse(x_gt(0.0, 0.0))
        self.assertFalse(x_lt(MinusInf, MinusInf))
        self.assertFalse(x_lt(0.0, 0.0))

        #
        self.assertTrue(x_ge(MinusInf, MinusInf))
        self.assertTrue(x_le(MinusInf, MinusInf))
        self.assertTrue(x_ge(0.0, 0.0))
        self.assertTrue(x_le(0.0, 0.0))

        self.assertTrue(x_ge(PlusInf, MinusInf))
        self.assertTrue(x_ge(PlusInf, 0.0))
        self.assertTrue(x_le(MinusInf, PlusInf))
        self.assertTrue(x_le(0.0, PlusInf))

        self.assertFalse(x_ge(MinusInf, PlusInf))
        self.assertFalse(x_ge(0.0, PlusInf))
        self.assertFalse(x_le(PlusInf, MinusInf))
        self.assertFalse(x_le(PlusInf, 0.0))

    def test_sorting(self):
        s_key = cmp_to_key(x_cmp)
        self.assertEqual(
            sorted(
                [1.0, PlusInf, 0.0, MinusInf, -1.0],
                key=s_key,
            ),
            [MinusInf, -1.0, 0.0, 1.0, PlusInf],
        )

    def test_hashable(self):
        """Hashability and equality tests"""
        self.assertTrue(PlusInf == PlusInf)
        self.assertFalse(PlusInf == MinusInf)
        self.assertFalse(PlusInf == 0.0)
        #
        self.assertTrue(
            len(
                {
                    PlusInf,
                    MinusInf,
                    PlusInf,
                    2.0,
                    1.0 + 1.0,
                }
            )
            == 3
        )

    def test_arithmetic(self):
        """Arithmetic operations with symbols."""
        def _adder(v1, v2): return v1 + v2
        def xx_sum(v1, v2): return x_sum(v1, v2, _adder)
        def _subtracter(v1, v2): return v1 - v2
        def xx_subtract(v1, v2): return x_subtract(v1, v2, _subtracter)
        # sums
        self.assertEqual(xx_sum( PlusInf,  PlusInf),  PlusInf)
        with self.assertRaises(IndeterminateFormError):
            xx_sum( PlusInf, MinusInf)
        self.assertEqual(xx_sum( PlusInf,        1),  PlusInf)
        with self.assertRaises(IndeterminateFormError):
            xx_sum(MinusInf,  PlusInf)
        self.assertEqual(xx_sum(MinusInf, MinusInf), MinusInf)
        self.assertEqual(xx_sum(MinusInf,        1), MinusInf)
        self.assertEqual(xx_sum(       1,  PlusInf),  PlusInf)
        self.assertEqual(xx_sum(       1, MinusInf), MinusInf)
        self.assertEqual(xx_sum(       1,        1),        2)
        # differences
        self.assertEqual(xx_subtract( PlusInf, MinusInf),  PlusInf)
        with self.assertRaises(IndeterminateFormError):
            xx_subtract( PlusInf, PlusInf)
        self.assertEqual(xx_subtract( PlusInf,        1),  PlusInf)
        with self.assertRaises(IndeterminateFormError):
            xx_subtract(MinusInf,  MinusInf)
        self.assertEqual(xx_subtract(MinusInf,  PlusInf), MinusInf)
        self.assertEqual(xx_subtract(MinusInf,        1), MinusInf)
        self.assertEqual(xx_subtract(       1, MinusInf),  PlusInf)
        self.assertEqual(xx_subtract(       1,  PlusInf), MinusInf)
        self.assertEqual(xx_subtract(       1,        1),        0)

if __name__ == "__main__":
    unittest.main()
