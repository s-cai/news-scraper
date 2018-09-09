"""
Static webpage that holds the scraped contents.

Note: currently the page is constructed by formatting html
directly.  This is a bit hacky and we may want to eventually
use more pythonic way of constructing the html.
"""

import datetime


def make_blocks(entries):
    entries = sorted(entries, key=lambda e: (e.date, e.spot_time), reverse=True)
    accum = ""
    li_s = ""
    date = None
    for entry in entries:
        if date and date != entry.date:
            accum += f"<div><h3>{date:%Y-%m-%d}</h3><ul>{li_s}</ul></div>"
            li_s = ""
        date = entry.date
        li_s += entry.manual_li()
    # collect entries for the last date
    accum += f"<div><h3>{date:%Y-%m-%d}</h3><ul>{li_s}</ul></div>"
    return accum


def _latest_spot_time(entries):
    return max(e.spot_time for e in entries)


def _add_web_link(html, webpage_url):
    return f'新：<a href="{webpage_url}">网页版要闻汇总</a> (链接打不开的话欢迎回复邮件告诉我)<br>{html}'


def make_page(entries, full_html : bool, webpage_url=None):
    """
    :param full_html:
      True for webpage html; False for email html.
    """
    blocks = make_blocks(entries)
    if not full_html:
        if webpage_url is not None:
            return _add_web_link(blocks, webpage_url)
        else:
            return blocks
    else:
        last_check = '上次刷新: ' + datetime.datetime.now().isoformat()
        last_update = '最新消息: ' + _latest_spot_time(entries).isoformat()
        meta = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></meta>'
        return f'<html><head>{meta}</head><body>{last_check}<br>{last_update}<br><br>{blocks}</body></html>'
