#!/usr/bin/env python3

from secrets import token_hex

'''
Main settings
- locket_masks: a number of masks directories (from begining) to be
  generated for all pictures (with all masks inside). Numbers 0 and 1
  set equal parameters, because first masks directory is always generated,
  as base layer
- gen_dir: random folder name for each generation inside out_dir
'''
main_set = {
    "locked_masks": 2,
    "layers_dir": "layers/",
    "out_dir": "out/",
    "gen_dir": token_hex(8) + "/",
    "max_threads": 3
}

'''
Images properties
By default background color set from top-left pixel color of first layer image
If mask is smaller than out_size, it may be centered.
'''
image_set = {
    "out_size": (512, 512),
    "mask_size": (256, 256),
    "centered_mask": True,
    "in_ext": "png",
    "out_ext": "png"
}

'''
Collection properties
If enabled, each file will be placed in separate folder named as file,
with description text file.
At the end of name_id main script adds id number.
'''
collection = {
    "enabled": False,
    "start_id": 1,
    "name": "Sample collection"
}
collection["name_id"] = f"SUBJECT: {collection['name']} #"
collection["description"] = f"DETAILS: {collection['name']} is an ..."

