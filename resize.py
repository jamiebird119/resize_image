from PIL import Image, ImageOps
import csv
import os
from os import listdir


def resize_image(image, size):
    # Load image and resize using pillow - currently not maintaining aspect ratio
    img = Image.open(image)
    fname = image.replace("images/", "").replace(".jpg", "").replace(".png", "")

     # Convert size from cm to pixels
    newsize = (int(size[0]*37.795275591),int(size[1]*37.795275591)) 

    # Set border at 5% of original image
    border = (int((newsize[0]/100)*5),int((newsize[1]/100)*5))

    img_new =  ImageOps.expand(img, border=border, fill="#fff")


    # Image is resized below - Can be edited to specification
    img_new_resized = img_new.resize(newsize)
    size_string = f"{size[0]}cmx{size[1]}cm"

    

    # Uses image dpi however if info not available will return false
    if 'dpi' in img_new_resized.info.keys() :
        dpi = img_new_resized.info['dpi']
        if dpi >= 300:
            img_new_resized.save(f"./resized_images/{fname}-{size_string}.jpg","JPEG")
            return size_string
        else:
            return False
    else:
        area_cm = size[0]* size[1]
        area_inch = 0.393701*area_cm
        dpi = (newsize[0]*newsize[1])/area_inch 
        if dpi >= 300:
            img_new_resized.save(f"./resized_images/{fname}-{size_string}.jpg","JPEG")
            return size_string
        else:
            return False
        


def resize_and_write():
    # takes images in image_folder
    image_folder = os.listdir("images")

    # Add desired sizes here in nested list format
    # [[x1,y1],[[x2,y2]] etc
    #

    sizes = [[29.7,42],[21,29.7],[14.8,21],[30,40],[45,60]]

    # Will take each file in image_folder and run the resize saving only if dpi matches specification and adding to csv file 
    for f in image_folder:
        file_path = f"images/{f}"
        with open('info.csv','a') as fd:
            applied_sizes =[]
            fieldnames = ["filename", "sizes"]
            writer = csv.DictWriter(fd, fieldnames=fieldnames)
            for size in sizes:
                img_resize_function = resize_image(file_path, size)
                if img_resize_function:
                    if img_resize_function == "Does Not Contain DPI info":
                        applied_sizes = "Does Not Contain DPI info"
                    else:    
                        applied_sizes.append(img_resize_function)
            writer.writeheader()       
            writer.writerow({"filename": f, "sizes": applied_sizes})

resize_and_write()