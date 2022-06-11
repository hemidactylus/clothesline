"""
Tests for serialization of intervals*/sets*
"""

import json
import unittest

from clothesline import RealIntervalSet
from clothesline.enriched.datetime_interval_set import DatetimeIntervalSet
from clothesline.enriched.string_interval_set import StringIntervalSet

from clothesline.exceptions import UnserializableItemError


class TestIntervalSetSerialization(unittest.TestCase):
    """
    Tests for serializing an RealIntervalSet
    """

    def test_serializability(self):
        """Back-and-forth ser/des check with real intervalset."""
        builder = RealIntervalSet.builder()
        is1 = builder[10](11) + builder[12](...)
        is_dict = is1.to_dict()
        restored_is1 = RealIntervalSet.utils().from_dict(
            json.loads(json.dumps(is_dict)),
        )
        self.assertEqual(is1, restored_is1)


class TestDatetimeIntervalSetSerialization(unittest.TestCase):
    """
    Tests for serializing a DatetimeIntervalSet
    """

    def test_serializability(self):
        """Back-and-forth ser/des check with datetime intervalset."""
        from datetime import datetime  # noqa: PLC0415

        dat0 = datetime(2010, 1, 1)
        dat1 = datetime(2011, 1, 1)
        dat2 = datetime(2012, 1, 1)
        #
        builder = DatetimeIntervalSet.builder()
        is1 = builder[dat0](dat1) + builder[dat2](...)
        is_dict = is1.to_dict()
        restored_is1 = DatetimeIntervalSet.utils().from_dict(
            json.loads(json.dumps(is_dict)),
        )
        self.assertEqual(is1, restored_is1)


class TestStringIntervalSetSerialization(unittest.TestCase):
    """
    Tests for serializing a StringIntervalSet (which has
    no encoders defined).
    """

    def test_serializability(self):
        """Serializability error-raise check for 'string intervalsets'."""
        builder = StringIntervalSet.builder()
        is1 = builder["a"]("bm") + builder["m"](...)
        with self.assertRaises(UnserializableItemError):
            is1.to_dict()
        with self.assertRaises(UnserializableItemError):
            StringIntervalSet.utils().from_dict({})


if __name__ == "__main__":
    unittest.main()
