#!/usr/bin/env python3

from secrets import token_hex

'''
Collection properties
If enabled, each file will be placed in separate folder named as file,
with description text file.
'''
collection = {
    "enabled": True,
    "start_id": 1,
    "name": "Sample collection"
}
collection["name_id"] = f"SUBJECT: {collection['name']} #"
collection["description"] = f"DETAILS: {collection['name']} is an ..."

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
System settings
- locket_masks: a number of masks directories (from begining) to be
  generated for all pictures. Numbers 0 and 1 set equal parameters,
  because first masks directory is always generated, as base layer.
- gen_dir: folder name for each generation inside out_dir
'''
main_set = {
    "locked_masks": 0,
    "layers_dir": "layers/",
    "out_dir": "out/",
    "gen_dir": token_hex(8) + "/",
    "max_threads": 3
}
