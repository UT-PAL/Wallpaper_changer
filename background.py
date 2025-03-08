#need to install
# requests,bs4,pyautogui, pillow, schedule

import requests
import random
import os
import time
import tempfile
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
import ctypes,sys
import cloudscraper

search_query=['https://4kwallpapers.com/','https://www.uhdpaper.com/','https://www.pexels.com/search/4k%20wallpaper/']

#wallpaper_dir= os.path.join(os.getenv("APPDATA"),"wallpaper_changer")
script_path = os.path.abspath(sys.argv[0])
print(script_path)
bg_storage = r"C:\WallpaperChanger"

if not os.path.exists(bg_storage):
    os.makedirs(bg_storage)

###############dummy code###############
def random_math_operations():
    x = 123456
    y = x * 42 / 7 + 19
    return y




def fetch_picture():
    scraper = cloudscraper.create_scraper()
    selected_url = random.choice(search_query)
    response = scraper.get(selected_url)
    soup = BeautifulSoup(response.text,"html.parser")
    images = [urljoin(selected_url, img["src"]) for img in soup.find_all("img", src=True)]
    if not images:
        print("no image found")
        return None
    img_url = random.choice(images)
    img_data = requests.get(img_url,stream=True)
    img_path = os.path.join(bg_storage,"wallpaper.jpg")
    print(img_path)
    with open (img_path,"wb") as file:
        for chunk in img_data.iter_content(1024):
            file.write(chunk)
    print(f"downloaded new wallpaper:{img_path}")
    #To check validity of the image otherwise black screen 
    try:
        with Image.open(img_path) as img:
            img.verify()  # Check if image is valid
            image = Image.open(img_path)
            print(image.size)
            if image.size < (500,500):
                return fetch_picture()
            print("Image is valid.")
    except (IOError, SyntaxError) as e:
            print(f"Error: Image is not valid. {e}")
            return None
    return img_path

def apply_background():
    for i in range(10):  # Try up to 3 times
        img_path = fetch_picture()
        print(i)
        if img_path:
            print("valid image")
            break
    if not img_path:
        print(f"Failed to download a valid image after {i+1} attempts.")

    image_path = os.path.abspath(img_path)
    print(f"Wallpaper changed successfully: {image_path}")
    return ctypes.windll.user32.SystemParametersInfoW(20,0,image_path,3)


# for windows to run the script every minutes and save it for later run 
def is_task_scheduled(task_name="wallpaper"):
    result = subprocess.run(
        ["schtasks","/Query","/TN",task_name],
            capture_output=True,
            text=True
    )
    # Debugging output
    print(f"Task Query Output:\n{result.stdout}")
    print(f"Task Query Error:\n{result.stderr}")

    # If "cannot find the file specified" appears, the task does NOT exist
    if "ERROR: The system cannot find the file specified." in result.stderr:
        return False
    
    return result.returncode == 0  # If returncode is 0, task exists
#function to add script to task scheduler
def add_to_task_scheduler():
    task_name= "wallpaper"
    python_path=sys.executable
    exe_path = sys.executable
    task_command = (
        f'schtasks /Create /SC MINUTE /MO 2 /TN "{task_name}" '
        #f'/TR "{exe_path}" /RU "{os.getlogin()}" /F' #to run the exe file hideway
        f'/TR "{python_path} {script_path}" /F'  #to run the code in the terminal
    )
    r=subprocess.run(task_command,shell=True)
    if r.returncode==0:
        print(f"task '{task_name}' added to the task scheduler")
        return True
    else:
        print(f"Error while creating task: {r.stderr}")
        return False
    
##################################for license###########################################
import platform
def get_machine_id():
    sys_info = platform.uname()
    return f"{sys_info.system}-{sys_info.node}-{sys_info.release}"


def generate_license():
    """Generate a license key based on the machine ID."""
    machine_id = get_machine_id()
    with open("readme.txt", "w") as f:
        f.write(machine_id)
    print("License generated successfully!")
    return machine_id

def validate_license():
    """Validate the existing license file."""
    try:
        with open("readme.txt", "r") as f:
            stored_license = f.read()
            print("stored",stored_license)
        
        machine_id = get_machine_id()
        expected_license = machine_id
        print("lic",expected_license)
        if stored_license == expected_license:
            print("License validated successfully!")
            return True
        else:
            print("Invalid license!")
            return False
    except FileNotFoundError:
        print("License file not found! Generate one first.")
        return False
    

if __name__ == "__main__":
    if not is_task_scheduled():
        try:
            generate_license()
            validate_license()
        except FileNotFoundError:
            print("issues file not found")   
        print(random_math_operations())
        add_to_task_scheduler()
        print("hey , you should see a new task in the task scheduler now")
        apply_background()
    else:
        print("task is already scheduled")
        apply_background()









