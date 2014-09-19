import json
import time
import pusherclient

import RPi.GPIO as GPIO
global pusher

def channel_callback(data):
    a = str(data)
    b = json.loads(a)
    #print bool( b["fan_status"] )
    GPIO.output(7,bool( b["fan_status"] ))

def connect_handler(data):
    channel = pusher.subscribe('pi_channel')
    channel.bind('fan_control', channel_callback)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.OUT)
    appkey = 'b0dd682a76bd9cb063d7'
    pusher = pusherclient.Pusher(appkey)
    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()

    while True:
        time.sleep(1)
