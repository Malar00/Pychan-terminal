import requests
import json
import os
import html2text
from datetime import datetime

current_board = "g"


def get_boards():
    response = requests.get('https://a.4cdn.org/boards.json')
    response_json = response.json()
    with open('4chan_boards.json', 'w') as file:
        json.dump(response_json, file)


def get_threads(board):
    response = requests.get('https://a.4cdn.org/' + board + '/threads.json')
    response_json = response.json()
    with open('4chan_threads.json', 'w') as file:
        json.dump(response_json, file)


def list_threads():
    data = read_json("4chan_threads.json")
    thread_list = []
    for threads in data:
        for thread_number in threads['threads']:
            print(thread_number['no'])
            thread_list.append(
                requests.get(
                    'https://a.4cdn.org/' + current_board + '/thread/' + str(thread_number['no']) + '.json'))
        break

    for threads in thread_list:
        for thread in threads.json()['posts']:
            try:
                print(str(thread['no']))
            except KeyError:
                print("no number")

            try:
                h = html2text.HTML2Text()
                print(h.handle(thread['com']))
            except KeyError:
                print("no com")

            for width in range(os.get_terminal_size()[0]):
                print("-", end='')


def list_boards():
    data = read_json("4chan_boards.json")
    board_number = 0
    boards_list = []
    for boards in data['boards']:
        boards_list.append(boards['board'])
        print(str(board_number) + ") " + boards['meta_description'].replace('&quot;', ' '))
        board_number += 1
    board_choose(boards_list)


def board_choose(board_list):
    choice = int(input("choose a board from [0-" + str(len(board_list) - 1) + "]: "))
    get_threads(board_list[choice])
    global current_board
    current_board = board_list[choice]


def read_json(json_name):
    with open(json_name, 'r') as file:
        data = file.read()
    obj = json.loads(data)
    return obj


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_boards()
    list_boards()
    list_threads()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
