
from ortools.sat.python import cp_model

from planner.constrainers.utils import base_reify, and_reify, or_reify, eq_tuple_reify

from typing import List, Tuple

def all_shapes_adjacent_in_order(
    shapes: List[Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar]],
    model: cp_model.CpModel
):
    return and_reify(
        [
            shapes_are_adjacent(shapes[i], shapes[i + 1], model)
            for i in range(len(shapes) - 1)
        ],
        model
    )


def shape_adjacent_to_any(
    target_shape: Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar],
    shapes: List[Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar]],
    model: cp_model.CpModel
):
    return or_reify(
        [
            shapes_are_adjacent(target_shape, shape, model)
            for shape in shapes
        ],
        model
    )


def shapes_are_adjacent(
    a: Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar],
    b: Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar],
    model: cp_model.CpModel
) -> cp_model.IntVar:

    # a_nw, a_ne, a_sw, a_se
    a_corners = get_shape_corners(a)
    b_corners = get_shape_corners(b)

    # b_n, b_s, b_w, b_e
    b_sides = get_shape_sides(b)

    possible_adjacencies = []

    for i, corner in enumerate(a_corners):
        # j is 1 if corner is nw or ne and 0 if corner is sw or se
        j = 1 - i // 2
        possible_adjacencies.append(
            is_sandwiched(corner, b_sides[j], 0, model)
        )

        # k is 3 if corner is nw or sw and 2 if corner is ne or se
        k = 3 - i % 2
        possible_adjacencies.append(
            is_sandwiched(corner, b_sides[k], 1, model)
        )

    possible_adjacencies.extend(
        get_inclusive_adjacencies(a_corners, b_corners, model)
    )
    are_adjacent = or_reify(possible_adjacencies, model)
    return are_adjacent


def get_shape_corners(variables: Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar]) -> tuple:
    x_start, x_end, y_start, y_end = variables
    nw = (x_start, y_start)
    ne = (x_end, y_start)
    sw = (x_start, y_end)
    se = (x_end, y_end)
    return nw, ne, sw, se


def get_shape_sides(variables: Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar]) -> tuple:
    nw, ne, sw, se = get_shape_corners(variables)
    n = (nw, ne)
    s = (sw, se)
    w = (nw, sw)
    e = (ne, se)
    return n, s, w, e


def get_inclusive_adjacencies(a_corners: tuple, b_corners: tuple, model: cp_model.CpModel) -> list:
    a_nw, a_ne, a_sw, a_se = a_corners

    b_nw, b_ne, b_sw, b_se = b_corners

    # a_nw can coincide with b_ne or b_sw

    inclusive_adjacencies = []

    inclusive_adjacencies.extend(
        [
            eq_tuple_reify(a_nw, b_ne, model),
            eq_tuple_reify(a_nw, b_sw, model),
        ]
    )

    # a_ne can coincide with b_nw or b_se

    inclusive_adjacencies.extend(
        [
            eq_tuple_reify(a_ne, b_nw, model),
            eq_tuple_reify(a_ne, b_se, model),
        ]
    )

    # a_se can coincide with b_nw or b_se

    inclusive_adjacencies.extend(
        [
            eq_tuple_reify(a_se, b_ne, model),
            eq_tuple_reify(a_se, b_sw, model),
        ]
    )

    # a_sw can coincide with b_ne or b_sw

    inclusive_adjacencies.extend(
        [
            eq_tuple_reify(a_sw, b_nw, model),
            eq_tuple_reify(a_sw, b_se, model),
        ]
    )

    return inclusive_adjacencies


def is_between(start: cp_model.IntVar, in_between: cp_model.IntVar, end: cp_model.IntVar, model: cp_model.CpModel) -> cp_model.IntVar:
    """Exclusive
    """

    after_start = base_reify(
        in_between > start,
        in_between <= start,
        model
    )

    before_end = base_reify(
        in_between < end,
        in_between >= end,
        model
    )

    return and_reify([after_start, before_end], model)


def is_sandwiched(sandwiched: tuple, side: tuple, direction: int, model: cp_model.CpModel) -> cp_model.IntVar:
    """ Assumes end is on same horizontal or vertical line as start. 0 is horizontal, 1 is vertical for direction
    """

    start, end = side

    other_direction = 1 - direction
    are_aligned = base_reify(
        start[other_direction] == sandwiched[other_direction],
        start[other_direction] != sandwiched[other_direction],
        model
    )

    is_between_in_direction = is_between(
        start[direction],
        sandwiched[direction],
        end[direction],
        model
    )

    return and_reify(
        [are_aligned, is_between_in_direction],
        model
    )