import time
import threading


def shower():
    for i in range(10):
        print("Shower...")
        time.sleep(0.5)


def brush():
    for i in range(10):
        print("Toothbrush...")
        time.sleep(0.3)


start = time.time()
# shower()
# brush()

task1 = threading.Thread(target=shower)
task2 = threading.Thread(target=brush)

task1.start()
task2.start()

task1.join()
task2.join()

print("EXECUTED IN", time.time()-start)


