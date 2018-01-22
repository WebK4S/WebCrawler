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
        for href in parser.hrefs:
            u_parse = urlparse(href)
            if href.startswith('/'):
                hrefs.add(u_parse.path)
            else:
                if u_parse.netloc == domain :
                    hrefs.add(u_parse.path)
        return hrefs

"""
Class resposible for connection with database, and data transfering
"""


class Crawler_SQLite(object):


    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        c = self.conn.cursor()
        query = '''CREATE TABLE IF NOT EXIST sites (domain text, url text, content text)'''
        c.execute(query)
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def set(self,domain, url, data):
        query = "INSERT INTO sites VALUES(?,?,?)"
        self.cursor.execute(query,(domain,url,data))
        self.conn.commit()

    def get(self,domain,url):
        query = "SELECT content FROM site WHERE domain=? AND url =?"
        self.cursor.execute(query,(domain,url))
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_urls(self,domain):
        query = "SELECT url FROM sites WHERE domain=?"
        self.cursor.execute(query, (domain,))

        return [row[0] for row in self.cursor.fetchall()]

"""
Main crawler class
"""
class Crawler(object):
    """
    cache - basic controller
    depth - how deep we need to crawl page
    """
    def __init__(self, cache=None, depth=2):
        self.depth = depth
        self.cache=cache
        self.content = {}

    """
    One of basic method, 
    url - should be full url adress 
    no_cache - function returning True if the web page should be refreshed
    """
    def crawl(self,url, no_cache=None):
        u_parse = urlparse(url)
        self.domain = u_parse.netloc
        self.content[self.domain] = {}
        self.scheme = u_parse.scheme
        self.no_cache = no_cache
        self._crawl([u_parse.path], self.depth)

    def set(self, url, html):




