import os
import time
import threading
import rpyc

# This code will create a SYCHORNIZATION folder under client .
# The address will be client/client/SYNCHRONIZED.
#If any changes are made in the files in this folder it will automatically get sync to the server .
# The autosync runs every 10 seconds.
#All the changes in this folder like update ,delete ,rename will be auto synced to client

FILE_SERVER_ADDRESS = os.getenv("FILE_SERVER_ADDRESS", "localhost")
FILE_SERVER_PORT = int(os.getenv("FILE_SERVER_PORT", 50000))
SYNCHRONIZED_FOLDER = 'client/SYNCHRONIZED'
SYNC_INTERVAL = 1  # Check every 1 seconds

# Ensure the synchronized folder exists
os.makedirs(SYNCHRONIZED_FOLDER, exist_ok=True)

# here we are creating a connection  to the file server
file_server_conn = rpyc.connect(FILE_SERVER_ADDRESS, FILE_SERVER_PORT)

# this class is for helper thread to create a synchronization
class SynchronizationHelper(threading.Thread):
    def __init__(self):
        super().__init__()
        self.last_sync_time = 0  # Initialize last synchronization time
        self.stop_event = threading.Event()
        self.synced_files = set()  # Track files that have been synchronized

    def run(self):
        while not self.stop_event.is_set():
            self.check_changes()
            self.stop_event.wait(SYNC_INTERVAL)  # Wait for the next sync cycle

# this part of code checks if any changes are made 10 seconds from the last sync cycle .
# If yes it sync the changes.

    def check_changes(self):
        print("\nChecking for changes in synchronized folder...")
        current_files = set(os.listdir(SYNCHRONIZED_FOLDER))
        # Check for new or modified files
        for filename in current_files:
            file_path = os.path.join(SYNCHRONIZED_FOLDER, filename)
            if os.path.isfile(file_path):
                try:
                    # Get file modification time
                    modified_time = os.path.getmtime(file_path)
                    if modified_time > self.last_sync_time or filename not in self.synced_files:
                        # Perform synchronization
                        self.sync_file(filename)
                except FileNotFoundError:
                    pass  # Handle if file is deleted during iteration
                except Exception as e:
                    print(f"Error checking file {filename}: {e}")

        # Check for deleted files
        deleted_files = self.synced_files - current_files
        for filename in deleted_files:
            self.delete_file(filename)

        self.last_sync_time = time.time()  # Update last synchronization time
        self.synced_files = current_files  # Update tracked files

    def sync_file(self, filename):
        file_path = os.path.join(SYNCHRONIZED_FOLDER, filename)
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
            # Assuming you have a method in your file server to handle uploads
            result = file_server_conn.root.upload(filename, data)
            print(f"Synchronized {filename} with server: {result}")
            self.synced_files.add(filename)  # Track the file as synchronized
        except Exception as e:
            print(f"Error synchronizing file {filename}: {e}")

    def delete_file(self, filename):
        try:
            # Assuming you have a method in your file server to handle deletions
            result = file_server_conn.root.delete(filename)
            print(f"Deleted {filename} from server: {result}")
            self.synced_files.discard(filename)  # Remove from tracked files
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")

    def stop(self):
        self.stop_event.set()

# Create and start the synchronization helper thread
sync_helper = SynchronizationHelper()
sync_helper.start()

try:
    # Keep the main thread running while synchronization helper is active
    while True:
        time.sleep(1)
finally:
    # Clean up resources
    sync_helper.stop()
    sync_helper.join()
    file_server_conn.close()
