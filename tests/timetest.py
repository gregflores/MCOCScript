import time

sec = time.time()
print(sec)
local_time = time.ctime(sec)
print(local_time)
time.sleep(.001)
sec2 = time.time()
print(sec2)
deltatime = sec2-sec
print(deltatime)