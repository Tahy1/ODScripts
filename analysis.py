import json

JSON_FILE = 'instances_val2017.json'
a = json.load(open(JSON_FILE))
images = a['images']
annotations = a['annotations']
categories = a['categories']
num_images = len(images)
num_classes = len(categories)
oirg_cate_dict = {}
for i in categories:
    oirg_cate_dict[i['id']] = i['name']
bbox_dict = {}
img_dict = {}
for i in annotations:
    bbox_dict[i['category_id']] = bbox_dict.get(i['category_id'], 0) + 1
    img_list = img_dict.get(i['category_id'], [])
    img_list.append(i['image_id'])
    img_dict[i['category_id']] = img_list
for k, v in img_dict.items():
    v = list(set(v))
    img_dict[k] = len(v)

print('一共有%d幅图像，%d种类别。\n'%(num_images, num_classes))
print('每个类别的框的数量为：')
for k, v in bbox_dict.items():
    print('类别%s的框数量为%d个'%(oirg_cate_dict[k], v))
print('\n每个类别的图像数量为：')
for k, v in img_dict.items():
    print('含有%s的图像数量为%d个'%(oirg_cate_dict[k], v))
