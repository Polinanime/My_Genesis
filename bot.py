from consts import *


# 11 - лето 10 - весна осень  9 - зимa

class Bot:
    def __init__(self, y: int, x: int, gens: list, energy: int, minerals: int, is_multi: bool):
        self.y = y
        self.x = x
        # self.world_width = len(world[0])
        # self.board_height = len(world)
        self.gens = gens
        self.max_commands = 15
        self.direction = 0
        self.energy = energy
        self.minerals = minerals
        self.color = [0, 255, 0]
        self.delta_color = 2
        self.hp = 100
        self.is_multi = is_multi

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
            self.color[2] =

    def move(self, is_rel: bool):  # здесь явно есть ошибки
        if is_rel:
            n = 2 * self.direction
            if n > 7:
                n -= 8
            if n in (0, 6, 7):
                self.x -= 1
                if self.x < 0:
                    self.x = WORLD_WIDTH - 1
            elif n in (2, 3, 4):
                self.x += 1
                if self.x > WORLD_WIDTH - 1:
                    self.x = 0

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
            elif command == 26:
                if not self.is_multi:
                    self.direction = self.gens[count + 1] % 8
                    count += move(False)


if __name__ == '__main__':
    season = 2
    levels = {}
    world = [[i // 20 for _ in range(WORLD_WIDTH)] for i in range(WORLD_HEIGHT)]
    bots_board = [[None for _ in range(WORLD_WIDTH)] for __ in range(WORLD_HEIGHT)]
    adam = Bot(20, 20, [25] * 64, 150, 150, False)
