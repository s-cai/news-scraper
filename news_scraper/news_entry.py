from .util import *
import datetime

serialization_date_format = '%Y-%m-%d'
serialization_time_format = '%Y-%m-%dT%H:%M:%S'

class NewsEntry:
    def __init__ (self):
        pass


    # FIXME: what is this...
    def set_fields (self, site_name, title, url, date, spot_time):
        self.site_name = site_name
        self.title     = title
        self.url       = url
        self.date      = date
        self.spot_time = spot_time
        return self


    def from_parsed (self, site, title, url, date):
        self.site_name = site.name
        self.title     = str(title.encode(site.chinese_encoding), 'utf-8')
        self.url       = absolute_url(site.base_url, url)
        self.date      = datetime.datetime.strptime(date, site.date_format).date()
        self.spot_time = now_in_china()
        return self


    def manual_li (self):
        return '<li>[' + self.site_name + '] <a href="' + self.url + '">' + self.title + '</a>  ' + '</li>'


    def __str__(self):
        return f"{self.title} {self.url} {self.date.strftime(serialization_date_format)}"


    # customly defined uniqueness for set operations
    def __eq__(self, other):
        return self.title == other.title and self.site_name == other.site_name


    def __hash__(self):
        return hash(self.title) ^ hash(self.site_name)


    # serialization functions
    def to_dict(self):
        dic = {}
        dic['site_name'] = self.site_name
        dic['title'    ] = self.title
        dic['url'      ] = self.url
        dic['date'     ] = datetime.date.strftime(self.date, serialization_date_format)
        dic['spot_time'] = datetime.datetime.strftime(self.spot_time, serialization_time_format)
        return dic


    def from_dict(self, dic):
        self.site_name = dic['site_name']
        self.title     = dic['title']
        self.url       = dic['url']
        self.date      = datetime.datetime.strptime(dic['date'], serialization_date_format).date()
        # The best practice is to include tz in the serialization,
        # but I don't want to waster the time to look it up...
        self.spot_time = china_tz.localize(datetime.datetime.strptime(dic['spot_time'], serialization_time_format))
        return self
