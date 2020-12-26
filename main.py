import pygame
import sys

from bot import *
from consts import *
from front import *

def terminate():
    pygame.quit()
    sys.exit()

class Game:
    def init_world(self):
        # global world, bots, season
        self.world = [[0 for _ in range(WORLD_WIDTH)] for __ in range(WORLD_HEIGHT)]
        adam = Bot(0, WORLD_WIDTH // 2, [25] * 64, 300, 300, 3)
        self.world[adam.y][adam.x] = adam.index
        update_world(self.world)
        self.season = 11
        self.bots = []
        self.bots.append(adam)
        update_bots(self.bots)

    def radiation(self):
        for index in range(len(self.bots)):
            if self.bots[index] is not None:
                if self.bots[index].y <= 10:
                    self.bots[index].gens[randint(0, 63)] = randint(1, 64)
                    # print('changed')

    def main_do_one_turn(self):
        global running
        self.bot_count = 0
        self.season_time = 0
        bot_count = 0
        while self.bot_count < len(self.bots):
            update_world(self.world)
            update_bots(self.bots)
            self.bots[self.bot_count].season = self.season
            self.bots[self.bot_count].execute_commands()
            # print(bots[bot_count].gens)
            bot_count += 1
        self.season_time += 1
        self.radiation()
        # print(bots)
        if self.season_time == MAX_SEASON_TIME:
            season_temp = self.season_time % 4
            if season_temp == 0:
                self.season = 11
            elif season_temp == 2:
                self.season = 9
            else:
                self.season = 10
            update_season(self.season)
            self.season_time = 0


if __name__ == '__main__':
    genesis = Game()
    genesis.init_world()
    smth = 0
    for row in genesis.world:
        for elem in row:
            if elem >= 3:
                smth += 1
    print(smth)
    running = True
    fps = 10
    size = WIDTH, HEIGHT = WORLD_WIDTH * 4, WORLD_HEIGHT * 4
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    board = Board(WORLD_WIDTH, WORLD_HEIGHT)
    board.set_view(1, 1, 4)

    while running:
        smth = 0
        for row in genesis.world:
            for elem in row:
                if elem >= 3:
                    smth += 1
        print(smth)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

        genesis.main_do_one_turn()
        genesis.radiation()
        screen.fill((0, 0, 0))
        board.board = genesis.world
        board.render(genesis.bots, screen)
        pygame.display.flip()
        clock.tick(fps)


