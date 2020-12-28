from ortools.sat.python import cp_model
from planner.constrainers.floor_constrainer import constrain_floor
from planner.constrainers.objective_function import add_objective_function


def plan_floor(floor):
    model = cp_model.CpModel()

    create_variables(floor, model)

    constrain_floor(floor, model)
    add_objective_function(floor, model)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Set the objective to a fixed value
    model.Add(floor.score_variable == round(solver.ObjectiveValue()))
    model.Proto().ClearField('objective')

    solver.SearchForAllSolutions(
        model,
        cp_model.VarArraySolutionPrinter([floor.score_variable])
    )

    return status, solver


def create_variables(floor, model):
    floor.score_variable = model.NewIntVar(0, 1, 'floor_score')
    for number, room in enumerate(floor.rooms, 1):
        room_name = f'Room#{number}'
        room.area_variable = model.NewIntVar(
            0,
            floor.width * floor.length,
            room_name + 'area'
        )
        room.variables = (
            model.NewIntVar(0, floor.width, room_name + '_xs'),
            model.NewIntVar(0, floor.width, room_name + '_xe'),
            model.NewIntVar(0, floor.length, room_name + '_ys'),
            model.NewIntVar(0, floor.length, room_name + '_ye')
        )
