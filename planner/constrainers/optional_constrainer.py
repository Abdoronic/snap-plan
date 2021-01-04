from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.constrainers.room_constrainer import has_landscape_view
from planner.constrainers.symmetry_constrainer import constrain_symmetry_over_apartment_class
from planner.constrainers.utils import and_reify, or_reify


def constrain_optional_constraints(floor: Floor, model: cp_model.CpModel):
    constrain_symmetry_over_apartment_class(floor, model)
    constrain_apartments_have_landscape(floor, model)


def constrain_apartments_have_landscape(floor: Floor, model: cp_model.CpModel):
    apartments_have_landscape = and_reify(
        [
            or_reify(
                [
                    has_landscape_view(room, floor, model)
                    for room in apartment.rooms
                ],
                model
            )
            for apartment in floor.apartments
        ],
        model
    )
    model.Add(apartments_have_landscape == 1)
