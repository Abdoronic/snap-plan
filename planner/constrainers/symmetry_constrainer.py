from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.apartment import Apartment
from planner.models.room import Room

from planner.constrainers.utils import and_reify, eq_var_reify, fail_reify, or_reify

from typing import List


def constrain_symmetry_over_apartment_class(floor: Floor, model: cp_model.CpModel):

    apartment_classes = get_apartments_classes(floor)
    classes_counts = [
        len(apartment_class) for apartment_class in apartment_classes
    ]

    for class_count in classes_counts:
        if class_count % 2 == 1:
            fail = fail_reify(model)
            model.Add(fail == 1)
            return

    for apartment_class in apartment_classes:
        for i in range(0, len(apartment_class), 2):
            possible_reflections = [
                are_reflected_in_direction(
                    apartment_class[i],
                    apartment_class[i + 1],
                    direction,
                    floor,
                    model
                ) for direction in range(2)
            ]
            are_reflected_on_any_direction = or_reify(
                possible_reflections,
                model
            )
            model.Add(are_reflected_on_any_direction == 1)


def get_apartments_classes(floor: Floor) -> List[List[Apartment]]:
    apartment_classes: List[List[Apartment]] = []
    current_apartment_class: List[Apartment] = []

    for apartment in floor.apartments:
        if len(current_apartment_class) == 0 or apartment.type_id == current_apartment_class[-1].type_id:
            current_apartment_class.append(apartment)
        else:
            apartment_classes.append(current_apartment_class)
            current_apartment_class = []
            current_apartment_class.append(apartment)

    if len(current_apartment_class) != 0:
        apartment_classes.append(current_apartment_class)

    return apartment_classes


def are_reflected_in_direction(
    first_apartment: Apartment,
    second_apartment: Apartment,
    direction: int,
    floor: Floor,
    model: cp_model.CpModel
) -> cp_model.IntVar:
    needed_constraints = []

    for i in range(len(first_apartment.rooms)):
        first_room: Room = first_apartment.rooms[i]
        second_room: Room = second_apartment.rooms[i]
        for j in range(2 * direction, 2 * direction + 2):
            have_equal_coordinate = eq_var_reify(
                first_room.variables[j],
                second_room.variables[j],
                model
            )
            needed_constraints.append(have_equal_coordinate)

        for j in range(2 * (1 - direction), 2 * (1 - direction) + 2):
            floor_side = (floor.length, floor.width)[direction]
            add_up_to_floor_side = eq_var_reify(
                first_room.variables[j] + second_room.variables[1 - j],
                floor_side,
                model
            )
            needed_constraints.append(add_up_to_floor_side)

    return and_reify(needed_constraints, model)
