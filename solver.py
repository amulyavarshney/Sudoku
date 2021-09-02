def find_empty_square(grid):
    """
    Function to Find the entry in the Grid that is still not used

    Args:
        grid (List[List[int]]): A partially filled grid.

    Returns:
        tuple(int, int): the empty position
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # if unassigned entry found,
            if grid[i][j] == 0:
                return (i, j)  # returns (row, col)
    return None


def isValid(grid, row, col, num) -> bool:
    """
    Checks whether it is valid to assign num to given row and column

    Args:
        grid (List[List[int]]): A partially filled grid.
        row (int): row number of current position
        col (int): column number of current position
        num (int): A digit between 1 to 9 (inclusive)

    Returns:
        bool: True if valid else False
    """
    # Check if num is already placed in current column
    for i in range(len(grid)):
        if grid[i][col] == num and row != i:
            return False
            
    # Check if num is already placed in current row
    for j in range(len(grid[0])):
        if grid[row][j] == num and col != j:
            return False

    # Check if num is already placed in current box
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if grid[i][j] == num and (i,j) != (row, col):
                return False

    # if not placed already
    return True


def solve(grid) -> bool:
    """
    A recursive function that takes a partially completed grid and 
    try to assign values to all unassigned spots in order to fulfil 
    the Sudoku criteria (no duplicates across rows, columns and boxes)
    Args:
        grid (List[List[int]]): A partially filled grid.

    Returns:
        bool: True if Sudoku solved successfully else False
    """
    loc = find_empty_square(grid)

    # If there is no unassigned location, we are done
    if not loc:
        return True
    else:
        # Assigning loc values to row and col
        row, col = loc

    # consider digits 1 to 9
    for num in range(1,10):
        # Checks whether it looks promising to assign 
        # num to the given row, col
        if isValid(grid, row, col, num):
            # tenative assignment of num
            grid[row][col] = num
            # if solved, return True
            if solve(grid):
                return True
            # if fails, undo the assignment
            grid[row][col] = 0

    # triggers backtracking
    return False


def print_grid(grid):
    """
    A utility function to print the grid.

    Args:
        grid (List[List[int]]): A partially filled grid.
    """
    for i in range(len(grid)):
        if i%3 == 0 and i != 0:
            print("--------------------------")
        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")