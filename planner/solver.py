from ortools.sat.python import cp_model
from planner.constrainers.floor_constrainer import constrain_floor


def plan_floor(floor):
    model = cp_model.CpModel()

    create_variables(floor, model)

    constrain_floor(floor, model)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    return status, solver


def create_variables(floor, model):
    for number, room in enumerate(floor.rooms, 1):
        room_name = f'Room#{number}'
        room.variables = (
            model.NewIntVar(0, floor.width, room_name + '_xs'),
            model.NewIntVar(0, floor.width, room_name + '_xe'),
            model.NewIntVar(0, floor.length, room_name + '_ys'),
            model.NewIntVar(0, floor.length, room_name + '_ye')
        )
