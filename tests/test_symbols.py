import unittest

from clothesline.symbols import PLUS_INF, MINUS_INF
from clothesline.symbols import isSymbol
from clothesline.symbols import xEquals, xGt, xLt, xGe, xLe

class TestSymbols(unittest.TestCase):

    def test_symbols(self):
        plusInf = PLUS_INF
        self.assertIs(PLUS_INF, plusInf)
        self.assertIsNot(PLUS_INF, MINUS_INF)

        piInstance = PLUS_INF()
        self.assertIsNot(PLUS_INF, piInstance)

    def test_isSymbol(self):
        PLUS_INF
        plusInf = PLUS_INF
        piInstance = PLUS_INF()
        self.assertTrue(isSymbol(PLUS_INF))
        self.assertTrue(isSymbol(plusInf))
        self.assertFalse(isSymbol(piInstance))
        self.assertFalse(isSymbol(0.0))

    def test_comparisons(self):
        self.assertTrue(xEquals(0.0, 0.0))
        self.assertTrue(xEquals(MINUS_INF, MINUS_INF))
        self.assertFalse(xEquals(0.0, 1.0))
        self.assertFalse(xEquals(0.0, PLUS_INF))

        #
        self.assertTrue(xGt(1.0, 0.0))
        self.assertTrue(xGt(PLUS_INF, 0.0))
        self.assertTrue(xGt(0.0, MINUS_INF))
        self.assertTrue(xGt(PLUS_INF, MINUS_INF))

        self.assertFalse(xLt(1.0, 0.0))
        self.assertFalse(xLt(PLUS_INF, 0.0))
        self.assertFalse(xLt(0.0, MINUS_INF))
        self.assertFalse(xLt(PLUS_INF, MINUS_INF))

        self.assertFalse(xGt(0.0, 1.0))
        self.assertFalse(xGt(0.0, PLUS_INF))
        self.assertFalse(xGt(MINUS_INF, 0.0))
        self.assertFalse(xGt(MINUS_INF, PLUS_INF))

        self.assertTrue(xLt(0.0, 1.0))
        self.assertTrue(xLt(0.0, PLUS_INF))
        self.assertTrue(xLt(MINUS_INF, 0.0))
        self.assertTrue(xLt(MINUS_INF, PLUS_INF))

        self.assertFalse(xGt(MINUS_INF, MINUS_INF))
        self.assertFalse(xGt(0.0, 0.0))
        self.assertFalse(xLt(MINUS_INF, MINUS_INF))
        self.assertFalse(xLt(0.0, 0.0))

        #
        self.assertTrue(xGe(MINUS_INF, MINUS_INF))
        self.assertTrue(xLe(MINUS_INF, MINUS_INF))
        self.assertTrue(xGe(0.0, 0.0))
        self.assertTrue(xLe(0.0, 0.0))

        self.assertTrue(xGe(PLUS_INF, MINUS_INF))
        self.assertTrue(xGe(PLUS_INF, 0.0))
        self.assertTrue(xLe(MINUS_INF, PLUS_INF))
        self.assertTrue(xLe(0.0, PLUS_INF))

        self.assertFalse(xGe(MINUS_INF, PLUS_INF))
        self.assertFalse(xGe(0.0, PLUS_INF))
        self.assertFalse(xLe(PLUS_INF, MINUS_INF))
        self.assertFalse(xLe(PLUS_INF, 0.0))

if __name__ == '__main__':
    unittest.main()
