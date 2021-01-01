from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.models.apartment import Apartment
from planner.constrainers.room_constrainer import rooms_are_adjacent


def constrain_apartment(apartment: Apartment, floor: Floor, model: cp_model.CpModel):
    constrain_room_adjacency(apartment, model)
    constraint_ducts(apartment, model)
    constraint_hallways(apartment, model)

def constrain_room_adjacency(apartment: Apartment, model: cp_model.CpModel):
    for room in apartment.rooms:
        for other_room_idx in room.adjacent_to:
            other_room = apartment.rooms[other_room_idx]
            adjacent = rooms_are_adjacent(room, other_room, model)
            model.Add(adjacent == 1)

def constraint_ducts(apartment: Apartment, model: cp_model.CpModel):
    pass


def constraint_hallways(apartment: Apartment, model: cp_model.CpModel):
    pass
