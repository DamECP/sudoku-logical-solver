from classes import Sudoku
from techniques import naked_single, naked_pairs_triples, hidden_pairs_triples


def parse_sudokus():
    with open("sudokus.txt", "r") as sudo:
        sudoku_examples = [line.strip() for line in sudo.readlines()]

        sudoku_dictionnary = {}
        for index, line in enumerate(sudoku_examples):
            if line.startswith("Sudoku"):
                key = line
                sudoku = sudoku_examples[index + 1 : index + 10]
                sudoku_dictionnary[key] = sudoku

        return sudoku_dictionnary


def resolve(sudoku):

    techniques = [naked_single, naked_pairs_triples, hidden_pairs_triples]

    progress = True
    while progress:
        progress = False
        for i in range(len(techniques)):
            result = techniques[i](sudoku)
            if result:
                progress = True


if __name__ == "__main__":

    sudokus = parse_sudokus()

    for name, grid in sudokus.items():
        s = Sudoku(grid)

        print(name)
        print(s)
        print()

        resolve(s)

        print("Solution")
        print(s)

        print()
        print()
