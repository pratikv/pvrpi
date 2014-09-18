import time

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
	print temperature
	time.sleep(1)

try:
	read_file()
except:
	print 'Keyboard interrupted the data'
