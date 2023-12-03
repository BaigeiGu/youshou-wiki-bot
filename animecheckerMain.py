import logging

import Config

import common
from anime import *

# 配置logging
logging.basicConfig(level=Config.LOG_LEVEL)

# 添加站点并登录

site = common.login()
logging.info('已登录')

# 获取动画更新信息
latest = get_latest(Config.ANIME_ID)
page_title = get_title(latest)
logging.info('动画更新数据获取完成')

# 查询页面是否存在
logging.info('开始创建最新话页面')
page = site.pages[page_title]
if page.exists:
    logging.error('页面已存在')
else:
    logging.info(f'页面不存在 将创建新页面：{page_title}')
    # 编写页面
    page.edit(generate_wikitext(
        Config.TEMPLATE_PATH, latest), '动画更新',bot=True)
    logging.info(f'页面更新完成')


# 查询图片是否存在
logging.info('开始上传最新话封面')
img_title = f"{page_title}封面{latest['cover'][-4:]}"
img = site.images[img_title]
if img.exists:
    logging.error('图片已存在')
else:
    logging.info(f'封面不存在 将上传封面：{img_title}')
    # 上传图片
    r = site.upload(dl_img(latest['cover']),
                img_title,
                generate_wikitext(Config.IMG_TEMPLATE_PATH, latest))
    if r['result'] == 'Success':
        logging.info(f'图片上传成功')
    else:
        logging.error(f'图片上传失败：\n{r}')

logging.info('任务完成')
