import json
import logging

import requests
from mwclient import Site

HEADER = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Uesr-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79'
}

BMangaApiUrl = {
    'ComicDetail': 'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web',
    'GetEpisode': 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web',
    'GetImageIndex': 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web',
    'ImageToken': 'https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web',
}


def getComicDetail(comic_id: int) -> dict:
    # 获取漫画信息
    r = requests.post(BMangaApiUrl['ComicDetail'],
                      headers=HEADER,
                      params={'comic_id': comic_id})
    res = json.loads(r.text)
    if res['code'] == 0:
        return res
    else:
        raise TypeError


def read_episode(episode: int) -> str:
    with open(f'/wikitext/{episode}.txt', encoding='UTF-8') as f:
        return f.read()


def get_latest_episode(comicDetail):
    for i in comicDetail['data']['ep_list']:
        if i['short_title'] != '请假条':
            if i['is_locked'] == False:
                return i


def get_cn_number(number):
    num_map = {
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九',
        '0': '〇'
    }
    chars = list(str(number))
    output = ''
    for i in chars:
        output += num_map[i]
    return output


site = Site(host='wiki.zorua.top',
            path='/',
            clients_useragent='NsunBot/0.0.1')

site.login('bot的用户名', 'bot的密码')

logging.info('登录完成')
detail = getComicDetail(29329)

latest_episode = get_latest_episode(detail)
logging.info('漫画信息获取完成')

page_title = f"第{latest_episode['short_title']}话"
logging.info(f'最新话：{page_title}')

page = site.pages[page_title]
if page.exists:
    logging.error('页面已存在')
else:
    logging.info(f'页面不存在 将创建新页面：{page_title}')
    # 编写页面
    page.edit(
        read_episode(int(latest_episode['short_title'])),
        '漫画更新',
        bot=True)
    logging.info(f'页面创建完成')

# 添加重定向
ep_cn = get_cn_number(latest_episode['short_title'])

titles = [
    latest_episode['title'],
    f'第{get_cn_number(ep_cn)}话',
    f"{latest_episode['short_title']}话"
]

for i in titles:
    page = site.pages[i]
    if page.exists:
        logging.error('重定向页面已存在')
    else:
        logging.info(f'重定向页面不存在 将创建新页面：{i}')
        page.edit(
            f"#REDIRECT [[第{latest_episode['short_title']}话]]",
            f"创建第{latest_episode['short_title']}话重定向",
            bot=True)
    logging.info(f'重定向页面创建完成')
