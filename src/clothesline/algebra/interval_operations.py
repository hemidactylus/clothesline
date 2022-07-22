"""
interval algebra primitives.
"""

from functools import cmp_to_key

from clothesline.algebra.symbols import x_cmp
from clothesline.interval_peg import IntervalPeg
from clothesline.exceptions import InvalidCombineEndState


def combine_intervals(  # noqa: PLR0914, PLR0912
    int_maker,
    interval_iterables,
    combiner_function=lambda q: q[0],
):
    """
    The main workhorse for interval algebra.
    A list of N iterables over intervals is combined according to some
    prescriptions.

    `int_maker` is a function from (peg1, peg2) to an instance of the desired
    interval* class (e.g. the constructor "Interval" itself).

    `interval_iterables` is a list of iterables, each consisting of several
    intervals. Each of the iterables is an "operand" in some arbitrary
    (set-, i.e. boolean-) prescription to combine them.

    With a single iterable as input (N=1), i.e.
    `interval_iterables = [[int1, int2, ...]]`
    these are made into a normalized-form list of intervals.

    With two iterables as input (N=2),
    `interval_iterables = [[intA1, intA2, ...], [intB1, intB2, ...]]`

    one can achieve
    - setA U setB (default)
    - setA - setB
    - setA ^ setB
    depending on the passed combiner_function.

    `combiner_function` is a function from a tuple of N booleans
    to a single boolean: it specifies whether a point or an open interval
    will be in the result according to whether it was contained in each of the
    N inputs:
    - (q0, q1) => q0 or q1            # for union
    - (q0, q1) => q0 and (not q1)     # for set difference
    - (q0, q1) => q0 xor q1           # for '^'

    N > 2 will presumably never be used.
    """

    interval_lists = [
        list(interval_ite) for interval_ite in interval_iterables
    ]  # noqa: E501
    n_i_lists = len(interval_lists)

    # 1. 'split' phase
    markers = sorted(
        set(
            peg.value
            for i_list in interval_lists
            for interval in i_list
            for peg in interval.pegs()
        ),
        key=cmp_to_key(x_cmp),
    )
    m_index_map = {val: index for index, val in enumerate(markers)}

    point_included = {marker: {} for marker in markers}
    range_included = {marker: {} for marker in markers}
    # looping labeling to be tweaked for multi-source case
    for i_list_index, i_list in enumerate(interval_lists):
        for interval in i_list:
            # ends pointlike status
            for peg in interval.pegs():
                if peg.included:
                    point_included[peg.value][i_list_index] = True
            # internal pointlike values, if any
            begin_peg = interval.begin
            end_peg = interval.end
            begin_m_index = m_index_map[begin_peg.value]
            end_m_index = m_index_map[end_peg.value]
            for internal_m_index in range(begin_m_index + 1, end_m_index):
                internal_marker = markers[internal_m_index]
                point_included[internal_marker][i_list_index] = True
            # ranges (first + internal if any)
            for m_index in range(begin_m_index, end_m_index):
                marker = markers[m_index]
                range_included[marker][i_list_index] = True

    # 2. 'project' phase, using combiner_function
    point_merged = {marker: False for marker in markers}
    range_merged = {marker: False for marker in markers}
    for marker in markers:
        point_merged[marker] = combiner_function(
            [
                point_included[marker].get(i_list_index, False)
                for i_list_index in range(n_i_lists)
            ]
        )
    for marker in markers[:-1]:
        range_merged[marker] = combiner_function(
            [
                range_included[marker].get(i_list_index, False)
                for i_list_index in range(n_i_lists)
            ]
        )

    # # 3. 'merge' phase
    final_intervals = []
    i_buffer = []  # a mutable state
    for m_index, marker in enumerate(markers):
        next_is_range = range_merged[marker]
        point_included = point_merged[marker]
        if not i_buffer:
            if next_is_range:
                i_buffer = [(marker, point_included), None]
            else:
                if point_included:
                    # this point, isolated, is a zero-length interval:
                    final_intervals.append(
                        int_maker(
                            IntervalPeg(marker, True),
                            IntervalPeg(marker, True),
                        )
                    )
                else:
                    # no-op
                    pass
        else:
            # i_buffer exists already
            if next_is_range:
                if point_included:
                    # write/extend current buffer's endpoint
                    i_buffer[1] = (marker, point_included)
                else:
                    # a hole: finalize/flush buffer and re-init it at once
                    i_buffer[1] = (marker, point_included)
                    final_intervals.append(
                        int_maker(
                            IntervalPeg(i_buffer[0][0], i_buffer[0][1]),
                            IntervalPeg(i_buffer[1][0], i_buffer[1][1]),
                        )
                    )
                    i_buffer = [(marker, point_included), None]
            else:
                # end of the interval being built: flush and reset buffer
                i_buffer[1] = (marker, point_included)
                final_intervals.append(
                    int_maker(
                        IntervalPeg(i_buffer[0][0], i_buffer[0][1]),
                        IntervalPeg(i_buffer[1][0], i_buffer[1][1]),
                    )
                )
                i_buffer = []
    #
    if i_buffer:
        raise InvalidCombineEndState("Inconsistent end state in merge phase")

    return final_intervals
