# 11 - лето 10 - весна осень  9 - зимa
import sys
from copy import deepcopy
from random import randint

from front import *
from saver import *


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
        self.index = index
        self.left_friend_index = None
        self.right_friend_index = None
        self.command_count = 0

    def check_values(self):
        if self.energy <= 0:
            self.die_or_kill(self.index - 3)
        if self.energy > 999:
            self.energy = 999
        if self.minerals > 999:
            self.minerals = 999

    def die_or_kill(self, index):
        if genesis.bots[index] is not None:
            left, right = genesis.bots[index].left_friend_index, genesis.bots[index].right_friend_index
            if left is not None:
                genesis.bots[right].left_friend_index = left
            if right is not None:
                genesis.bots[left].right_friend_index = right
            genesis.world[genesis.bots[index].y][genesis.bots[index].x] = 2
            genesis.bots[index] = None
            # print('дэд инсайд')

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

    def move(self, new_y, new_x):  # здесь явно есть ошибки (хотя наверное нет)
        genesis.world[self.y][self.x] = 0  # убираем бота из мира
        self.x, self.y = new_x, new_y
        genesis.world[self.y][self.x] = self.index  # создаем бота в мире

    def is_relative(self, index):
        right = self.right_friend_index
        while right is not None:
            if right == index:
                return True
            right = genesis.bots[right].right_friend_index
        left = self.left_friend_index
        while left is not None:
            if left == index:
                return True
            left = genesis.bots[left].left_friend_index
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
                if 0 <= new_y <= WORLD_HEIGHT - 1:
                    new_y, new_x = self.check_coords(new_y, new_x)
                    if genesis.world[new_y][new_x] == 0 and (dx, dy) != (0, 0):
                        return new_y, new_x  # DIRECTIONS_FOR_DELTAS[(dy, dx)]
        return -1, -1

    def bot_double(self, to_tie):
        self.energy -= 150
        new_y, new_x = self.find_empty_cell()
        # print(new_y, new_x)
        # print(self.energy)
        if (new_y, new_x) == (-1, -1) or self.energy <= 0:  # умер
            self.die_or_kill(self.index - 3)
            # print(123)
            return

        new_gens = deepcopy(self.gens)
        if randint(1, 4) == 1:
            new_gens[randint(0, 63)] = randint(1, 64)
        self.energy //= 2
        self.minerals //= 2

        new_bot = Bot(new_y, new_x, new_gens, self.energy, self.minerals, 0)
        # здесь ему задаются здоровье, минералы и все такое
        new_bot.color = deepcopy(self.color)
        new_bot_index = None
        for i in range(len(genesis.bots)):
            if genesis.bots[i] is None:
                new_bot_index = i

        if new_bot_index is None:
            new_bot_index = len(genesis.bots)
            genesis.bots.append(None)
        new_bot_index += 3

        # new_bot_index += 3

        new_bot.index = new_bot_index
        new_bot.direction = randint(0, 7)
        genesis.world[new_bot.y][new_bot.x] = new_bot_index

        if to_tie:
            if self.is_multi() == 3:  # есть оба соседа
                new_bot.left_friend_index, new_bot.right_friend_index = self.index, self.right_friend_index
                genesis.bots[self.right_friend_index].left_friend_index = new_bot_index
                self.right_friend_index = new_bot_index
            elif self.is_multi() == 2:  # только правый сосед
                new_bot.left_friend_index, new_bot.right_friend_index = 0, self.index
                self.left_friend_index = new_bot_index
            elif self.is_multi() == 1:  # только левый сосед
                new_bot.left_friend_index, new_bot.right_friend_index = self.index, 0
                self.right_friend_index = new_bot_index

        genesis.bots[new_bot_index - 3] = new_bot

    def execute_commands(self):
        count = self.command_count
        for _ in range(15):
            count %= 64
            command = self.gens[count]
            if command == 23:  # поменять направление на параметр
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
                new_energy = genesis.season - self.y // 6 + smth
                new_energy *= 10
                # print(f'после фотосинтеза прибавилось {new_energy} энергии')
                if new_energy > 0:
                    self.energy += new_energy
                    self.more_green()
                count += 1
            elif command in (26, 27):  # движение (отностельно, абсолютно)
                # print('here')
                if self.is_multi() == 0:  # только одноклеточные двигаются
                    if command == 26:  # относительно
                        self.direction = (self.direction + self.gens[(count + 1) % 64]) % 8
                    if command == 27:
                        self.direction = self.gens[(count + 1) % 64] % 8
                    delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                    new_x, new_y = self.x + delta_x, self.y + delta_y
                    new_y, new_x = self.check_coords(new_y, new_x)
                    # self.direction = new_direction  # ЕЩЕ НЕ ЗНАЮ, НАДО ЛИ МЕНЯТЬ НАПРАВЛЕНИЕ ВСЕГДА ИЛИ ТОЛЬКО, ЕСЛИ БОТ ТОЧНО ПЕРЕМЕЩАЕТСЯ # НАДО
                    if genesis.world[new_y][new_x] == 0:
                        # self.direction = new_direction
                        self.move(new_y, new_x)
                        # print('moved')
                        count += 2
                    elif genesis.world[new_y][new_x] == 1:
                        count += 3
                    elif genesis.world[new_y][new_x] == 2:
                        count += 4
                    elif self.is_relative(genesis.world[new_y][new_x]):
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
                if genesis.world[new_y][new_x] == 0:
                    count += 2
                elif genesis.world[new_y][new_x] == 1:
                    count += 3
                elif genesis.world[new_y][new_x] == 2:  # скушал органику
                    genesis.world[new_y][new_x] = 0
                    self.y, self.x = new_y, new_x
                    genesis.world[new_y][new_x] = self.index
                    self.energy += 100
                    self.minerals += 150
                    self.more_red()
                    count += 4
                elif genesis.world[new_y][new_x] >= 3:  # скушал бота (сложная механика)
                    dinner = genesis.bots[genesis.world[new_y][new_x] - 3]
                    if dinner is not None:
                        if self.minerals >= dinner.minerals:
                            self.minerals -= dinner.minerals
                            self.die_or_kill(genesis.world[new_y][new_x] - 3)  # удаляем жертву
                            # genesis.world[new_y][new_x] = self.index  # перемещаем бота
                            self.move(new_y, new_x)  # а теперь нормально перемещаем
                            self.energy += 100 + (dinner.energy // 2)
                            self.more_red()
                            count += 5
                        else:
                            dinner.minerals -= self.minerals
                            self.minerals = 0
                            if self.energy >= dinner.minerals * 2:
                                self.die_or_kill(genesis.world[new_y][new_x] - 3)  # обед умеръ
                                self.energy += 100 + (dinner.energy // 2) - 2 * dinner.minerals
                                self.more_red()
                                count += 5
                            else:
                                dinner.minerals = 0
                                self.die_or_kill(self.index - 3)  # бот умеръ
                                count += 5
                                break
                    else:
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
                if genesis.world[new_y][new_x] == 0:
                    count += 2
                elif genesis.world[new_y][new_x] == 1:
                    count += 3
                elif genesis.world[new_y][new_x] == 2:
                    count += 4
                else:  # бот
                    if self.is_relative(genesis.world[new_y][new_x]):
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
                if genesis.world[new_y][new_x] == 0:
                    count += 2
                elif genesis.world[new_y][new_x] == 1:
                    count += 3
                elif genesis.world[new_y][new_x] == 2:
                    count += 4
                else:  # там бот
                    # print(genesis.world[new_y][new_x])
                    try:
                        friend = genesis.bots[genesis.world[new_y][new_x] - 3]
                        if self.energy > friend.energy:
                            new_hp = (self.energy + friend.energy) // 2
                            self.energy, genesis.bots[genesis.world[new_y][new_x] - 3].energy = new_hp, new_hp
                        if self.minerals > friend.minerals:
                            new_minerals = (self.minerals + friend.minerals) // 2
                            self.minerals, genesis.bots[
                                genesis.world[new_y][new_x] - 3].minerals = new_minerals, new_minerals
                        # разделили поровну минералы и энергию, если у нас больше, чем у соседа
                    except Exception:
                        pass
                    count += 5
            elif command in (34, 50, 35, 52):  # безвозмездно отдать четверть минералов и энергии
                if command in (34, 50):  # относительно
                    self.direction = (self.direction + self.gens[(count + 1) % 64] % 8) % 8
                else:  # абсолютно
                    self.direction = self.gens[(count + 1) % 64] % 8
                delta_y, delta_x = DELTAS_FOR_DIRECTIONS[self.direction]
                new_y, new_x = self.y + delta_y, self.x + delta_x
                new_y, new_x = self.check_coords(new_y, new_x)
                if genesis.world[new_y][new_x] == 0:
                    count += 2
                elif genesis.world[new_y][new_x] == 1:
                    count += 3
                elif genesis.world[new_y][new_x] == 2:
                    count += 4
                else:  # там бот
                    if genesis.bots[genesis.world[new_y][new_x] - 3] is not None:
                        quarter = self.energy // 4  # энергия
                        self.energy -= quarter
                        genesis.bots[genesis.world[new_y][new_x] - 3].energy += quarter
                        quarter = self.minerals // 4
                        self.minerals -= quarter
                        genesis.bots[genesis.world[new_y][new_x] - 3].minerals += quarter
                        if genesis.bots[genesis.world[new_y][new_x] - 3].minerals > 999:
                            genesis.bots[genesis.world[new_y][new_x] - 3].minerals = 999
                    count += 5
            elif command == 36:  # выравниться по горизонтали
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
                self.bot_double(True)
                count += 1
                break
            elif command == 41:  # размножение (свободного бота)
                self.bot_double(False)
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
                smth = genesis.season - (self.y - 1) // 5 + t
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
                if self.energy > 0 and genesis.world[new_y][new_x] >= 3 and genesis.bots[
                    genesis.world[new_y][new_x] - 3] is not None:
                    # print(world[new_y][new_x] - 3, bots)
                    genesis.bots[genesis.world[new_y][new_x] - 3].gens[randint(0, 63)] = randint(1, 64)
                count += 1
            else:
                count += command
        self.command_count = count


def terminate():
    pygame.quit()
    sys.exit()


class Game:
    def init_world(self):
        # global world, bots, season
        self.world = [[0 for _ in range(WORLD_WIDTH)] for __ in range(WORLD_HEIGHT)]
        self.bots = []
        self.prev_world, self.prev_bots = deepcopy(self.world), deepcopy(self.bots)
        # for i in range(WORLD_HEIGHT):
        adam = Bot(0, WORLD_WIDTH // 2, [25] * 64, 500, 500, 3)
        eva = Bot(WORLD_HEIGHT - 1, WORLD_WIDTH // 2, [27] * 64, 500, 500, 3)
        adam.direction = randint(0, 7)
        eva.direction = randint(0, 7)
        self.world[adam.y][adam.x] = adam.index
        # self.world[eva.y][eva.x] = eva.index
        self.season = 11
        self.bots.append(adam)
        # self.bots.append(eva)

    def world_fixer(self):
        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                if self.world[y][x] >= 3 and self.bots[self.world[y][x] - 3] is None:
                    self.world[y][x] = 0

    def move_bodies(self):
        for y in range(WORLD_HEIGHT - 1, -1, -1):
            for x in range(WORLD_WIDTH):
                if self.world[y][x] == 2 and y + 1 <= WORLD_HEIGHT - 1 and self.world[y + 1][x] == 0:
                    self.world[y + 1][x] = 2
                    self.world[y][x] = 0

    def radiation(self):
        for index in range(len(self.bots)):
            if self.bots[index] is not None:
                if self.bots[index].y <= 10:  # or self.bots[index].y >= WORLD_HEIGHT - 10:
                    self.bots[index].gens[randint(0, 63)] = randint(1, 64)

    def main_do_one_turn(self):
        global running
        # print('turn started')
        self.bot_count = 0
        self.season_time = 0
        while self.bot_count < len(self.bots):
            if self.bots[self.bot_count] is not None:
                # self.bots[self.bot_count].season = self.season
                self.bots[self.bot_count].execute_commands()
                if self.bots[self.bot_count] is not None:
                    self.bots[self.bot_count].check_values()
                self.world_fixer()
            self.bot_count += 1
            # print(self.bot_count)
        self.season_time += 1
        self.radiation()
        self.move_bodies()
        if self.season_time == MAX_SEASON_TIME:
            season_temp = self.season_time % 4
            if season_temp == 0:
                self.season = 11
            elif season_temp == 2:
                self.season = 9
            else:
                self.season = 10
            self.season_time = 0
        snapshot = make_snapshot(self.prev_world, self.world, self.bots)
        # print(snapshot)
        save_new_snapshot(file_name + '.gns', snapshot)
        self.prev_bots, self.prev_world = deepcopy(self.bots), deepcopy(self.world)
        # print('turn ended')


def load_matrix(file_name):
    file = open(f'saves/{file_name}', mode='rt', encoding='utf-8')
    bots = []
    world = [[0 for _ in range(WORLD_WIDTH)] for __ in range(WORLD_HEIGHT)]
    for y in range(WORLD_HEIGHT):
        row = file.readline().split(';')[1:]
        # print(len(row), row)
        for x in range(WORLD_WIDTH):
            elem = row[x].split('-')
            if int(elem[0]) >= 3:
                gens = list(map(int, elem[1].split(',')))
                energy = int(elem[2])
                minerals = int(elem[3])
                direction = int(elem[4])
                color = elem[5]
                color = list(map(int, color[1:len(color) - 1].split(', ')))
                left_friend = elem[6]
                right_friend = elem[7]
                if left_friend == 'None':
                    left_friend = None
                else:
                    left_friend = int(left_friend)
                if right_friend == 'None':
                    right_friend = None
                else:
                    right_friend = int(right_friend)
                command_count = int(elem[8])
                index = len(bots) + 3
                bot = Bot(y, x, gens, energy, minerals, index)
                bot.direction = direction
                bot.color = color
                bot.left_friend_index, bot.right_friend_index = left_friend, right_friend
                bot.command_count = command_count
                bots.append(bot)
                world[y][x] = index
            else:
                world[y][x] = int(elem[0])
    return world, bots


if __name__ == '__main__':
    genesis = Game()
    genesis.init_world()
    smth = 0
    mode = 0
    running = True
    fps = 30
    cell_size = 6
    is_pause = True
    size = WIDTH, HEIGHT = WORLD_WIDTH * cell_size, WORLD_HEIGHT * cell_size
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    board = Board(WORLD_WIDTH, WORLD_HEIGHT)
    board.set_view(1, 1, cell_size)
    # prepare_file('test.gns')
    s_down, ctrl_down = False, False
    file_name = 'test'
    if os.path.exists(f'saves/{file_name + "_matrix.gns"}'):
        genesis.world, genesis.bots = load_matrix(file_name + '_matrix.gns')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                save_new_matrix(file_name + '_matrix.gns', genesis.bots, genesis.world)
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    mode += 1
                    mode %= 3
                if event.button == 1 and is_pause:
                    board.get_click(event.pos, screen)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    ctrl_down = True
                if event.key == pygame.K_s:
                    s_down = True
                if event.key == pygame.K_ESCAPE:
                    is_pause = not is_pause
                    print('here')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    ctrl_down = False
                if event.type == pygame.K_s:
                    s_down = False
            if s_down and ctrl_down:
                save_new_matrix(file_name + '_matrix.gns', genesis.bots, genesis.world)
                s_down, ctrl_down = False, False
        if not is_pause:
            genesis.main_do_one_turn()
            genesis.radiation()
            screen.fill((0, 0, 0))
            board.board = genesis.world
            board.render(genesis.bots, screen, mode)
        else:
            board.render_pause(screen)
        # print(*genesis.bots[0].gens)
        # print(len(genesis.bots))

        pygame.display.flip()
        clock.tick(fps)
