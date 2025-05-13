def draw_window(surface, grid1, grid2):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS MULTIJUGADOR', 1, (255, 255, 255))
    surface.blit(label, (s_width / 2 - label.get_width() / 2, 30))

    # Dibujar grillas
    for grid, offset_x in [(grid1, 100), (grid2, 450)]:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (offset_x + j * 30, top_left_y + i * 30, 30, 30), 0)
        for i in range(20):
            pygame.draw.line(surface, (128, 128, 128), (offset_x, top_left_y + i * 30), (offset_x + 300, top_left_y + i * 30))
            for j in range(10):
                pygame.draw.line(surface, (128, 128, 128), (offset_x + j * 30, top_left_y), (offset_x + j * 30, top_left_y + 600))
        pygame.draw.rect(surface, (255, 0, 0), (offset_x, top_left_y, play_width, play_height), 5)

def main():
    locked_positions1 = {}
    locked_positions2 = {}
    grid1 = create_grid(locked_positions1)
    grid2 = create_grid(locked_positions2)

    current_piece1 = get_shape()
    current_piece2 = get_shape()
    next_piece1 = get_shape()
    next_piece2 = get_shape()

    change_piece1 = False
    change_piece2 = False

    run = True
    clock = pygame.time.Clock()
    fall_time1 = 0
    fall_time2 = 0
    fall_speed = 0.3

    while run:
        grid1 = create_grid(locked_positions1)
        grid2 = create_grid(locked_positions2)

        fall_time1 += clock.get_rawtime()
        fall_time2 += clock.get_rawtime()
        clock.tick()

        if fall_time1 / 1000 >= fall_speed:
            fall_time1 = 0
            current_piece1.y += 1
            if not valid_space(current_piece1, grid1):
                current_piece1.y -= 1
                change_piece1 = True

        if fall_time2 / 1000 >= fall_speed:
            fall_time2 = 0
            current_piece2.y += 1
            if not valid_space(current_piece2, grid2):
                current_piece2.y -= 1
                change_piece2 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Jugador 1 - Flechas
                if event.key == pygame.K_LEFT:
                    current_piece1.x -= 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece1.x += 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece1.rotation += 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.rotation -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece1.y += 1
                    if not valid_space(current_piece1, grid1):
                        current_piece1.y -= 1

                # Jugador 2 - WASD
                elif event.key == pygame.K_a:
                    current_piece2.x -= 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.x += 1
                elif event.key == pygame.K_d:
                    current_piece2.x += 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.x -= 1
                elif event.key == pygame.K_w:
                    current_piece2.rotation += 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.rotation -= 1
                elif event.key == pygame.K_s:
                    current_piece2.y += 1
                    if not valid_space(current_piece2, grid2):
                        current_piece2.y -= 1

        # Actualizar piezas en el grid
        for shape, grid, locked, change_flag, next_piece in [
            (current_piece1, grid1, locked_positions1, change_piece1, next_piece1),
            (current_piece2, grid2, locked_positions2, change_piece2, next_piece2)
        ]:
            for x, y in convert_shape_format(shape):
                if y > -1:
                    grid[y][x] = shape.color

        if change_piece1:
            for pos in convert_shape_format(current_piece1):
                locked_positions1[(pos[0], pos[1])] = current_piece1.color
            current_piece1 = next_piece1
            next_piece1 = get_shape()
            change_piece1 = False

        if change_piece2:
            for pos in convert_shape_format(current_piece2):
                locked_positions2[(pos[0], pos[1])] = current_piece2.color
            current_piece2 = next_piece2
            next_piece2 = get_shape()
            change_piece2 = False

        draw_window(win, grid1, grid2)
        pygame.display.update()

        if check_lost(locked_positions1) or check_lost(locked_positions2):
            run = False

    draw_text_middle("¡Fin del juego!", 60, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(3000)
