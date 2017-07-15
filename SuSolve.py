# SuSolve.py
# Skeletorfw
#
# 15/07/17
#
# Python 3.6

import numpy as np
from collections import namedtuple


class Container:
    """Contains a distinct subclass of the sudoku matrix, e.g. row or column."""
    def __init__(self, containertype, mapping):
        self.containertype = containertype
        self.mapping = []
        self.assigned = set()
        self.unassigned = set()
        self.solved = False     # Is the container solved?
        self.update(mapping)

    def update(self, mapping):
        """Refresh mapping list from provided mapping."""
        self.mapping = list(mapping)
        self.regen()    # Regenerate sets

    def regen(self):
        """Regenerate sets from mapping."""
        self.assigned = set()
        self.unassigned = set()
        for x in range(1, 10):
            if x in self.mapping:
                self.assigned.add(x)
            else:
                self.unassigned.add(x)
        self.validate()     # Validate that set is not solved

    def validate(self):
        """Check whether the container is solved."""
        if len(self.unassigned) < 1:
            self.solved = True

    # Solution Methods
    def lastone(self):
        """Find whether only one value is left unassigned"""
        if len(self.unassigned) == 1:
            final = self.unassigned.pop()   # Pop off final value in set
            self.mapping = [final if x == "x" else x for x in self.mapping]     # Insert into mapping
            self.assigned.add(final)
            self.solved = True  # self.validate()


class SudokuMatrix:
    """Class to hold the main Sudoku matrix and associated methods."""
    def __init__(self):
        self.values = []    # Won't actually be a list, placeholder for now.

    def input(self, updater):
        # Takes an updater NamedTuple and updates the noted cell with the value provided.
        pass


def main():
    """Main loop"""
    updater = namedtuple("Updater", "x, y, value")  # Named tuple for holding update transactions.