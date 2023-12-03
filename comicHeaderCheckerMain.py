import logging

import Config
from comic import *
from comicHeaderCutter import cutHeader

import common


# 配置logging
logging.basicConfig(level=Config.LOG_LEVEL)

# 添加站点并登录
     
site = common.login()
logging.info('已登录')


comic_detail = getComicDetail(Config.COMIC_ID)
Episode_list = comic_detail['data']['ep_list']

# 最新免费话
selectingEpisode = Episode_list[3]

ImgList = getImageList(selectingEpisode['id'])
headerImgBin = getImage(ImgList[0]['path'])

headerImgCutted = cutHeader(headerImgBin)
imgdesc = common.generate_wikitext(Config.IMG_TEMPLATE1_PATH,
                            {'episode': selectingEpisode['short_title']})