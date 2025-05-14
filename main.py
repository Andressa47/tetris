import pygame
import random

pygame.font.init()

# Ajuste del tamaño de la ventana
s_width = 1000
s_height = 700
play_width = 400
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# Las piezas y colores permanecen iguales
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface, offset_x, offset_y, label_text):
    font = pygame.font.SysFont('comicsans', 24)
    label = font.render(label_text, 1, (255, 255, 255))
    surface.blit(label, (offset_x, offset_y))
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (offset_x + j * 30, offset_y + 30 + i * 30, 30, 30), 0)

def draw_score(score, surface, offset_x, offset_y, label_text):
    font = pygame.font.SysFont('comicsans', 24)
    label = font.render(f'{label_text} Puntaje: {score}', 1, (255, 255, 255))
    surface.blit(label, (offset_x, offset_y))

def draw_window(surface, grid1, grid2, next_piece1, next_piece2, score1, score2):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS MULTIJUGADOR', 1, (255, 255, 255))
    surface.blit(label, (s_width / 2 - label.get_width() / 2, 30))
    for grid, offset_x in [(grid1, 100), (grid2, 500)]:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (offset_x + j * 30, top_left_y + i * 30, 30, 30), 0)
        for i in range(20):
            pygame.draw.line(surface, (128, 128, 128), (offset_x, top_left_y + i * 30), (offset_x + 300, top_left_y + i * 30))
            for j in range(10):
                pygame.draw.line(surface, (128, 128, 128), (offset_x + j * 30, top_left_y), (offset_x + j * 30, top_left_y + 600))
        pygame.draw.rect(surface, (255, 0, 0), (offset_x, top_left_y, play_width, play_height), 5)
    draw_next_shape(next_piece1, surface, 100, 100, 'Jugador 1')
    draw_score(score1, surface, 100, 250, 'Jugador 1')
    draw_next_shape(next_piece2, surface, 500, 100, 'Jugador 2')
    draw_score(score2, surface, 500, 250, 'Jugador 2')

def main_single():
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.3
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 4:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        win.fill((0,0,0))
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(win, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)
        draw_grid(win, 20, 10)
        pygame.draw.rect(win, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
        draw_next_shape(next_piece, win, s_width - 200, 150, 'Siguiente')
        draw_score(score, win, s_width - 200, 250, 'Puntaje')
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("Has perdido", 40, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

def main():
    locked_positions1 = {}
    grid1 = create_grid(locked_positions1)
    locked_positions2 = {}
    grid2 = create_grid(locked_positions2)

    change_piece1 = False
    change_piece2 = False
    run = True
    current_piece1 = get_shape()
    next_piece1 = get_shape()
    current_piece2 = get_shape()
    next_piece2 = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.3
    score1 = 0
    score2 = 0

    while run:
        grid1 = create_grid(locked_positions1)
        grid2 = create_grid(locked_positions2)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 4:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece1.y += 1
            if not valid_space(current_piece1, grid1):
                current_piece1.y -= 1
                change_piece1 = True

            current_piece2.y += 1
            if not valid_space(current_piece2, grid2):
                current_piece2.y -= 1
                change_piece2 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece1.x -= 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece1.x += 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.x -= 1
                if event.key == pygame.K_UP:
                    current_piece1.rotation += 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.rotation -= 1
                if event.key == pygame.K_DOWN:
                    current_piece1.y += 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.y -= 1

                if event.key == pygame.K_a:
                    current_piece2.x -= 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.x += 1
                if event.key == pygame.K_d:
                    current_piece2.x += 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.x -= 1
                if event.key == pygame.K_w:
                    current_piece2.rotation += 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.rotation -= 1
                if event.key == pygame.K_s:
                    current_piece2.y += 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.y -= 1

        shape_pos1 = convert_shape_format(current_piece1)
        for x, y in shape_pos1:
            if y > -1:
                grid1[y][x] = current_piece1.color

        shape_pos2 = convert_shape_format(current_piece2)
        for x, y in shape_pos2:
            if y > -1:
                grid2[y][x] = current_piece2.color

        if change_piece1:
            for pos in shape_pos1:
                locked_positions1[pos] = current_piece1.color
            current_piece1 = next_piece1
            next_piece1 = get_shape()
            change_piece1 = False
            score1 += clear_rows(grid1, locked_positions1) * 10

        if change_piece2:
            for pos in shape_pos2:
                locked_positions2[pos] = current_piece2.color
            current_piece2 = next_piece2
            next_piece2 = get_shape()
            change_piece2 = False
            score2 += clear_rows(grid2, locked_positions2) * 10

        win.fill((0, 0, 0))

        draw_window(win, grid1, grid2, next_piece1, next_piece2, score1, score2)
        pygame.display.update()

        if check_lost(locked_positions1) or check_lost(locked_positions2):
            draw_text_middle("Has perdido", 40, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Presiona 1 para Jugar Solo\nPresiona 2 para Multijugador', 40, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main_single()
                elif event.key == pygame.K_2:
                    main()
    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TETRIS')
main_menu()
