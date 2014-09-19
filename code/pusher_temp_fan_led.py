import json
import time
import datetime
import pusher
import pusherclient
import RPi.GPIO as GPIO

global pusher

fan_pin = 11
led_pin = 15

delay_time = 1

global pusherObj

def channel_callback(data):
    a = str(data)
    b = json.loads(a)
#    print b
#    #print bool( b["fan_status"] )
    GPIO.output(fan_pin,bool( b["fan_status"] ))
    GPIO.output(led_pin,bool( b["fan_status"] ))

def connect_handler(data):
    channel = pusher_client.subscribe('pi_fan_channel')
    channel.bind('fan_control', channel_callback)

def read_file():
  while True:
	tfile = open( "/sys/bus/w1/devices/10-0008006318b6/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature_raw = int(temperaturedata[2:])
	#temperature_raw = temperature_raw + 50
	temperature = float(temperature_raw)
	temperature = temperature/1000
	temperature += 60
	ts = datetime.datetime.now()
	print "{0:000} {1}".format( temperature, ts )
	pusherObj['pi_channel'].trigger('temperature_recorded', {'temp':temperature })
	time.sleep(delay_time)

if __name__ == "__main__" :
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(fan_pin,GPIO.OUT)
	GPIO.setup(led_pin,GPIO.OUT)
	appkey = 'b0dd682a76bd9cb063d7'
	pusher_client = pusherclient.Pusher(appkey)
	pusher_client.connection.bind('pusher:connection_established', connect_handler)
	pusher_client.connect()
	pusherObj = pusher.Pusher( app_id='88925',
        key='b0dd682a76bd9cb063d7',
        secret='c8590ca5ea5a08612fa1')
	read_file()

