import random

def get_blocks(line):
    # return list of lengths of contiguous blocks of 1's in a list
    blocks = []
    count = 0
    for bit in line:
        if bit == 1:
            count += 1
        elif count > 0:
            blocks.append(count)
            count = 0
    if count > 0:
        blocks.append(count)
    return blocks

def line_error(line, clues):
    """
    Compute an error value for a given row (or column) based on its current binary list `line`
    and the expected clue (a list of integers). The error is 0 when the contiguous blocks
    of 1's exactly match the clues.
    
    Heuristic:
      - For each corresponding block, add |block_length - clue|.
      - For extra blocks (more blocks than clues), add the sum of extra block lengths.
      - For missing blocks (fewer blocks than clues), add the sum of missing clue values.
    """
    blocks = get_blocks(line)
    error = 0
    # compare the common part (minimum number of blocks/clues)
    min_len = min(len(blocks), len(clues))
    for i in range(min_len):
        error += abs(blocks[i] - clues[i])
    # penalty for extra blocks
    if len(blocks) > len(clues):
        error += sum(blocks[len(clues):])
    # penalty for missing blocks
    elif len(blocks) < len(clues):
        error += sum(clues[len(blocks):])
    return error

def get_col(grid, j):
    # return column j from grid as list
    return [row[j] for row in grid]

def total_error(grid, row_clues, col_clues):
    # return sum of errors over all rows and columns
    err = 0
    for i, row in enumerate(grid):
        err += line_error(row, row_clues[i])
    n_cols = len(grid[0])
    for j in range(n_cols):
        err += line_error(get_col(grid, j), col_clues[j])
    return err

def try_flip(grid, i, j, row_clues, col_clues):
    # Compute improvement (error reduction) if we flip pixel (i,j).
    # Returns: improvement = (current error) - (new error) for row i and column j.

    current_row = grid[i]
    current_col = get_col(grid, j)
    curr_err = line_error(current_row, row_clues[i]) + line_error(current_col, col_clues[j])
    
    # Flip the bit temporarily
    grid[i][j] = 1 - grid[i][j]
    new_row = grid[i]
    new_col = get_col(grid, j)
    new_err = line_error(new_row, row_clues[i]) + line_error(new_col, col_clues[j])
    # Restore the bit
    grid[i][j] = 1 - grid[i][j]
    return curr_err - new_err

def random_initial_grid(n_rows, n_cols):
    # return a grid of size n_rows x n_cols with random bits (0 or 1)
    return [[random.randint(0, 1) for _ in range(n_cols)] for _ in range(n_rows)]

def solve_nonogram(row_clues, col_clues, max_iterations=300000, restart_threshold=10000):
    # solve the simplified nonogram using iterative improvement
    # returns grid (list of lists of int: 0 or 1) that satisfies all clues (error==0)
    # if not found within max_iterations, returns best found solution
    
    n_rows = len(row_clues)
    n_cols = len(col_clues)
    grid = random_initial_grid(n_rows, n_cols)
    best_error = total_error(grid, row_clues, col_clues)
    iterations_since_restart = 0
    iteration = 0
    
    while best_error > 0 and iteration < max_iterations:
        # identify rows and columns that are "bad" (non-zero error)
        bad_rows = [i for i in range(n_rows) if line_error(grid[i], row_clues[i]) > 0]
        bad_cols = [j for j in range(n_cols) if line_error(get_col(grid, j), col_clues[j]) > 0]
        if not bad_rows and not bad_cols:
            break  # solution found
        # with 50/50 chance choose row or column, if both exist
        if bad_rows and (not bad_cols or random.random() < 0.5):
            i = random.choice(bad_rows)
            best_improve = -1
            best_j = None
            for j in range(n_cols):
                improve = try_flip(grid, i, j, row_clues, col_clues)
                if improve > best_improve:
                    best_improve = improve
                    best_j = j
                    
            if best_j is None:
                best_j = random.randint(0, n_cols - 1)
            # with small probability (10%) choose a random pixel even if improvement is not positive
            if best_improve <= 0 and random.random() < 0.1:
                best_j = random.randint(0, n_cols - 1)
            grid[i][best_j] = 1 - grid[i][best_j]
        elif bad_cols:
            j = random.choice(bad_cols)
            best_improve = -1
            best_i = None
            for i in range(n_rows):
                improve = try_flip(grid, i, j, row_clues, col_clues)
                if improve > best_improve:
                    best_improve = improve
                    best_i = i

            if best_i is None:
                best_i = random.randint(0, n_rows - 1)
            # with small probability (10%) choose a random pixel even if improvement is not positive
            if best_improve <= 0 and random.random() < 0.1:
                best_i = random.randint(0, n_rows - 1)
            grid[best_i][j] = 1 - grid[best_i][j]
        
        curr_error = total_error(grid, row_clues, col_clues)
        if curr_error < best_error:
            best_error = curr_error
            iterations_since_restart = 0
        else:
            iterations_since_restart += 1
        # Restart if no improvement for a while
        if iterations_since_restart > restart_threshold:
            grid = random_initial_grid(n_rows, n_cols)
            best_error = total_error(grid, row_clues, col_clues)
            iterations_since_restart = 0
        iteration += 1
    return grid


def main():
    with open("zad_input.txt", "r", encoding="utf-8") as read_file:
        lines = [line.strip() for line in read_file if line.strip()]
    
    # first line: dimensions
    dims = lines[0].split()
    n_rows = int(dims[0])
    n_cols = int(dims[1])
    
    # next n_rows lines: row clues
    row_clues = [[int(elem) for elem in lines[i+1].split()] for i in range(n_rows)]
    
    # next n_cols lines: column clues
    col_clues = [[int(elem) for elem in lines[n_rows+1+i].split()] for i in range(n_cols)]
    
    # solve nonogram
    grid = solve_nonogram(row_clues, col_clues, restart_threshold=50*n_rows*n_cols)
    
    with open("zad_output.txt", "w", encoding="utf-8") as write_file:
        for row in grid:
            # Convention: 1 -> '#' (filled), 0 -> '.' (empty)
            line = "".join('#' if cell==1 else '.' for cell in row)
            write_file.write(line + "\n")

if __name__ == "__main__":
    main()