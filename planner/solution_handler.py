from ortools.sat.python import cp_model

from planner.models.floor import Floor


class SolutionHandler(cp_model.CpSolverSolutionCallback):
    """Handle intermediate solutions."""

    def __init__(self, floor: Floor):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.floor = floor

    def OnSolutionCallback(self):
        print('Floor Score:', self.Value(self.floor.score_variable))
        self.StopSearch()
