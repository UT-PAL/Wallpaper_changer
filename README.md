Wallpaper Changer
This Python script allows you to download and set a random 4K wallpaper from various online sources. It also integrates with the Windows Task Scheduler to automate the wallpaper change process at regular intervals. The script includes a built-in licensing mechanism to ensure that it is being used legally on a given machine.

Features
Random Wallpaper Fetching: Downloads a random 4K wallpaper from predefined sources such as 4kWallpapers, uhdpaper, and Pexels.
Automatic Wallpaper Change: Once a valid image is downloaded, it sets the image as the desktop wallpaper on Windows.
Windows Task Scheduler Integration: The script can be scheduled to run at regular intervals (every 2 minutes) using the Windows Task Scheduler, ensuring your wallpaper is periodically updated.
Licensing Mechanism: Each installation generates a unique license based on the machine ID to ensure that the script is used legally.
Script Explanation
Fetching Wallpaper: The fetch_picture() function uses cloudscraper to fetch images from random wallpaper sites. The images are then saved locally.
Wallpaper Validation: After downloading an image, the script checks whether the image is valid using the PIL (Pillow) library.
Background Application: Once a valid wallpaper is downloaded, the apply_background() function sets it as the desktop wallpaper using ctypes.windll.user32.SystemParametersInfoW.
Task Scheduling: The add_to_task_scheduler() function ensures that the script runs automatically every 2 minutes using the Windows Task Scheduler.
License Management: A unique license key is generated based on the machine ID using platform.uname(). This ensures that the script is being used only on the machine it was activated on.
Licensing
The script generates a license based on the machine ID. The generate_license() function will create a license file (readme.txt) containing the machine’s ID. The validate_license() function checks whether the current machine’s ID matches the one in the license file.

License Generation and Validation:
When you first run the script, it will create a license file with a unique machine ID.
The script will validate this license to ensure the program is used legally on the specified machine.
If you have trouble with the license file (e.g., if it’s missing or invalid), the script will inform you and will not continue running.

Adjusting Task Schedule
The script is configured to run every 2 minutes. You can modify the frequency by adjusting the /SC MINUTE /MO 2 part in the task creation command:

bash
Copy
schtasks /Create /SC MINUTE /MO 2 /TN "wallpaper" /TR "{python_path} {script_path}" /F
License Issues
File Not Found: If the script cannot find the readme.txt license file, it will prompt you to generate a new license.
Invalid License: If the machine ID in the license file does not match the current machine, the script will display an error and stop execution.
Task Scheduler Not Working
Task Not Found: If the task is not scheduled, try running the script again to add it to the Task Scheduler.
Permissions: Ensure you are running the script with appropriate permissions to allow Task Scheduler to create a new task.


NB. always run the exe file with admin support
