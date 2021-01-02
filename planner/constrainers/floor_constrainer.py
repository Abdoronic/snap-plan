from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.room_type import RoomType
from planner.constrainers.apartment_constrainer import apartment_connected_to_corridors, constrain_apartment
from planner.constrainers.room_constrainer import constrain_room, has_daylight
from planner.constrainers.modules_constrainer import constraint_module, constraint_slim_modules
from planner.constrainers.utils import all_shapes_adjacent_in_order, and_reify, shape_adjacent_to_any

from planner.constrainers.symmetry_constrainer import constrain_symmetry_over_apartment_class


def constrain_floor(floor: Floor, model: cp_model.CpModel):
    constrain_no_overlap(floor, model)

    constrain_symmetry_over_apartment_class(floor, model)

    constrain_all_area_utilized(floor, model)

    constrain_sunrooms_daylight(floor, model)

    constrain_stairs(floor, model)
    constrain_elevator(floor, model)
    constrain_corridors(floor, model)

    for apartment in floor.apartments:
        constrain_apartment(apartment, floor, model)

    for room in floor.rooms:
        constrain_room(room, floor, model)


def constrain_no_overlap(floor: Floor, model: cp_model.CpModel):
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


def constrain_all_area_utilized(floor: Floor, model: cp_model.CpModel):
    areas = []
    areas.append(floor.stairs.area_variable)
    areas.append(floor.elevator.area_variable)

    for corridor in floor.corridors:
        areas.append(corridor.area_variable)

    for apartment in floor.apartments:
        for room in apartment.rooms:
            areas.append(room.area_variable)
        for duct in apartment.ducts:
            areas.append(duct.area_variable)
        for hallway in apartment.hallways:
            areas.append(hallway.area_variable)

    model.Add(sum(areas) == floor.width * floor.length)


def constrain_sunrooms_daylight(floor: Floor, model: cp_model.CpModel):
    for room in floor.rooms:
        if room.room_type == RoomType.SUN_ROOM:
            model.Add(has_daylight(room, floor, model) == 1)


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
    corridors = floor.corridors
    constraint_slim_modules(corridors, model)

    corridors_shapes = [*map(lambda corridor: corridor.variables, corridors)]
    corridors_adjacent = all_shapes_adjacent_in_order(corridors_shapes, model)

    stairs_connected = shape_adjacent_to_any(
        floor.stairs.variables,
        corridors_shapes,
        model
    )
    elevator_connected = shape_adjacent_to_any(
        floor.elevator.variables,
        corridors_shapes,
        model
    )

    hallways_connected = and_reify(
        [
            apartment_connected_to_corridors(apartment, corridors, model)
            for apartment in floor.apartments
        ],
        model
    )
    model.Add(
        and_reify(
            [
                corridors_adjacent,
                stairs_connected,
                elevator_connected,
                hallways_connected
            ],
            model
        ) == 1
    )
