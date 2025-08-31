from logger import log_change


def phistomefel_ring(sudoku):
    """TO BE IMPLEMENTED : https://www.youtube.com/watch?v=iAiUOTNUIGY"""

    changes = False
    ring_coords = [
        (3, 3),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (4, 7),
        (5, 7),
        (6, 7),
        (7, 7),
        (7, 6),
        (7, 5),
        (7, 4),
        (7, 3),
        (6, 3),
        (5, 3),
        (4, 3),
    ]

    squares_coords = [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (1, 8),
        (1, 9),
        (2, 8),
        (2, 9),
        (8, 1),
        (8, 2),
        (9, 1),
        (9, 2),
        (8, 8),
        (8, 9),
        (9, 8),
        (9, 9),
    ]

    ring_values = [
        sudoku.cells[i].value for i in ring_coords if sudoku.cells[i].value is not None
    ]
    squares_values = [
        sudoku.cells[i].value
        for i in squares_coords
        if sudoku.cells[i].value is not None
    ]


if __name__ == "__main__":
    from main import parse_sudokus
    from classes import Cell, Sudoku

    sudokus_dictionary = parse_sudokus()

    sudoku = sudokus_dictionary["Sudoku 1 : Difficulty 3"]

    s = Sudoku(sudoku)
    print(s)

    print(phistomefel_ring(s))
