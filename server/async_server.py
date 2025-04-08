# server.py

import time
import rpyc
from rpyc.utils.server import ThreadedServer

class ComputationService(rpyc.Service):
    
    def exposed_add(self, i, j):
        print(f"Received add request: {i} + {j}")
        result = i + j
        return result

    def exposed_sort(self, A):
        print("Received sort request:", A)
        sorted_A = sorted(A)
        return sorted_A

    def exposed_async_sort(self, A, callback):
        print("Received asynchronous sort request:", A)
        # Simulate a time-consuming sort operation
        time.sleep(3)  # Introduce a 3-second delay to simulate a slow operation
        sorted_A = sorted(A)
        # Invoke the callback with the sorted result
        callback(sorted_A)

    def exposed_async_add(self, i, j, callback):
        print(f"Received asynchronous add request: {i} + {j}")
        # Simulate a time-consuming addition operation
        time.sleep(2)  # Introduce a 2-second delay to simulate a slow operation
        result = i + j
        # Invoke the callback with the addition result
        callback(result)

if __name__ == "__main__":
    server = ThreadedServer(ComputationService, port=50002)
    print("Starting RPC server on port 50002...")
    server.start()
