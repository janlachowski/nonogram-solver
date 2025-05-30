def generate_patterns(length, clue):
    """
    Generates all 0/1 sequences of length 'length' whose blocks of ones match 'clue'.
    'clue' is a list of consecutive lengths of 1-blocks.
    """
    patterns = []

    def backtrack(idx_block, pos, current):
        # idx_block: which block we're processing
        # pos: index of the first position where the block can be placed
        if idx_block == len(clue):
            # fill the rest with zeros
            tail = [0] * (length - len(current))
            patterns.append(current + tail)
            return
        block = clue[idx_block]
        # number of remaining blocks after the current one
        m = len(clue) - idx_block - 1
        # minimum space needed after the current block: sum of remaining + min. separators (m zeros)
        sum_remaining = sum(clue[idx_block+1:])
        min_space_after = sum_remaining + m
        # last valid starting position for the current block
        max_start = length - block - min_space_after
        for start in range(pos, max_start + 1):
            # add zeros up to position 'start'
            prefix = current + [0] * (start - len(current))
            # insert block of ones
            block_seg = prefix + [1] * block
            # if there are more blocks, leave 1 zero as a separator
            next_pos = len(block_seg) + (1 if m > 0 else 0)
            next_current = block_seg + ([0] if m > 0 else [])
            backtrack(idx_block + 1, next_pos, next_current)

    backtrack(0, 0, [])
    # filter patterns to match exactly the desired 'length'
    return [p for p in patterns if len(p) == length]

def propagate(grid, row_patterns, col_patterns, rows, cols):
    """
    Propagates certain assignments by filtering patterns
    and detecting consistent values. Returns False if conflicts are found.
    """
    changed = True
    while changed:
        changed = False
        # rows
        for i in range(rows):
            valid = [p for p in row_patterns[i]
                     if all(grid[i][j] is None or grid[i][j] == p[j]
                            for j in range(cols))]
            if not valid:
                return False
            row_patterns[i] = valid
            for j in range(cols):
                vals = {p[j] for p in valid}
                if len(vals) == 1 and grid[i][j] is None:
                    grid[i][j] = vals.pop()
                    changed = True
        # columns
        for j in range(cols):
            valid = [p for p in col_patterns[j]
                     if all(grid[i][j] is None or grid[i][j] == p[i]
                            for i in range(rows))]
            if not valid:
                return False
            col_patterns[j] = valid
            for i in range(rows):
                vals = {p[i] for p in valid}
                if len(vals) == 1 and grid[i][j] is None:
                    grid[i][j] = vals.pop()
                    changed = True
    return True

def solve(rows, cols, row_specs, col_specs):
    # None = unknown, 0 = empty, 1 = filled
    grid = [[None] * cols for _ in range(rows)]
    row_patterns = [generate_patterns(cols, clue) for clue in row_specs]
    col_patterns = [generate_patterns(rows, clue) for clue in col_specs]
    # initial propagation
    if not propagate(grid, row_patterns, col_patterns, rows, cols):
        return None

    def backtrack(grid, row_patterns, col_patterns):
        # is the solution complete?
        if all(all(cell is not None for cell in row) for row in grid):
            return grid
        # choose the first unknown cell
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] is None:
                    # try both values
                    for v in (0, 1):
                        g2 = [list(r) for r in grid]
                        g2[i][j] = v
                        rp2 = [list(pats) for pats in row_patterns]
                        cp2 = [list(pats) for pats in col_patterns]
                        # local filtering
                        rp2[i] = [p for p in rp2[i] if p[j] == v]
                        if not rp2[i]:
                            continue
                        cp2[j] = [p for p in cp2[j] if p[i] == v]
                        if not cp2[j]:
                            continue
                        # propagation
                        if propagate(g2, rp2, cp2, rows, cols):
                            result = backtrack(g2, rp2, cp2)
                            if result is not None:
                                return result
                    return None
        return None

    return backtrack(grid, row_patterns, col_patterns)

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
    grid = solve(n_rows, n_cols, row_clues, col_clues)
    
    with open("zad_output.txt", "w", encoding="utf-8") as write_file:
        for row in grid:
            # Convention: 1 -> '#' (filled), 0 -> '.' (empty)
            line = "".join('#' if cell==1 else '.' for cell in row)
            write_file.write(line + "\n")

if __name__ == "__main__":
    main()