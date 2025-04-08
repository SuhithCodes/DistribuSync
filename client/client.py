import os
import rpyc
import threading
import concurrent.futures
import subprocess


#this code requests the server for performing certain activities .
#When a file is uploaded it can be seen in client/client/Upload

# Define a global thread pool executor
executor = concurrent.futures.ThreadPoolExecutor()

#defining helper client scripts to run
async_script = 'client/async_client.py'
sync_script = 'client/sync_client.py'

# starting synchornization
command_sync = f'start cmd /k python {sync_script}'

# Run the command
os.system(command_sync)

# Constants
COMPUTATION_SERVER_ADDRESS = "localhost"
COMPUTATION_SERVER_PORT = 50005
FILE_SERVER_ADDRESS = "localhost"
FILE_SERVER_PORT = 50000

# Define the path to the UPLOAD, DOWNLOAD AND SYNC folders
UPLOAD_FOLDER = 'client/UPLOADS'
DOWNLOAD_FOLDER = 'client/DOWNLOADS'
SYNCHRONIZED_FOLDER = 'client/SYNCHRONIZED'

# Ensure the UPLOAD, DOWNLOAD AND SYNC folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(SYNCHRONIZED_FOLDER, exist_ok=True)

# Connections to servers
file_server_conn = rpyc.connect(FILE_SERVER_ADDRESS, FILE_SERVER_PORT)
computation_conn = rpyc.connect(COMPUTATION_SERVER_ADDRESS, COMPUTATION_SERVER_PORT)

# File system functions
#this function can upload a file and even create it if not present .It also asks to enter the data .
# This makes a request to the server fo the upload.
def upload_file():
    filename = input("\nEnter filename to upload: ")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            data = file.read()
        result = file_server_conn.root.upload(filename, data)
        print(result)
    else:
        create_file = input(f"\nThe file '{filename}' does not exist. Do you want to create it? (yes/no): ")
        if create_file.lower() == 'yes':
            data = input("Enter file data: ").encode('utf-8')
            with open(file_path, 'wb') as file:
                file.write(data)
            result = file_server_conn.root.upload(filename, data)
            print(result)
        else:
            print("File creation canceled.")

def delete_file():
    filename = input("\nEnter filename to delete: ")
    result = file_server_conn.root.delete(filename)
    print(result)

def rename_file():
    old_filename = input("\nEnter current filename: ")
    new_filename = input("Enter new filename: \n")
    result = file_server_conn.root.rename(old_filename, new_filename)
    print(result)

def list_files():
    files = file_server_conn.root.list_files()
    print("\nFiles on server:\n")
    for file in files:
        print(file)

def download_file(filename):
    data = file_server_conn.root.download(filename)
    if data:
        download_path = os.path.join(DOWNLOAD_FOLDER, filename)
        with open(download_path, "wb") as f:
            f.write(data)
        print(f"\nDownloaded {filename} to {download_path}")
    else:
        print(f"Failed to download {filename}. File not found on server.\n")

# Computation functions
def add_numbers():
    i = int(input("\nEnter first number: "))
    j = int(input("Enter second number: "))
    result = computation_conn.root.add(i, j)
    print(f"Addition result: {result}")

def sort_array():
    array_str = input("\nEnter array elements separated by spaces: \n")
    array = list(map(int, array_str.split()))
    result = computation_conn.root.sort(array)
    print(f"Sorted array: {result}")

# Menus
def menu():
    print("\nMenu:\n")
    print("1. FILE SYSTEM")
    print("2. SYNC COMPUTATION SYSTEM")
    print("3. ASYNC COMPUTATION SYSTEM")
    print("4. EXIT")

def file_menu():
    print("\nFile Menu:\n")
    print("1. UPLOAD")
    print("2. DELETE")
    print("3. RENAME")
    print("4. LIST FILES ON SERVER")
    print("5. DOWNLOAD")
    print("6. GO BACK")

def sync_async_menu():
    print("\nRPC type \nDefault: SYNC: \n")
    print("1. SYNC")
    print("2. ASYNC")
    print("3. GO BACK")

#This function is for doing the computation stuff like add and sort

def computation_menu():
    print("\nComputation Menu:")
    print("1. ADD")
    print("2. SORT")
    print("3. GO BACK")

# Define threads
class HelperThread(threading.Thread):
    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self):
        self.code()

def start_upload():
    t = threading.Thread(target=upload_file)
    t.start()
    t.join()

def start_delete():
    t = threading.Thread(target=delete_file)
    t.start()
    t.join()

def start_rename():
    t = threading.Thread(target=rename_file)
    t.start()
    t.join()

def start_list_files():
    t = threading.Thread(target=list_files)
    t.start()
    t.join()

def start_download(filename):
    t = threading.Thread(target=download_file, args=(filename,))
    t.start()
    t.join()

# Main function
def main():
    while True:
        menu()
        main_choice = input("\nEnter your choice (1-4): ")

        # File system menu
        if main_choice == '1':
            while True:
                file_menu()
                file_choice = input("Enter your choice (1-6): ")

                if file_choice == '1':
                    start_upload()
                elif file_choice == '2':
                    start_delete()
                elif file_choice == '3':
                    start_rename()
                elif file_choice == '4':
                    start_list_files()
                elif file_choice == '5':
                    filename = input("\nEnter filename to download: ")
                    start_download(filename)
                elif file_choice == '6':
                    print("Going back to main menu.\n")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.\n")

        # Computation system menu
#For Add() and Sort() ,the client requests to the computation_server to perform the tasks and asks for a result.

        elif main_choice == '2':
            while True:
                computation_menu()
                computation_choice = input("\nEnter your choice (1-3): ")
                if computation_choice == '1':
                    add_numbers()
                elif computation_choice == '2':
                    sort_array()
                elif computation_choice == '3':
                    print("Going back to main menu.")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.\n")
        elif main_choice == '3':
            print("ASYNCHRONOUS OPERATION.\n")
            #defining helper client scripts to run
            async_script = 'client/async_client.py'
            # starting synchornization
            command_async = f'start cmd /k python {async_script}'
            # Run the command
            os.system(command_async)

        elif main_choice == '4':
            print("Exiting the program.\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.\n")

    file_server_conn.close()
    computation_conn.close()

if __name__ == "__main__":
    main()
 