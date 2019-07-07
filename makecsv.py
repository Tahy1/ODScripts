# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:52:32 2019
制作用于产生json的中间文件data/xx_annotations.csv
@author: Tahy
"""

body = [['id','classes','x','y','w','h']]
import csv
from copy import deepcopy as dc
import pickle as pk
import numpy as np
from random import shuffle as sf

with open('ann.pkl','rb') as fr:
    have_ann = pk.load(fr)

def calc_Euclid(px,py,sx,sy):
#    px,py,sx,sy=int(px),int(py),int(sx),int(sy)
    if (px-sx)**2 + (py-sy)**2 <= 225:
        return True
    else:
        return False

def NMS(xys):
    xys = [list(map(float,i)) for i in xys]
    xys = sorted(xys)
    nms = []
    while len(xys) > 0:
        temp = [xys.pop(0)]
        c_xys = dc(xys)
        bias = 0
        if len(xys) > 0:
            for i, xy in enumerate(xys):
                if calc_Euclid(xy[0],xy[1],temp[0][0],temp[0][1]):
                    temp.append(c_xys.pop(i-bias))
                    bias += 1
        xys = c_xys
        nms.append(temp)
    ret = []
    for near in nms:
        t = np.array(near)
        t = [int(i) for i in np.mean(t,axis=0).tolist()]
        ret.append(list(map(str,t)))
    return ret
have_ann = sorted(have_ann)

def addData(i):
    users = i[-1].split('|')
    xys = []
    for user in users:
        poses = user.split(';')[:-1]
        for pos in poses:
            xys.append(pos.split(','))
    xys = NMS(xys)
    return xys

for i in have_ann:
    if 'known' in i or 'newtarget' in i\
    or 'isnova' in i or 'isstar' in i or 'asteroid' in i:
        xys = addData(i)
        for xy in xys:
            body.extend([[i[0]+'.jpg',i[3],xy[0],xy[1],'30','30']])  #如果出现某一项坐标为空的情况，for循环就不会执行，也就不会向body添加，更不会报错。
    else:
        xys = addData(i)
        for xy in xys:
            body.extend([[i[0]+'.jpg','nostar',xy[0],xy[1],'30','30']])

with open('data/test_annotations.csv','w', newline='') as fw:
#    csv_write = csv.writer(fw,dialect='excel')
    csv_write = csv.writer(fw)
    csv_write.writerows(body)