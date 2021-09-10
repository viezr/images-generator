# Image generator
Generate all variants of images combinations.

## Features
- Any number of layers (folders), images
- Lock number of layer folders, to generate in all images
- Center input image if output image is bigger (optional)
- Organize output images to specific collection (optional)

## About layers and source images
Input folder contain other folders used as layers.  
Each layer folder contain source images. Empty folders are omitted.  
Number of files and folders, their names, doesn't matter, 
but important for sorting and merging order. Layers list will be sorted.  
Used fixed depth of folders: "main layers folder" / "layer folder".  
By default, first layer folder used as base for all images.

## Other notes
Background color for new image sets from upper-left pixel of first image.  
If enabled in config, organize generated images to specific collection
(each file will be placed in separate folder named same as file,
with description text file).  
Threads using with semaphore.
