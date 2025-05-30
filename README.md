# Nonogram Solvers – AC3 & WalkSAT

This repository contains **two solvers for Nonograms (also known as Picross or Griddlers)**, both of which I implemented as part of a university course on **Artificial Intelligence**:

- `AC3.py`: Solves the puzzle using **AC-3 constraint propagation** and backtracking.
- `WalkSAT.py`: Solves the puzzle using a **local search strategy**, inspired by the **WalkSAT** algorithm and randomized hill climbing.

Both solvers accept the same input and generate output in an identical format.

---

## Input Format

Both programs read the puzzle definition from a file named `zad_input.txt`. The format is:

```
<row-count> <column-count>
<row-clue-1>
<row-clue-2>
...
<row-clue-N>
<column-clue-1>
...
<column-clue-M>
```

Each clue is a space-separated sequence of integers representing lengths of filled blocks.

**Example:**
```
5 5
5
1 1 1
3
2 2
5
2 2
1 3
3 1
1 3
2 2
```

This describes a 5×5 puzzle with clues for each row and column.

---

## Output Format

The solution is written to `zad_output.txt`. Each line represents one row of the nonogram. Symbols used are:

- `#` → filled cell
- `.` → empty cell

📝 **Example output:**
```
#####
#.#.#
.###.
##.##
#####
```

---

## Running the Solvers

To run either program, make sure you have a valid `zad_input.txt` file in the same folder and then run:

```bash
python AC3.py
# or
python WalkSAT.py
```

A solution (if found) will be written to `zad_output.txt`.

---

## Want to Try Solving Yourself?

You can play interactive nonograms online here! 
[https://www.puzzle-nonograms.com/](https://www.puzzle-nonograms.com/)
