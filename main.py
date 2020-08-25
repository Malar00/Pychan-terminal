import requests
import json
import os
import html2text

# Global variable to share the current board for image and catalog fetch. Defaults to /g/ ofc
current_board = "g"


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Downloads an json files with boards info. Can be used only once.
def get_boards():
    response = requests.get('https://a.4cdn.org/boards.json')
    response_json = response.json()
    with open('4chan_boards.json', 'w') as file:
        json.dump(response_json, file)


# Downloads a catalog of threads on the current_board as a json file.
def get_catalog(board):
    response = requests.get('https://a.4cdn.org/' + board + '/catalog.json')
    response_json = response.json()
    with open('4chan_catalog.json', 'w') as file:
        json.dump(response_json, file)


# Lists threads on the chosen board from 4chan_catalog.json downloaded by get_catalog().
def list_threads():
    data = read_json("4chan_catalog.json")
    for catalog in data:
        for thread in catalog['threads']:
            try:
                print(BColors.HEADER + "No." + str(thread['no']) + BColors.ENDC)
            except KeyError:
                print("<no number>")

            # Prints title of the thread
            try:
                print(str(thread['sub']))
            except KeyError:
                print("<no subject>")

            # Combines time of the post and the file format to get image ID.
            try:
                print("https://i.4cdn.org/" + current_board + "/" + str(thread['tim']) + thread['ext'])
            except KeyError:
                print("<no file>")

            # Prints body of the thread and converts html to plaintext
            try:
                h = html2text.HTML2Text()
                h.body_width = int(os.get_terminal_size()[0])-1
                text = h.handle(thread['com'])
                print(text.replace(">", BColors.WARNING + ">").replace("\n", BColors.ENDC + "\n"))
                # print(thread['com'])
            except KeyError:
                print("<no comment>")

            # Prints number of replies and images
            try:
                print("Replies: " + str(thread['replies']) + " | Images: " + str(thread['images']))
            except KeyError:
                print("<no replies or images>")

            # Threads borders
            for width in range(os.get_terminal_size()[0]):
                print("-", end='')
            input()
            os.system("clear")


# Lists boards and their full description from 4chan_boards.json downloaded by get_boards().
def list_boards():
    data = read_json("4chan_boards.json")
    board_number = 0
    boards_list = []
    boards_list_title = []
    for boards in data['boards']:
        boards_list.append(boards['board'])
        boards_list_title.append(str(board_number) + ") " + boards['title'])
        board_number += 1
    i = 0
    while i < len(boards_list_title) - 1:
        print("%-30s %s" % (boards_list_title[i], boards_list_title[i + 1]))
        i += 2
    board_choose(boards_list)

    # User interaction to choose the board for further action.


def board_choose(board_list):
    choice = int(input("choose a board from [0-" + str(len(board_list) - 1) + "]: "))
    get_catalog(board_list[choice])
    global current_board
    current_board = board_list[choice]


# Json file parsing shared by other functions
def read_json(json_name):
    with open(json_name, 'r') as file:
        data = file.read()
    obj = json.loads(data)
    return obj


if __name__ == '__main__':
    try:
        get_boards()
        list_boards()
        list_threads()
    except KeyboardInterrupt:
        print("<----------exiting---------->")
        exit()
