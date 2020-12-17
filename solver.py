from ortools.sat.python import cp_model
from constrainers.floor_constrainer import constrain_floor

def plan_floor(floor):
    
    model = cp_model.CpModel()
    constrain_floor(floor, model)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    return status, solver
