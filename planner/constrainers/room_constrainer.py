import uuid


def constrain_room(room, floor, model):
    constraint_room_area(room, floor, model)


def constraint_room_area(room, floor, model):
    (xs, xe, ys, ye) = room.variables

    width_var = model.NewIntVar(0, floor.width, str(uuid.uuid4()))
    length_var = model.NewIntVar(0, floor.length, str(uuid.uuid4()))
    model.Add(xe - xs == width_var)
    model.Add(ye - ys == length_var)

    if room.has_preferred_width():
        model.Add(width_var == room.width)
    
    if room.has_preferred_length():
        model.Add(length_var == room.length)

    area = model.NewIntVar(0, floor.width * floor.length, str(uuid.uuid4()))
    model.AddMultiplicationEquality(area, [width_var, length_var])

    model.Add(area >= room.min_area)


def enforce_rooms_be_adjacent(a, b, model):

    #a_nw, a_ne, a_sw, a_se
    a_corners = get_room_corners(a)

    #b_n, b_s, b_w, b_e
    b_sides = get_room_sides(b)

    possible_adjacencies = []

    for i, corner in enumerate(a_corners):
        # j is 1 if corner is nw or ne and 0 if corner is sw or se
        j = 1 - i//2
        possible_adjacencies.append(
            is_sandwiched(corner, b_sides[j], 0, model))

        # k is 3 if corner is nw or sw and 2 if corner is ne or se
        k = 3 - i % 2
        possible_adjacencies.append(is_sandwiched(
            corner, b_sides[k], 1, model))

    are_adjacent = or_reify(possible_adjacencies, model)
    model.Add(are_adjacent == 1)


def get_room_corners(room):
    x_start, x_end, y_start, y_end = room.variables

    nw = (x_start, y_start)
    ne = (x_end, y_start)
    sw = (x_start, y_end)
    se = (x_end, y_end)

    return nw, ne, sw, se


def get_room_sides(room):
    nw, ne, sw, se = get_room_corners(room)
    n = (nw, ne)
    s = (sw, se)
    w = (nw, sw)
    e = (ne, se)

    return n, s, w, e


def is_between(start, in_between, end, model):
    """Inclusive, one-sided only
    """

    after_start = base_reify(in_between >= start,
                             in_between < start, model)

    before_end = base_reify(in_between <= end,
                            in_between > end, model)

    is_after_start_and_before_end = and_reify(after_start, before_end, model)

    is_not_start = base_reify(start != in_between,
                              start == in_between, model)

    is_not_end = base_reify(end != in_between,
                            end == in_between, model)

    is_not_start_or_end = or_reify(is_not_start, is_not_end, model)

    return and_reify(is_after_start_and_before_end, is_not_start_or_end, model)


def is_sandwiched(sandwiched, side, direction, model):
    """ Assumes end is on same horizontal or vertical line as start. 0 is horizontal, 1 is vertical for direction
    """

    start, end = side

    other_direction = 1 - direction
    are_aligned = base_reify(start[other_direction] == sandwiched[other_direction],
                             start[other_direction] != sandwiched[other_direction],
                             model)

    is_between_in_direction = is_between(
        start[direction], sandwiched[direction], end[direction], model)

    return and_reify(are_aligned, is_between_in_direction, model)


def base_reify(condition, not_condition, model):
    b = model.NewBoolVar(uuid.uuid4())

    # Implement b == condition.
    model.Add(condition).OnlyEnforceIf(b)
    model.Add(not_condition).OnlyEnforceIf(b.Not())

    return b


def not_reify(a_var, model):
    return base_reify(a_var == 0,
                      a_var != 0,
                      model)


def sum_vars(var_list):
    sum = 0
    for var in var_list:
        sum += var
    return sum


def and_reify(var_list, model):
    sum = sum_vars(var_list)
    len = len(var_list)
    return base_reify(sum == len,
                      sum != len,
                      model)


def or_reify(var_list, model):
    sum = sum_vars(var_list)
    return base_reify(sum >= 1,
                      sum < 1,
                      model)


def xor_reify(var_list, model):
    sum = sum_vars(var_list)
    return base_reify(sum == 1,
                      sum != 1,
                      model)


def add_if_then_else(unique_name, if_condition, else_condition, then_constraint, else_constraint, model):
    """Constrains that for model when the if_condition holds, then_constraint is enforced and that otherwise when else_condition holds, else_constraint is enforced. This creates a BoolVar to enforce the constraints, which is returned. Based on official code at https://github.com/google/or-tools/blob/master/ortools/sat/doc/channeling.md#if-then-else-expressions

    Parameters
    ----------
        unique_name: str
            Name to uniquely identify a generated BoolVar.
        if_condition: BoundedLinearExpression
            When satisfied, the then_constraint is enforced.
        else_condition: BoundedLinearExpression
            When satisfied, the else_constraint is enforced. This must be the logical negation of if_condition.
        then_constraint: BoundedLinearExpression
            Enforced when if_condition holds.
        else_constraint: BoundedLinearExpression
            Enforced when else_condition holds.
        model: CpModel
            Model to add the constraints to.

    Returns
    -------
        BoolVar
            BoolVar created to enforce the complex constraint.
    """

    # Declare intermediate boolean variable.
    b = model.NewBoolVar(unique_name)

    # Implement b == if_condition.
    model.Add(if_condition).OnlyEnforceIf(b)
    model.Add(else_condition).OnlyEnforceIf(b.Not())

    # Create two half-reified constraints.
    # First, b implies then_constraint.
    model.Add(then_constraint).OnlyEnforceIf(b)
    # Second, not(b) implies else_constraint.
    model.Add(else_constraint).OnlyEnforceIf(b.Not())

    return b
