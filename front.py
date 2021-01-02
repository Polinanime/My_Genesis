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

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, bots, screen):
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
                    try:
                        color = pygame.Color(bots[self.board[y][x] - 3].color)
                    except Exception:
                        color = pygame.Color('pink')
                else:
                    print('WTF')
                pygame.draw.rect(screen, color, (sx, sy, self.cell_size, self.cell_size))
                    # pygame.draw.rect(screen, pygame.Color('white'), (sx, sy, self.cell_size, self.cell_size), 1)