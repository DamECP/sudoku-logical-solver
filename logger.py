import os

logs = []


def log_change(cell, technique, explanation, before, after):
    logs.append(
        f"Changes on cell {cell.coord} : technique = {technique}\n"
        f"{explanation}\n"
        f"{before}\n"
        f"{after}\n"
    )


def save_logs(filename="logs.txt"):
    folder = "solutions"
    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as logfile:

        logfile.write("\n".join(logs))
        logfile.write("\n")


def log_cleaner():
    folder = os.path.join(os.getcwd(), "solutions")
    if not os.path.exists(folder):
        return
    files = os.listdir(folder)
    for f in files:
        if f.startswith("LogSudoku") and f.endswith(".txt"):
            os.remove(os.path.join(folder, f))


log_cleaner()
