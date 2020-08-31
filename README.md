# Pychan-terminal
**4chan linux terminal reader and image downloader**

![Menu](https://github.com/Malar00/Pychan-terminal/blob/extra/leafterm.png?raw=true "Menu")

* Made with 4chanAPI - https://github.com/4chan/4chan-API

## Requirements:

```bash
$ pip install requests html2text wget pyfiglet
```
## Usage:

```bash
$ python Pychan-terminal -p 4 -d images/
```

## Help:

```bash
optional arguments:
  -h, --help            show this help message and exit
  -p POSTS, --posts POSTS
                        change number of posts to show at once. Default: 4
  -d DIRECTORY, --directory DIRECTORY
                        change image save directory. Default: images/
  -b, --banner          compacts the banner into 2 lines
```
