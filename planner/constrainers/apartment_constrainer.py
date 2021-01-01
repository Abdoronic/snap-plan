from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.apartment import Apartment
from planner.models.module import Module
from planner.models.room_type import RoomType
from planner.constrainers.modules_constrainer import constraint_module, constraint_slim_modules
from planner.constrainers.utils import all_shapes_adjacent_in_order, and_reify, or_reify, shape_adjacent_to_any, shapes_are_adjacent

from typing import List


def constrain_apartment(apartment: Apartment, floor: Floor, model: cp_model.CpModel):
    constrain_room_adjacency(apartment, model)
    constrain_dinning_rooms(apartment, model)
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


def constrain_dinning_rooms(apartment: Apartment, model: cp_model.CpModel):
    kitchens = [
        room for room in apartment.rooms
        if room.room_type == RoomType.KITCHEN
    ]
    dining_rooms = [
        room for room in apartment.rooms
        if room.room_type == RoomType.DINING_ROOM
    ]
    kitchens_shapes = [*map(lambda kitchen: kitchen.variables, kitchens)]
    if len(dining_rooms) > 0:
        near_a_kitchen = and_reify(
            [
                shape_adjacent_to_any(room.variables, kitchens_shapes, model)
                for room in dining_rooms
            ],
            model
        )
        model.Add(near_a_kitchen == 1)


def constrain_ducts(apartment: Apartment, model: cp_model.CpModel):
    ducts = apartment.ducts
    for duct in ducts:
        constraint_module(duct, model)
        model.Add(duct.width_variable == 1)
        model.Add(duct.length_variable == 1)
    ducts_shapes = [*map(lambda duct: duct.variables, ducts)]
    room_types_needing_ducts = [
        RoomType.KITCHEN,
        RoomType.MASTER_BATHROOM,
        RoomType.BATHROOM
    ]
    if len(ducts) > 0:
        have_ducts = and_reify(
            [
                shape_adjacent_to_any(room.variables, ducts_shapes, model)
                for room in apartment.rooms
                if room.room_type in room_types_needing_ducts
            ],
            model
        )
        model.Add(have_ducts == 1)


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
    corridors_shapes = [*map(lambda corridor: corridor.variables, corridors)]
    return or_reify(
        [
            shape_adjacent_to_any(hallway.variables, corridors_shapes, model)
            for hallway in apartment.hallways
        ],
        model
    )
