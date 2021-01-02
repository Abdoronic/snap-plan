from ortools.sat.python import cp_model

from planner.models.room_type import RoomType

from typing import List, Tuple


class Room:
    def __init__(
        self,
        room_type: RoomType,
        min_area: int,
        preferred_width: int = None,
        preferred_length: int = None,
        adjacent_to: List[int] = []
    ):
        """
        Parameters
        ----------

            room_type: RoomType
                type of the room, e.g. RoomType.BEDROOM, RoomType.KITCHEN, etc.

            min_area: int
                Minimum area of the room in square meters

            preferred_width: int
                preferred width of the room in meters

            preferred_length: int
                Preferred length of the room in meters

            adjacent_to: list
                A list of room indices (in a certain apartment), that this room must be adjacent to one of.
        """
        self.room_type = room_type
        self.min_area = min_area
        self.preferred_width = preferred_width
        self.preferred_length = preferred_length
        self.adjacent_to = adjacent_to

        self.variables: Tuple[
            cp_model.IntVar,
            cp_model.IntVar,
            cp_model.IntVar,
            cp_model.IntVar
        ] = None
        self.area_variable: cp_model.IntVar = None
        self.width_variable: cp_model.IntVar = None
        self.length_variable: cp_model.IntVar = None

    def has_preferred_width(self):
        """ Check if a preferred width was specified """
        return self.preferred_width is not None

    def has_preferred_length(self):
        """ Check if a preferred length was specified """
        return self.preferred_length is not None

    def has_adjacent_rooms(self):
        """ Check if a adjacent rooms constraint was specified """
        return len(self.adjacent_to) > 0

    def __str__(self):
        return f'Room(room_type={self.room_type}, min_area={self.min_area}, preferred_width={self.preferred_width}, preferred_length={self.preferred_length}, adjacent_to={self.adjacent_to}, variables={self.variables})'
