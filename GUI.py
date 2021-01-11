import pygame
import time
pygame.font.init()

class Grid:
    board = [
        [7,5,3,0,9,0,4,8,2],
        [0,1,8,7,0,0,0,0,0],
        [4,0,0,8,0,0,0,0,1],
        [0,6,0,0,0,8,0,0,0],
        [1,0,0,4,0,0,3,0,0],
        [0,7,0,0,0,0,8,2,9],
        [0,2,0,0,1,0,0,0,0],
        [0,0,0,9,0,4,2,7,0],
        [6,0,0,0,5,0,1,0,0]
        ]

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.window = window
        self.selected = None
        self.model = None
        self.squares = [[Square(i, j, width, height, self.board[i][j]) for j in range(9)] for i in range(9)]
        self.update_grid()

    def update_grid(self):
        self.model = [[self.squares[i][j].value for j in range(9)] for i in range(9)]

    def place_number(self, notes):
        for i in range(9):
            if notes[i] != 0:
                value = notes[i]
        row, col = self.selected

        if self.squares[row][col].value == 0:
            self.squares[row][col].set_value(value)
            self.update_grid()

            if validMove(self.model, (row, col), value) and self.solve():
                return True
            else:
                self.squares[row][col].set_value(0)
                self.squares[row][col].add_note(value)
                self.update_grid()
                return False

    def sketch_notes(self, val):
        row, col = self.selected
        self.squares[row][col].add_note(val)

    def draw(self):
        gap = self.width / 9

        for i in range(0, 10):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            #horizontal lines
            pygame.draw.line(self.window, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            #vertical lines
            pygame.draw.line(self.window, (0,0,0), (i * gap, 0), (i * gap, self.height), thick)

        #Draw Cubes
        for i in range(9):
            for j in range(9):
                self.squares[i][j].draw(self.window)

    def select_cube(self, row, col):
        for i in range(9):
            for j in range(9):
                self.squares[i][j].selected = False
        self.squares[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos):
        row, col = pos[0], pos[1]

        if row < self.width and col < self.height:
            gap = self.width / 9
            y = row // gap
            x = col // gap
            return (int(x),int(y))
        else:
            return False

    def solved(self):
        for i in range(9):
            for j in range(9):
                if self.squares[i][j].value == 0:
                    return False
        return True

    def solve(self):
        location = findEmptySpace(self.model)
        if location:
            row, col = location
        else:
            return True

        for i in range(1,10):
            if validMove(self.model, (row,col), i):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False


    # very similar to the textual solving method just draws green and red squares
    # around correct iterations of the board

    # this function takes a while because of the visual delay on the board
    # however, if the delay is removed the board can be solved in seconds
    # or you can try out the textual version which prints out the final
    # solution as a string to the console
    def solve_gui(self):
        self.update_grid()
        location = findEmptySpace(self.model)
        if location:
            row, col = location
        else:
            return True

        for i in range(1, 10):
            if validMove(self.model, (row, col), i):
                self.model[row][col] = i
                self.squares[row][col].set_value(i)
                self.squares[row][col].draw_change(self.window, True)
                self.update_grid()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.squares[row][col].set_value(0)
                self.update_grid()
                self.squares[row][col].draw_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def select_all_cubes_with_num(self, value):
        for i in range(9):
            for j in range(9):
                if self.squares[i][j].value == value:
                    self.squares[i][j].selected = True


class Square:
    def __init__(self, row, col, width, height, value):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.value = value
        self.notes = [0]*9
        self.selected = False

    def draw(self, window):
        font = pygame.font.SysFont("Arial", 45)
        fnt = pygame.font.SysFont("Arial", 20)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.only_one() >= 1 and self.value == 0:
            note = ""
            for i in range(3):
                if self.notes[i] != 0:
                    note = note + str(self.notes[i]) + " "
                else:
                    note += "   "
            notes = note[:-1]
            text = fnt.render(notes, 1, (128,128,128))
            window.blit(text, (x+5, y+5))

            note2 = ""
            for i in range(3,6):
                if self.notes[i] != 0:
                    note2 = note2 + str(self.notes[i]) + " "
                else:
                    note2 += "   "
            notes2 = note2[:-1]
            text = fnt.render(notes2, 1, (128,128,128))
            window.blit(text, (x+5, y+25))

            note3 = ""
            for i in range(6,9):
                if self.notes[i] != 0:
                    note3 = note3 + str(self.notes[i]) + " "
                else:
                    note3 += "   "
            notes3 = note3[:-1]
            text = fnt.render(notes3, 1, (128,128,128))
            window.blit(text, (x+5, y+45))

        elif self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, window, correct = True):
        font = pygame.font.SysFont("Arial", 45)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(window, (255, 255, 255), (x, y, gap, gap), 0)

        text = font.render(str(self.value), 1, (0, 0, 0))
        window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if correct:
            pygame.draw.rect(window, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 3)

    def set_value(self, value):
        self.value = value

    def add_note(self, val):
        if self.notes[val-1] != 0:
            self.notes[val-1] = 0
        else:
            self.notes[val-1] = val

        return

    def only_one(self):
        cnt = 0
        for i in range(9):
            if self.notes[i] != 0:
                cnt += 1
        return cnt


def validMove(board, pos, num):
    row, col = pos
    for i in range(0,9):
        if board[row][i] == num and pos[1] != i:
            return False
    for i in range(0,9):
        if board[i][col] == num and pos[0] != i:
            return False

    x = col//3
    y = row//3

    for i in range(y*3, y*3 + 3):
        for j in range(x*3, x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True

def findEmptySpace(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i, j
    return False

def redraw_window(window, board, seconds, mistakes):
    window.fill((255,255,255))
    font = pygame.font.SysFont("Arial", 45)

    text = font.render("Time: " + format_time(seconds), 1, (0,0,0))
    window.blit(text, (630 - 220, 640))

    text = font.render("X " * mistakes, 1, (255, 0, 0))
    window.blit(text, (20, 640))
    board.draw()
    pygame.display.update()

def format_time(seconds):
    sec = seconds % 60
    minutes = seconds // 60
    mat = ""
    if sec < 10:
        mat = str(minutes) + ":0" + str(sec)
    else:
        mat = str(minutes) + ":" + str(sec)
    return mat

def main():
    window = pygame.display.set_mode((630,690))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 630, 630, window)
    key = None
    run = True
    start = time.time()
    mistakes = 0

    while run:
        time_played_so_far = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9

                if event.key == pygame.K_RETURN:
                    row, col = board.selected

                    # Makes sure there's only one note in the selected square
                    # so the user can place that number down
                    if board.squares[row][col].only_one() == 1:
                        if board.place_number(board.squares[row][col].notes):
                            print("Success")
                            board.select_all_cubes_with_num(board.squares[row][col].value)
                            board.update_grid()
                        else:
                            print("Wrong")
                            mistakes += 1
                            if mistakes == 3:
                                print("You lost the game")
                                font = pygame.font.SysFont("comicsans", 40)
                                text = font.render("You lost the game", 1, (255, 0, 0))
                                window.blit(text, (window.get_width() /2 - text.get_width() / 2 - 40, 640))
                                pygame.display.update()
                                pygame.time.delay(5000)
                                pygame.quit()
                        key = None

                        if board.solved():
                            print("Congrats you did it!")
                            font = pygame.font.SysFont("comicsans", 40)
                            text = font.render("You Won!!", 1, (0, 255, 0))
                            redraw_window(window, board, time_played_so_far, mistakes)
                            window.blit(text, (window.get_width() /2 - text.get_width() / 2 - 40, 640))
                            pygame.time.delay(5000)
                            pygame.quit()

                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                    print(time.time() - start)
                    run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_valid_spot = board.click(pos)

                if clicked_valid_spot:
                    board.select_cube(clicked_valid_spot[0], clicked_valid_spot[1])
                    if board.squares[clicked_valid_spot[0]][clicked_valid_spot[1]].value != 0:
                        board.select_all_cubes_with_num(board.squares[clicked_valid_spot[0]][clicked_valid_spot[1]].value)
                    key = None

        if board.selected and (key is not None):
            board.sketch_notes(key)
            key = None

        redraw_window(window, board, time_played_so_far, mistakes)

main()
pygame.quit()
