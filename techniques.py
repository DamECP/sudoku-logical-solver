from logger import log_change
from collections import Counter


def repeat_until_no_change(func):
    """Decorator"""

    def wrapper(sudoku):
        inner_changes = True
        global_changes = False
        while inner_changes:
            inner_changes = func(sudoku)
            if inner_changes:
                global_changes = True
        return global_changes

    return wrapper


def narrow_cell_candidates(cell, sudoku):
    """Reduces the candidates for each cell based on their row/col/square values"""
    changes = False

    all_values = {
        c.value
        for c in sudoku.rows[cell.row]
        + sudoku.cols[cell.col]
        + sudoku.squares[cell.square]
        if c.value is not None
    }

    if cell.value is None:
        before = f"Before candidates = {sorted(cell.candidates)}"
        explanation = f"Values around = {sorted(all_values)}"
        if cell.discard_candidates(all_values):
            after = f"After candidates = {sorted(cell.candidates)   }"
            log_change(cell, "narrow_candidates", explanation, before, after)
            changes = True

    return changes


def narrow_all_cells(sudoku):
    changes = False
    for cell in sudoku.cells.values():
        if narrow_cell_candidates(cell, sudoku):
            changes = True
            narrow_all_cells(sudoku)
    return changes


@repeat_until_no_change
def naked_single(sudoku):
    """If only one possibility within the group : the cell gets the value"""
    changes = False

    for i in range(1, 10):
        for j in range(1, 10):
            cells = [c for c in sudoku.rows[i] if j in c.candidates]
            if len(cells) == 1:
                cells[0].assign_value(j)
        for k in range(1, 10):
            cells = [c for c in sudoku.rows[i] if k in c.candidates]
            if len(cells) == 1:
                cells[0].assign_value(k)
        for l in range(1, 10):
            cells = [c for c in sudoku.rows[i] if l in c.candidates]
            if len(cells) == 1:
                cells[0].assign_value(l)

    return changes


if __name__ == "__main__":

    from main import parse_sudokus
    from classes import Cell, Sudoku

    sudoku = parse_sudokus()
    s = Sudoku(sudoku["Sudoku 1 : Difficulty 3"])
    print(s)
    narrow_all_cells(s)
    print(naked_single(s))
