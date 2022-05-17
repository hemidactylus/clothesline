"""
An arbitrary set defined by a finite number of intervals.
"""

from functools import cmp_to_key

from clothesline import Interval, IntervalPeg
# from clothesline.symbols import PlusInf, MinusInf
from clothesline.symbols import x_lt

# #
# from clothesline.exceptions import InvalidValueError


class IntervalSet:
    """
    A portion of the continuous line (e.g. the reals + infinities)
    defined by an arbitrary (finite) number of Interval objects.
    """

    intervals = None

    def __init__(self, intervals):
        """`intervals` is a list of Interval instances."""
        self.intervals = self._normalize(intervals)

    def contains(self, value):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __hash__(self, other):
        raise NotImplementedError

    def __repr__(self):
        return ' U '.join(interval.__repr__() for interval in self.intervals)

    @staticmethod
    def _normalize(intervals):
        """
        DOCSTRING TO WRITE
        """

        # 1. 'split' phase
        markers = sorted(
            set(peg.value for intervalList in [intervals] for interval in intervalList for peg in interval.pegs()),
            key=cmp_to_key(x_lt),
        )
        markersIndexMap = {val: index for index, val in enumerate(markers)}

        pointIncluded = {marker: {} for marker in markers}
        rangeIncluded = {marker: {} for marker in markers}
        # looping labeling to be tweaked for multi-source case
        for intervalListIndex, intervalList in enumerate([intervals]):
            for interval in intervalList:
                # ends pointlike status
                for peg in interval.pegs():
                    if peg.included:
                        pointIncluded[peg.value][intervalListIndex] = True
                # internal pointlike values, if any
                beginPeg = interval.begin
                endPeg = interval.end
                beginMarkerIndex = markersIndexMap[beginPeg.value]
                endMarkerIndex = markersIndexMap[endPeg.value]
                for internalMarkerIndex in range(beginMarkerIndex + 1, endMarkerIndex):
                    internalMarker = markers[internalMarkerIndex]
                    pointIncluded[internalMarker][intervalListIndex] = True
                # ranges (first + internal if any)
                for markerIndex in range(beginMarkerIndex, endMarkerIndex):
                    marker = markers[markerIndex]
                    rangeIncluded[marker][intervalListIndex] = True

        # 2. 'project' phase
        pointMerged = {marker: False for marker in markers}
        rangeMerged = {marker: False for marker in markers}
        for marker in markers:
            # this is specific to the one-/two-input op type. Here it's trivial
            pointMerged[marker] = pointIncluded[marker].get(0, False)
        for marker in markers[:-1]:
            # this is specific to the one-/two-input op type. Here it's trivial
            rangeMerged[marker] = rangeIncluded[marker].get(0, False)

        # # 3. 'merge' phase
        finalIntervals = []
        intBuffer = None  # a mutable state
        for markerIndex, marker in enumerate(markers):
            nextIsRange = rangeMerged[marker]
            pointIncluded = pointMerged[marker]
            if intBuffer is None:
                if nextIsRange:
                    intBuffer = [(marker, pointIncluded), None]
                else:
                    if pointIncluded:
                        # this point, isolated, is a zero-length interval:
                        finalIntervals.append(Interval(
                            IntervalPeg(marker, True),
                            IntervalPeg(marker, True),
                        ))
                    else:
                        # no-op
                        pass                        
            else:
                # intBuffer exists already
                if nextIsRange:
                    if pointIncluded:
                        # write/extend current buffer's endpoint
                        intBuffer[1] = (marker, pointIncluded)
                    else:
                        # a hole: finalize/flush buffer and re-init it at once
                        intBuffer[1] = (marker, pointIncluded)
                        finalIntervals.append(Interval(
                            IntervalPeg(intBuffer[0][0], intBuffer[0][1]),
                            IntervalPeg(intBuffer[1][0], intBuffer[1][1]),
                        ))
                        intBuffer = [(marker, pointIncluded), None]
                else:
                    # end of the interval being built: flush and reset buffer
                    intBuffer[1] = (marker, pointIncluded)
                    finalIntervals.append(Interval(
                        IntervalPeg(intBuffer[0][0], intBuffer[0][1]),
                        IntervalPeg(intBuffer[1][0], intBuffer[1][1]),
                    ))
                    intBuffer = None
        #
        if intBuffer is not None:
            raise ValueError('Inconsistent end state in merge phase')

        return finalIntervals
