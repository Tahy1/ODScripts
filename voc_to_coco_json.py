#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: hbchen
# @Time: 2018-01-29
# @Description: xml转换到coco数据集json格式

import os, json
from tqdm import tqdm
from xml.etree.ElementTree import ElementTree

XML_PATH = 'anns'
JSON_PATH = "eval_perfect.json"
json_obj = {}
images = []
annotations = []
categories = []
categories_dict = {}
annotation_idx = 1
img_idx = 1
cls_idx = 1

def read_xml(in_path):
    '''读取并解析xml文件'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def if_match(node, kv_map):
    '''判断某个节点是否包含所有传入参数属性
      node: 节点
      kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True

def get_node_by_keyvalue(nodelist, kv_map):
    '''根据属性及属性值定位符合的节点，返回节点
      nodelist: 节点列表
      kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes

def find_nodes(tree, path):
    '''查找某个路径匹配的所有节点
      tree: xml树
      path: 节点路径'''
    return tree.findall(path)

print("-----------------Start------------------")
xml_names = []
for xml in os.listdir(XML_PATH):
    if xml.split('.')[-1] == 'xml':
        xml_names.append(xml)

for xml in tqdm(xml_names):
    tree = read_xml(XML_PATH + "/" + xml)
    object_nodes = get_node_by_keyvalue(find_nodes(tree, "object"), {})
    if len(object_nodes) == 0:
        print(xml, "no object")
        continue
    else:
        image = {}
        file_name = os.path.splitext(xml)[0];  # 文件名
        image["file_name"] = file_name + ".jpg"
        width_nodes = get_node_by_keyvalue(find_nodes(tree, "size/width"), {})
        image["width"] = int(width_nodes[0].text)
        height_nodes = get_node_by_keyvalue(find_nodes(tree, "size/height"), {})
        image["height"] = int(height_nodes[0].text)
        image["id"] = img_idx
        images.append(image)    #构建images

        name_nodes = get_node_by_keyvalue(find_nodes(tree, "object/name"), {})
        xmin_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/xmin"), {})
        ymin_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/ymin"), {})
        xmax_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/xmax"), {})
        ymax_nodes = get_node_by_keyvalue(find_nodes(tree, "object/bndbox/ymax"), {})
        for index, node in enumerate(object_nodes):
            category_name = str(name_nodes[index].text)
            if categories_dict.get(category_name) is None:
                categories_dict[category_name] = cls_idx
                categories.append(dict(id=cls_idx, name=category_name, supercategory='nothing'))
                cls_idx += 1
            category_idx = categories_dict[category_name]
            annotation = {}
            bbox = []
            width = int(xmax_nodes[index].text) - int(xmin_nodes[index].text)
            height = int(ymax_nodes[index].text) - int(ymin_nodes[index].text)
            area = width * height
            bbox.append(int(xmin_nodes[index].text))
            bbox.append(int(ymin_nodes[index].text))
            bbox.append(width)
            bbox.append(height)

            annotation["area"] = area
            annotation["iscrowd"] = 0
            annotation['segmentation'] = []
            annotation["image_id"] = img_idx
            annotation["bbox"] = bbox
            annotation["category_id"] = category_idx
            annotation["id"] = annotation_idx
            annotation_idx += 1
            annotation["ignore"] = 0
            annotations.append(annotation)
        img_idx += 1

json_obj["images"] = images
json_obj["annotations"] = annotations
json_obj["categories"] = categories

print('Writing annotations into json...')
f = open(JSON_PATH, "w")
json.dump(json_obj, f)
f.close()
print("------------------End-------------------")
