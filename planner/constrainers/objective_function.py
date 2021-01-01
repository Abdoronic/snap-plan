from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.constrainers.utils import base_reify


def add_objective_function(floor: Floor, model: cp_model.CpModel):
    model.Add(floor.score_variable == 1)

    model.Maximize(floor.score_variable)
