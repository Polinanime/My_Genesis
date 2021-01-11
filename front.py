import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.mode = 0

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, bots, screen, mode):
        for x in range(self.width):
            for y in range(self.height):
                sx = self.left + self.cell_size * x
                sy = self.top + self.cell_size * y
                if self.board[y][x] == 0:
                    color = pygame.Color('black')
                elif self.board[y][x] == 1:
                    color = pygame.Color('grey')
                elif self.board[y][x] == 2:
                    color = pygame.Color((26, 22, 42))
                elif self.board[y][x] >= 3:
                    if mode == 0:
                        color_list = bots[self.board[y][x] - 3].color
                        color = pygame.Color(color_list)
                    if mode == 1:
                        red = bots[self.board[y][x] - 3].energy // 4
                        if red > 255:
                            red = 255
                        color = pygame.Color((red, 0, 0))
                    if mode == 2:
                        blue = bots[self.board[y][x] - 3].minerals // 4
                        if blue > 255:
                            blue = 255
                        color = pygame.Color((0, 0, blue))
                else:
                    print('WTF')
                pygame.draw.rect(screen, color, (sx, sy, self.cell_size, self.cell_size))
                # pygame.draw.rect(screen, pygame.Color('white'), (sx, sy, self.cell_size, self.cell_size), 1)

    def render_pause(self, screen):
        screen.fill((0, 0, 0))
        print(self.mode)
        if self.mode == 0:
            intro_text = ["Игра Искусственная жизнь (alpha)", "",
                          "Продолжить",
                          "Изменить файл сохранения",
                          "Управлeние", "", "", "", "", "", ""
                          "*copyright*"]

        # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        # screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 40)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def get_click(self, mouse_pos, screen):
        option = self.get_option(mouse_pos)
        self.mode = option
        self.render_pause(screen)

    def get_option(self, mouse_pos):
        y, x = mouse_pos
        # print(y, x)
        if 9 <= y <= 186 and 133 <= x <= 155:
            return 1    # продолжить
        if 11 <= y <= 383 and 174 <= x <= 195:
            return 2    # сменить файл сохранения
        if 9 <= y <= 171 and 209 <= 234:
            return 3    # управление
        return 0