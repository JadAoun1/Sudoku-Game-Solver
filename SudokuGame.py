
import pygame
import random
import time
import copy

# Initialize Pygame
pygame.init()
pygame.font.init()

# Color definitions
BACKGROUND_COLOR = (175, 238, 238)
CELL_COLOR = (240, 255, 240)
SELECTED_CELL_COLOR = (124, 252, 0)
HIGHLIGHT_COLOR = (0, 0, 0)
GRID_COLOR = (119, 136, 153)
TEXT_COLOR = (70, 130, 180)
BUTTON_COLOR = (224, 255, 255)
BUTTON_SELECTED_COLOR = (0, 191, 255)
BOX_EDGE_COLOR = (25, 25, 112)
CORRECT_CELL_COLOR = (50, 205, 50)

# Font definitions
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 18)  
MEDIUM_FONT = pygame.font.Font('freesansbold.ttf', 25)  
INSTRUCTIONS_FONT = pygame.font.Font('freesansbold.ttf', 15)

# Grid and Cell sizes
CELL_SIZE = 60
MARGIN = 5
GRID_SIZE = 9
BOX_SIZE = 3

# GUI window initialization
WINDOW_SIZE = (700, 770)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sudoku")

# Button coordinates and sizes
EASY_BUTTON_RECT = pygame.Rect(WINDOW_SIZE[0] - 125, 170, 100, 40)
MEDIUM_BUTTON_RECT = pygame.Rect(WINDOW_SIZE[0] - 125, 220, 100, 40)
HARD_BUTTON_RECT = pygame.Rect(WINDOW_SIZE[0] - 125, 270, 100, 40)

# Sudoku board initialization
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
initial_board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Sudoku game instructions
instructions = [
    "",
    "Sudoku Instructions:",
    "- Fill in the empty cells with numbers from 1 to 9.",
    "- Each number can only appear once in each row, column, and 3x3 box.",
    "",
    "User Inputs:",
    "- Generate a new random Sudoku board by selecting 'R' on your keyboard.",
    "- Select a cell by clicking with your mouse.",
    "- Fill in a selected cell with the corresponding number with your number keys (1 - 9).",
    "- Clear a selected cell by selecting 'Backspace' on your keyboard.",
]

# Game state variables
selected_cell = None  # Holds the coordinates of the selected cell

# Holds the game's time
timer = 0

# Records the start time of the game
start_time = time.time()  

# Counts the number of mistakes made by the player
mistake_counter = 0  

# Difficulty levels
difficulty = 0
EASY = 35
MEDIUM = 25
HARD = 15


def create_solved_board():
    fill_diagonal_box(0, 0)
    fill_diagonal_box(3, 3)
    fill_diagonal_box(6, 6)
    fill_remaining_cells(0, 3)
    return [row[:] for row in board]


def fill_diagonal_box(row, col):
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(num)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = num.pop()


def unUsedInBox(rowStart, colStart, num):
    for i in range(3):
        for j in range(3):
            if board[i + rowStart][j + colStart] == num:
                return False
    return True


def fill_remaining_cells(i, j):
    if j >= 9 and i < 8:
        i = i + 1
        j = 0
    if i >= 9 and j >= 9:
        return True
    if i < 3:
        if j < 3:
            j = 3
    elif i < GRID_SIZE - 3:
        if j == (int)(i / 3) * 3:
            j = j + 3
    else:
        if j == GRID_SIZE - 3:
            i = i + 1
            j = 0
            if i >= 9:
                return True
    for num in range(1, 10):
        if CheckIfSafe(i, j, num):
            board[i][j] = num
            if fill_remaining_cells(i, j + 1):
                return True
            board[i][j] = 0
    return False


def CheckIfSafe(i, j, num):
    return not in_row_col(board, num, i, j) and unUsedInBox(i - i % 3, j - j % 3, num)


def in_row_col(board, num, row, col):
   
    for i in range(9):
        if (board[i][col] == num) or (board[row][i] == num):
            return True
    return False


def generate_board():
    fill_diagonal_box(0, 0)
    fill_diagonal_box(3, 3)
    fill_diagonal_box(6, 6)
    fill_remaining_cells(0, 3)
    remove_numbers(difficulty)


def remove_numbers(difficulty):
    count = 81 - difficulty
    while count > 0:
        cell_id = random.randint(0, 80)
        row = cell_id // 9
        col = cell_id % 9
        if board[row][col] != 0:
            board[row][col] = 0
            count -= 1


def init():
    global selected_cell, board, solved_board, initial_board, mistake_counter, start_time
    selected_cell = None
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    solved_board = create_solved_board()  
    initial_board = [row[:] for row in solved_board]  
    remove_numbers(difficulty)  
    mistake_counter = 0  
    start_time = time.time()


def highlight_error(row, col):
    if (row, col) != selected_cell and board[row][col] != initial_board[row][col]:
        if not is_valid_move(row, col, board[row][col]):
            cell_x = col * CELL_SIZE + MARGIN
            cell_y = row * CELL_SIZE + MARGIN
            pygame.draw.rect(window, (255, 0, 0), (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 3)
    elif (row, col) != selected_cell and board[row][col] != 0:
        if not is_valid_move(row, col, board[row][col]):
            cell_x = col * CELL_SIZE + MARGIN
            cell_y = row * CELL_SIZE + MARGIN
            pygame.draw.rect(window, (255, 0, 0), (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 3)


def draw_board():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_x = col * CELL_SIZE + MARGIN
            cell_y = row * CELL_SIZE + MARGIN


            if selected_cell == (row, col):
                pygame.draw.rect(window,SELECTED_CELL_COLOR,(cell_x, cell_y, CELL_SIZE, CELL_SIZE),3)
            else:
                pygame.draw.rect(window, CELL_COLOR, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))

            if ((row, col) != selected_cell and board[row][col] != initial_board[row][col] and board[row][col] != 0):
                if not is_valid_move(row, col, board[row][col]):
                    pygame.draw.rect(
                        window, (255, 0, 0), (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 3)
            
            if board[row][col] != 0:
                number_text = MEDIUM_FONT.render(str(board[row][col]), True, TEXT_COLOR)
                text_x = cell_x + (CELL_SIZE // 2) - (number_text.get_width() // 2)
                text_y = cell_y + (CELL_SIZE // 2) - (number_text.get_height() // 2)
                window.blit(number_text, (text_x, text_y))
                
            pygame.draw.rect(window, GRID_COLOR, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 1)
            
            if row % BOX_SIZE == 0 and row != 0 and row != GRID_SIZE - 1:
                pygame.draw.line(window,HIGHLIGHT_COLOR,(cell_x, cell_y),(cell_x + CELL_SIZE, cell_y),3)
            if col % BOX_SIZE == 0 and col != 0 and col != GRID_SIZE - 1:
                pygame.draw.line(window,HIGHLIGHT_COLOR,(cell_x, cell_y),(cell_x, cell_y + CELL_SIZE),3)
    
    pygame.draw.line(window,HIGHLIGHT_COLOR,(MARGIN - 1, MARGIN - 1),(MARGIN + GRID_SIZE * CELL_SIZE + 1, MARGIN - 1),3)
    pygame.draw.line(window,HIGHLIGHT_COLOR,(MARGIN - 1, MARGIN - 1),(MARGIN - 1, MARGIN + GRID_SIZE * CELL_SIZE + 1),3)
    pygame.draw.line(window,HIGHLIGHT_COLOR,(MARGIN + GRID_SIZE * CELL_SIZE + 1, MARGIN - 1),(MARGIN + GRID_SIZE * CELL_SIZE + 1, MARGIN + GRID_SIZE * CELL_SIZE + 1),3,)
    pygame.draw.line(window,HIGHLIGHT_COLOR,(MARGIN - 1, MARGIN + GRID_SIZE * CELL_SIZE + 1),(MARGIN + GRID_SIZE * CELL_SIZE + 1, MARGIN + GRID_SIZE * CELL_SIZE + 1),3,)


def display_instructions():
    y = (GRID_SIZE * CELL_SIZE) + (MARGIN * 2)
    for instruction in instructions:
        instruction_text = INSTRUCTIONS_FONT.render(instruction, True, TEXT_COLOR)
        text_x = MARGIN
        text_y = y
        window.blit(instruction_text, (text_x, text_y))
        y += instruction_text.get_height() + MARGIN


def handle_key_press(key):
    global selected_cell, mistake_counter
    if selected_cell is not None:
        row, col = selected_cell
        if key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
            if board[row][col] == solved_board[row][col]:
                board[row][col] = 0
        elif pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            if board[row][col] == 0 and initial_board[row][col] == 0:
                board[row][col] = num
                if not is_valid_move(row, col, num):
                    mistake_counter += 1
                    highlight_error(row, col)


def is_valid_placement(row, col, num):
   
    for i in range(GRID_SIZE):
        if board[row][i] == num and i != col:
            return False
 

    for i in range(GRID_SIZE):
        if board[i][col] == num and i != row:
            return False

    
    grid_x, grid_y = 3 * (row // 3), 3 * (col // 3)  # Top left position of the 3x3 grid
    for i in range(3):
        for j in range(3):
            if (grid_x + i != row or grid_y + j != col) and board[grid_x + i][grid_y + j] == num:
                return False
    return True


def get_cell_coordinates(mouse_pos):
    x, y = mouse_pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col


def is_valid_move(row, col, num):
    return solved_board[row][col] == num
 

def is_correct_solution():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (board[row][col] != solved_board[row][col]):  # Compare with the solved board
                return False
    return True


def is_mistake(row, col, value):
    return initial_board[row][col] != value



def handle_button_click(mouse_pos):
    global difficulty, start_time
    if EASY_BUTTON_RECT.collidepoint(mouse_pos):
        difficulty = EASY
    elif MEDIUM_BUTTON_RECT.collidepoint(mouse_pos):
        difficulty = MEDIUM
    elif HARD_BUTTON_RECT.collidepoint(mouse_pos):
        difficulty = HARD
    start_time = time.time()


def check_mistakes_and_highlight():
    mistake_counter = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] != initial_board[row][col]:
                mistake_counter += 1
                highlight_error(row, col)
    return mistake_counter



def button_clicked(mouse_pos):
    if EASY_BUTTON_RECT.collidepoint(mouse_pos):
        return EASY
    elif MEDIUM_BUTTON_RECT.collidepoint(mouse_pos):
        return MEDIUM
    elif HARD_BUTTON_RECT.collidepoint(mouse_pos):
        return HARD
    else:
        return None  


running = True
time_remaining = 100

while running:

    time_elapsed = time.time() - start_time

    if difficulty == EASY:
        time_remaining = 1201 - time_elapsed  
    elif difficulty == MEDIUM:
        time_remaining = 901 - time_elapsed  
    elif difficulty == HARD:
        time_remaining = 601 - time_elapsed  

    if time_remaining <= 0:
        running = False
        print("Game Over!")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            check_mistakes_and_highlight()
            if event.key == pygame.K_r:
                init()
            elif event.key == pygame.K_BACKSPACE:
                if selected_cell is not None:
                    row, col = selected_cell
                    board[row][col] = 0  
            elif pygame.K_1 <= event.key <= pygame.K_9:  
                if selected_cell is not None:
                    row, col = selected_cell
                if not is_valid_move(row, col, event.key - pygame.K_0):
                    mistake_counter += 1
                    highlight_error(row, col)
                board[row][col] = event.key - pygame.K_0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_pos = pygame.mouse.get_pos()
                clicked_difficulty = button_clicked(mouse_pos)
                if clicked_difficulty is not None:
                    difficulty = clicked_difficulty
                    init()  
                    start_time = time.time()  
                else:
                    row, col = get_cell_coordinates(mouse_pos)
                    selected_cell = (row, col)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (row, col) != selected_cell and board[row][col] != initial_board[row][col]:
                if not is_valid_move(row, col, board[row][col]):
                    highlight_error(row, col)

    window.fill(BACKGROUND_COLOR)
    draw_board()
    display_instructions()

    pygame.draw.rect(window, BUTTON_COLOR, EASY_BUTTON_RECT)
    pygame.draw.rect(window, BUTTON_COLOR, MEDIUM_BUTTON_RECT)
    pygame.draw.rect(window, BUTTON_COLOR, HARD_BUTTON_RECT)

    if difficulty == EASY:
        pygame.draw.rect(window, BUTTON_SELECTED_COLOR, EASY_BUTTON_RECT)
    elif difficulty == MEDIUM:
        pygame.draw.rect(window, BUTTON_SELECTED_COLOR, MEDIUM_BUTTON_RECT)
    elif difficulty == HARD:
        pygame.draw.rect(window, BUTTON_SELECTED_COLOR, HARD_BUTTON_RECT)

    pygame.draw.rect(window, GRID_COLOR, EASY_BUTTON_RECT, 2)
    pygame.draw.rect(window, GRID_COLOR, MEDIUM_BUTTON_RECT, 2)
    pygame.draw.rect(window, GRID_COLOR, HARD_BUTTON_RECT, 2)

    difficulty_text = SMALL_FONT.render("Difficulty:", True, TEXT_COLOR)
    difficulty_text_rect = difficulty_text.get_rect()
    difficulty_text_rect.center = (WINDOW_SIZE[0] - 75, 150)

    window.blit(difficulty_text, difficulty_text_rect)
    easy_text = SMALL_FONT.render("Easy", True, TEXT_COLOR)
    window.blit(easy_text, (EASY_BUTTON_RECT.x + 30, EASY_BUTTON_RECT.y + 10))
    medium_text = SMALL_FONT.render("Medium", True, TEXT_COLOR)
    window.blit(medium_text, (MEDIUM_BUTTON_RECT.x + 20, MEDIUM_BUTTON_RECT.y + 10))
    hard_text = SMALL_FONT.render("Hard", True, TEXT_COLOR)
    window.blit(hard_text, (HARD_BUTTON_RECT.x + 30, HARD_BUTTON_RECT.y + 10))

    timer_text = SMALL_FONT.render("Time: " + str(int(time_remaining)), True, TEXT_COLOR)

    window.blit(timer_text, (WINDOW_SIZE[0] - 115, 350))  

    mistake_text = SMALL_FONT.render("Mistakes: " + str(mistake_counter), True, TEXT_COLOR)
    mistake_text_rect = mistake_text.get_rect()
    mistake_text_rect.center = (WINDOW_SIZE[0] - 75, 100)
    window.blit(mistake_text, mistake_text_rect)
    pygame.display.flip()

pygame.quit()
