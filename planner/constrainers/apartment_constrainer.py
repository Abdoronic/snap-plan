from planner.constrainers.room_constrainer import enforce_rooms_be_adjacent

def constrain_apartment(apartment, floor, model):
    for room in apartment.rooms:
        for other_room_idx in room.adjacent_to:
            other_room = apartment.rooms[other_room_idx]
            enforce_rooms_be_adjacent(room, other_room, model)
    
