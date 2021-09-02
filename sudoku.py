from random import shuffle
from copy import deepcopy
N = 9


class Generator:
    def __init__(self):
        self.counter = 0
        self.grid = [[0 for i in range(N)] for j in range(N)]
        self.generate_sudoku()
        self.solution()

    def generate_sudoku(self):
        """
        generates and solves Sudoku puzzles using a backtracking algorithm.
        """
        self.generate_solution(self.grid)
        self.solved = deepcopy(self.grid)
        self.remove_numbers_from_grid()
        return None

    def solution(self):
        """
        Returns:
            list(list(int)): the solution of sudoku puzzle.
        """
        return self.solved

    def test_sudoku(self, grid):
        """Tests each square to make sure it is a valid puzzle

        Args:
            grid (List[List[int]]): A partially filled grid.

        Returns:
            bool: Returns True if puzzle is valid else False
        """
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                num = grid[row][col]
                # remove number from grid to test if it's valid
                grid[row][col] = 0
                if not self.isValid(grid, row, col, num):
                    return False
                else:
                    # put number back in grid
                    grid[row][col] = num
        return True

    def isValid(self, grid, row, col, num) -> bool:
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
                if grid[i][j] == num and (i, j) != (row, col):
                    return False

        # if not placed already
        return True

    def find_empty_square(self, grid):
        """return the next empty square coordinates in the grid

        Args:
            grid (List[List[int]]): A partially filled grid.

        Returns:
            pos: index of next empty square
        """
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def solve_sudoku(self, grid):
        """
        solve the sudoku puzzle with backtracking.

        Args:
            grid (List[List[int]]): A partially filled grid.

        Returns:
            bool: Returns True if solved else False
        """
        for i in range(0, 9**2):
            row = i // 9
            col = i % 9
            # find next empty cell
            if grid[row][col] == 0:
                for num in range(1, 10):
                    # check that the number hasn't been used in the row/col/subgrid
                    if self.isValid(grid, row, col, num):
                        grid[row][col] = num
                        if not self.find_empty_square(grid):
                            self.counter += 1
                            break
                        else:
                            if self.solve_sudoku(grid):
                                return True
                break
        grid[row][col] = 0
        return False

    def generate_solution(self, grid):
        """
        Generate a solution of Sudoku using Backtracking

        Args:
            grid (List[List[int]]): A partially filled grid.

        Returns:
            bool: True if there are no more empty squares else False.
        """
        # list of valid digits
        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # check empty space in each square
        for i in range(0, 9**2):
            row = i // 9
            col = i % 9
            # if cell is empty
            if grid[row][col] == 0:
                shuffle(num_list)
                for num in num_list:
                    if self.isValid(grid, row, col, num):
                        grid[row][col] = num
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_solution(grid):
                                # if the grid is full
                                return True
                break
        grid[row][col] = 0
        return False

    def get_non_empty_squares(self, grid):
        """
        Get non-empty squares in the puzzle

        Args:
            grid (List[List[int]]): A partially filled grid.

        Returns:
            List(int): Returns a shuffled list of non-empty squares in the puzzle
        """
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != 0:
                    non_empty_squares.append((i, j))
        shuffle(non_empty_squares)
        return non_empty_squares

    def remove_numbers_from_grid(self):
        """
        Removing numbers one at a time to create the puzzle and ensure that 
        the solution is unique.
        Steps:
        1. Remove a random non-empty square.
        2. Solve the new grid with backtracking, but count the solutions and 
        make sure there is only one unique solution.
        3. If there is only one solution, then continue on and remove another 
        empty square and repeat the process, or if there is more than one 
        solution, put the number back in the grid and either try again removing 
        more squares, or stop and keep the generated puzzle.
        """
        # get all non-empty squares from the grid
        non_empty_squares = self.get_non_empty_squares(self.grid)
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3
        while rounds > 0 and non_empty_squares_count >= 17:
            # there should be at least 17 clues
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1

            # might need to put the square value back if there is more than one solution
            num = self.grid[row][col]
            self.grid[row][col] = 0

            # make a copy of the grid to solve
            grid_copy = deepcopy(self.grid)

            # initialize solutions counter to zero
            self.counter = 0
            self.solve_sudoku(grid_copy)

            # if there is more than one solution, put the last removed cell back into the grid
            if self.counter != 1:
                self.grid[row][col] = num
                non_empty_squares_count += 1
                rounds -= 1

    def print_grid(self, grid):
        """
        A utility function to print the grid.

        Args:
            grid (List[List[int]]): A partially filled grid.
        """
        for i in range(len(grid)):
            if i % 3 == 0 and i != 0:
                print("--------------------------")
            for j in range(len(grid[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(grid[i][j])
                else:
                    print(str(grid[i][j]) + " ", end="")


# if __name__ == '__main__':
#     sudoku = Generator()
#     sudoku.print_grid(sudoku.grid)
#     print('\n')
#     sudoku.print_grid(sudoku.solved)