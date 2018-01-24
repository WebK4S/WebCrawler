import re

from Crawler import Crawler, Crawler_SQLite

if __name__ == '__main__':
    crawler = Crawler(Crawler_SQLite('crawler.db'), depth=2)
    root_re = re.compile('^/$').match
    crawler.crawl('http://wmp.uksw.edu.pl', no_cache=root_re)
    print(crawler.content['wmp.uksw.edu.pl'].keys())
    print(len(crawler.content['wmp.uksw.edu.pl'].keys()))