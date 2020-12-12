from consts import *


# 11 - лето 10 - весна осень  9 - зимa

class Bot:
    def __init__(self, y: int, x: int, gens: list, energy: int, minerals: int, is_multi: bool, relatives: list,
                 index: int):
        self.y = y
        self.x = x
        self.gens = gens
        self.max_commands = 15
        self.direction = 0
        self.energy = energy
        self.minerals = minerals
        self.color = [0, 255, 0]
        self.delta_color = 2
        self.hp = 100
        self.is_multi = is_multi
        self.relatives = relatives
        self.index = index

    def more_green(self):
        self.color[1] += DELTA_COLOR
        if self.color[1] > 255:
            self.color[1] = 255

        self.color[0] -= DELTA_COLOR
        if self.color[0] < 0:
            self.color[0] = 0
        self.color[2] -= DELTA_COLOR
        if self.color[2] < 0:
            self.color[2] = 0

    def more_red(self):
        self.color[0] += DELTA_COLOR
        if self.color[0] > 255:
            self.color[0] = 255

        self.color[1] -= DELTA_COLOR
        if self.color[1] < 0:
            self.color[1] = 0
        self.color[2] -= DELTA_COLOR
        if self.color[2] < 0:
            self.color[2] = 0

    def move(self):  # здесь явно есть ошибки (хотя наверное нет)
        delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
        new_x, new_y = self.x + delta_x, self.y + delta_y
        world[self.y][self.x] = 0  # убираем бота из мира
        self.x, self.y = new_x, new_y
        world[self.y][self.x] = self.index  # создаем бота в мире

    def is_relative(self, index):
        return index in self.relatives

    def execute_commands(self):
        count = 0
        while count < 15:
            command = self.gens[count]
            if command == 23:  # поменять направление на параметр
                param = self.gens[count + 1] % 8
                self.direction = (self.direction + self.gens[count + 1] % 8) % 8
                count += 2
            elif command == 24:  # повернуться в сторону, которая определяется параметром
                self.direction = self.gens[count + 1] % 8
                count += 2
            elif command == 25:  # фотосинтез
                if self.minerals < 400:
                    smth = 1
                else:
                    smth = 2
                new_energy = season - self.y // 6 + smth
                if new_energy > 0:
                    self.energy += new_energy
                    self.more_green()
                count += 1
            elif command in (26, 27):  # движение (отностельно, абсолютно)
                if not self.is_multi:
                    if command == 26:  # относительно
                        new_direction = (self.direction + self.gens[count + 1]) % 8
                    if command == 27:
                        new_direction = self.gens[count + 1] % 8
                    delta_y, delta_x = DELTAS_FOR_DIRECTIONS[new_direction]
                    new_x, new_y = self.x + delta_x, self.y + delta_y
                    self.direction = new_direction  # ЕЩЕ НЕ ЗНАЮ, НАДО ЛИ МЕНЯТЬ НАПРАВЛЕНИЕ ВСЕГДА ИЛИ ТОЛЬКО, ЕСЛИ БОТ ТОЧНО ПЕРЕМЕЩАЕТСЯ
                    if world[new_y][new_x] == 0:
                        # self.direction = new_direction
                        self.move()
                        count += 2
                    elif world[new_y][new_x] == 1:
                        count += 3
                    elif world[new_y][new_x] == 2:
                        count += 4
                    elif self.is_relative(world[new_y][new_x]):
                        count += 6
                    else:
                        count += 5
            elif command in (28, 29):   # скушать
                if command == 28:   # в относительном нправлении
                    self.direction = (self.direction + self.gens[count + 1]) % 8
                if command == 27:
                    new_direction = self.gens[count + 1] % 8
                delta_y, delta_x = DELTAS_FOR_DIRECTIONS[new_direction]
                new_x, new_y = self.x + delta_x, self.y + delta_y
                self.direction = new_direction
                if world[new_y][new_x] == 0:
                    count += 2
                elif world[new_y][new_x] == 1:
                    count += 3
                elif world[new_y][new_x] == 2:  # скушал органику
                    world[new_y][new_x] = 0
                    self.y, self.x = new_y, new_x
                    world[new_y][new_x] = self.index
                    self.hp += 100
                    self.more_red()
                    count += 4
                else:   # скушал бота (сложная механика)




if __name__ == '__main__':
    season = 2
    levels = {}
    world = [[i // 20 for _ in range(WORLD_WIDTH)] for i in range(WORLD_HEIGHT)]
    # bots_board = [[None for _ in range(WORLD_WIDTH)] for __ in range(WORLD_HEIGHT)]
    adam = Bot(20, 20, [25] * 64, 150, 150, False, [], 0)
    bots = []
    bots.append(adam)
    world[adam.y][adam.x] = adam.index + 3
