import requests
import json
import os
import html2text
import wget
import time
import pyfiglet
import pyfiglet.fonts
import argparse

# Global variable to share the current board for image and catalog fetch. Defaults to /g/ ofc
current_board = "g"

# Global variable to set amount of posts printed in browse_thread()
amount_of_posts = 4

# Global variable to point to the download folder
download_folder_location = "images/"

# Global variable to change the banner
ascii_banner = pyfiglet.figlet_format("Pychan Terminal")

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--posts", type=int, help="change number of posts to show at once. Default: 4")
parser.add_argument("-d", "--directory", type=str, help="change image save directory. Default: images/")
parser.add_argument("-b", "--banner", action="store_true", help="compacts the banner into 2 lines")
args = parser.parse_args()
if args.posts:
    amount_of_posts = args.posts
if args.directory:
    download_folder_location = args.directory
if args.banner:
    ascii_banner = pyfiglet.figlet_format("Pychan\nTerminal")


class BColors:
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[10m'


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


# Converts json keys into arrays to prepare to print into readable format
def write_posts(data, searchword, numbers, title, image, text, replies):
    for thread in data[searchword]:
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

    return numbers, title, image, text, replies


# Lists threads on the chosen board from 4chan_catalog.json downloaded by get_catalog().
def list_threads():
    data = read_json("4chan_catalog.json")
    numbers, title, image, text, replies = [], [], [], [], []
    for catalog in data:
        numbers, title, image, text, replies = write_posts(catalog, "threads", numbers, title, image, text, replies)
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
        print_border()
        x = input("go back: q+Return | go forward: e+Return | browse thread: w+Return\n")
        if x == 'q' and i > 0:
            i -= 1
        elif x == 'e' and i < len(numbers) - 1:
            i += 1
        elif x == 'w':
            print("LOADING THREAD")
            browse_thread(numbers[i])


def download_images(images, images_start, images_end):
    global download_folder_location
    image_count, num = 0, images_start
    while num <= images_end:
        if images[num] != "<no file>":
            image_count += 1
        num += 1
    i, num = 1, images_start
    while num <= images_end:
        if images[num] != "<no file>":
            print(str(i) + " / " + str(image_count))
            image_url = str(images[num])
            try:
                image_filename = wget.download(url=image_url, out=download_folder_location)
            except UnboundLocalError:
                os.system("mkdir " + download_folder_location)
                continue
            except FileNotFoundError:
                os.system("mkdir " + download_folder_location)
                continue
            print('\nImage Successfully Downloaded: ', image_filename)
            i += 1
            time.sleep(1.2)
        num += 1


def browse_thread(thread_number):
    data = get_posts(thread_number)
    numbers, title, image, text, replies = [], [], [], [], []
    numbers, title, image, text, replies = write_posts(data, "posts", numbers, title, image, text, replies)
    i = 0
    global amount_of_posts
    while i < len(numbers) - 1:
        os.system("clear")
        for check in range(amount_of_posts):
            print(i)
            print(BColors.HEADER + "No." + str(numbers[i]) + BColors.ENDC)
            print(title[i])
            print(BColors.UNDERLINE + image[i] + BColors.ENDC)
            print(text[i])
            print_border()
            i += 1
        x = input(
            "back: q+Return | forward: e+Return | back to catalog: w+Return | download images: d{amount}+Return | "
            "download all: da+Return\n")
        if x == 'q' and i > amount_of_posts:
            i -= amount_of_posts + 1
        elif x == 'e' and i < len(numbers):
            i -= amount_of_posts - 1
        elif x == 'w':
            break
        # Download mode
        elif x[0] == 'd':
            if len(x) == 1:
                download_images(image, i - 1, i - 1)
                i -= amount_of_posts
            elif x[1] == 'a':
                download_images(image, 0, len(image) - 1)
                i -= amount_of_posts
            elif x[1].isdigit():
                download_images(image, 0, int(x[1:]) - 1)
                i -= amount_of_posts
        else:
            i -= amount_of_posts


# TODO: filter NSFW boards
# Lists boards and their full description from 4chan_boards.json downloaded by get_boards().
def list_boards():
    data = read_json("4chan_boards.json")
    board_number = 0
    boards_list = []
    boards_list_title = []
    for boards in data['boards']:
        boards_list.append(boards['board'])
        if boards['ws_board'] == 0:
            boards_list_title.append(BColors.WARNING + str(board_number) + ") " + boards['title'] + BColors.ENDC)
        else:
            boards_list_title.append(BColors.RESET + str(board_number) + ") " + boards['title'] + BColors.ENDC)
        board_number += 1
    i = 0
    while i < len(boards_list_title) - 1:
        print("%-50s%s" % (boards_list_title[i], boards_list_title[i + 1]))
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


# Threads borders
def print_border():
    for width in range(os.get_terminal_size()[0]):
        print("-", end='')


def cli():
    global ascii_banner
    print(ascii_banner)
    get_boards()
    list_boards()
    list_threads()


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print()
        exit()
