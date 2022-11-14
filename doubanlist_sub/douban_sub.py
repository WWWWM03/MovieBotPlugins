import random
import re

import requests
from lxml import etree
import time
import logging
import math
from mbot.core.params import ArgSchema, ArgType
from mbot.core.plugins import plugin, PluginCommandContext, PluginCommandResponse
from mbot.openapi import mbot_api

server = mbot_api
_LOGGER = logging.getLogger(__name__)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Cookie": 'talionnav_show_app="0"; douban-fav-remind=1; gr_user_id=f9a0ef84-8dc3-4b4b-a7bc-a1352aac6f1a; ll="108288"; __gads=ID=75657e16628bbb3b-22d359e1fad000c2:T=1647326733:RT=1647326733:S=ALNI_MZI5klIMOEvILRHPHChCje4RFbHzw; __gpi=UID=000006cbd06f5ada:T=1655703179:RT=1663662807:S=ALNI_MZEguntr-jBZvVtCOK6XK8tdHTMhw; __utma=30149280.1601438195.1598874039.1660627136.1663662808.20; __utmc=30149280;  dbcl2="206223078:WsuK9BYuAhY"; ck=sd8t; frodotk="ebd2ab03388fdde0c3780109a9af99a0"; push_noty_num=0; push_doumail_num=0; bid=iw51NQrzuXY; vtd-d="1"; ct=y; talionusr="eyJpZCI6ICIyMDYyMjMwNzgiLCAibmFtZSI6ICJXV1dXV1dXVyJ9"; Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1668255382; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1668255382'
}


def parse_douban_id(douban_id):
    if douban_id:
        if str(douban_id).find("douban.com/doulist/") != -1:
            re_id = re.search(r'\d+', str(douban_id))
            if re_id:
                douban_id = int(re_id.group())
            else:
                douban_id = None
    return douban_id


@plugin.command(name='doubansub', title='豆瓣片单订阅', desc='输入豆瓣片单链接批量订阅影片', icon='Bookmark', run_in_background=True)
def doubanlist_sub_command(ctx: PluginCommandContext, url: ArgSchema(ArgType.String, '豆单地址', '输入豆单链接或者豆单编号')):
    dou_id = parse_douban_id(url)
    _LOGGER.info(f'豆瓣listId：{dou_id} 加载成功')
    try:
        get_urllist(dou_id)
        return PluginCommandResponse(True, f'豆瓣listId：{dou_id} 运行成功')
    except Exception as e:
        _LOGGER.error(f'豆单订阅失败', e)
        return PluginCommandResponse(False, f'豆单订阅失败：{dou_id}')


def douban_get(doubanid):
    meta = server.douban.get(doubanid)
    return meta


def get_urllist_pagenumber(doubanlist):
    url_page = "https://www.douban.com/doulist/{}/?start=".format(doubanlist)
    res = requests.get(url_page, headers=HEADERS).text
    html = etree.HTML(res)
    if html.xpath('//*[@id="content"]/div/div[@class="article"]/div[@class="doulist-filter"]/a/span/text()')[0].strip(
            '()') != []:
        get_urllist_pagenumber = \
            html.xpath('//*[@id="content"]/div/div[@class="article"]/div[@class="doulist-filter"]/a/span/text()')[
                0].strip(
                '()')
    else:
        quit()
    get_urllist_pagenumber = math.ceil(int(get_urllist_pagenumber) / 25)
    print(f"共{get_urllist_pagenumber}页")
    return get_urllist_pagenumber


def get_urllist(doubanlist):
    url_list = ["https://www.douban.com/doulist/{}/?start={}".format(doubanlist, i * 25) for i in
                range(get_urllist_pagenumber(doubanlist))]
    get_movie(url_list)


def get_movie(urls):
    rank = 1
    for url in urls:
        res = requests.get(url, headers=HEADERS).text
        html = etree.HTML(res)
        lis = html.xpath('//*[@id="content"]/div/div[@class="article"]/div[@class="doulist-item"]')
        for li in lis:
            if li.xpath('.//div[@class="title"]/a/@href') != []:
                doubanid = li.xpath('.//div[@class="title"]/a/@href')[0].split('/')[4]
                server.subscribe.sub_by_douban(doubanid)
                print(f'第{rank}项，'
                      f'豆瓣id：{doubanid},')
                rank += 1
                # _LOGGER.info(f'豆瓣id：{doubanid}')
            else:
                pass
        time.sleep(random.randint(3, 8))
