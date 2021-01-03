from planner.models.apartment import Apartment
from ortools.sat.python import cp_model

from math import sqrt

from planner.models.floor import Floor
from planner.models.room_type import RoomType
from planner.constrainers.room_constrainer import has_daylight
from planner.constrainers.distance_constrainer import distance_between_shapes_doubled
from planner.constrainers.utils import and_reify, base_reify


def add_objective_function(floor: Floor, model: cp_model.CpModel):
    have_daylight = all_rooms_have_daylight(floor, model)
    have_good_spacings = all_rooms_have_good_spacings(floor, model)
    bedrooms_are_close = all_bedrooms_are_close(floor, model)
    bathroom_is_close = main_bathroom_is_close(floor, model)
    model.Add(floor.score_variable == sum([
        have_daylight,
        have_good_spacings,
        bedrooms_are_close,
        bathroom_is_close
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


def all_bedrooms_are_close(floor: Floor, model: cp_model.CpModel):
    return and_reify(
        [
            all_bedrooms_are_close_in_apartment(
                apartment,
                floor,
                model
            )
            for apartment in floor.apartments
        ],
        model
    )


def all_bedrooms_are_close_in_apartment(
    apartment: Apartment,
    floor: Floor,
    model: cp_model.CpModel
):
    bedrooms = [
        room
        for room in apartment.rooms
        if room.room_type == RoomType.BEDROOM
    ]

    if len(bedrooms) == 0:
        return 1

    avg_area = sum([room.min_area for room in bedrooms]) / len(bedrooms)
    delta = round(2.5 * sqrt(avg_area))

    distances_less_than_delta = []
    for i in range(len(bedrooms)):
        for j in range(i + 1, len(bedrooms)):
            dist = distance_between_shapes_doubled(
                bedrooms[i].variables,
                bedrooms[j].variables,
                floor,
                model
            )
            distances_less_than_delta.append(
                base_reify(
                    dist < delta,
                    dist >= delta,
                    model
                )
            )

    return and_reify(distances_less_than_delta, model)


def main_bathroom_is_close(floor: Floor, model: cp_model.CpModel):
    return and_reify(
        [
            main_bathroom_is_close_in_apartment(
                apartment,
                floor,
                model
            )
            for apartment in floor.apartments
        ],
        model
    )


def main_bathroom_is_close_in_apartment(
    apartment: Apartment,
    floor: Floor,
    model: cp_model.CpModel
):
    bathrooms = [
        room
        for room in apartment.rooms
        if room.room_type == RoomType.BATHROOM
        or room.room_type == RoomType.MASTER_BATHROOM
    ]

    all_rooms = [
        room
        for room in apartment.rooms
        if room.room_type != RoomType.BATHROOM
        and room.room_type != RoomType.MASTER_BATHROOM
    ]

    if len(bathrooms) == 0 or len(all_rooms) == 0:
        return 1

    main_bathroom = max(
        bathrooms,
        key=lambda b: b.min_area
    )

    avg_area = sum([room.min_area for room in all_rooms]) / len(all_rooms)
    delta_room = round(3.5 * sqrt(avg_area))
    delta_living = round(2.25 * sqrt(avg_area))

    distances_less_than_delta = []
    for room in all_rooms:
        dist = distance_between_shapes_doubled(
            room.variables,
            main_bathroom.variables,
            floor,
            model
        )

        delta = delta_room
        if room.room_type == RoomType.LIVING_ROOM:
            delta = delta_living

        distances_less_than_delta.append(
            base_reify(
                dist < delta,
                dist >= delta,
                model
            )
        )

    return and_reify(distances_less_than_delta, model)
