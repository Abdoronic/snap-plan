from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.room import Room
from planner.models.room_type import RoomType
from planner.constrainers.apartment_constrainer import constrain_apartment
from planner.constrainers.room_constrainer import constrain_room, rooms_are_adjacent


def constrain_floor(floor: Floor, model: cp_model.CpModel):
    no_overlap(floor, model)

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
