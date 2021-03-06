import datetime
import logging

from   .news_entry import NewsEntry
from   .util import *


def deserialize_entry(dic):
    entry = NewsEntry()
    return entry.from_dict(dic)


def cutoff_entry_date (entries):
    today = today_in_china()
    keep = datetime.timedelta(7)
    cutoff = today - keep
    for e in entries:
        if e.date > today:
            logging.warning(f"News entry is marked to have a date later than today {today:%Y-%m-%d}: {e}")
    return [ e for e in entries if e.date > cutoff and e.date <= today ]


class EntriesCache:
    def __init__(self, filename):
        self.filename = filename


    def load(self):
        serializer = load_json(self.filename)
        self.entries = [ deserialize_entry(x) for x in serializer ]


    def dump(self):
        serializer = [ entry.to_dict() for entry in self.entries ]
        dump_json(serializer, self.filename)


    def update(self, entries_new):
        """
        :return:
          (entries added, True/False for whether there is any update)
        """
        updated = False

        original_cnt = len(self.entries)
        self.entries = cutoff_entry_date(self.entries)
        if len(self.entries) < original_cnt:
            updated = True

        entries_new = cutoff_entry_date(entries_new)
        # keep the [spot_time] in the cache!
        entries_to_add = []
        set_old = set(self.entries)
        for entry in entries_new:
            if entry not in set_old:
                entries_to_add.append(entry)
        if entries_to_add:
            self.entries = self.entries + entries_to_add
            updated = True

        return entries_to_add, updated
