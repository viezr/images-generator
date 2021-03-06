#!/usr/bin/env python3
'''
Image generator
Generate all variants of images combinations.
First layer folder used as base for others.
'''

import os, gc
from time import time
from threading import Thread, Semaphore
from secrets import token_hex
from PIL import Image
from config import collection, image_set, main_set


masks = []
th_pool = []
sem = Semaphore(main_set["max_threads"])
center_xy = (0,0)
out_path = main_set["out_dir"] + main_set["gen_dir"]
out_ext = image_set["out_ext"]

def initial_run():
    '''
    Generate list of layers files in layers_dir and create current out folder.
    Folder names does'n matter but important for sorting and merging order.
    Layers list sorted. Empty dirs omitted.
    Used fixed depth of folders: main layers folder / layer folders.
    '''
    global center_xy, out_path
    layers_dir = main_set["layers_dir"]
    for layer_dir in sorted(os.listdir(layers_dir)):
        layer_path = layers_dir + layer_dir
        if len(os.listdir(layer_path)):
            masks.append([])
            for mask in os.listdir(layer_path):
                masks[len(masks) - 1].append(layer_path + "/" + mask)

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    if image_set["centered_mask"]:
        out_size = image_set["out_size"]
        mask_size = image_set["mask_size"]
        center_xy = (int((out_size[0] - mask_size[0]) / 2),
                     int((out_size[1] - mask_size[1]) / 2))

def make_image(*args):
    '''
    Merge images from given files.
    Set background color for new image from upper-left pixel of first image.
    Semaphore is used for threads.
    '''
    sem.acquire()
    global out_path,out_ext
    with Image.open(args[0]) as base_image:
        bg_color = base_image.getpixel((0,0))
        new_image = Image.new("RGB", image_set["out_size"], bg_color)
        new_image.paste(base_image, center_xy, base_image)
        for i in range(1,len(args)):
            mask_image = Image.open(args[i])
            new_image.paste(mask_image, center_xy, mask_image)
            mask_image.close()
        file_name = token_hex(8) + "." + out_ext
        new_image.save( out_path + file_name, out_ext.upper())
    del base_image
    del new_image
    gc.collect()
    sem.release()

def generate_variants(mask_num = 0, *args):
    '''
    Recursion for all masks. Calls make_image for each iteration
    Each mask from first layer folder ignored and used as base for others
    '''
    if mask_num < len(masks):
        for i in masks[mask_num]:
            if main_set["locked_layers"] < 2:
                th_pool.append( Thread(target=make_image, args=(*args,i)) )
            else:
                if len(args) > main_set["locked_layers"] - 2:
                    th_pool.append( Thread(target=make_image, args=(*args,i)) )
            generate_variants(mask_num + 1, *args, i)

def threads_run():
    '''
    Run threads for each iteration generated by generate_variants.
    Thread runs with semaphore and wait for completion for all threads
    '''
    for th in th_pool:
        th.start()
    for th in range(len(th_pool)):
        print("\rGenerating:", th + 1, "of", len(th_pool), "images...",
            end="", flush=True)
        th_pool[th].join()
    print("\n")

def make_collection():
    '''
    If enabled in config, organize generated images to specific collection
    By default each file will be placed in separate folder named same as file,
    with description text file.
    '''
    if not collection["enabled"]:
        print("Collection disabled")
        return
    global out_path, out_ext
    coll_id = collection["start_id"]
    coll_name = collection["name"]
    for file in os.scandir(out_path):
        if file.is_file():
            coll_dir = out_path + f"{coll_name.lower()}_{coll_id}/"
            coll_img = f"{coll_name.lower()}_{coll_id}.{out_ext}"
            coll_txt = f"{coll_name.lower()}_{coll_id}.txt"

            if not os.path.exists(coll_dir):
                os.mkdir(coll_dir)
            os.rename(file.path, coll_dir + coll_img)

            coll_text_name = collection["name_id"] + str(coll_id)
            with open(coll_dir + coll_txt, "x") as f:
                f.write(coll_text_name + "\n" + collection["description"])

            coll_id += 1

def count_time():
    '''
    Count program running time
    '''
    global start_time
    pass_time = time() - start_time
    if pass_time > 3600:
        pass_time = "Program takes {:.2f} hours".format(pass_time / 3600)
    elif pass_time > 60:
        pass_time = "Program takes {:.2f} minutes".format(pass_time / 60)
    else:
        pass_time = "Program takes {:.2f} seconds".format(pass_time)
    print(pass_time)


if __name__ == "__main__":
    start_time = time()
    initial_run()
    generate_variants()
    threads_run()
    make_collection()
    count_time()
