#!/usr/bin/env python3
'''
Generate images with masks
counted as (mask folders ** masks in each folder).
First masks folder used as base for others
'''

import os
from threading import Thread
from secrets import token_hex
from PIL import Image

masks = []
def prepare_func():
    '''
    Generate list of masks files in masks_dir and create current out folder.
    Folder names important for merging and layer order (so masks list sorted).
    Used fixed depth of folders: main masks folder / masks category folders.
    '''
    for mask_dir in sorted(os.listdir(masks_dir)):
        if len(os.listdir(masks_dir + mask_dir)):
            masks.append([])
            for mask in os.listdir(masks_dir + mask_dir):
                masks[len(masks) - 1].append(masks_dir + mask_dir + "/" + mask)

    if not os.path.exists(out_dir + dir_name):
        os.mkdir(out_dir + dir_name)

def make_image(*args):
    '''
    Merge images from given files.
    Set background color for new image from upper-left pixel of first image
    '''
    image = Image.open(args[0])
    bg_color = image.getpixel((0,0))
    new_image = Image.new("RGB", out_size, bg_color)
    for i in range(len(args)):
        if i > 0:
            image = Image.open(args[i])
        new_image.paste(image, center_xy, image)
    file_name = token_hex(8) + ".png"
    new_image.save(out_dir + dir_name + file_name,"PNG")

def generate_images(mask_num = 0, *args):
    '''
    Recursion for all masks. Calls make_image for each iteration
    Each mask from first folder ignored and used as base for others
    '''
    if mask_num < len(masks):
        for i in masks[mask_num]:
            if len(args) > 1:
                th = Thread(target=make_image, args=(*args,i))
                th.start()
                #make_image(*args,i)
            generate_images(mask_num + 1, *args, i)

out_size = (1024, 1024)
mask_size = (64, 64)
center_xy = (int((out_size[0] - mask_size[0]) / 2), int((out_size[1] - mask_size[1]) / 2))

masks_dir = "masks/"
out_dir = "out/"
dir_name = token_hex(8) + "/" # folder name for each iteration inside out_dir

prepare_func()
generate_images()
