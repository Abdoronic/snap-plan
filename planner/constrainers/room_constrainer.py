from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.room import Room


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

