from classes import Cell, Sudoku
from techniques import narrow_all_cells, naked_single, naked_pairs
from logger import save_logs


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
    techniques = [narrow_all_cells, naked_single, naked_pairs]
    for title, grid in sudoku.items():
        s = Sudoku(grid)
        changes = True
        print("\n", title, "\n\n")
        print(s, "\n")
        while changes:
            changes = False
            for technique in techniques:
                if technique(s):
                    changes = True

        title = f"Log" + title.replace(" ", "").split(":")[0] + ".txt"
        save_logs(title)
        print(s, "\n")
        print("___________________________________")


if __name__ == "__main__":

    # build the sudoku dict
    sudokus_dictionary = parse_sudokus()

    resolve(sudokus_dictionary)
