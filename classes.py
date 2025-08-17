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

        if len(self.candidates) == 1:
            single_value = next(iter(self.candidates))
            self.assign_value(single_value)
            progress = True

        return progress

    def build_candidates(self):
        return set(range(1, 10))

    def get_value(self):
        return self.value

    def get_candidates(self):
        return self.candidates

    def __repr__(self):
        if self.value is not None:
            return f"Cell{self.coord}: {self.value}"
        else:
            return f"Cell{self.coord}: {sorted(self.candidates)}"


class Sudoku:
    def __init__(self, grid):

        self.grid = grid
        self.cells = self.build_cells()
        self.rows = self.build_rows()
        self.cols = self.build_cols()
        self.squares = self.build_squares()

    def build_cells(self):
        cells = {}
        for row in range(9):
            for col in range(9):
                square = 3 * (row // 3) + (col // 3) + 1
                c = Cell(row + 1, col + 1, square)
                char = self.grid[row][col]
                if char.isdigit():
                    c.assign_value(int(char))
                else:
                    c.build_candidates()

                cells[(row + 1, col + 1)] = c
        return cells

    def build_rows(self):
        return {
            row + 1: [self.cells[(row + 1, col + 1)] for col in range(9)]
            for row in range(9)
        }

    def build_cols(self):
        return {
            col + 1: [self.cells[(row + 1, col + 1)] for row in range(9)]
            for col in range(9)
        }

    def build_squares(self):
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

    def get_row_values(self, row_number):
        return {c.value for c in self.get_row(row_number) if c.value is not None}

    def get_col_values(self, col_number):
        return {c.value for c in self.get_col(col_number) if c.value is not None}

    def get_square_values(self, square_number):
        return {c.value for c in self.get_square(square_number) if c.value is not None}

    def get_row_candidates(self, row_number):
        return [c.candidates for c in self.get_row(row_number) if c.value is None]

    def get_col_candidates(self, col_number):
        return [c.candidates for c in self.get_col(col_number) if c.value is None]

    def get_square_candidates(self, square_number):
        return [c.candidates for c in self.get_square(square_number) if c.value is None]

    def __repr__(self):

        grid = ""
        for row in range(1, 10):
            for cell in self.rows[row]:
                grid += str(cell.value) if cell.value is not None else "x"
                grid += " "
            grid += "\n"

        return grid

    def show_cell_candidates(self):
        for row in range(1, 10):
            for cell in self.rows[row]:
                if cell.value is None:
                    print(cell.coord, sorted(cell.candidates))
