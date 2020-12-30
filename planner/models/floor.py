from ortools.sat.python import cp_model

from planner.models.apartment import Apartment
from planner.models.room import Room
from planner.models.view import View

from typing import List, Tuple


class Floor:
    def __init__(self, width: int, length: int, sides_views: Tuple[View, View, View, View], apartments: List[Apartment]):
        """
        Parameters
        ----------

            width : int
                width of the floor

            length : int
                length of the floor

            sides_views : 4-tuple
                floor Views at its 4 sides (N,S,E,W)

            apartments : list
                list of apartments
        """

        self.width = width
        self.length = length
        self.sides_views = sides_views
        self.apartments = apartments
        self.rooms: List[Room] = []
        for apartment in self.apartments:
            self.rooms.extend(apartment.rooms)

        self.score_variable: cp_model.IntVar = None

    def __str__(self):
        floor_repr = f'Floor(width={self.width}, length={self.length}, sides_views={self.sides_views},\n'
        floor_repr += 'apartments=[\n' + '\n\n'.join(
            [str(apartment) for apartment in self.apartments]) + '\n])'
        return floor_repr
