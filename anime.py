import io
import json
import time
from string import Template

import requests

import Config


def get_ep_data(ep_id: int) -> dict:
    # 通过B站接口获取动画更新数据
    url = f'https://api.bilibili.com/pgc/view/web/season?ep_id={ep_id}'
    with requests.get(url, headers=Config.HEADER) as r:
        data = json.loads(r.text)
        if data['message'] == 'success':
            return data
        else:
            raise TypeError

def formatdata(data):
    args = {}
    args['title'] = data['long_title']

    episode = int(data['title'])
    if episode <= 12:
        args['season'] = 1
        args['episode'] = episode
    elif episode <= 24:
        args['season'] = 2
        args['episode'] = episode-12

        args['title'] = args['title'].split(' ')[1]
        # 去除第二季前缀

    args['date'] = time.strftime("%Y-%m-%d", time.localtime(data['pub_time']))
    args['datezh'] = time.strftime("%Y年%#m月%#d日",
                                   time.localtime(data['pub_time']))

    match data['badge']:
        case '会员':
            args['needpay'] = 'yes'
            args['status'] = '3'
        case '限免':
            args['needpay'] = 'limited'
            args['status'] = '2'
        case '预告':
            args['needpay'] = 'no'
            args['status'] = '预告'
        case '':
            args['needpay'] = 'no'
            args['status'] = '1'

    args['link'] = 'ep' + str(data['ep_id'])

    args['next'] = '待更新'
    args['color'] = '#22cbde'

    if data['cover'][-4:] == 'webp':
        args['imgformat'] = 'webp'
    elif data['cover'][-3:] == 'jpg':
        args['imgformat'] = 'jpg'
    elif data['cover'][-3:] == 'png':
        args['imgformat'] = 'png'

    return args

def generate_wikitext(template_path, data):
    with open(template_path, encoding='UTF-8') as f:
        template = Template(f.read())
    t = template.safe_substitute(formatdata(data))
    return t

def get_latest(epid):
    a = get_ep_data(epid)
    ep = a['result']['episodes']

    if ep[-1]['badge'] != '预告':
        latest = ep[-1]
    else:
        latest = ep[-2]

    return latest

def get_title(latest):
    episode = int(latest['title'])
    season = 1
    if episode <= 12:
        episode = episode
    elif episode <= 24:
        season = 2
        episode = episode-12
    return f"第{season}季第{episode}集"

def dl_img(url: str):
    with requests.get(url, headers=Config.HEADER) as r:
        return io.BytesIO(r.content)


