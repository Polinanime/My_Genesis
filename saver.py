import os

from consts import *


def save_new_snapshot(file_name, bots, world, new_snapshot):
    file = open(f'saves/{file_name}', mode='at', encoding='utf-8')
    if new_snapshot == []:
        file.writelines(['-\n'])
    else:
        file.writelines(';'.join(new_snapshot))
    file.close()


def save_new_matrix(file_name, bots, world):
    file = open(f'saves/{file_name}', mode='a', encoding='utf-8')
    new_matrix = make_matrix_with_bots(bots, world)
    file.writelines('\n')
    file.writelines(new_matrix)
    file.close()


def prepare_file(file_name):
    if os.path.exists(f'saves/{file_name}'):
        file = open(f'saves/{file_name}', mode='rt', encoding='utf-8')
        data = file.readlines()
        # print(data)
        old_snapshots = data[:len(data) - WORLD_HEIGHT]
        print(old_snapshots)
        file.close()
        file = open(f'saves/{file_name}', mode='wt', encoding='utf-8')
        file.writelines(old_snapshots)
        del old_snapshots
    else:
        file = open(f'saves/{file_name} ', mode='wt', encoding='utf-8')
    file.close()


def make_snapshot(last, cur, bots):
    snapshot = []
    for y in range(WORLD_HEIGHT):
        for x in range(WORLD_WIDTH):
            if last[y][x] != cur[y][x]:
                if cur[y][x] < 3:
                    snapshot.append(str(cur[y][x]))
                else:
                    bot = bots[cur[y][x] - 3]
                    snapshot.append('-'.join([str(i) for i in make_bot_characteristic(bot)]))
    return snapshot


def make_bot_characteristic(bot):
    matrix_elem_list = []
    matrix_elem_list.append(bot.index)
    matrix_elem_list.append(','.join([str(i) for i in bot.gens]))
    matrix_elem_list.append(bot.energy)
    matrix_elem_list.append(bot.minerals)
    matrix_elem_list.append(bot.direction)
    matrix_elem_list.append(bot.color)
    matrix_elem_list.append(bot.left_friend_index)
    matrix_elem_list.append(bot.right_friend_index)
    matrix_elem_list.append(bot.command_count)
    return matrix_elem_list


def make_matrix_with_bots(bots, world):
    matrix = []
    for y in range(len(world)):
        row = ''
        for x in range(len(world[0])):
            if world[y][x] >= 3:
                bot = bots[world[y][x] - 3]
                list_elem = make_bot_characteristic(bot)
                elem = ','.join([str(i) for i in list_elem])
                row += ';' + elem
            else:
                row += ';' + str(world[y][x])
        matrix.append(row)
    return matrix
