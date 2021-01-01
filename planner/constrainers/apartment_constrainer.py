from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.apartment import Apartment
from planner.models.module import Module
from planner.constrainers.modules_constrainer import constraint_module, constraint_slim_modules
from planner.constrainers.utils import all_shapes_adjacent_in_order, and_reify, or_reify, shape_adjacent_to_any, shapes_are_adjacent

from typing import List

def constrain_apartment(apartment: Apartment, floor: Floor, model: cp_model.CpModel):
    constrain_room_adjacency(apartment, model)
    constrain_ducts(apartment, model)
    constrain_hallways(apartment, model)


def constrain_room_adjacency(apartment: Apartment, model: cp_model.CpModel):
    for room in apartment.rooms:
        for other_room_idx in room.adjacent_to:
            other_room = apartment.rooms[other_room_idx]
            adjacent = shapes_are_adjacent(
                room.variables,
                other_room.variables,
                model
            )
            model.Add(adjacent == 1)


def constrain_ducts(apartment: Apartment, model: cp_model.CpModel):
    for duct in apartment.ducts:
        constraint_module(duct, model)
        model.Add(duct.width_variable == 1)
        model.Add(duct.length_variable == 1)


def constrain_hallways(apartment: Apartment, model: cp_model.CpModel):
    hallways = apartment.hallways
    constraint_slim_modules(hallways, model)
    hallways_shapes = [*map(lambda hallway: hallway.variables, hallways)]
    hallways_adjacent = all_shapes_adjacent_in_order(hallways_shapes, model)
    rooms_connected = and_reify(
        [
            shape_adjacent_to_any(room.variables, hallways_shapes, model)
            for room in apartment.rooms
        ],
        model
    )
    model.Add(and_reify([hallways_adjacent, rooms_connected], model) == 1)

def apartment_connected_to_corridors(
    apartment: Apartment,
    corridors: List[Module],
    model: cp_model.CpModel):
    corridors_shapes = [*map(lambda corridor : corridor.variables, corridors)]
    return or_reify(
        [
            shape_adjacent_to_any(hallway.variables, corridors_shapes, model)
            for hallway in apartment.hallways
        ],
        model
    )