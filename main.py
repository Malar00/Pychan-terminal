import requests
import json
import os
import html2text

# Global variable to share the current board for image and catalog fetch. Defaults to /g/ ofc
current_board = "g"

# Global variable to set amount of posts printed in browse_thread()
amount_of_posts = 5


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


def get_posts(op_id):
    response = requests.get("https://a.4cdn.org/" + current_board + "/thread/" + op_id + ".json")
    return response.json()


# Lists threads on the chosen board from 4chan_catalog.json downloaded by get_catalog().
def list_threads():
    data = read_json("4chan_catalog.json")
    numbers, title, image, text, replies = [], [], [], [], []
    for catalog in data:
        for thread in catalog['threads']:
            try:
                numbers.append(str(thread['no']))
            except KeyError:
                numbers.append("<no number>")

            # Prints title of the thread
            try:
                title.append(str(thread['sub']))
            except KeyError:
                title.append("<no subject>")

            # Combines time of the post and the file format to get image ID.
            try:
                image.append("https://i.4cdn.org/" + current_board + "/" + str(thread['tim']) + thread['ext'])
            except KeyError:
                image.append("<no file>")

            # Prints body of the thread and converts html to plaintext
            try:
                h = html2text.HTML2Text()
                h.body_width = int(os.get_terminal_size()[0]) - 1
                comment = h.handle(thread['com'])
                text.append(comment.replace(">", BColors.WARNING + ">").replace("\n", BColors.ENDC + "\n"))
                # print(thread['com'])
            except KeyError:
                text.append("<no comment>")

            # Prints number of replies and images
            try:
                replies.append("Replies: " + str(thread['replies']) + " | Images: " + str(thread['images']))
            except KeyError:
                replies.append("<no replies or images>")

        browse_catalog(numbers, title, image, text, replies)


def browse_catalog(numbers, title, image, text, replies):
    i = 0
    while i < len(numbers) - 1:
        os.system("clear")
        print(i)
        print(BColors.HEADER + "No." + str(numbers[i]) + BColors.ENDC)
        print(title[i])
        print(image[i])
        print(text[i])
        print(replies[i])

        # Threads borders
        for width in range(os.get_terminal_size()[0]):
            print("-", end='')

        x = input("go back: q+Return | go forward: e+Return | browse thread: w+Return\n")
        if x == 'q' and i > 0:
            i -= 1
        elif x == 'e' and i < len(numbers) - 1:
            i += 1
        elif x == 'w':
            browse_thread(numbers[i])


def browse_thread(thread_number):
    data = get_posts(thread_number)
    numbers, title, image, text = [], [], [], []
    for post in data['posts']:
        try:
            numbers.append(BColors.HEADER + "No." + str(post['no']) + BColors.ENDC)
        except KeyError:
            print("<no number>")

        # Prints title of the thread
        try:
            title.append(str(post['sub']))
        except KeyError:
            title.append("<no subject>")

        # Combines time of the post and the file format to get image ID.
        try:
            image.append("https://i.4cdn.org/" + current_board + "/" + str(post['tim']) + post['ext'])
        except KeyError:
            image.append("<no file>")

        # Prints body of the thread and converts html to plaintext
        try:
            h = html2text.HTML2Text()
            h.body_width = int(os.get_terminal_size()[0]) - 1
            comment = h.handle(post['com'])
            text.append(comment.replace(">", BColors.WARNING + ">").replace("\n", BColors.ENDC + "\n"))
            # print(thread['com'])
        except KeyError:
            text.append("<no comment>")

    i = 0
    global amount_of_posts
    while i < len(numbers) - 1:
        os.system("clear")
        for qwe in range(amount_of_posts):
            print(i)
            print(numbers[i])
            print(title[i])
            print(image[i])
            print(text[i])
            print("--------------")
            i += 1
        x = input("go back: q+Return | go forward: e+Return | back to catalog: w+Return\n")
        if x == 'q' and i == amount_of_posts:
            i -= amount_of_posts
        elif x == 'q' and i > amount_of_posts:
            i -= amount_of_posts + 1
        elif x == 'e' and i < len(numbers) - 1:
            i -= amount_of_posts - 1
        elif x == 'w':
            break
        else:
            i -= amount_of_posts


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
