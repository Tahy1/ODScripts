# -*- coding: utf-8 -*-
"""
Created on Mon May 13 19:13:55 2019
这是保证mmdet能够运行的最小json文件结构
输入data/xx_annotations.csv的格式为
0:图片名称  1:框类别  2:x  3:y  4:框宽  5:框高
@author: Tahy
"""

import csv, json
from PIL import Image
import numpy as np

def xymodify(psize, bpos):  #允许坐标位于图像的边缘，修正超出边缘的坐标
    w_bias = 0
    h_bias = 0
    if bpos[0] >= psize[0]:
        w_bias = bpos[0] - psize[0] + 1
    if bpos[1] >= psize[1]:
        h_bias = bpos[1] - psize[1] + 1
    return bpos[0] - w_bias, bpos[1] - h_bias

def boxmodify(psize, bbox):  #当框超过图像边缘时，截去超过边缘的部分，框允许位于图像边缘。
    bx, by = xymodify(psize, (bbox[0], bbox[1]))
    bw = bbox[2]
    bh = bbox[3]
    xmin = bx - bw / 2
    xmax = bx + bw / 2
    ymin = by - bh / 2
    ymax = by + bh / 2
    if xmax >= psize[0]:
        xmax = psize[0] - 1
    if xmin < 0:
        xmin = 0
    if ymin < 0:
        ymin = 0
    if ymax >= psize[1]:
        ymax = psize[1] - 1
    bx = xmin
    by = ymin
    bw = xmax - xmin
    bh = ymax - ymin
    return [bx, by, bw, bh]
        

with open('data/train_annotations.csv','r') as fr:
    reader = csv.reader(fr)
    lines = [i for i in reader]
    del lines[0]
lines = np.array(lines)
ids = sorted(list(set(lines[:,0].tolist())))  #这里去除了重复的id
classes = sorted(list(set(lines[:,1].tolist())))  #这里去除了重复的classes
lines = lines.tolist()
jsonSet = {'images':[], 'annotations':[], 'categories':[]}

#0:id  1:classes  2:x  3:y  4:w  5:h
for index in range(len(ids)):
    im = Image.open('data/coco/train2017/'+ids[index])
    width, height = [im.size[0],im.size[1]]
    jsonSet['images'].append({'file_name': ids[index], 'id': ids[index].split('.jpg')[0], 'width': width, 'height': height})
for index in range(len(classes)):
    jsonSet['categories'].append({'id':classes[index], 'name':classes[index]})
for index in range(len(lines)):
    bbox = [int(lines[index][i]) for i in range(2,6)]
    im = Image.open('data/coco/train2017/'+lines[index][0])
    psize = [im.size[0],im.size[1]]
    bbox = boxmodify(psize, bbox)
    jsonSet['annotations'].append({'id':index,
                                   'image_id':lines[index][0].split('.jpg')[0],
                                   'category_id':lines[index][1],
                                   'bbox':bbox,
                                   'iscrowd':0,
                                   'area':bbox[2]*bbox[3]})
with open('data/coco/annotations/train2017.json','w') as fw:
    json.dump(jsonSet, fw)
print('Done!')