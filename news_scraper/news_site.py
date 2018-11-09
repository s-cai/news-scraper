import logging
import requests

from   .util import *
from   .news_entry import NewsEntry
from   .timeout import timeout


class NewsSite:
    def __init__(self, name, chinese_encoding, base_url, date_format, node_xpath, parse_node):
        self.name             = name
        self.chinese_encoding = chinese_encoding
        self.base_url         = base_url
        self.date_format      = date_format
        self.node_xpath       = node_xpath
        self.parse_node       = parse_node


    @timeout(60)
    def scrape(self):
        def node_to_entry (node):
            result = self.parse_node(node)
            if result:
                (title, url, date) = result
                entry = NewsEntry()
                return entry.from_parsed(self, title, url, date)
            else:
                return None
        # end of node_to_entry
        try:
            page = requests.get(self.base_url)
            tree = html.fromstring(page.content)
            nodes = tree.xpath(self.node_xpath)
        except Exception as e:
            logging.error(f"unable to get site {self.name}", exc_info=True)
            return []
        entries = [ node_to_entry(node) for node in nodes ]
        entries = [ x for x in entries if x ]
        return list(set(entries))
