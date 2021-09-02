import pygame as pg
import sudoku
from solver import isValid, solve
import time
pg.font.init()


class Grid:
    sudoku_game = sudoku.Generator()
    grid = sudoku_game.grid

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.grid[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if isValid(self.model, row, col, val) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        """
        To draw grid Lines and cubes.

        Args:
            win ([type]): [description]
        """
        # draw grid lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pg.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        get position where mouse is clicked 

        Args:
            pos(int, int): coordinates where mouse clicked

        Returns:
            tuple(int, int): (row, col) square where mouse is clicked
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pg.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pg.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, grid, time, strikes):
    win.fill((255,255,255))
    
    font = pg.font.SysFont("comicsans", 40)
    # Draw Strikes
    text = font.render(f"Penalty: {strikes}", 1, (0, 0, 0))
    win.blit(text, (540 - 170, 560))
    # Draw time
    text = font.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (20, 560))
    # Draw grid and grid
    grid.draw(win)


def format_time(secs):
    """

    Args:
        secs (int): number of seconds passed

    Returns:
        string: current time in HH:MM:SS format.
    """
    seconds = secs % 60
    minutes = secs // 60
    hours = minutes // 60
    return f"{str(hours)}:{str(minutes)}:{str(seconds)}"


def main():
    win = pg.display.set_mode((540,600))
    pg.display.set_caption("SUDOKU")
    grid = Grid(9, 9, 540, 540)
    key = None
    gameExit = False
    gameMove = True
    startTime = time.time()
    strikes = 0
    grid.select(0, 0)
    x, y = 0, 0
    while not gameExit:
        play_time = round(time.time() - startTime)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameExit = True
            
            if event.type == pg.KEYDOWN:
                update_x, update_y = 0, 0
                if event.key == pg.K_UP:
                    update_x, update_y, gameMove = -1, 0, False
                elif event.key == pg.K_DOWN:
                    update_x, update_y, gameMove = 1, 0, False
                elif event.key == pg.K_LEFT:
                    update_x, update_y, gameMove = 0, -1, False
                elif event.key == pg.K_RIGHT:
                    update_x, update_y, gameMove = 0, 1, False
                x, y = x + update_x, y + update_y
                if 0<=x<9 and 0<=y<9:
                    grid.select(x, y)
                else:
                    x, y = x - update_x, y - update_y
                key = None

            if gameMove and event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                if event.key == pg.K_DELETE:
                    grid.clear()
                    key = None
                if event.key == pg.K_RETURN:
                    i, j = grid.selected
                    if grid.cubes[i][j].temp != 0:
                        if grid.place(grid.cubes[i][j].temp):
                            # print("Success")
                            pass
                        else:
                            # print("Wrong")
                            strikes += 1
                        key = None

                        if grid.is_finished():
                            # print("Game Over")
                            gameExit = True

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    x, y = clicked
                    grid.select(x, y)
                    key = None

        if gameMove and grid.selected and key != None:
            grid.sketch(key)
        else:
            gameMove = True

        redraw_window(win, grid, play_time, strikes)
        pg.display.update()

main()
pg.quit()
