import ctypes, os, requests, re, time, wget, sys, tempfile
from system import System
from random import randint
from datetime import datetime

# Directory where the downloaded images will be stored 
potd_dir = tempfile.gettempdir() + "/potd/"
s = System()

def set_wallpaper(path):
    s.set_wallpaper(file_loc=path, first_run=True)

def get_formatted_date(timestamp, formatting='%Y%m%d'):
    return datetime.utcfromtimestamp(timestamp).strftime(formatting)

# This is used to get a random image from the NASA APOD archive
# The images there are addressable by their post date timestamp
def get_date():
    startFrom = 1420070400 # 1st of Jan, 2010
    endAt = int(time.time())
    
    randomStamp = randint(startFrom, endAt)
    date_string = get_formatted_date(randomStamp)
    
    return date_string[2:]

def get_files():
    return os.listdir(potd_dir)
    
def delete_old_images():
    for file in get_files():
        os.remove(potd_dir + file)

def todays_image_downloaded():
    try:
        files = get_files()
    except FileNotFoundError:
        return False

    if len(files) == 0:
        return False
    else:
        file_date = int(files[0].replace('.jpg', ''))
        file_date = get_formatted_date(file_date)
        todays_date = get_formatted_date(int(time.time()))
        
        return (todays_date == file_date)

def log(message):
    date = get_formatted_date(timestamp=time.time(), formatting='%Y-%m-%d %H:%M:%S')
    try:
        with open('error.log', 'a+') as f:
            f.write(f'{date} -- {message}\n')
    except IOError as e:
        print(str(e))

def get_image(img_location):
    site_link = 'https://apod.nasa.gov/'
    
    r = requests.get(site_link + img_location)
    pattern = re.compile(r'href.*?image.*\.[a-z]{3}')
    img_location = pattern.search(r.text)
    
    assert type(img_location) is re.Match, "no image was found, nasa likely has a video as the potd today"

    img_location = img_location.group().replace('href="', '')
    image_name = str(int(time.time())) + ".jpg"
    
    wget.download(site_link + img_location, out=potd_dir + image_name)

    return image_name

def run():
    if len(sys.argv) > 1 and '--random' in sys.argv[1]:
        img_location = f"apod/ap{get_date()}.html"
    else:
        if todays_image_downloaded(): quit()
        
        img_location = "apod/astropix.html"
        
    try:
        delete_old_images()

        image_name = get_image(img_location)
        set_wallpaper(path=potd_dir + image_name)
    except FileNotFoundError:
        os.makedirs(name=potd_dir, exist_ok=False)
        run()
    except AssertionError as e:
        log(str(e))


if __name__ == '__main__':
    run()
    
    
