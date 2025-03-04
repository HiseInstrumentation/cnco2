import time

my_string = "<ok>"

while True:
    if "ok" not in my_string:
        print("looking!")
        time.sleep(1)
