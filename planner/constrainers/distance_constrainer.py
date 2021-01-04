from ortools.sat.python import cp_model

from planner.models.floor import Floor

from typing import Tuple

def distance_between_shapes_doubled(
    a: Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar],
    b: Tuple[cp_model.IntVar, cp_model.IntVar, cp_model.IntVar, cp_model.IntVar],
    floor: Floor,
    model: cp_model.CpModel
) -> cp_model.IntVar:
    """ 
    Returns double the manhatten distance between the two center points of two rectangles.
    """
    dx = model.NewIntVar(-floor.width, floor.width, '')
    model.Add(dx == (a[0] + a[1]) - (b[0] + b[1]))
    abs_dx = model.NewIntVar(0, 2 * floor.width, '')
    model.AddAbsEquality(abs_dx, dx)

    dy = model.NewIntVar(-floor.length, floor.length, '')
    model.Add(dy == (a[2] + a[3]) - (b[2] + b[3]))
    abs_dy = model.NewIntVar(0, 2 * floor.length, '')
    model.AddAbsEquality(abs_dy, dy)

    distance = model.NewIntVar(0, 2 * (floor.width + floor.length), '')
    model.Add(distance == abs_dx + abs_dy)

    return distance
