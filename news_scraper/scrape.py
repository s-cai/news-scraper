#!/usr/bin/python

# TODO: relative import
from news_scraper.util import *
from news_scraper.news_entry import NewsEntry
from news_scraper.news_site import NewsSite
from news_scraper.entries_cache import EntriesCache
from news_scraper.config import load_config
from news_scraper.webpage import make_page
from news_scraper import sites
import sys
import argparse
import logging


last_summary_date = None


def notify_subscribers(email_client, is_update, entries, subscribers, webpage_url=None):
    global last_summary_date
    html_text = make_page(entries, False, webpage_url=webpage_url)
    if is_update:
        subject = f'[速递] {entries[0].site_name} - {entries[0].title}'
        if len(entries) > 1:
            subject += '  等%d条' % len(entries)
    else:
        subject = today_in_china_str() + ' 今日新闻汇总'
    email_client.send(subscribers, subject, html_text)
    # mark global variable when successfully sent a summary
    if not is_update:
        last_summary_date = today_in_china()


# FIXME: if send fails, the updates shouldn't be added to cache
def scrape_once (entriesCache, send_summary, subscribers, index_page, email_client, webpage_url=None):
    entriesCache.load()
    all_sites = sites.all()
    entries_new = sum( list(map(NewsSite.scrape, all_sites)), [] )
    entries_added, cache_updated = entriesCache.update(entries_new)
    if send_summary:
        notify_subscribers(
            email_client, False, entriesCache.entries,
            subscribers, webpage_url=webpage_url
        )
    elif entries_added:
        entries_text = '\n'.join(str(e) for e in entries_added)
        logging.info(f"New entries found:\n{entries_text}")
        notify_subscribers(
            email_client, True, entries_added,
            subscribers, webpage_url=webpage_url
        )
    else:
        # send email every morning
        now = now_in_china()
        if now.hour >= 8 \
           and (not last_summary_date or last_summary_date < today_in_china()):
            notify_subscribers(
                email_client, False, entriesCache.entries,
                subscribers, webpage_url=webpage_url
            )

    # update webpage everytime (for last_check time...)
    entriesCache.dump()
    page_str = make_page(entriesCache.entries, True)
    unicode_to_file(index_page, page_str)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file')
    parser.add_argument('--no_init_email', action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level='INFO',
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    if args.no_init_email and now_in_china().hour >= 8: # FIXME: This is twisted.
        global last_summary_date
        last_summary_date = today_in_china()

    config = load_config(args.config_file)

    entriesCache = EntriesCache(config["cache_file"])
    while True:
        logging.info("new scrape job")
        try:
            scrape_once(
                entriesCache, False,
                config["subscribers"],
                config["index_page"],
                config["email_client"],
                webpage_url=config.get("webpage_url")
            )
        except Exception as e:
            logging.error("scrape failure:", exc_info=e)


if __name__ == '__main__':
    main()
