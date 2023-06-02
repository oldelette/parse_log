import threading
import time

# Global variable
global_var = 0
global_dic = {"port_0": 0, "port_1": 0, "port_2": 0}

# Lock for synchronization
lock = threading.Lock()

# Function to increment the global variable


def increment_global(by):
    global global_var
    # with lock:
    #     loc=global_var
    #     loc += by
    #     time.sleep(1)
    #     global_var=loc

    with lock:
        a = global_dic["port_0"]
        a += by
        time.sleep(1)
        global_dic["port_0"] = a

# Function to decrement the global variable


def decrement_global(by):
    global global_var
    # with lock:
    #     loc=global_var
    #     loc -= by
    #     time.sleep(1)
    #     global_var=loc

    with lock:
        a = global_dic["port_0"]
        a -= by
        time.sleep(1)
        global_dic["port_0"] = a


def threaded_function_1():
    count = 500
    while count > 0:
        increment_global()
        count -= 1


def threaded_function_2():
    count = 500
    while count > 0:
        # decrement_global()
        increment_global()
        count -= 1


def threaded_function_3():
    count = 500
    while count > 0:
        increment_global()
        count -= 1


# Create threads
# thread1 = threading.Thread(target=threaded_function_1)
# thread2 = threading.Thread(target=threaded_function_2)
# thread3 = threading.Thread(target=threaded_function_3)
thread1 = threading.Thread(target=increment_global, args=(10,))
thread2 = threading.Thread(target=decrement_global, args=(20,))
thread3 = threading.Thread(target=decrement_global, args=(30,))

# Start threads
thread1.start()
thread2.start()
thread3.start()

# Wait for threads to complete
thread1.join()
thread2.join()
thread3.join()

# Print the final value of the global variable
# print("Global variable:", global_var)
print("Global dictionary:", global_dic)
