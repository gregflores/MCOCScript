import time

try:
    while True:
        print(time.time)
        time.sleep(1)
except KeyboardInterrupt:
    pass