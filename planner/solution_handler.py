from ortools.sat.python import cp_model


class SolutionHandler(cp_model.CpSolverSolutionCallback):
    """Handle intermediate solutions."""

    def __init__(self, floor):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.floor = floor

    def OnSolutionCallback(self):
        print('Floor Score:', self.Value(self.floor.score_variable))
        self.StopSearch()
