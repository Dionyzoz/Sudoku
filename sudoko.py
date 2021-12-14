import time
import sys
import itertools as it
# grids = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
solutions = []
total = 0
col_ = 0
row_ = 0
_flush = True
sys.stdout.write("\033[?25l")
sys.stdout.flush()
std = False

color_gen = it.cycle([
    "0;32m",
    "0;33m",
    "0;34m",
    "0;35m",
    "0;36m"]
)

art = ["   _____           _       _            _",
       "  / ____|         | |     | |          | |",
       " | (___  _   _  __| | ___ | | ___   _  | |",
       r"  \___ \| | | |/ _` |/ _ \| |/ / | | | | |",
       "  ____) | |_| | (_| | (_) |   <| |_| | |_|",
       r" |_____/ \__,_|\__,_|\___/|_|\_\\__,_| (_)", ]

try:
    speed = sys.argv[1]
    if "-i" in sys.argv:
        std = True

except IndexError:
    speed = "-f"
    print("Choosing default speed fast because no speed flag was set")
    print("Select one flag out of:")
    print("-s 'Slow speed' shows how the algorithm really functions")
    print("-f 'Fast speed' for a fast and satisfying completion")
    print("-u 'Ultra speed' the fastest your cpu can handle")
    print("\n\n")
    sys.stdout.flush()
    time.sleep(2)

ultra = False
if speed == "-u":
    ultra = True

elif speed == "-s":
    timeStop = 0.3

elif speed == "-f":
    timeStop = 0.001
    # TODO add arguments for slow speed, fast speed, and ultra

else:
    print("Invalid speed argument")
    sys.exit()


try:
    try:
        if std:
            raise FileNotFoundError
        sudoku = open("p096_sudoku.txt", "r")

    except FileNotFoundError:
        sudoku = sys.stdin

    finally:
        puzzles = []
        indexPuzzle = -1
        while True:
            line = sudoku.readline()

            if line == "":
                break

            elif "Grid" in line:
                indexPuzzle += 1
                puzzles.append([])
            else:
                puzzles[indexPuzzle].append([
                    int(i) for i in list(line)[0:9]])

        sudoku.close()

    def overwrite(puzzle: list, final: bool = False, row: int = 0, col: int = 0):
        global col_
        global row_
        # globals are _col and _row these indicate where the last cursor was

        if final is True:
            color = next(color_gen)
            temp = 0
            for i in range(8, -1, -1):
                if temp == 0:
                    print("\r", end="")
                else:
                    print("\r\033[%dA" % temp, end="")
                temp = 2
                for j in range(9):
                    print(f"\033[{color}{puzzle[i][j]}", end="   ")
                    sys.stdout.flush()
                    time.sleep(.01)

            for i in range(16):
                if 11 >= i >= 6:
                    print(f"\033[34C{art[i - 6]}")
                else:
                    print("")
                print("\r", end="")

            time.sleep(.25)
        else:
            # UP all the way is 16
            temp = 2 * (8 - row)
            if temp != 0:
                print("\r\033[%dA" % temp, end="", flush=_flush)
            # underscores are global
            if row_ > row or (col_ > col and row == row_):
                diff = row_ - row
                if diff != 0:
                    if col_ != 0:
                        print("\033[0m\033[%dC\033[%dB" %
                              (col_ * 4, diff * 2), end="", flush=_flush)
                    else:
                        print("\r\033[0m\033[%dB" %
                              (diff * 2), end="", flush=_flush)
                    while row_ > row:
                        # _col decrease until row decrease
                        time.sleep(timeStop)
                        print(f"\033[0m{puzzle[row_][col_]}",
                              end="", flush=_flush)
                        print("\033[5D", end="", flush=_flush)
                        col_ -= 1
                        if col_ == -1:
                            print("\033[2A\033[1D", end="", flush=_flush)
                            row_ -= 1
                            col_ = 8
                            print("\r", end="", flush=_flush)
                            print(f"\033[{col_ * 4}C", end="", flush=_flush)
                print("\r", end="", flush=_flush)
                print(f"\033[{col_ * 4}C", end="", flush=_flush)
                while col_ > col:
                    time.sleep(timeStop)
                    print(f"\033[0m{puzzle[row_][col_]}", end="", flush=_flush)
                    print("\033[5D", end="", flush=_flush)
                    col_ -= 1

                print(f"\033[0;31m{puzzle[row][col]}", end="", flush=_flush)
                col_ = col
            else:
                shift = 4 * (col)
                time.sleep(timeStop)
                if shift != 0:
                    print("\033[%dC" % shift, end="", flush=_flush)

                print(f"\033[0;31m{puzzle[row][col]}", end="", flush=_flush)
                col_ = col
                row_ = row
            for _ in range(temp):
                print("\033[1C \n", end="", flush=_flush)
            if temp == 0:
                print("\r", end="", flush=_flush)
        # sys.stdout.flush()

    def recursive(_possible: list = [], index=0):
        # first find possiblities
        # then loop through all of them
        # finally find if the row index = 8 because that means it is complete
        # row = []
        if index == 9:
            overwrite(_possible, True)
            raise GeneratorExit

        def createRows(_col=0, possible=[]):
            # col can be any value as long as it is not in col limits row limits or grid limits
            # pos = possible.copy()
            if possible[index][_col] == 0:
                rowLimitations = [i for i in range(
                    1, 10) if i in possible[index]]

                colLimitations = []
                gridLimits = []
                for i in range(9):
                    if possible[i][_col] != 0:
                        colLimitations.append(possible[i][_col])

                # check for limitations within the grid
                if index in (0, 1, 2):
                    if _col in (0, 1, 2):
                        for i in (0, 1, 2):
                            for j in (0, 1, 2):
                                gridLimits.append(possible[i][j])

                    elif _col in (3, 4, 5):
                        for i in (0, 1, 2):
                            for j in (3, 4, 5):
                                gridLimits.append(possible[i][j])

                    elif _col in (6, 7, 8):
                        for i in (0, 1, 2):
                            for j in (6, 7, 8):
                                gridLimits.append(possible[i][j])

                elif index in (3, 4, 5):

                    if _col in (0, 1, 2):
                        for i in (3, 4, 5):
                            for j in (0, 1, 2):
                                gridLimits.append(possible[i][j])

                    elif _col in (3, 4, 5):
                        for i in (3, 4, 5):
                            for j in (3, 4, 5):
                                gridLimits.append(possible[i][j])

                    elif _col in (6, 7, 8):
                        for i in (3, 4, 5):
                            for j in (6, 7, 8):
                                gridLimits.append(possible[i][j])

                elif index in (6, 7, 8):

                    if _col in (0, 1, 2):
                        for i in (6, 7, 8):
                            for j in (0, 1, 2):
                                gridLimits.append(possible[i][j])

                    elif _col in (3, 4, 5):
                        for i in (6, 7, 8):
                            for j in (3, 4, 5):
                                gridLimits.append(possible[i][j])

                    elif _col in (6, 7, 8):
                        for i in (6, 7, 8):
                            for j in (6, 7, 8):
                                gridLimits.append(possible[i][j])

                # now you have all the limits .... gridlimits, rowlimits, collimits
                for i in range(1, 10):
                    if i not in gridLimits and i not in rowLimitations and i not in colLimitations:
                        possible[index][_col] = i
                        if ultra is not True:
                            overwrite(possible, final=False,
                                      row=index, col=_col)
                        if _col != 8:
                            x = createRows(_col + 1, [row[:]
                                                      for row in possible])
                            if x is not None:
                                return x
                        else:
                            y = recursive([row[:]
                                           for row in possible], index + 1)
                            if y is not None:
                                return y

                return None

            if _col != 8:
                a = createRows(_col + 1, [row[:] for row in possible])
                return a
            else:
                b = recursive([row[:] for row in possible], index + 1)
                return b

        createRows(possible=[row[:] for row in _possible])

    # for i in puzzles:
    for i, currentPuzzle in enumerate(puzzles):
        for x in range(0, 9):
            print("\n", flush=_flush)
            for j in range(0, 9):
                print(f"\033[0m{puzzles[i][x][j]}", end="   ", flush=_flush)
        print("\n\n\n\n", end="", flush=_flush)
        print("\033[4A", end="", flush=_flush)
        try:
            recursive(_possible=[row[:] for row in currentPuzzle])
        except GeneratorExit:
            print("\n\n")
            time.sleep(.1)
            _col = 0
            _row = 0
            i = 0

    sys.stdout.write("\033[?25h")

except KeyboardInterrupt:
    sys.stdout.write("\033[?25h")
    sys.exit(0)
