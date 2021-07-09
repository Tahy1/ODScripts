import json, random
import os

JSON_PATH = 'action_wear_all.json'
train_ratio = 0.7

json_name = os.path.splitext(os.path.split(JSON_PATH)[-1])[0]
a = json.load(open(JSON_PATH))
images = a['images']
annotations = a['annotations']
categories = a['categories']
random.shuffle(images)
random.shuffle(images)
train_images = images[:int(len(images)*train_ratio)]
val_images = images[int(len(images)*train_ratio):]
train_imgidx = []
val_imgidx = []
for i in train_images:
    train_imgidx.append(i['id'])
for i in val_images:
    val_imgidx.append(i['id'])
train_annotations = []
val_annotations = []
for i in annotations:
    if i['image_id'] in train_imgidx:
        train_annotations.append(i)
    if i['image_id'] in val_imgidx:
        val_annotations.append(i)

train_json = dict(images=train_images, annotations=train_annotations, categories=categories)
val_json = dict(images=val_images, annotations=val_annotations, categories=categories)

json.dump(train_json, open('%s_train.json'%json_name, 'w'))
json.dump(val_json, open('%s_val.json'%json_name, 'w'))
