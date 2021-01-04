from ortools.sat.python import cp_model

from planner.models.floor import Floor
from planner.io.converter import get_floor_plan

from typing import Dict


class SolutionHandler(cp_model.CpSolverSolutionCallback):
    """Handle intermediate solutions."""

    def __init__(self, floor: Floor, scores: Dict, max_num_of_solutions: int):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.floor = floor
        self.scores = scores
        self.max_num_of_solutions = max_num_of_solutions
        self.__solutions_count = 0
        self.__solutions = []

    def OnSolutionCallback(self):
        self.__solutions.append(
            get_floor_plan(self.floor, self.scores, self)
        )
        self.__solutions_count += 1
        if self.__solutions_count >= self.max_num_of_solutions:
            self.StopSearch()

    def get_solutions(self):
        return self.__solutions
