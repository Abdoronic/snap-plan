from planner.models.room import Room
from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.apartment import Apartment


def get_floor_plan(floor: Floor, solver: cp_model.CpSolver):
    plan = {}
    plan['width'] = floor.width
    plan['length'] = floor.length

    plan['stairs'] = get_module_plan(floor.elevator, solver)
    plan['elevator'] = get_module_plan(floor.elevator, solver)

    plan['apartments'] = []
    for apartment in floor.apartments:
        plan['apartments'].append(
            get_apartment_plan(apartment, solver)
        )

    plan['corridors'] = []
    for corridor in floor.corridors:
        plan['corridors'].append(
            get_module_plan(corridor, solver)
        )


def get_apartment_plan(apartment: Apartment, solver: cp_model.CpSolver):
    plan = {}
    plan['rooms'] = []
    for room in apartment.rooms:
        plan['rooms'].append(
            get_room_plan(room, solver)
        )
    plan['hallways'] = []
    for hallway in apartment.hallways:
        plan['hallways'].append(
            get_module_plan(hallway, solver)
        )
    plan['ducts'] = []
    for duct in apartment.ducts:
        plan['ducts'].append(
            get_module_plan(duct, solver)
        )
    return plan


def get_room_plan(room: Room, solver: cp_model.CpSolver):
    plan = get_module_plan(room, solver)
    plan['roomType'] = room.room_type
    return plan


def get_module_plan(module, solver: cp_model.CpSolver):
    variables = module.variables
    xs = solver.Value(variables[0])
    xe = solver.Value(variables[1])
    ys = solver.Value(variables[2])
    ye = solver.Value(variables[3])
    return {
        'xs': xs,
        'xe': xe,
        'ys': ys,
        'ye': ye,
        'width': solver.Value(module.width_variable),
        'length': solver.Value(module.length_variable),
        'area': solver.Value(module.area_variable)
    }
