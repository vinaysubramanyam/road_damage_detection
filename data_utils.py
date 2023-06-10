import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join
import shutil

dirs = ['China_MotorBike', 'Czech', 'India', 'Japan', 'Norway', 'United_States']
classes = ['D00', 'D10', 'D20', 'D40']
num_images = 0
total_annotations = 0

def getImagesInDir(dir_path):
    global num_images
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        num_images += 1
        image_list.append(filename)
    return image_list

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(full_annotation_path, output_path, image_path):
    global total_annotations
    total_annotations += 1
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(full_annotation_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + basename_no_ext + '.txt', 'w')

    print(image_path)
    print(output_path)
    
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        if obj.find('difficult') is None:
            continue
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        # print(f"Writing to file: {str(cls_id) + ' ' + ' '.join([str(a) for a in bb])}")
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

cwd = getcwd()
both_same = True

for dir_path in dirs:
    full_dir_path = cwd + '/RDD2022_Dataset/' + dir_path + '/train/images'
    full_annotation_path = cwd + '/RDD2022_Dataset/' + dir_path + '/train/annotations/xmls'

    image_paths = getImagesInDir(full_dir_path)
    list_file = open(full_dir_path + '.txt', 'w')

    count = len(image_paths)
    print("Total images in " + dir_path + ": " + str(count))

    train_count = int(count * 0.8)
    valid_count = int(count * 0.1)
    test_count = count - train_count - valid_count
    i = 0
    for image_path in image_paths:
        basename = os.path.basename(image_path)
        basename_no_ext = os.path.splitext(basename)[0]
        if i < train_count:
            output_txt_path = cwd +'/road_annotations/train/'
            output_image_path = cwd +'/road_images/train/'
            output_xml_path = cwd +'/road_annotations_xml/train/'
            output_image_path_rcnn = cwd +'/road_images_rcnn/train/'

        elif i < train_count + valid_count:
            output_txt_path = cwd +'/road_annotations/valid/'
            output_image_path = cwd +'/road_images/valid/'
            output_xml_path = cwd +'/road_annotations_xml/valid/'
            output_image_path_rcnn = cwd +'/road_images_rcnn/valid/'
        else:
            output_txt_path = cwd +'/road_annotations/test/'
            output_image_path = cwd +'/road_images/test/'
            output_xml_path = cwd +'/road_annotations_xml/test/'
            output_image_path_rcnn = cwd +'/road_images_rcnn/test/'
        
        if not os.path.exists(output_txt_path):
            os.makedirs(output_txt_path)
        if not os.path.exists(output_image_path):
            os.makedirs(output_image_path)
        if not os.path.exists(output_xml_path):
            os.makedirs(output_xml_path)
        if not os.path.exists(output_image_path_rcnn):
            os.makedirs(output_image_path_rcnn)
        
        xml_path = full_annotation_path + '/' + basename_no_ext + '.xml'
        
        if both_same:
            shutil.copy(image_path, output_image_path_rcnn)
            shutil.copy(xml_path, output_image_path_rcnn)
        else:
            shutil.copy(image_path, output_image_path)
            shutil.copy(xml_path, output_xml_path)

        list_file.write(image_path + '\n')
        convert_annotation(full_annotation_path, output_txt_path, image_path)
        i+=1

    list_file.close()

    print("Finished processing: " + dir_path)

print("Total images: " + str(num_images))
print("Total annotations: " + str(total_annotations))
