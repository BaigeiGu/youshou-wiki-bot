import io
import re
from pathlib import Path

import cnocr
from PIL import Image

CnOCR = cnocr.CnOcr()


def cutHeader(_img: io.BytesIO | io.FileIO | Path) -> Image.Image:
    img = Image.open(_img)

    p = CnOCR.ocr(img, min_box_size=24)
    # min_box_size用于防止出现类似第12话的空白文本框

    found = False

    # 如果ocr失败就整张图全丢上去
    top = img.size[1]

    for i in p:
        if re.findall('第(.+)话', i['text']) != []:
            # 获取标题字符顶部的y坐标
            top = min([i[1] for i in p[i]['position']])
            # 再往上拉几个像素
            top -= 10

            # 找到标题之后直接退出
            found = True
            break

    if found == False:
        if len(p) >= 2:
            # 如果监测到至少两串文字按第二个取 反正有兽焉三个字1000%会识别成什么奇怪东西 大多数情况下第二个应该就是标题了
            top = min([i[1] for i in p[1]['position']])
            found = True

    img1 = img.crop((0, 0, img.size[0], top))

    img.close()

    return img1
