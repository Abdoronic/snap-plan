from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.constrainers.utils import base_reify


def add_objective_function(floor: Floor, model: cp_model.CpModel):
    floor_area = floor.width * floor.length
    rooms_area = [room.area_variable for room in floor.rooms]

    floor_area_maximized = base_reify(
        sum(rooms_area) == floor_area,
        sum(rooms_area) != floor_area,
        model
    )

    model.Add(floor.score_variable == sum([floor_area_maximized]))

    model.Maximize(floor.score_variable)
