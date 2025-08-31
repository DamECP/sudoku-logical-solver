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

    if cell.value is None:

        peers = cell.get_peers(sudoku)
        all_values = [i.value for i in peers if i.value is not None]

        before = f"Before candidates = {sorted(cell.candidates)}"
        explanation = f"Values around = {sorted(all_values)}"

        if cell.discard_candidates(all_values, sudoku):

            after = f"After candidates = {sorted(cell.candidates)   }"
            log_change(cell, "narrow_candidates", explanation, before, after)
            changes = True

    return changes


@repeat_until_no_change
def narrow_all_cells(sudoku):
    changes = False
    for cell in sudoku.cells.values():
        if narrow_cell_candidates(cell, sudoku):
            changes = True
    return changes


@repeat_until_no_change
def naked_single(sudoku):
    """If only one possibility within the group : the cell gets the value"""
    changes = False

    groups = [sudoku.rows, sudoku.cols, sudoku.squares]

    for group in groups:
        for i in range(1, 10):
            for j in range(1, 10):
                cells = [c for c in group[i] if j in c.candidates]
                before = f"unique value = {j}\ncandidates around = {[c.candidates for c in group[i] if c.value is None]}"
                # if value j appears only once within the group
                if len(cells) == 1:
                    # then assign it to the cell
                    cell = next(iter(cells))
                    explanation = f"only one cell can get {j} as value : {cell.coord}"
                    cell.assign_value(j, sudoku)
                    after = f"new value for cell {cell.coord} : {cell}\nupdated candidates = {[c.candidates for c in group[i] if c.value is None]}"
                    log_change(cell, "naked single", explanation, before, after)
                    changes = True

    return changes


@repeat_until_no_change
def naked_pairs(sudoku):
    changes = False
    groups = [sudoku.rows, sudoku.cols, sudoku.squares]

    for group in groups:
        for i in range(1, 10):
            pairs = [
                c.candidates
                for c in group[i]
                if c.value is None and len(c.candidates) == 2
            ]

            if len(pairs) > 1:

                # build a counter object to get pairs that appear twice
                counter = Counter(map(frozenset, pairs))
                # list of duplicates
                duplicates = [set(pair) for pair, count in counter.items() if count > 1]

                for dup in duplicates:
                    for cell in group[i]:
                        if cell.candidates != dup:
                            if cell.discard_candidates(dup, sudoku):
                                changes = True
    return changes


if __name__ == "__main__":

    from main import parse_sudokus
    from classes import Cell, Sudoku

    sudoku = parse_sudokus()
    s = Sudoku(sudoku["Sudoku 1 : Difficulty 3"])
    print(s)

    narrow_all_cells(s)
    naked_single(s)

    print(s)
