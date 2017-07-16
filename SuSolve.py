# SuSolve.py
# Skeletorfw
#
# 15/07/17
#
# Python 3.6

import numpy as np
from collections import namedtuple
from pprint import pprint


class Container:
    """Contains a distinct subclass of the sudoku matrix, e.g. a row or column."""
    def __init__(self, containertype, containernumber, mapping):
        self.containertype = containertype
        self.containernumber = containernumber
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

    # Pure container solution methods - need no other info.
    def lastone(self):
        """Find whether only one value is left unassigned"""
        if len(self.unassigned) == 1:
            final = self.unassigned.pop()   # Pop off final value in set
            self.mapping = [final if x == "x" else x for x in self.mapping]     # Insert into mapping
            self.assigned.add(final)
            self.solved = True  # self.validate()


class SudokuMatrix:
    """Class to hold the main Sudoku matrix and associated methods."""
    def __init__(self, matrixlist):
        self.values = []
        self.columncontainers = []
        self.rowcontainers = []
        self.boxcontainers = []
        self.fullinput(matrixlist)
        self.refresh_containers_full()

    def fullinput(self, inputlist):
        """Convert a list of cell values to SudokuCell instances"""
        self.values = []
        counter = 0
        for x in inputlist:
            self.values.append(SudokuCell(counter, x))      # Put in cell id and value to a SudokuCell
            counter += 1

    def refresh_containers_full(self):
        """Creates and fills the 27 containers, split into 3 9s"""
        # This could (and should) be collapsed down to only parse self.values once.
        # Create column containers
        containermapping_meta = [[], [], [], [], [], [], [], [], []]  # List of 9 lists, 1 for each row
        for x in self.values:
            containermapping_meta[x.column].append(x.value)     #
        counter = 0
        for mapping in containermapping_meta:
            self.columncontainers.append(Container("column", counter, mapping))
            counter += 1

        # Create row containers
        containermapping_meta = [[], [], [], [], [], [], [], [], []]  # List of 9 lists, 1 for each row
        for x in self.values:
            containermapping_meta[x.row].append(x.value)
        counter = 0
        for mapping in containermapping_meta:
            self.rowcontainers.append(Container("row", counter, mapping))
            counter += 1

        # Create box containers
        containermapping_meta = [[], [], [], [], [], [], [], [], []]  # List of 9 lists, 1 for each row
        for x in self.values:
            containermapping_meta[x.box].append(x.value)
        counter = 0
        for mapping in containermapping_meta:
            self.boxcontainers.append(Container("box", counter, mapping))
            counter += 1

    def cellinput(self, updater):
        # Takes a list of updater namedtuples and updates the noted cells with the values provided.
        #
        pass


class SudokuCell:
    """Class to hold a single Sudoku cell"""
    def __init__(self, cellid, value="x"):
        self.cellid = cellid    # Cells are numbered from 0 to 80
        self.column = cellid % 9
        self.row = cellid // 9
        self.box = 0
        self.find_box()
        self.value = value

    def find_box(self):
        """Find box id number"""
        baserow = self.row - self.row % 3
        basecolumn = self.column - self.column % 3
        boxcolumn = basecolumn // 3
        self.box = boxcolumn + baserow


def sudostring_parse(sudostr):
    """Take Sudoku in string format and output in list format"""
    numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}    # Create set literal containing all numbers 1 - 9 inclusive
    outlist = []
    for i in range(0, len(sudostr)):
        if sudostr[i] in numbers:
            outlist.append(int(sudostr[i]))     # Output only numbers 1 - 9 inclusive
        else:
            outlist.append(str(sudostr[i]))
    return outlist


def main():
    """Main loop"""
    updater = namedtuple("Updater", "x, y, value")  # Named tuple for holding update transactions.
    # Test data
    testsudo = "xxxxxxx4554x3x27xx8x694xx32x21xxx5x776x52x4xxxx5x64x1xx3217xxx49xxxx8x7xx8x4xx3x9"
    if len(testsudo) == 81:     # Check input string length
        matrixlist = sudostring_parse(testsudo)
    # matrixlist = [SudokuCell(x) for x in range(0, 81)]
        sudoku = SudokuMatrix(matrixlist)
        for x in sudoku.values:
            print("{}:{}".format(x.cellid, x.value))

main()