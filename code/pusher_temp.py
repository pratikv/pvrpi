import time
import datetime
import pusher

global pusherObj

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
	time.sleep(1)

#try:
if __name__ == "__main__" :
	pusherObj = pusher.Pusher( app_id='88925',
        key='b0dd682a76bd9cb063d7',
        secret='c8590ca5ea5a08612fa1')
	read_file()
#	pusherObj
#except:
#	print 'Keyboard interrupted the data'
