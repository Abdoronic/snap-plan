from planner.constrainers.distance_constrainer import distance_between_shapes_doubled
from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.constrainers.room_constrainer import has_landscape_view
from planner.constrainers.symmetry_constrainer import constrain_symmetry_over_apartment_class
from planner.constrainers.utils import and_reify, base_reify, or_reify


def constrain_optional_constraints(floor: Floor, model: cp_model.CpModel):
    constrain_symmetry_over_apartment_class(floor, model)
    constrain_apartments_have_landscape(floor, model)
    constrain_apartments_equidistant_to_elevator(floor, model)


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


def constrain_apartments_equidistant_to_elevator(floor: Floor, model: cp_model.CpModel):
    elevator = floor.elevator
    apartments_distances = [
        [
            distance_between_shapes_doubled(
                hallway.variables,
                elevator.variables,
                floor,
                model
            ) for hallway in apartment.hallways
        ]
        for apartment in floor.apartments
    ]
    min_distances = [
        model.NewIntVar(0, 2 * (floor.width + floor.length), '')
        for _ in range(len(floor.apartments))
    ]
    for i in range(len(floor.apartments)):
        model.AddMinEquality(min_distances[i], apartments_distances[i])

    differences = [
        model.NewIntVar(-2 * (floor.width + floor.length), 2 * (floor.width + floor.length), '')
        for _ in range(len(floor.apartments) - 1)
    ]
    for i in range(len(floor.apartments) - 1):
        model.Add(differences[i] == min_distances[i] - min_distances[i + 1])

    abs_differences = [
        model.NewIntVar(0, 2 * (floor.width + floor.length), '')
        for _ in range(len(differences))
    ]
    for i in range(len(differences)):
        model.AddAbsEquality(abs_differences[i], differences[i])

    error_factor = 5
    apartments_equidistant = and_reify(
        [
            base_reify(
                diff < error_factor,
                diff >= error_factor,
                model
            )
            for diff in abs_differences
        ],
        model
    )
    model.Add(apartments_equidistant == 1)
