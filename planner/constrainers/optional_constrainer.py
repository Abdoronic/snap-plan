from planner.constrainers.distance_constrainer import distance_between_shapes_doubled
from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.constrainers.room_constrainer import has_landscape_view
from planner.constrainers.symmetry_constrainer import constrain_symmetry_over_apartment_class
from planner.constrainers.utils import and_reify, base_reify, or_reify


def constrain_optional_constraints(floor: Floor, model: cp_model.CpModel):
    if floor.has_symmetry_constraint:
        constrain_symmetry_over_apartment_class(floor, model)
    if floor.has_all_landscape_constraint:
        constrain_apartments_have_landscape(floor, model)
    if floor.has_all_near_elevator_constraint:
        constrain_apartments_equidistant_to_elevator(floor, model)
    if floor.has_golden_ratio_constraint:
        constrain_golden_ratio(floor, model)


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
        model.NewIntVar(-2 * (floor.width + floor.length),
                        2 * (floor.width + floor.length), '')
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


def constrain_golden_ratio(floor: Floor, model: cp_model.CpModel):
    for room in floor.rooms:
        width = room.width_variable
        length = room.length_variable
        golden_ratio = or_reify(
            [
                is_golden_ratio(width, length, model),
                is_golden_ratio(length, width, model)
            ],
            model
        )
        model.Add(golden_ratio == 1)


def is_golden_ratio(a: cp_model.IntervalVar, b: cp_model.IntVar, model: cp_model.CpModel):
    """
    Reifies the relation:
    (0.1 * golden_ratio_lb <= a / b <= 0.1 * golden_ratio_ub)
    """
    golden_ratio_lb = 16
    golden_ratio_ub = 17
    return and_reify(
        [
            base_reify(
                10 * a <= golden_ratio_ub * b,
                10 * a > golden_ratio_ub * b,
                model
            ),
            base_reify(
                10 * a >= golden_ratio_lb * b,
                10 * a < golden_ratio_lb * b,
                model
            ),
        ],
        model
    )
