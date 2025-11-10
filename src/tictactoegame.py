import pygame as pg
import sys


from pygame import MOUSEBUTTONDOWN

from src.ttt_logic import ttt_logic

# Initialize Pygame
pg.init()

# Styling
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
font = pg.font.SysFont(None,75)

# XO images
x_img = pg.image.load("images/letter_x.png")
o_img = pg.image.load("images/letter_o.png")

IMG_SIZE = 100
x_img = pg.transform.scale(x_img, (IMG_SIZE, IMG_SIZE))
o_img = pg.transform.scale(o_img, (IMG_SIZE, IMG_SIZE))

# Board setup
EDGE_SPACE = 40
BOARD_SIZE = 480
STATUS_BAR_HEIGHT = 70
WIDTH, HEIGHT = BOARD_SIZE + 2*EDGE_SPACE, BOARD_SIZE + 2*EDGE_SPACE + STATUS_BAR_HEIGHT

BOARD_LEFT = EDGE_SPACE
BOARD_TOP  = EDGE_SPACE + STATUS_BAR_HEIGHT
CELL       = BOARD_SIZE // 3

def in_board(px: int, py: int) -> bool:
    return (BOARD_LEFT <= px < BOARD_LEFT + BOARD_SIZE) and (BOARD_TOP <= py < BOARD_TOP + BOARD_SIZE)

def position_to_indexes(x: int, y: int) -> tuple[int, int]:
    row = (y - BOARD_TOP) // CELL
    col = (x - BOARD_LEFT) // CELL
    #print(f"{x}:{col}, {y}:{row}")
    return row, col

def draw_board():
    # Reset board
    screen.fill(COLOR_WHITE)

    # Grid lines — inside the padded board rectangle
    # Vertical
    for i in (1, 2):
        x = BOARD_LEFT + i * CELL
        pg.draw.line(screen, COLOR_BLACK, (x, BOARD_TOP), (x, BOARD_TOP + BOARD_SIZE), 7)

    # Horizontal
    for i in (1, 2):
        y = BOARD_TOP + i * CELL
        pg.draw.line(screen, COLOR_BLACK, (BOARD_LEFT, y), (BOARD_LEFT + BOARD_SIZE, y), 7)

    # Separator line above the status bar
    #sep_y = board_top + BOARD_SIZE + EDGE_SPACE
    #pg.draw.line(screen, COLOR_BLACK, (0, sep_y), (WIDTH, sep_y), 5)

def print_banner(string: str):
    blank =  pg.Rect(0, 0, WIDTH , EDGE_SPACE + STATUS_BAR_HEIGHT)
    pg.draw.rect(screen, COLOR_WHITE, blank)
    txt = font.render(string, True, COLOR_BLACK)

    center_height = (STATUS_BAR_HEIGHT + EDGE_SPACE) / 2 - txt.get_height() / 2    # Cover over previous message
    center_width = WIDTH / 2 - txt.get_width() / 2
    screen.blit(txt, (center_width, center_height))

# Places either an X or O into the screen
def drawXO(row: int, column: int, val: str) -> None:
    # Subtract half of the size for offset
    xVal = BOARD_SIZE / 6 + column * BOARD_SIZE / 3 - IMG_SIZE / 2 + EDGE_SPACE
    yVal = BOARD_SIZE / 6 + row * BOARD_SIZE / 3 - IMG_SIZE / 2 + EDGE_SPACE + STATUS_BAR_HEIGHT
    img = x_img if val == "X" else o_img
    screen.blit(img, (xVal, yVal))

def check_winner():
    winner = ttt.getWinner()
    if winner == "X":
        print_banner("X wins!")
    elif winner == "O":
        print_banner("O wins!")
    elif winner == "T":
        print_banner("The game is a tie!")


def on_click():
    x, y = pg.mouse.get_pos()
    row, column = position_to_indexes(x, y)

    if row < 0 or row > 2 or column < 0 or column > 2:
        return

    if not ttt.isFree(row * 3 + column):
        return

    drawXO(row, column, ttt.turn)
    ttt.play(row, column)

    if ttt.getWinner() is None:
        original_turn = ttt.turn
        row, column = ttt.play_best_move() # This changes the turn which is why we need to save the original turn
        drawXO(row, column, original_turn)

    check_winner()

def prompt_user():
    print_banner("Tic Tac Toe")
    x1 = WIDTH / 3 - IMG_SIZE / 2
    x2 = 2 * WIDTH / 3 - IMG_SIZE / 2
    y_prompt = HEIGHT * .35
    y_vals = HEIGHT * .5

    x_rec = pg.Rect((x1,y_vals), (IMG_SIZE, IMG_SIZE))
    y_rec = pg.Rect((x2, y_vals), (IMG_SIZE, IMG_SIZE))

    prompt = pg.font.SysFont("Arial", 50)
    play_as = prompt.render("Play as:", True, COLOR_BLACK)
    x_prompt_center = WIDTH / 2 - play_as.get_width() / 2

    screen.blit(play_as, (x_prompt_center, y_prompt))
    screen.blit(x_img, (x1 , y_vals))
    screen.blit(o_img, (x2 , y_vals))

    while (True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if x_rec.collidepoint(x, y):
                    return "X"
                elif y_rec.collidepoint(x, y):
                    return "O"
        pg.display.flip()


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic Tac Toe")
screen.fill(COLOR_WHITE)

XO = prompt_user()

ttt = ttt_logic()
draw_board()
print_banner("Play!")

if XO == "O":
    r, c = ttt.play_best_move()
    drawXO(r, c, ttt.getNextTurn(ttt.turn))

# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if not ttt.getWinner():
                on_click()

    pg.display.flip()

pg.quit()
sys.exit()



