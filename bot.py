from copy import deepcopy
from random import randint

from consts import *

# 11 - лето 10 - весна осень  9 - зимa
world = []
bots = []
season = 11


def update_world(new_world):
    global world
    world = new_world


def update_bots(new_bots):
    global bots
    bots = new_bots


def update_season(new_season):
    global season
    season = new_season


class Bot:
    def __init__(self, y: int, x: int, gens: list, energy: int, minerals: int, index: int):
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
        self.index = index
        self.left_friend_index = None
        self.right_friend_index = None
        self.command_count = 0

    def die_or_kill(self, index):
        left, right = bots[index].left_friend_index, bots[index].right_friend_index
        if left is not None:
            bots[right].right_friend_index = left
        if right is not None:
            bots[left].left_friend_index = right
        world[bots[index].y][bots[index].x] = 0
        bots[index] = None

    def more_green(self):
        self.color[1] += DELTA_COLOR
        if self.color[1] > 255:
            self.color[1] = 255

        self.color[0] -= DELTA_COLOR // 2
        if self.color[0] < 0:
            self.color[0] = 0
        self.color[2] -= DELTA_COLOR // 2
        if self.color[2] < 0:
            self.color[2] = 0

    def more_red(self):
        self.color[0] += DELTA_COLOR
        if self.color[0] > 255:
            self.color[0] = 255

        self.color[1] -= DELTA_COLOR // 2
        if self.color[1] < 0:
            self.color[1] = 0
        self.color[2] -= DELTA_COLOR // 2
        if self.color[2] < 0:
            self.color[2] = 0

    def more_blue(self):
        self.color[2] += DELTA_COLOR
        if self.color[2] > 255:
            self.color[2] = 255

        self.color[1] -= DELTA_COLOR // 2
        if self.color[1] < 0:
            self.color[1] = 0
        self.color[0] -= DELTA_COLOR // 2
        if self.color[0] < 0:
            self.color[0] = 0

    def move(self):  # здесь явно есть ошибки (хотя наверное нет)
        delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
        new_x, new_y = self.x + delta_x, self.y + delta_y
        world[self.y][self.x] = 0  # убираем бота из мира
        self.x, self.y = new_x, new_y
        world[self.y][self.x] = self.index  # создаем бота в мире

    def is_relative(self, index):
        right = self.right_friend_index
        while right is not None:
            if right == index:
                return True
            right = bots[right].right_friend_index

        left = self.left_friend_index
        while left is not None:
            if left == index:
                return True
            left = bots[left].left_friend_index
        return False

    def is_multi(self):
        if self.left_friend_index is None and self.right_friend_index is None:  # нет соседей (одноклеточное существо0
            return 0
        if self.left_friend_index is not None and self.right_friend_index is None:  # есть только левый сосед (в составе колонии)
            return 1
        if self.left_friend_index is None and self.right_friend_index is not None:  # есть только правый сосед (в составе колонии)
            return 2
        if self.left_friend_index is not None and self.right_friend_index is not None:  # есть оба соседа (и слева, и справа, в составе колонии)
            return 3

    def check_coords(self, new_y, new_x):
        if new_x >= WORLD_WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = WORLD_WIDTH - 1
        if new_y >= WORLD_HEIGHT:
            new_y = 0
        elif new_y < 0:
            new_y = WORLD_HEIGHT - 1
        return new_y, new_x

    def find_empty_cell(self):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                new_y, new_x = self.y + dy, self.x + dx
                new_y, new_x = self.check_coords(new_y, new_x)
                if world[new_y][new_x] == 0 and (dx, dy) != (0, 0):
                    return new_y, new_x  # DIRECTIONS_FOR_DELTAS[(dy, dx)]
        return -1, -1

    def bot_double(self, to_tie):
        self.energy -= 150
        new_y, new_x = self.find_empty_cell()
        if (new_y, new_x) == (-1, -1) or self.energy <= 0:  # умер
            world[self.y][self.x] = 2
            self.die_or_kill(self.index - 3)

        new_gens = deepcopy(self.gens)
        if randint(1, 4) == 1:
            new_gens[randint(0, 63)] = randint(1, 64)
        self.energy //= 2
        self.minerals //= 2

        new_bot = Bot(new_y, new_x, new_gens, self.energy, self.minerals, 0)
        # здесь ему задаются здоровье, минералы и все такое
        new_bot.color = self.color
        new_bot_index = None
        for i in range(len(bots)):
            if bots[i] is None:
                new_bot_index = i

        if new_bot_index is None:
            new_bot_index = len(bots)
            bots.append(None)
        new_bot_index += 3

        # new_bot_index += 3

        new_bot.index = new_bot_index
        new_bot.direction = randint(0, 7)

        if to_tie:
            if self.is_multi() == 3:  # есть оба соседа
                new_bot.left_friend_index, new_bot.right_friend_index = self.index, self.right_friend_index
                bots[self.right_friend_index].left_friend_index = new_bot_index
                self.right_friend_index = new_bot_index
            elif self.is_multi() == 2:  # только правый сосед
                new_bot.left_friend_index, new_bot.right_friend_index = 0, self.index
                self.left_friend_index = new_bot_index
            elif self.is_multi() == 1:  # только левый сосед
                new_bot.left_friend_index, new_bot.right_friend_index = self.index, 0
                self.right_friend_index = new_bot_index

        bots[new_bot_index - 3] = new_bot

    def execute_commands(self):
        count = self.command_count
        for _ in range(15):
            count %= 64
            command = self.gens[count]
            if command == 23:  # поменять направление на параметр
                param = self.gens[(count + 1) % 64] % 8
                self.direction = (self.direction + self.gens[(count + 1) % 64] % 8) % 8
                count += 2
            elif command == 24:  # повернуться в сторону, которая определяется параметром
                self.direction = self.gens[(count + 1) % 64] % 8
                count += 2
            elif command == 25:  # фотосинтез
                if self.minerals < 400:
                    smth = 1
                else:
                    smth = 2
                new_energy = self.season - self.y // 6 + smth
                if new_energy > 0:
                    self.energy += new_energy
                    self.more_green()
                count += 1
            elif command in (26, 27):  # движение (отностельно, абсолютно)
                if not self.is_multi:
                    if command == 26:  # относительно
                        self.direction = (self.direction + self.gens[(count + 1) % 64]) % 8
                    if command == 27:
                        self.direction = self.gens[(count + 1) % 64] % 8
                    delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                    new_x, new_y = self.x + delta_x, self.y + delta_y
                    new_y, new_x = self.check_coords(new_y, new_x)
                    # self.direction = new_direction  # ЕЩЕ НЕ ЗНАЮ, НАДО ЛИ МЕНЯТЬ НАПРАВЛЕНИЕ ВСЕГДА ИЛИ ТОЛЬКО, ЕСЛИ БОТ ТОЧНО ПЕРЕМЕЩАЕТСЯ # НАДО
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
            elif command in (28, 29):  # скушать
                if command == 28:  # в относительном нправлении
                    self.direction = (self.direction + self.gens[(count + 1) % 64]) % 8
                if command == 27:
                    self.direction = self.gens[(count + 1) % 64] % 8
                delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                new_x, new_y = self.x + delta_x, self.y + delta_y
                new_y, new_x = self.check_coords(new_y, new_x)
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
                else:  # скушал бота (сложная механика)
                    dinner = bots[world[new_y][new_x] - 3]
                    if self.minerals >= dinner.minerals:
                        self.minerals -= dinner.minerals
                        self.die_or_kill(world[new_y][new_x] - 3) # удаляем жертву
                        world[new_y][new_x] = self.index  # перемещаем бота
                        self.hp += 100 + (dinner.hp // 2)
                        self.more_red()
                        count += 5
                    else:
                        dinner.minerals -= self.minerals
                        self.minerals = 0
                        if self.hp >= dinner.minerals * 2:
                            self.die_or_kill(world[new_y][new_x] - 3)   #  обед умеръ
                            self.hp += 100 + (dinner.hp // 2) - 2 * dinner.minerals
                            self.more_red()
                            count += 5
                        else:
                            dinner.minerals = 0
                            self.die_or_kill(self.index - 3) # бот умеръ
                            count += 5
                    # теперь бот наелся (ну или жертва наелась)
            elif command in (30, 31):  # посмотреть относительно или абсолютно
                if command == 30:  # относительно
                    self.direction = (self.direction + self.gens[(count + 1) % 64] % 8) % 8
                else:  # абсолютно
                    self.direction = self.gens[(count + 1) % 64] % 8
                delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                new_y, new_x = self.y + delta_y, self.x + delta_x
                new_y, new_x = self.check_coords(new_y, new_x)
                if world[new_y][new_x] == 0:
                    count += 2
                elif world[new_y][new_x] == 1:
                    count += 3
                elif world[new_y][new_x] == 2:
                    count += 4
                else:  # бот
                    if self.is_relative(world[new_y][new_x]):
                        count += 6
                    else:
                        count += 5
            elif command in (32, 42, 33, 51):  # поделиться относительно/абсолютно
                if command in (32, 42):  # относительно
                    self.direction = (self.direction + self.gens[(count + 1) % 64] % 8) % 8
                else:  # абсолютно
                    self.direction = self.gens[(count + 1) % 64] % 8
                delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                new_y, new_x = self.y + delta_y, self.x + delta_x
                new_y, new_x = self.check_coords(new_y, new_x)
                if world[new_y][new_x] == 0:
                    count += 2
                elif world[new_y][new_x] == 1:
                    count += 3
                elif world[new_y][new_x] == 2:
                    count += 4
                else:  # там бот
                    friend = bots[world[new_y][new_x] - 3]

                    if self.hp > friend.hp:
                        new_hp = (self.hp + friend.hp) // 2
                        self.hp, bots[world[new_y][new_x] - 3].hp = new_hp, new_hp
                    if self.minerals > friend.minerals:
                        new_minerals = (self.minerals + friend.minerals) // 2
                        self.minerals, bots[world[new_y][new_x] - 3].minerals = new_minerals, new_minerals
                    # разделили поровну минералы и энергию, если у нас больше, чем у соседа
                    count += 5
            elif command in (34, 50, 35, 52):  # безвозмездно отдать четверть минералов и энергии
                if command in (34, 50):  # относительно
                    self.direction = (self.direction + self.gens[(count + 1) % 64] % 8) % 8
                else:  # абсолютно
                    self.direction = self.gens[(count + 1) % 64] % 8
                delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                new_y, new_x = self.y + delta_y, self.x + delta_x
                new_y, new_x = self.check_coords(new_y, new_x)
                if world[new_y][new_x] == 0:
                    count += 2
                elif world[new_y][new_x] == 1:
                    count += 3
                elif world[new_y][new_x] == 2:
                    count += 4
                else:  # там бот
                    quarter = self.energy // 4  # энергия
                    self.energy -= quarter
                    bots[world[new_y][new_x] - 3].energy += quarter
                    quarter = self.minerals // 4
                    self.minerals -= quarter
                    bots[world[new_y][new_x] - 3].minerals += quarter
                    if bots[world[new_y][new_x] - 3].minerals > 999:
                        bots[world[new_y][new_x] - 3] = 999
                    count += 5
            elif command == 36:  # выравниться по горизонтали (пока хз что делает)
                if randint(0, 1):  # с шансом 0.5 поворачиваемся направо
                    self.direction = 3
                else:
                    self.direction = 7  # а тут налево
                count += 1
            elif command == 37:  # узнать, на какой высоте
                param = int(self.gens[(count + 1) % 64] * 1.5)
                if self.y < param:
                    count += 2
                else:
                    count += 3
            elif command == 38:  # узнать, сколько здоровья ( энергии )
                param = self.gens[(count + 1) % 64] * 15
                if self.energy < param:
                    count += 2
                else:
                    count += 3
            elif command == 39:  # узнать, сколько минералов
                param = self.gens[(count + 1) % 64] * 15
                if self.minerals < param:
                    count += 2
                else:
                    count += 3
            elif command == 40:  # многоклеточность (создать потомка, связанного с текущим ботом)
                self.bot_double(False)
                count += 1
                break
            elif command == 41:  # размножение (свободного бота)
                self.bot_double(True)
                count += 1
                break
            elif command == 43:  # окружен ли бот
                if self.find_empty_cell() == (-1, -1):
                    count += 1
                else:
                    count += 2
            elif command == 44:  # есть ли приход энергии
                if self.minerals < 100:
                    t = 0
                elif self.minerals < 400:
                    t = 1
                else:
                    t = 2
                smth = season - (self.y - 1) // 5 + t
                if smth >= 3:
                    count += 1
                else:
                    count += 2
            elif command == 45:  # прибавляются ли минералы
                if self.y > MAX_EAT_SUN_HEIGHT:
                    count += 1
                else:
                    count += 2
            elif command == 46:  # многоклеточный ли я
                if self.is_multi() == 0:  # одноклеточный
                    count += 1
                elif self.is_multi() == 3:  # внутри цепочки
                    count += 3
                else:
                    count += 2  # с краю
            elif command == 47:  # преобразовать минералы в энергию
                self.more_blue()
                if self.minerals > 100:
                    self.minerals -= 100
                    self.energy += 400
                else:
                    self.energy += 4 * self.minerals
                    self.minerals = 0
                if self.energy > 999:
                    self.energy = 999
                count += 1
            elif command == 48:  # мутировать
                for _ in range(2):
                    self.gens[randint(0, 63)] = randint(1, 64)
                count += 1
                break
            elif command == 49:  # генная атака
                delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                new_y, new_x = self.y + delta_y, self.x + delta_x
                new_y, new_x = self.check_coords(new_y, new_x)
                self.energy -= 10
                if self.energy > 0 and world[new_y][new_x] >= 3:
                    # print(world[new_y][new_x] - 3, bots)
                    bots[world[new_y][new_x] - 3].gens[randint(0, 63)] = randint(1, 64)
                count += 1
            else:
                count += command
        self.command_count = count


if __name__ == '__main__':
    season = 2
    levels = {}
    world = [[i // 20 for _ in range(WORLD_WIDTH)] for i in range(WORLD_HEIGHT)]
    # bots_board = [[None for _ in range(WORLD_WIDTH)] for __ in range(WORLD_HEIGHT)]
    adam = Bot(20, 20, [25] * 64, WORLD_HEIGHT // 2, WORLD_WIDTH // 2, set(), 3)
    bots = []
    bots.append(adam)
    world[adam.y][adam.x] = adam.index + 3
