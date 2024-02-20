'''
-Create a folder on your computer called "week3"
-Create a script that, when run, checks every second indefinitely for a new file in that folder
-If file found, report back to the user:
    1. File found
    2. What type of file it is
    3. When it was put there
You as the user can introduce what ever file you want to invoke the notification portion of the script
(i.e put a text file, image, etc)
'''
import os
import time
from datetime import datetime

def always_checking(folder_path, previous_files):
    current_files = os.listdir(folder_path)
    #Find files that are in current_files but not in previous_files which is new_files
    new_files = [file for file in current_files if file not in previous_files]
    if new_files:
        for file in new_files:
            file_path = os.path.join(folder_path, file)
            #Get file extension
            file_type = os.path.splitext(file)[1]
            #get creation time
            file_created_time = os.path.getctime(file_path)
            file_created_time_str = datetime.fromtimestamp(file_created_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"New file found: {file}\n")
            print(f"Type: {file_type}\n")
            print(f"Created at: {file_created_time_str}")
    #returning the list of current file to be used as previous files for next iteration 
    return current_files

def main():
    folder_path = "Weekly Assignment 3\week3"

    previous_files = []
    while True:
        previous_files = always_checking(folder_path, previous_files)
        time.sleep(1) #wait for 1 second

if __name__ == "__main__":
    main()