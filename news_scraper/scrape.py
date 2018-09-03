#!/usr/bin/python

from news_scraper.util import *
from news_scraper.news_entry import NewsEntry
from news_scraper.news_site import NewsSite
from news_scraper.entries_cache import EntriesCache
from news_scraper.config import load_config
from news_scraper import sites
import datetime
import sys
import argparse
import logging


def make_blocks(entries):
    entries = sorted(entries, key=lambda e: (e.date, e.spot_time), reverse=True)
    accum = ""
    li_s = ""
    date = None
    for entry in entries:
        if date and date != entry.date:
            date_str = date.strftime('%Y-%m-%d')
            accum += "<div><h3>%s</h3><ul>%s</ul></div>" % (date_str, li_s)
            li_s = ""
        date = entry.date
        li_s += entry.manual_li()
    # collect entries for the last date
    date_str = date.strftime('%Y-%m-%d')
    accum += "<div><h3>%s</h3><ul>%s</ul></div>" % (date_str, li_s)
    return accum


def make_page(entries, full_html):
    blocks = make_blocks(entries)
    if not full_html:
        return blocks
    else:
        timestamp = 'last updated: ' + datetime.datetime.now().isoformat()
        meta = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></meta>'
        return '<html><head>%s</head><body>%s<br><br>%s</body></html>' % (meta, timestamp, blocks)


last_summary_date = None


def notify_subscribers(email_client, is_update, entries, subscribers):
    global last_summary_date
    html_text = make_page(entries, False)
    if is_update:
        subject = '[速递] %s - %s' % (entries[0].site_name, entries[0].title)
        if len(entries) > 1:
            subject += '  等%d条' % len(entries)
    else:
        subject = today_in_china_str() + ' 今日新闻汇总'
    email_client.send(subscribers, subject, html_text)
    # mark global variable when successfully sent a summary
    if not is_update:
        last_summary_date = today_in_china()


# FIXME: if send fails, the updates shouldn't be added
def scrape_once (entriesCache, send_summary, subscribers, index_page, email_client):
    entriesCache.load()
    all_sites = sites.all()
    entries_new = sum( list(map(NewsSite.scrape, all_sites)), [] )
    entries_added, cache_updated = entriesCache.update(entries_new)
    if send_summary:
        notify_subscribers(email_client, False, entriesCache.entries, subscribers)
    elif entries_added:
        print("New entries found:")
        for entry in entries_added: entry.quick_print()
        sys.stdout.flush()
        notify_subscribers(email_client, True, entries_added, subscribers)
    else:
        # send email every morning
        now = now_in_china()
        if now.hour >= 8 \
           and (not last_summary_date or last_summary_date < today_in_china()):
            notify_subscribers(email_client, False, entriesCache.entries, subscribers)

    if cache_updated:
        entriesCache.dump()
        page_str = make_page(entriesCache.entries, True)
        unicode_to_file(index_page, page_str)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file')
    parser.add_argument('--no_init_email', action="store_true")
    args = parser.parse_args()

    if args.no_init_email and now_in_china().hour >= 8: # FIXME: This is twisted.
        global last_summary_date
        last_summary_date = today_in_china()

    config = load_config(args.config_file)

    entriesCache = EntriesCache(config["cache_file"])
    while True:
        # CR scai: logging
        print("new scrape job", datetime.datetime.now())
        sys.stdout.flush()
        try:
            scrape_once(
                entriesCache, False,
                config["subscribers"], config["index_page"], config["email_client"]
            )
        except Exception as e:
            logging.error("scrape failure:", exc_info=e)


if __name__ == '__main__':
    main()
