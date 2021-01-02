from planner.models.room import Room
from planner.models.module import Module
from planner.models.room_type import RoomType

from typing import List, Tuple


class Apartment:
    def __init__(
        self,
        type_id: int,
        rooms: List[Room],
        number_of_hallways: int,
        spacings: List[Tuple[int, int, str, int]]
    ):
        """
        Parameters
        ----------
            rooms : list
                list of rooms
        """
        self.type_id = type_id
        self.rooms = rooms
        self.number_of_hallways = number_of_hallways
        self.spacings = spacings

        self.number_of_ducts: int = 1
        for room in rooms:
            if room.room_type == RoomType.BATHROOM or room.room_type == RoomType.KITCHEN:
                self.number_of_ducts += 1
        self.number_of_ducts //= 2

        self.ducts: List[Module] =  [
            Module()
            for _ in range(self.number_of_ducts)
        ]
        self.hallways: List[Module] = [
            Module()
            for _ in range(self.number_of_hallways)
        ]


    def __str__(self):
        return '\t' + '\n\t'.join([str(room) for room in self.rooms])
