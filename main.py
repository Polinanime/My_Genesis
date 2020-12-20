from bot import *
from consts import *
from random import randint


def init_world():
    # global world, bots, season
    world = [[0 for _ in range(WORLD_WIDTH)] for __ in range(WORLD_HEIGHT)]
    update_world(world)
    season = 11
    adam = Bot(0, WORLD_WIDTH // 2, [25] * 64, 300, 300, set(), 3)
    bots = []
    bots.append(adam)
    update_bots(bots)
    return world, bots, season


def radiation():
    for index in range(len(bots)):
        if bots[index] is not None:
            if bots[index].y <= 10:
                bots[index].gens[randint(0, 63)] = randint(1, 64)
                # print('changed')


if __name__ == '__main__':
    world, bots, season = init_world()
    bot_count = 0
    running = True
    season_time = 0
    while running:
        bot_count = 0
        while bot_count < len(bots):
            update_world(world)
            update_bots(bots)
            bots[bot_count].season = season
            bots[bot_count].execute_commands()
            # print(bots[bot_count].gens)
            bot_count += 1
        season_time += 1
        radiation()
        # print(bots)
        if season_time == MAX_SEASON_TIME:
            season_temp = season_time % 4
            if season_temp == 0:
                season = 11
            elif season_temp == 2:
                season = 9
            else:
                season = 10
            update_season(season)
            season_time = 0
