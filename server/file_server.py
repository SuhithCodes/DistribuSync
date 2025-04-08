import os
import threading
import rpyc
from rpyc.utils.server import ThreadedServer

# Constants
MASTER_DIR = "server/MASTER"

# Ensure directories exist or create them
os.makedirs(MASTER_DIR, exist_ok=True)

# Lock for thread safety
lock = threading.Lock()

class FileService(rpyc.Service):
    def on_connect(self, conn):
        print("Client connected")
    
    def on_disconnect(self, conn):
        print("Client disconnected")

    def exposed_upload(self, filename, data):
        print(f"Upload request for {filename}")
        with lock:
            with open(os.path.join(MASTER_DIR, filename), "wb") as f:
                f.write(data)
        return "Upload successful"

    def exposed_delete(self, filename):
        print(f"Delete request for {filename}")
        with lock:
            file_path = os.path.join(MASTER_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return "Delete successful"
            else:
                return "File not found"

    def exposed_rename(self, old_filename, new_filename):
        print(f"Rename request: {old_filename} to {new_filename}")
        with lock:
            old_path = os.path.join(MASTER_DIR, old_filename)
            new_path = os.path.join(MASTER_DIR, new_filename)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                return "Rename successful"
            else:
                return "File not found"

    def exposed_list_files(self):
        with lock:
            files = os.listdir(MASTER_DIR)
        return files


if __name__ == "__main__":
    server = ThreadedServer(FileService, port=50000)
    print("File server started on port 50000")
    server.start()
