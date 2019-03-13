import ctypes
import os
import requests
import re
import time
import wget
import sys
import appenv
from random import randint
from datetime import datetime

def set_wallpaper(path):
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)

def get_formatted_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y%m%d')

def get_date():
    startFrom = 1262304000 # 1st of Jan, 2010
    endAt = int(time.time())
    
    randomStamp = randint(startFrom, endAt)

    date_string = get_formatted_date(randomStamp)
    
    return date_string[2:]

def get_files():
    return os.listdir(appenv.potd_dir)

def delete_old_images():
    for file in get_files():
        os.remove(appenv.potd_dir + file)

def todays_image_downloaded():
    files = get_files()
    
    if len(files) == 0:
        return False
    else:
        file_date = int(files[0].replace('.jpg', ''))
        file_date = get_formatted_date(file_date)
        todays_date = get_formatted_date(int(time.time()))
        
        return (todays_date == file_date)

def get_image(img_location):
    site_link = 'https://apod.nasa.gov/'
    
    r = requests.get(site_link + img_location)
    pattern = re.compile('href.*?image.*\.[a-z]{3}')
    img_location = pattern.search(r.text)
    
    assert type(img_location) is re.Match, "no image was found, the nasa likely has a video as the potd today"

    img_location = img_location.group().replace('href="', '')
    image_name = str(int(time.time())) + ".jpg"
    
    file = wget.download(site_link + img_location, out='/Users/hvssz/Documents/potd/' + image_name) # string encoding weirdness

    return image_name

if __name__ == '__main__':
    if 'random' not in sys.argv:
        if todays_image_downloaded(): quit()
        
        img_location = "apod/astropix.html"
    else:
        img_location = "apod/ap" + get_date() + ".html"

    delete_old_images()

    image_name = get_image(img_location)
    
    set_wallpaper(appenv.potd_dir + image_name)
