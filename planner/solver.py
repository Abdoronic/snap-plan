from ortools.sat.python import cp_model

from planner.constrainers.floor_constrainer import constrain_floor
from planner.constrainers.objective_function import add_objective_function
from planner.solution_handler import SolutionHandler

from planner.models.floor import Floor
from planner.models.apartment import Apartment
from planner.models.module import Module


def plan_floor(floor: Floor):
    model = cp_model.CpModel()

    create_variables(floor, model)

    constrain_floor(floor, model)
    add_objective_function(floor, model)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Set the objective to a fixed value
    model.Add(floor.score_variable == round(solver.ObjectiveValue()))
    model.Proto().ClearField('objective')

    solver.SearchForAllSolutions(model, SolutionHandler(floor))

    return status, solver


def create_variables(floor: Floor, model: cp_model.CpModel):
    floor.score_variable = model.NewIntVar(0, 4, 'floor_score')

    create_module_variables(floor, floor.stairs, model)
    create_module_variables(floor, floor.elevator, model)
    for corridor in floor.corridors:
        create_module_variables(floor, corridor, model)

    for apartment in floor.apartments:
        create_room_variables(floor, apartment, model)
        for hallway in apartment.hallways:
            create_module_variables(floor, hallway, model)
        for duct in apartment.ducts:
            create_module_variables(floor, duct, model)


def create_module_variables(floor: Floor, module: Module, model: cp_model.CpModel):
    module.variables = new_shape_var(floor.width, floor.length, model)
    module.width_variable = model.NewIntVar(0, floor.width, '')
    module.length_variable = model.NewIntVar(0, floor.length, '')
    module.area_variable = model.NewIntVar(0, floor.width * floor.length, '')


def create_room_variables(floor: Floor, apartment: Apartment, model: cp_model.CpModel):
    width = floor.width
    length = floor.length
    area = width * length
    for room in apartment.rooms:
        room.area_variable = model.NewIntVar(room.min_area, area, '')
        room.width_variable = model.NewIntVar(1, width, '')
        room.length_variable = model.NewIntVar(1, length, '')
        room.variables = new_shape_var(width, length, model)


def new_shape_var(max_width: int, max_length: int, model: cp_model.CpModel):
    return (
        model.NewIntVar(0, max_width, ''),
        model.NewIntVar(0, max_width, ''),
        model.NewIntVar(0, max_length, ''),
        model.NewIntVar(0, max_length, '')
    )
