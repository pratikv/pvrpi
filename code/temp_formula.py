import time

def read_file():
  while True:
	tfile = open( "/sys/bus/w1/devices/10-000800629cc5/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature_raw = int(temperaturedata[2:])
	temperature_raw = (~temperature_raw )+ 1
	temperature = float(temperature_raw)
	temperature = temperature/1000
	print temperature
	time.sleep(1)

read_file()
