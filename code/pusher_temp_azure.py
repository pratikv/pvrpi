import time
import datetime
import pusher
import urllib2
import httplib, urllib
import json
import sys
import requests
from urllib2 import Request, URLError
from AdapterOverride import MyAdapter

global pusherObj
url = "https://tempraturemonitorservice.azure-mobile.net/tables/tempratureLog/"
headers = {"Connection": "keep-alive",
           "Accept-Encoding": " gzip,deflate",
           "Accept-Language": "en-US,en;q=0.8",
           "Accept": " application/json, text/javascript, */*; q=0.01",
           "Content-Type": " application/json",
           "Content-Length": " 1000",
           "x-zumo-version": "Zumo.master.0.1.6.3890.Runtime",
           "X-ZUMO-APPLICATION": " bXRaOQFontMMZWcltoaajYAYZPRLfV95"}
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
	temp = {"deviceId": "1", "temprature": str(temperature), "createdAt":str( ts)}
	#temp = {"deviceId": "4", "temprature": "35", "createdat": "2014-09-25 17:15:54.467"}
	data_json = json.dumps(temp)
	s = requests.Session()
	s.mount('https://', MyAdapter())
	s.headers = headers;
#try:	
	s.post(url,data_json)
        print "{0:000} {1}".format( temperature, ts )
        pusherObj['pi_channel'].trigger('temperature_recorded', {'temp':temperature })
        

#try:
if __name__ == "__main__" :
        pusherObj = pusher.Pusher( app_id='88925',
        key='b0dd682a76bd9cb063d7',
        secret='c8590ca5ea5a08612fa1')
        read_file()
#       pusherObj
#except:
#       print 'Keyboard interrupted the data'

