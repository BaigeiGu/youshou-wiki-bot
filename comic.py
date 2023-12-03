import io
import json

import Config
import requests

BMangaApiUrl = {
    'ComicDetail': 'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web',
    'GetEpisode': 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web',
    'GetImageIndex': 'https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web',
    'ImageToken': 'https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web',
}


def getComicDetail(comic_id: int) -> dict:
    # 获取漫画信息
    r = requests.post(BMangaApiUrl['ComicDetail'],
                      headers=Config.HEADER,
                      params={'comic_id': comic_id})
    res = json.loads(r.text)
    if res['code'] == 0:
        return res
    else:
        raise TypeError


def getImageList(ep_id: int) -> dict:
    # 获取每话的图片信息
    r = requests.post(BMangaApiUrl['GetImageIndex'],
                      headers=Config.HEADER, params={'ep_id': ep_id})
    res = json.loads(r.text)
    if res['code'] == 0:
        return res['data']['images']


def getImage(imgurl: str) -> io.BytesIO:
    # 获取每话的图片
    r = requests.post(BMangaApiUrl['ImageToken'],
                      headers=Config.HEADER, params={
                          'urls': f"""[\"{imgurl}\"]"""},
                      cookies={'SESSDATA': Config.BILI_SESSDATA})
    res = json.loads(r.text)
    r.close()

    if res['code'] != 0:
        raise KeyError
    url = res['data'][0]['url'] + '?token=' + res['data'][0]['token']

    r = requests.get(url,
                     headers=Config.HEADER,
                     cookies={'SESSDATA': Config.BILI_SESSDATA})

    print('Downloaded.')

    return io.BytesIO(r.content)


def getHeader(ep: int | None = None)  -> io.BytesIO:
    comic_detail = getComicDetail(Config.COMIC_ID)
    Episode_list = comic_detail['data']['ep_list']
    
    if ep == None:
        selectingEpisode = Episode_list[3]
    else:
        ord_Episodelist = {i['short_title']: i for i in Episode_list} # 这样会干掉好几个请假条（
        selectingEpisode = ord_Episodelist['{:0>3d}'.format(ep)] #001补上0
    
    ImgList = getImageList(selectingEpisode['id'])
    headerImgBin = getImage(ImgList[0]['path'])
    
    return headerImgBin