# client.py
import time
import subprocess


def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"exiting in {i} seconds...")
        time.sleep(1)
    print("Time's up!")
    # Example command to exit the shell session
    command = "exit"
    # Execute the command
    subprocess.run(command, shell=True)

import rpyc
import threading

class AsyncCallback(object):
    def __init__(self):
        self.result = None
        self.ready_event = threading.Event()

    def __call__(self, result):
        self.result = result
        self.ready_event.set()

if __name__ == "__main__":
    conn = rpyc.connect("localhost", 50002)

    # Get user input for the add operation
    print("ADD OPERATION")
    i = int(input("Enter the first number to add: "))
    j = int(input("Enter the second number to add: "))

    # Get user input for the sort operation
    print("SORTING OPERATION")
    array_to_sort = input("Enter a list of numbers to sort, separated by spaces: ").split()
    array_to_sort = [int(x) for x in array_to_sort]

    # Asynchronous add operation using callback
    print("Sending asynchronous add request...")
    callback_add = AsyncCallback()
    conn.root.async_add(i, j, callback_add)

    # Asynchronous sort operation using callback
    print("Sending asynchronous sort request...")
    callback_sort = AsyncCallback()
    conn.root.async_sort(array_to_sort, callback_sort)


    # Wait for the sort callback to set the result
    callback_sort.ready_event.wait()
    sorted_array = callback_sort.result
    print("Result of asynchronous sort operation:", sorted_array)

    # Wait for the add callback to set the result
    callback_add.ready_event.wait()
    result_add = callback_add.result
    print("Result of asynchronous add operation:", result_add)
    
    countdown(3)
    conn.close()
