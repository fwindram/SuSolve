# SuSolve.py
# Skeletorfw
#
# 15/07/17
#
# Python 3.6

from collections import namedtuple
from testpuzzles import *


class Container:
    """Contains a distinct subclass of the sudoku matrix, e.g. a row or column."""
    def __init__(self, containertype, containernumber, mapping):
        self.containertype = containertype
        self.containernumber = containernumber
        self.mapping = []
        self.referredids = []    # Make it easier to reconstruct a container by addressing directly
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

    def fill_referredids(self, referred):
        """Pull provided referred ids into class"""
        self.referredids = referred

    # Pure container solution methods - need no other info.
    def lastone(self):
        """Find whether only one value is left unassigned"""
        # DEPRECATED BY .last_possible() CELL METHOD
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
        self.create_containers()

    def completion(self):
        """Count the number of unknown values left in a Sudoku matrix."""
        comp_counter = 0       # Number of unknowns
        for cell in self.values:
            if cell.value == "x":
                comp_counter += 1
        return comp_counter

    def print_grid(self):
        gridstring = ""
        griddivider_vert = " "
        sudoindex = 0
        for i in range(0, 11):      # Row Iteration
            grid_line = []
            if i in [3, 7]:     # Insert dividers
                gridstring += "- - - + - - - + - - -\n"
            else:
                for j in range(0, 9):   # Column Iteration
                    if j in [2, 5]:
                        grid_line.append(str(self.values[sudoindex].value) + " |")      # Insert dividers
                    else:
                        grid_line.append(str(self.values[sudoindex].value))
                    sudoindex += 1
                gridstring += "{}\n".format(griddivider_vert.join(grid_line))

        return gridstring

    def fullinput(self, inputlist):
        """Convert a list of cell values to SudokuCell instances"""
        self.values = []
        counter = 0
        for x in inputlist:
            self.values.append(SudokuCell(counter, x))      # Put in cell id and value to a SudokuCell
            counter += 1

    def create_containers(self):
        """Creates and fills the 27 containers, split into 3 9s for column, row & box"""
        containermapping_meta_columns = [[], [], [], [], [], [], [], [], []]  # List of 9 lists, 1 for each row
        containermapping_meta_rows = [[], [], [], [], [], [], [], [], []]  # List of 9 lists, 1 for each row
        containermapping_meta_boxes = [[], [], [], [], [], [], [], [], []]  # List of 9 lists, 1 for each row
        for x in self.values:
            containermapping_meta_columns[x.column].append(x.value)
            containermapping_meta_rows[x.row].append(x.value)
            containermapping_meta_boxes[x.box].append(x.value)
        counter = 0
        for mapping in containermapping_meta_columns:
            self.columncontainers.append(Container("column", counter, mapping))
            counter += 1
        counter = 0
        for mapping in containermapping_meta_rows:
            self.rowcontainers.append(Container("row", counter, mapping))
            counter += 1
        counter = 0
        for mapping in containermapping_meta_boxes:
            self.boxcontainers.append(Container("box", counter, mapping))
            counter += 1
        self.trace_referring_cells()

    def trace_referring_cells(self):
        """Fill in containers with the cells that refer to them."""
        # Create map structure
        referrals_map = []
        for i in range(0, 3):
            referrals_map.append([])
            for j in range(0, 9):
                referrals_map[len(referrals_map) - 1].append([])
        # Fill map structure
        for cell in self.values:
            referrals_map[0][cell.column].append(cell.cellid)
            referrals_map[1][cell.row].append(cell.cellid)
            referrals_map[2][cell.box].append(cell.cellid)
        # Fill container referrals from mappings
        for container in self.columncontainers:
            container.fill_referredids(referrals_map[0][container.containernumber])
        for container in self.rowcontainers:
            container.fill_referredids(referrals_map[1][container.containernumber])
        for container in self.boxcontainers:
            container.fill_referredids(referrals_map[2][container.containernumber])

    def regen_containers(self, containerlist):
        """Regenerate specified containers.
        :param containerlist: List of 3 lists, corresponding to columns, rows & boxes
        :type containerlist: list"""
        for column in containerlist[0]:
            referred = self.columncontainers[column].referredids
            mapping = []
            for cellid in referred:
                mapping.append(self.values[cellid].value)
            self.columncontainers[column].update(mapping)
        for row in containerlist[1]:
            referred = self.rowcontainers[row].referredids
            mapping = []
            for cellid in referred:
                mapping.append(self.values[cellid].value)
            self.rowcontainers[row].update(mapping)
        for box in containerlist[2]:
            referred = self.boxcontainers[box].referredids
            mapping = []
            for cellid in referred:
                mapping.append(self.values[cellid].value)
            self.boxcontainers[box].update(mapping)

    def cellinput(self, updater):
        # Takes a list of updater namedtuples and updates the noted cells with the values provided.
        #
        pass

    # Full & partial matrix updates
    def find_possible_full(self):
        """Update -all- cells with their possible values, only considering self and all containers."""
        for x in self.values:
            possible = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # Create set literal containing all numbers 1 - 9 inclusive
            impossible = set()  # Create base set for used numbers in all containers.
            impossible.update(self.columncontainers[x.column].assigned)  # Add used numbers from column
            impossible.update(self.rowcontainers[x.row].assigned)       # Add used numbers from row
            impossible.update(self.boxcontainers[x.box].assigned)       # Add used numbers from box
            possible.difference_update(impossible)  # Find possible (diff original possible with impossible).
            x.update_possible(possible, True)   # Update cell possible set with calculate possibles.

    def find_possible(self):
        """Update -unsolved- cells with their possible values, only considering self and all containers."""
        container_updates = [set(), set(), set()]
        for x in self.values:
            possible = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # Create set literal containing all numbers 1 - 9 inclusive
            if x.value not in possible:  # Run if value is "x"
                impossible = set()      # Create base set for used numbers in all containers.
                impossible.update(self.columncontainers[x.column].assigned)  # Add used numbers from column
                impossible.update(self.rowcontainers[x.row].assigned)        # Add used numbers from row
                impossible.update(self.boxcontainers[x.box].assigned)        # Add used numbers from box
                possible.difference_update(impossible)      # Find possible (diff original possible with impossible).
                if x.update_possible(possible):     # Update cell possible set with calculate possibles.
                    container_updates[0].add(x.column)   # If cell VALUE was updated, mark containers for regen
                    container_updates[1].add(x.row)
                    container_updates[2].add(x.box)
        self.regen_containers(container_updates)    # Regenerate containers.


class SudokuCell:
    """Class to hold a single Sudoku cell"""
    def __init__(self, cellid, value):
        self.cellid = cellid    # Cells are numbered from 0 to 80
        self.column = cellid % 9
        self.row = cellid // 9
        self.box = 0
        self.find_box()
        self.value = value
        self.possible = set()

    def find_box(self):
        """Find box id number"""
        baserow = self.row - self.row % 3
        basecolumn = self.column - self.column % 3
        boxcolumn = basecolumn // 3
        self.box = boxcolumn + baserow

    def update_possible(self, possible, fullrun=False):
        """Update possible numbers"""
        self.possible = possible
        if not fullrun:     # Only run if this is not the initial possibility update.
            if self.last_possible():
                return True
            # else return None (implicit)

    def last_possible(self):
        """Set to remaining number if possible set is len 1"""
        if len(self.possible) == 1 and self.value == "x":
            self.value = self.possible.pop()
            return True     # Tell outside world that we have put a value in!
            # NOW REGEN LINKED CONTAINERS


def sudostring_parse(sudostr):
    """Take Sudoku in string format and output in list format"""
    numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}    # Create set literal containing all numbers 1 - 9 inclusive
    outlist = []
    xcount = 0
    for i in range(0, len(sudostr)):
        try:
            test = int(sudostr[i]) + 0
            if not test:    # Account for if a 0 in inserted by accident.
                raise ValueError
            outlist.append(int(sudostr[i]))
        except ValueError:
            outlist.append("x")     # Replace unknown characters with x
            xcount += 1
    print("\nSudoku string:\n{}".format(sudostr))
    print("Initial values left to find: {}\n".format(xcount))
    return outlist


def main():
    """Main loop"""
    updater = namedtuple("Updater", "x, y, value")  # Named tuple for holding update transactions.

    completed_sudokus = 0
    for testsudo in sudotest_easy:
        if len(testsudo) == 81:     # Check input string length
            matrixlist = sudostring_parse(testsudo)
            sudoku = SudokuMatrix(matrixlist)
            match_count = 0
            previous_count = 0
            current_count = 0
            print("{}".format(sudoku.print_grid()))
            sudoku.find_possible_full()     # Initially generate possibility sets
            while True:
                # print("Run {}".format())
                sudoku.find_possible()      # Find new possibility sets & update values
                current_count = sudoku.completion()
                if current_count == previous_count:
                    match_count += 1
                if not current_count:   # Break if 0 remaining to solve
                    print("{}% solved ({}/81)".format(int((81 - current_count) / 81 * 100), current_count))
                    print("Success!\n")
                    completed_sudokus += 1
                    break
                elif match_count >= 3:     # Mark as incomplete after 3 runs with no change
                    print("Incomplete.\nPuzzle was solved {}% of the way."
                          .format(int((81 - current_count) / 81 * 100)))
                    failstr = ""
                    for cell in sudoku.values:
                        failstr += str(cell.value)
                    print("Final state:\n{}".format(failstr))
                    break
                previous_count = int(current_count)
                # print("Left to find: {}/81".format(current_count))
                print("{}% solved ({}/81)".format(int((81 - current_count) / 81 * 100), current_count))
            print("{}".format(sudoku.print_grid()))
    print("Successfully completed {}/{}".format(completed_sudokus, len(sudotest_easy)))

main()
