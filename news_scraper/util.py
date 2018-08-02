from lxml import html
import json
import sys
import datetime
import pytz
import os

def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def unicode_to_file(filename, u):
    with open (filename, 'w') as f:
        f.write(u)

def print_html (node):
    print((html.tostring(node, encoding="utf-8")))

china_tz = pytz.timezone('Asia/Shanghai')

def now_in_china():
    return datetime.datetime.now(china_tz)

def today_in_china():
    return now_in_china().date()

def today_in_china_str():
    return today_in_china().strftime('%Y-%m-%d')

http_prefix = 'http://'

def absolute_url (base, url):
    if url.startswith('./'):
        return base.strip('/') + '/' + url.strip('./')
    if url.startswith('/'):
        if base.startswith(http_prefix):
            base = base[len(http_prefix):]
            base = base.split('/')[0]
        return http_prefix + base + url
    return url

def dump_json(obj, filename):
    with open(filename,'w') as f:
        json.dump(obj, f)

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        # CR scai: logging
        print('Failed to open file', filename)
        print(str(e))
        sys.stdout.flush()
        # CR scai: make this type more general
        return []
