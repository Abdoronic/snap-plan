from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.room import Room
from planner.models.view import View
from planner.constrainers.apartment_constrainer import constrain_apartment
from planner.constrainers.room_constrainer import constrain_room
from planner.constrainers.modules_constrainer import constraint_module, constraint_slim_modules
from planner.constrainers.utils import shapes_are_adjacent

from planner.constrainers.utils import or_reify
from typing import List


def constrain_floor(floor: Floor, model: cp_model.CpModel):
    no_overlap(floor, model)

    constrain_stairs(floor, model)
    constrain_elevator(floor, model)
    constrain_corridors(floor, model)

    for apartment in floor.apartments:
        constrain_apartment(apartment, floor, model)

    for room in floor.rooms:
        constrain_room(room, floor, model)


def no_overlap(floor: Floor, model: cp_model.CpModel):
    x_intervals = []
    y_intervals = []

    def add_intervals(module):
        (xs, xe, ys, ye) = module.variables
        xd = module.width_variable
        yd = module.length_variable

        x_intervals.append(model.NewIntervalVar(xs, xd, xe, ''))
        y_intervals.append(model.NewIntervalVar(ys, yd, ye, ''))

    add_intervals(floor.stairs)
    add_intervals(floor.elevator)

    for corridor in floor.corridors:
        add_intervals(corridor)

    for apartment in floor.apartments:
        for room in apartment.rooms:
            add_intervals(room)
        for duct in apartment.ducts:
            add_intervals(duct)
        for hallway in apartment.hallways:
            add_intervals(hallway)


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
            lambda side: shapes_are_adjacent(room.variables, side.variables, model),
            possible_sides
        )
    )

    return or_reify(possible_side_adjacencies, model)

def constrain_stairs(floor: Floor, model: cp_model.CpModel):
    stairs = floor.stairs
    constraint_module(stairs, model)

    model.Add(stairs.width_variable == floor.stairs_dimensions[0])
    model.Add(stairs.length_variable == floor.stairs_dimensions[1])


def constrain_elevator(floor: Floor, model: cp_model.CpModel):
    elevator = floor.elevator
    constraint_module(elevator, model)

    model.Add(elevator.width_variable == floor.elevator_dimensions[0])
    model.Add(elevator.length_variable == floor.elevator_dimensions[1])


def constrain_corridors(floor: Floor, model: cp_model.CpModel):
    constraint_slim_modules(floor.corridors, model)

