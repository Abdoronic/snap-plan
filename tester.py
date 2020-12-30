from planner.io.parser import parse_floor
from planner.io.visualizer import visualize_floor
from planner.solver import plan_floor

floor = parse_floor("inputs/floor_input_2.json")

status, solver = plan_floor(floor)

visualize_floor(floor, solver)

precalculated_solutions = [
    (4, 6, 0, 10),
    (3, 4, 0, 10),
    (0, 3, 0, 5),
    (0, 3, 5, 12),
    (3, 9, 10, 12),
    (6, 9, 0, 10),
    (9, 12, 0, 12),
]

i = 0
for apartment_no, apartment in enumerate(floor.apartments, 1):
    for room_no, room in enumerate(apartment.rooms, 1):
        room_type = room.room_type
        xs = solver.Value(room.variables[0])
        xe = solver.Value(room.variables[1])
        ys = solver.Value(room.variables[2])
        ye = solver.Value(room.variables[3])
        assert ((xs, xe, ys, ye) == precalculated_solutions[i])
        i = i + 1
