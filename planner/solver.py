from ortools.sat.python import cp_model
from constrainers.floor_constrainer import constrain_floor


def plan_floor(floor):

    model = cp_model.CpModel()

    create_variables(floor, model)

    constrain_floor(floor, model)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    return status, solver


def create_variables(floor, model):
    for room, number in enumerate(floor.rooms, 1):
        room_name = f'Room#{number}'
        room.variables = (
            model.NewIntVar(0, floor.width, room_name + 'xs'),
            model.NewIntVar(0, floor.width, room_name + 'xe'),
            model.NewIntVar(0, floor.height, room_name + 'ys'),
            model.NewIntVar(0, floor.height, room_name + 'ye')
        )
