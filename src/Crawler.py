import urllib3
import sqlite3
import html
import urllib
import HTMLParser
from urllib import parse

class HREFParser(HTMLParser):


    """
    Extracting hrefs from prvided url
    """
    hrefs = set()
    def starttag(self, tag, attrs):
        if tag =='a':
            dict_attrs = dict(attrs)
            if dict_attrs == 'href':
                self.hrefs.add(dict_attrs['href'])
                """add to dictionary all tags <a href>"""

    def get_links(html, domain):
        hrefs = set()
        parser = HTMLParser
        parser.feed(html)
class Crawler_SQLite:

    hrefs = set()
    html = ''

    def __init__(self, html):

        self.html = html

