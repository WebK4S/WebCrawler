from sqlite3 import *
from urllib.request import *
from urllib.error import HTTPError
from html.parser import HTMLParser
from urllib.parse import urlparse


class HREFParser(HTMLParser):
    """
    Extracting hrefs from prvided url
    :param hrefs: set of hrefs extracted from web page
    """

    hrefs = set()


    def error(self, message):
        pass



    def handle_starttag(self, tag, attrs):
        """

        :param tag: tagname <a>
        :type tag: str
        :param attrs: attributes of single tag <a href>
        :type attrs:
        :return: none
        :rtype:
        """
        if tag == 'a':
            dict_attrs = dict(attrs)
            if dict_attrs.get('href'):
                self.hrefs.add(dict_attrs['href'])
                """add to dictionary all tags <a href>"""


def get_links(html, domain):
    """

    :param html: html addess to be parsed
    :type html: str
    :param domain: name of website
    :type domain:
    :return:
    :rtype:
    """
    hrefs = set()
    parser = HREFParser()
    parser.feed(html)
    for href in parser.hrefs:
        u_parse = urlparse(href)
        if href.startswith('/'):
            hrefs.add(u_parse.path)
        else:
            if u_parse.netloc == domain:
                hrefs.add(u_parse.path)
    return hrefs





class Crawler_SQLite(object):
    """
    Class resposible for connection with database, and data transfering

    """

    def __init__(self, db_file):
        """

        :param db_file: place to store results
        :type db_file: sqlite3 database file
        """
        self.conn = connect(db_file)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sites(domain TEXT, url TEXT, content TEXT)''')
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def set(self, domain, url, data):
        """
        Seting values in database
        :param domain: domain
        :type domain: str
        :param url: url provided
        :type url: str
        :param data: data inserted to database
        :type data: str
        :return: none
        :rtype:
        """
        self.cursor.execute("INSERT INTO sites VALUES(?,?,?)", (domain, url, data))
        self.conn.commit()

    def get(self, domain, url):
        self.cursor.execute("SELECT content FROM sites WHERE domain=? AND url =?", (domain, url))
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_urls(self, domain):
        self.cursor.execute("SELECT url FROM sites WHERE domain=?", (domain,))

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
        self.cache = cache
        self.content = {}

    """
    One of basic method, 
    url - should be full url address 
    no_cache - function returning True if the web page should be refreshed
    """

    def crawl(self, url, no_cache=None):
        u_parse = urlparse(url)
        self.domain = u_parse.netloc
        self.content[self.domain] = {}
        self.scheme = u_parse.scheme
        self.no_cache = no_cache
        self._crawl([u_parse.path], self.depth)

    def set(self, url, html):
        self.content[self.domain][url] = html
        if self.is_cacheable(url):
            self.cache.set(self.domain, url, html)

    def get(self, url):
        page = None
        if self.is_cacheable(url):
            page = self.cache.get(self.domain, url)
        if page is None:
            page = self.curl(url)
        else:
            print("cached url ... [%s] %s" % (self.domain, url))
        return page

    def is_cacheable(self, url):
        return not (not self.cache or not self.no_cache or self.no_cache(url))

    def _crawl(self, urls, max_depth):
        n_urls = set()
        if max_depth:
            for url in urls:

                if url not in self.content:
                    html = self.get(url)
                    self.set(url, html)
                    n_urls = n_urls.union(get_links(html, self.domain))

            self._crawl(n_urls, max_depth - 1)

    def curl(self, url):
        try:
            print("Retriving urls... [%s] %s" % (self.domain, url))
            req = Request("%s://%s%s" % (self.scheme, self.domain, url))
            response = urlopen(req)
            return response.read().decode('ascii', 'ignore')
        except HTTPError as e:
            print("Error [%s] %s: %s" % (self.domain, url, e))
            return ''
