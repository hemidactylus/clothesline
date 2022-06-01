"""
Tests for serialization of intervals*/sets*
"""

import json
import unittest

from clothesline import IntervalSet
from clothesline.enriched.datetime_interval_set import DatetimeIntervalSet
from clothesline.enriched.string_interval_set import StringIntervalSet

from clothesline.exceptions import UnserializableItemError


class TestIntervalSetSerialization(unittest.TestCase):
    """
    Tests for serializing an IntervalSet
    """

    def test_serializability(self):
        builder = IntervalSet.builder()
        is1 = builder[10](11) + builder[12](...)
        json.dumps((is1).to_dict(),indent=4)


class TestDatetimeIntervalSetSerialization(unittest.TestCase):
    """
    Tests for serializing a DatetimeIntervalSet
    """

    def test_serializability(self):
        from datetime import datetime
        d0 = datetime(2010, 1, 1)
        d1 = datetime(2011, 1, 1)
        d2 = datetime(2012, 1, 1)
        #
        builder = DatetimeIntervalSet.builder()
        is1 = builder[d0](d1) + builder[d2](...)
        json.dumps((is1).to_dict(),indent=4)


class TestStringIntervalSetSerialization(unittest.TestCase):
    """
    Tests for serializing a StringIntervalSet (which has
    no encoders defined).
    """

    def test_serializability(self):
        builder = StringIntervalSet.builder()
        is1 = builder["a"]("bm") + builder["m"](...)
        with self.assertRaises(UnserializableItemError):
            json.dumps((is1).to_dict(),indent=4)
