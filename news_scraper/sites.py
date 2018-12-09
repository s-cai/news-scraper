from .news_entry import NewsEntry
from .news_site import NewsSite

def FaGaiWei():

    def parse_node (node):
        title = node.xpath('./a/text()')[0]
        url   = node.xpath('./a/@href')[0]
        date  = node.xpath('./font[@class="date"]/text()')[0]
        return (title, url, date)

    url_and_names = [ ('http://www.sdpc.gov.cn/zcfb/zcfbl/', '发改委-政策发布'),
                      ('http://www.sdpc.gov.cn/xwzx/xwfb/', '发改委-新闻发布'),
                      ('http://www.sdpc.gov.cn/zcfb/zcfbtz/', '发改委-通知'),
                      ('http://www.sdpc.gov.cn/zcfb/zcfbghwb/', '发改委-规划文本') ]
    chinese_encoding = 'iso-8859-1'
    date_format = '%Y/%m/%d'
    node_xpath = '//div[@class="cell_two1_Right "]//ul[@class="list_02 clearfix"]/li[@class="li"]'
    newsSites = [ NewsSite(x[1], chinese_encoding, x[0], date_format, node_xpath, parse_node)
              for x in url_and_names ]
    return newsSites
# end of FaGaiWei

def CaiZhengBu():

    def parse_node(node):
        title = node.xpath('./a/text()')[0]
        url   = node.xpath('./a/@href')[0]
        date  = node.xpath('./@title')[0][-11:-1]
        return (title, url, date)

    name = '财政部-政策发布'
    url = 'http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/'
    date_format = '%Y-%m-%d'
    node_xpath = '//div[@id="divS"]//table[@class="ZIT"]//td[@class="ZITI"]'
    return [ NewsSite(name, 'utf-8', url, date_format, node_xpath, parse_node) ]
# end of CaiZhengBu

def NongYeBu():
    def parse_node(node):
        code  = node.xpath('./span[1]/a/script/text()')[0]
        url   = node.xpath('./span[1]/a/@href')[0]
        date  = node.xpath('./span[2]/text()')[0][1:11]
        title = (code.split("'"))[1].replace('<br />', '')
        return (title, url, date)

    name = '农业部-政策法规'
    url = 'http://www.moa.gov.cn/zwllm/zcfg/'
    date_format = '%Y-%m-%d'
    node_xpath = '//div[@class="rlr"]/ul/li'
    return [ NewsSite(name, 'utf-8', url, date_format, node_xpath, parse_node) ]
# end of NongYeBu

def KeJiBu ():
    def parse_node(node):
        title = node.xpath('./a/text()')[0]
        url   = node.xpath('./a/@href')[0]
        date  = node.xpath('./text()')[0].strip().strip('()')
        return (title, url, date)

    name = '科技部-通知通告'
    url = 'http://www.most.gov.cn/tztg/'
    date_format = '%Y-%m-%d'
    node_xpath = '//td[@class="STYLE30"]'
    return [ NewsSite(name, 'utf-8', url, date_format, node_xpath, parse_node) ]
# end of KeJiBu

# TODO: Better handle of multi-section
def ShangWuBu():
    def parse_node(node):
        title = node.xpath('./a/text()')[0]
        url   = node.xpath('./a/@href')[0]
        date  = node.xpath('./span/text()')[0]
        return (title, url, date)

    name = '商务部-政策发布'
    url = 'http://www.mofcom.gov.cn/article/b/'
    date_format = '%Y-%m-%d'
    node_xpath = '//div[@class="MainList"]//div[@class="col_l fl"]//div[@class="listBox borB"]/ul/li'
    return [ NewsSite(name, 'utf-8', url, date_format, node_xpath, parse_node) ]
# end of ShangWuBu

def GuoTuZiYuanBu():
    def parse_node(node):
        title = node.xpath('./a/text()')
        if len(title) == 0: return None
        title = title[0]
        url   = node.xpath('./a/@href')[0]
        date  = node.xpath('./following-sibling::*/text()')[0]
        return (title, url, date)

    name = '国土部-要闻播报'
    url = 'http://www.mlr.gov.cn/xwdt/jrxw/'
    date_format = '%Y.%m.%d'
    node_xpath = '//td[@class="outlinebig"]'
    return [ NewsSite(name, 'utf-8', url, date_format, node_xpath, parse_node) ]
# end of GuoTuZiYuanBu

def ZhengFuWang():
    def parse_node(node):
        title = node.xpath('./a/text()')[0]
        url   = node.xpath('./a/@href')[0]
        date  = node.xpath('./span/text()')[0].strip()
        return (title, url, date)

    name = '中国政府网-政策'
    url = 'http://www.gov.cn/zhengce/zuixin.htm'
    date_format = '%Y-%m-%d'
    node_xpath = '//div[@class="news_box"]//li/h4'
    return [ NewsSite(name, 'utf-8', url, date_format, node_xpath, parse_node) ]
# end of ZhengFuWang

def ZhengJianHui():
    def parse_node(node):
        anchor = node.xpath('./a')[0]
        title = anchor.attrib['title']
        url   = anchor.attrib['href']
        try:
            date = node.xpath('./span/text()')[0]
        except IndexError:
            # This is just because of a terrible lxml bug:
            # looks like very occassionally a normal input
            # will be parsed into ./a/span
            date = anchor.xpath('./span/text()')[0]
        return (title, url, date)

    name = '中国证监会'
    url = 'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd/'
    date_format = '%Y-%m-%d'
    node_xpath = '//div[@class="er_main"]/div[@class="er_right"]//li'
    return [ NewsSite(name, 'utf-8', url, date_format, node_xpath, parse_node) ]
# end of ZhengJianHui

def all ():
    return (
        ZhengJianHui() +
        ZhengFuWang() +
        GuoTuZiYuanBu() +
        ShangWuBu() +
        KeJiBu() +
        NongYeBu() +
        CaiZhengBu() +
        FaGaiWei()
    )


