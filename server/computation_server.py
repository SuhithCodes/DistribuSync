import time
import rpyc
from rpyc.utils.server import ThreadedServer

class ComputationService(rpyc.Service):
    
    def exposed_add(self, i, j):
        print(f"Received add request: {i} + {j}")
        return i + j

    def exposed_sort(self, array):
        print(f"Received sort request: {array}")
        return sorted(array)

    def exposed_async_add(self, i, j, callback):
        print(f"Received asynchronous add request: {i} + {j}")
        time.sleep(5)  # Simulate a delay for the async operation
        result = i + j
        callback(result)

    def exposed_async_sort(self, array, callback):
        print(f"Received asynchronous sort request: {array}")
        time.sleep(5)  # Simulate a delay for the async operation
        sorted_array = sorted(array)
        callback(sorted_array)

if __name__ == "__main__":
    server = ThreadedServer(ComputationService, port=50005)
    print("Computation server started on port 50005")
    server.start()
