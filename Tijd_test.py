import os
import serial
import thread
import time
import sys
import datetime

def asIntArray (s):
    return [ord(c) for c in s]

if __name__ == "__main__":
    Time_tmp = time.time()
    Timestamp = datetime.datetime.fromtimestamp(Time_tmp).strftime('%Y-%m-%d %H:%M:%S')
    print Timestamp
