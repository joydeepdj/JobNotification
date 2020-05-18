import schedule
import time
import os
def do_something():
    os.system("python check.py")
    #print("yes")
schedule.every().hour.do(do_something)

while 1:
    schedule.run_pending()
    time.sleep(1)
