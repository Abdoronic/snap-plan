from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.constrainers.room_constrainer import has_daylight
from planner.constrainers.utils import and_reify


def add_objective_function(floor: Floor, model: cp_model.CpModel):
    have_daylight = all_rooms_have_daylight(floor, model)

    model.Add(floor.score_variable == sum([have_daylight]))
    model.Maximize(floor.score_variable)

def all_rooms_have_daylight(floor: Floor, model: cp_model.CpModel):
    return and_reify(
        [
            has_daylight(room, floor, model)
            for room in floor.rooms
        ],
        model
    )
