# -*- coding:utf-8 -*-
# author:xinfei
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import sys
from pytesseract import *

# 二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

    # 由于都是数字
# 对于识别成字母的 采用该表进行修正
rep = {'O': '0',
       'I': '1', 'L': '1',
       'Z': '2',
       'S': '8'
       }

def getverify1(path, name):
    # 打开图片
    im = Image.open(path + name)
    # 转化到灰度图
    imgry = im.convert('L')
    # 保存图像
    imgry.save(path + 'g' + name)
    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')
    out.save(path + 'b' + name)
    # 识别
    text = image_to_string(out)
    # 识别对吗
    text = text.strip()
    text = text.upper()
    for r in rep:
        text = text.replace(r, rep[r])
        # out.save(text+'.jpg')
    return text


