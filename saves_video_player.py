import sys

import pygame

from consts import *


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
        self.generation_number = 0

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, deltas):
        # print(deltas)
        self.generation_number += 1
        for elem in deltas:
            is_bot = False
            elem = elem.split('-')
            if len(elem) == 5:
                is_bot = True
            if elem[0] == '' or elem[1] == '':
                break
            y, x = int(elem[0]), int(elem[1])
            if is_bot:
                if mode == 0:
                    color_list = list(map(int, elem[2][1:len(elem[2]) - 1].split(', ')))
                    color = pygame.Color(color_list)
                if mode == 1:
                    red = int(elem[3]) // 4
                    if red > 255:
                        red = 255
                    color = pygame.Color((red, 0, 0))
                if mode == 2:
                    blue = int(elem[4]) // 4
                    if blue > 255:
                        blue = 255
                    color = pygame.Color((0, 0, blue))
            else:
                type = int(elem[2])
                if type == 0:
                    color = pygame.Color('black')
                elif type == 1:
                    color = pygame.Color('grey')
                elif type == 2:
                    color = pygame.Color((26, 22, 42))
                else:
                    color = pygame.Color('pink')
            sx = self.left + self.cell_size * x
            sy = self.top + self.cell_size * y
            # print(y, x, color)
            pygame.draw.rect(screen, color, (sx, sy, self.cell_size, self.cell_size))
            # pygame.draw.rect(screen, pygame.Color('white'), (sx, sy, self.cell_size, self.cell_size), 1)
        pygame.draw.line(screen, (255, 0, 0), (WIDTH * self.cell_size, 0), (WIDTH * self.cell_size, HEIGHT * self.cell_size), 10)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    file_name = 'test'
    running = True
    fps = 5
    cell_size = 6
    size = WIDTH, HEIGHT = WORLD_WIDTH * cell_size + PLAYER_BOARD, WORLD_HEIGHT * cell_size
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    board = Board(WORLD_WIDTH, WORLD_HEIGHT)
    board.set_view(1, 1, cell_size)
    screen.fill((0, 0, 0))
    file = open(f'saves/{file_name}.gns', mode='rt', encoding='utf-8')
    is_end = False
    mode = 0
    to_show = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    mode += 1
                    mode %= 3
                elif event.button == 4 and fps <= 59:
                    fps += 1
                elif event.button == 5 and fps > 1:
                    fps -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    to_show = not to_show

        # print(data, len(data))
        if to_show:
            data = file.readline()
            if data == '\n':
                is_end = True
            if len(data) != 2 and not is_end:  # -\n
                # data = data[:len(data) - 2]
                board.render(data.split(';'))
            pygame.display.flip()
            clock.tick(abs(fps))
