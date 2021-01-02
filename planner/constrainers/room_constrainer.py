from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.room import Room
from planner.models.view import View
from planner.constrainers.adjacency_constrainer import shapes_are_adjacent
from planner.constrainers.utils import fail_reify, or_reify

from typing import List

def constrain_room(room: Room, floor: Floor, model: cp_model.CpModel):
    constraint_room_area(room, floor, model)


def constraint_room_area(room: Room, floor: Floor, model: cp_model.CpModel):
    (xs, xe, ys, ye) = room.variables

    width = room.width_variable
    length = room.length_variable

    model.Add(xs < xe)
    model.Add(ys < ye)
    model.Add(xe - xs == width)
    model.Add(ye - ys == length)

    if room.has_preferred_width():
        model.Add(width == room.preferred_width)

    if room.has_preferred_length():
        model.Add(length == room.preferred_length)

    area = room.area_variable

    model.AddMultiplicationEquality(area, [width, length])

    model.Add(area >= room.min_area)


def has_daylight(room: Room, floor: Floor, model: cp_model.CpModel):
    return has_view_of_types(room, [v for v in View if v != View.NO_VIEW], floor, model)


def has_landscape_view(room: Room, floor: Floor, model: cp_model.CpModel):
    return has_view_of_types(room, [View.LANDSCAPE], floor, model)


def has_view_of_types(room: Room, room_view_types: List[View], floor: Floor, model: cp_model.CpModel):

    sides_views = floor.sides_views

    zero = model.NewConstant(0)
    width = model.NewConstant(floor.width)
    length = model.NewConstant(floor.length)

    sides_coordinates = [
        (zero, width, length, length),
        (zero, width, zero, zero),
        (width, width, zero, length),
        (zero, zero, zero, length),
    ]

    possible_sides = []
    for i, view in enumerate(sides_views):
        if view in room_view_types:
            side_as_room = Room(None, 0)
            side_as_room.variables = sides_coordinates[i]
            possible_sides.append(side_as_room)

    if len(possible_sides) == 0:
        fail = fail_reify(model)
        model.Add(fail == 1)
        return

    possible_side_adjacencies = list(
        map(
            lambda side: shapes_are_adjacent(
                room.variables, side.variables, model),
            possible_sides
        )
    )

    return or_reify(possible_side_adjacencies, model)
