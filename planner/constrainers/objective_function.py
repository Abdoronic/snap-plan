from planner.constrainers.distance_constrainer import distance_between_shapes_doubled
from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.constrainers.room_constrainer import has_daylight
from planner.constrainers.utils import and_reify, base_reify


def add_objective_function(floor: Floor, model: cp_model.CpModel):
    have_daylight = all_rooms_have_daylight(floor, model)
    have_good_spacings = all_rooms_have_good_spacings(floor, model)

    model.Add(floor.score_variable == sum([
        have_daylight,
        have_good_spacings
    ]))
    model.Maximize(floor.score_variable)


def all_rooms_have_daylight(floor: Floor, model: cp_model.CpModel):
    return and_reify(
        [
            has_daylight(room, floor, model)
            for room in floor.rooms
        ],
        model
    )


def all_rooms_have_good_spacings(floor: Floor, model: cp_model.CpModel):
    all_spacings = []

    for apartment in floor.apartments:
        for a_idx, b_idx, rel, wanted_dist in apartment.spacings:
            dist = distance_between_shapes_doubled(
                apartment.rooms[a_idx].variables,
                apartment.rooms[b_idx].variables,
                floor,
                model
            )
            are_spaced = None
            if rel == 'lt':
                are_spaced = base_reify(
                    dist < 2 * wanted_dist,
                    dist >= 2 * wanted_dist,
                    model
                )
            else:
                are_spaced = base_reify(
                    dist > 2 * wanted_dist,
                    dist <= 2 * wanted_dist,
                    model
                )
            all_spacings.append(are_spaced)

    if len(all_spacings) == 0:
        return 1
    return and_reify(all_spacings, model)
