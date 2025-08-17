from classes import Sudoku, Cell


def repeat_until_stable(technique):
    """
    Decorator : applies a technique until there are no changes
    """

    def wrapper(sudoku):
        progress = True
        while progress:
            progress = technique(
                sudoku
            )  # if there is any change, the technique returns True
        return sudoku

    return wrapper


# @repeat_until_stable
def naked_single(sudoku):
    """Reduce candidates based on the values already in line/col/square"""
    progress = False

    for cell in sudoku.cells.values():
        if cell.value is None:
            row_values = sudoku.get_row_values(cell.row)
            col_values = sudoku.get_col_values(cell.col)
            square_values = sudoku.get_square_values(cell.square)

            before = set(cell.candidates)

            for group in [row_values, col_values, square_values]:
                for value in group:
                    if cell.discard_candidate(value):
                        progress = True

    return progress


# @repeat_until_stable
def naked_pairs_triples(sudoku):
    """If a n_length cell.candidates is found somewhere else in row/col/square
    n times = erase those candidates for the other cells within the group"""

    progress = False

    for cell in sudoku.cells.values():

        if cell.value is not None:
            continue

        ref = cell.candidates

        group_candidates = [
            sudoku.get_row_candidates(cell.row),
            sudoku.get_col_candidates(cell.col),
            sudoku.get_square_candidates(cell.square),
        ]

        identical_candidates_number = [group.count(ref) for group in group_candidates]

        row_col_square_cells = [
            sudoku.get_row(cell.row),
            sudoku.get_col(cell.col),
            sudoku.get_square(cell.square),
        ]

        for i, group in enumerate(group_candidates):
            if identical_candidates_number[i] > 1 and identical_candidates_number[
                i
            ] == len(ref):
                for c in row_col_square_cells[i]:
                    if c.candidates != ref:
                        for value in ref:
                            if c.discard_candidate(value):
                                progress = True

    return progress
