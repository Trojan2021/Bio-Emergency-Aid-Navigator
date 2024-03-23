import time
from Adafruit_IO import Client, Feed

ADAFRUIT_IO_USERNAME = 'g_nerone'
ADAFRUIT_IO_KEY = 'xxxxxxxx'

FEED_NAME = 'test'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY) 

def publish_to_feed(value):
    aio.send_data(FEED_NAME, value)
while True:

    value = input("Enter 0 for close or 1 for open (q to quit): ")
    
    if value.lower() == 'q':
        break

    try:
        value = int(value)
    except ValueError:
        print("Invalid input. Please enter 0, 1, or q to quit.")
        continue
    if value not in [0, 1]:
        print("Invalid input. Please enter 0 or 1.")
    else:

        publish_to_feed(value)
        print(f"Published value {value} to Adafruit IO feed")
        
