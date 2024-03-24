import threading
import random
import time

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
buffer_lock = threading.Lock()
buffer_empty = threading.Condition(buffer_lock)
all_numbers_written = threading.Event()
odd_numbers_written = threading.Event()
even_numbers_written = threading.Event()

all_file = open("all.txt", "w")
odd_file = open("odd.txt", "w")
even_file = open("even.txt", "w")


def producer():
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with buffer_lock:
            buffer.append(num)
            all_file.write(str(num) + '\n')
            print("Produced: "+str(num))
            if len(buffer) >= BUFFER_SIZE:
                all_numbers_written.set()
            
            buffer_empty.notify()

def consumer_odd():
    while not all_numbers_written.is_set() or len(buffer) > 0:
        with buffer_lock:
            if len(buffer) > 0 and buffer[-1] % 2 == 0:
                buffer.pop()
                continue
            elif len(buffer) > 0 and buffer[-1] % 2 != 0:
                num = buffer.pop()
                odd_file.write(str(num) + '\n')
                print("Consumed Odd: "+str(num))
                if len(buffer) < BUFFER_SIZE:
                    odd_numbers_written.set()
                
                buffer_empty.notify()


def consumer_even():
    while not all_numbers_written.is_set() or len(buffer) > 0:
        with buffer_lock:
            if len(buffer) > 0 and buffer[-1] % 2 != 0:
                buffer.pop()
                continue
            elif len(buffer) > 0 and buffer[-1] % 2 == 0:
                num = buffer.pop()
                even_file.write(str(num) + '\n')
                print(f"Consumed even: {num}")
                if len(buffer) < BUFFER_SIZE:
                    even_numbers_written.set()
                
                buffer_empty.notify()

producer_thread = threading.Thread(target=producer)
consumer_odd_thread = threading.Thread(target=consumer_odd)
consumer_even_thread = threading.Thread(target=consumer_even)

start_time=time.time()
producer_thread.start()
consumer_odd_thread.start()
consumer_even_thread.start()

producer_thread.join()

consumer_odd_thread.join()
consumer_even_thread.join()

all_file.close()
odd_file.close()
even_file.close()
end_time=time.time()

print("Program completed.")
print("Execution Time: "+str(end_time-start_time)+" second")