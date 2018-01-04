import urllib3
import sqlite3
import html
import urllib
import HTMLParser
from urllib import parse

class HREFParser(HTMLParser):
    """
    Extracting hrefs
    """
class Crawler:

    href = set()
    html = ''

    def __init__(self, html):

        self.html = html

