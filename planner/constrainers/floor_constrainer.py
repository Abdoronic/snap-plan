from planner.constrainers.room_constrainer import constrain_room
from planner.constrainers.apartment_constrainer import constrain_apartment


def constrain_floor(floor, model):
    no_overlap(floor, model)

    for apartment in floor.apartments:
        constrain_apartment(apartment, floor, model)

    for room in floor.rooms:
        constrain_room(room, floor, model)


def no_overlap(floor, model):
    x_intervals = []
    y_intervals = []

    for number, room in enumerate(floor.rooms, 1):
        room_name = f'Room#{number}'
        (xs, xe, ys, ye) = room.variables

        xd = model.NewIntVar(0, floor.width, room_name + '_xd')
        model.Add(xs < xe)
        model.Add(xe - xs == xd)
        x_intervals.append(
            model.NewIntervalVar(xs, xd, xe, room_name + '_x_interval')
        )

        yd = model.NewIntVar(0, floor.length, room_name + '_yd')
        model.Add(ys < ye)
        model.Add(ye - ys == yd)
        y_intervals.append(
            model.NewIntervalVar(ys, yd, ye, room_name + '_y_interval')
        )

    model.AddNoOverlap2D(x_intervals, y_intervals)
