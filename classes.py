class Cell:
    def __init__(self, row, col, square):

        self.row = row
        self.col = col
        self.square = square
        self.coord = (self.row, self.col)
        self.value = None
        self.candidates = self.build_candidates()

    def assign_value(self, value):
        self.value = value
        self.candidates.clear()

    def discard_candidate(self, value):
        progress = False
        if value in self.candidates:
            self.candidates.discard(value)
            progress = True
        # if only one candidate : becomes value and clear candidates
        if len(self.candidates) == 1:
            single_value = next(iter(self.candidates))
            self.assign_value(single_value)
            progress = True

        return progress

    def build_candidates(self) -> set:
        return set(range(1, 10))

    def get_value(self) -> int:
        return self.value

    def get_candidates(self) -> set:
        return self.candidates

    def __repr__(self):
        if self.value is not None:
            return f"Cell{self.coord}: {self.value}"
        else:
            return f"Cell{self.coord}: {sorted(self.candidates)}"


class Sudoku:
    def __init__(self, grid):

        # Deep copy for comparison purpose
        self.initial_state = [row[:] for row in grid]
        self.grid = grid
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
                char = self.grid[row][col]
                if char.isdigit():
                    c.assign_value(int(char))

                # key : coordinates | value = cell object
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

    def get_row(self, row_number):
        return self.rows[row_number]

    def get_col(self, col_number):
        return self.cols[col_number]

    def get_square(self, square_number):
        return self.squares[square_number]

    def current_version(self):
        return [
            "".join(
                str(cell.value) if cell.value is not None else "x"
                for cell in self.rows[r]
            )
            for r in range(1, 10)
        ]

    def get_cell_groups(self, cell):
        return {
            "row_values": {
                c.value for c in self.get_row(cell.row) if c.value is not None
            },
            "col_values": {
                c.value for c in self.get_col(cell.col) if c.value is not None
            },
            "square_values": {
                c.value for c in self.get_square(cell.square) if c.value is not None
            },
            "row_candidates": [
                c.candidates for c in self.get_row(cell.row) if c.value is None
            ],
            "col_candidates": [
                c.candidates for c in self.get_col(cell.col) if c.value is None
            ],
            "square_candidates": [
                c.candidates for c in self.get_square(cell.square) if c.value is None
            ],
        }

    def __repr__(self):

        white, green, red = "\033[97m", "\033[92m", "\033[91m"

        if self.current_version() == self.grid:
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

    def show_cell_candidates(self):
        for row in range(1, 10):
            for cell in self.rows[row]:
                if cell.value is None:
                    print(cell.coord, sorted(cell.candidates))
