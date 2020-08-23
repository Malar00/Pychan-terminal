import requests
import json


def get_api():
    response = requests.get('https://a.4cdn.org/boards.json')
    response_json = response.json()
    with open('4chan.json', 'w') as file:
        json.dump(response_json, file)


def list_boards():
    data = read_json()
    for boards in data['boards']:
        print(boards['meta_description'])


def read_json():
    with open('4chan.json', 'r') as file:
        data = file.read()
    obj = json.loads(data)
    return obj


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_api()
    list_boards()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
