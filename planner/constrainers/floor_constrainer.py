from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.room import Room
from planner.models.view import View
from planner.constrainers.apartment_constrainer import constrain_apartment
from planner.constrainers.room_constrainer import constrain_room, rooms_are_adjacent
from planner.constrainers.modules_constrainer import constraint_corridors, constraint_elevator, constraint_stairs

from planner.constrainers.utils import or_reify
from typing import List


def constrain_floor(floor: Floor, model: cp_model.CpModel):
    no_overlap(floor, model)

    constraint_stairs(floor, model)
    constraint_elevator(floor, model)
    constraint_corridors(floor, model)

    for apartment in floor.apartments:
        constrain_apartment(apartment, floor, model)

    for room in floor.rooms:
        constrain_room(room, floor, model)


def no_overlap(floor: Floor, model: cp_model.CpModel):
    x_intervals = []
    y_intervals = []

    for room in floor.rooms:
        (xs, xe, ys, ye) = room.variables
        xd = room.width_variable
        yd = room.length_variable

        x_intervals.append(model.NewIntervalVar(xs, xd, xe, ''))
        y_intervals.append(model.NewIntervalVar(ys, yd, ye, ''))

    model.AddNoOverlap2D(x_intervals, y_intervals)


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

    if possible_sides.count == 0:
        has_to_fail = model.NewBoolVar('')
        model.Add(has_to_fail == 0)
        model.Add(has_to_fail == 1)
        return

    possible_side_adjacencies = list(
        map(
            lambda side: rooms_are_adjacent(room, side, model),
            possible_sides
        )
    )

    return or_reify(possible_side_adjacencies, model)
