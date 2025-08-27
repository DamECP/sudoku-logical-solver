from logger import log_change


class Cell:
    def __init__(self, row, col, square):

        self.row = row
        self.col = col
        self.coord = (row, col)
        self.square = square
        self.value = None
        self.candidates = self.build_candidates()

    def assign_value(self, value):
        before = f"Before (candidates): {self.candidates}"
        self.value = value
        explanation = "only one candidate remaining"
        self.candidates.clear()
        after = (
            f"assigned_value = {self.value}, remaining candidates = {self.candidates}"
        )
        log_change(self, "assign_value", explanation, before, after)

    def discard_candidates(self, values):
        """Values can be a single value or a list"""
        changes = False
        if isinstance(values, int):
            values = [values]  # make it a list to loop

        for v in values:
            if v in self.candidates:
                self.candidates.discard(v)
                changes = True

        if len(self.candidates) == 1:
            single_value = list(self.candidates)[0]
            self.assign_value(single_value)
            changes = True

        if self.value is None and len(self.candidates) == 0:
            raise ValueError(f"{self.coord}")

        return changes

    def build_candidates(self) -> set:
        return set(range(1, 10))

    def __repr__(self):
        if self.value is not None:
            return f"Value : {self.value}"
        else:
            return f"Candidates: {sorted(self.candidates)}"


class Sudoku:
    def __init__(self, grid):

        self.original_grid = [row[:] for row in grid]
        self.cells = self.build_cells()
        self.rows = self.build_rows()
        self.cols = self.build_cols()
        self.squares = self.build_squares()

    # Parse the grid and build the sudoku/cells objects
    def build_cells(self) -> dict:
        cells = {}
        for row in range(9):
            for col in range(9):
                square = 3 * (row // 3) + (col // 3) + 1
                c = Cell(row + 1, col + 1, square)
                char = self.original_grid[row][col]
                if char.isdigit():
                    c.assign_value(int(char))

                # coord as key, Cell obj as value
                cells[(row + 1, col + 1)] = c
        return cells

    def build_rows(self) -> dict:
        return {
            row + 1: [self.cells[(row + 1, col + 1)] for col in range(9)]
            for row in range(9)
        }

    def build_cols(self) -> dict:
        return {
            col + 1: [self.cells[(row + 1, col + 1)] for row in range(9)]
            for col in range(9)
        }

    def build_squares(self) -> dict:
        squares = {}
        sq_id = 1
        for sr in range(3):
            for sc in range(3):
                sq_cells = []
                for r in range(sr * 3 + 1, sr * 3 + 4):
                    for c in range(sc * 3 + 1, sc * 3 + 4):
                        sq_cells.append(self.cells[(r, c)])
                squares[sq_id] = sq_cells
                sq_id += 1
        return squares

    def current_grid(self) -> list:
        current_grid = []
        for row in self.rows.values():
            cells = "".join([str(c.value) if c.value is not None else "x" for c in row])
            current_grid.append(cells)
        return current_grid

    def __repr__(self):

        white, green, red = "\033[97m", "\033[92m", "\033[91m"

        if self.current_grid() == self.original_grid:
            color = white
        elif all(c.value is not None for c in self.cells.values()):
            color = green
        else:
            color = red

        grid = ""
        for r in range(1, 10):
            for c, cell in enumerate(self.rows[r], 1):
                grid += str(cell.value) if cell.value else "x"
                if c % 3 == 0 and c != 9:
                    grid += " | "
                else:
                    grid += " "
            grid += "\n"
            if r % 3 == 0 and r != 9:
                grid += "-" * 21 + "\n"

        return f"{color}{grid}{white}"
