def visualize_floor(floor, solver):
    print(solver.StatusName())

    for number, room in enumerate(floor.rooms, 1):
        (xs, xe, ys, ye) = room.variables
        bounds = (solver.Value(xs), solver.Value(xe), solver.Value(ys), solver.Value(ye))
        print(
            f'Room #{number}:',
            f'nw{bounds[0], bounds[3]}, ne{bounds[1], bounds[3]}',
            f'sw{bounds[0], bounds[2]}, se{bounds[1], bounds[2]}'
        )
