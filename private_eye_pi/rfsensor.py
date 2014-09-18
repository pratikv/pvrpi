#!/usr/bin/env python
"""
rfsensor.py v10 PrivateEyePi RF Sensor Interface
---------------------------------------------------------------------------------
 Works conjunction with host at www.privateeyepi.com                              
 Visit projects.privateeyepi.com for full details                                 
                                                                                  
 J. Evans October 2013       
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                       
                                                                                  
 Revision History                                                                  
 V1.00 - Release
 V2.00 - Incorporation of rules functionality  
 V3.00 - Incorporated Button B logic
 V3.01 - High CPU utilization fixed
 V9    - Rule release   
 V10   - Added support for the BETA single button power saving wireless switch   
       - Functionality added for wireless temperature and humidity sensor  
 -----------------------------------------------------------------------------------
"""

import serial
import globals
import time
import sys
import thread
from alarmfunctionsr import UpdateHost
from alarmfunctionsr import GetDataFromHost
from alarmfunctionsr import SendEmailAlert
from time import sleep
global RFList
global numrf

def ProcessMessage(value, value2, DevId, type):
# Notify the host that there is new data from a sensor (e.g. door open)
        global numrf
        global RFList
            
        hostdata =[]
        
        #Send switch sensor value to host
        if type==1:
                button = value[1]
                value = value[2:]
                # If button B is pressed then we need to map the device ID to the button B sensor defined on the server
                if button == "B":
                        tempId = int(DevId)
                        DevId = 0
                        for z in range (0,len(globals.ButtonBList)):
                                if globals.ButtonBList[z] == tempId:
                                        DevId=globals.ButtonBId[z]
                for z in range(0,numrf,1):
                        if RFList[z]==int(DevId):
                                hostdata.append(RFList[z])
                            	if value=='OF' or value=='OFF':
                                        hostdata.append(1)
                                        rt=UpdateHost(26,hostdata)
                                if value=='ON':
                                        hostdata.append(0)
                                        rt=UpdateHost(26,hostdata)
        #Send battery level to host
        if type==2:
                for z in range(0,numrf,1):
                        if RFList[z]==int(DevId):
                                hostdata.append(DevId)
                                hostdata.append(value)
                                MaxVoltage=3
                                for z in range (0,len(globals.VoltageList)):
                                        if globals.VoltageList[z] == int(DevId):
                                                MaxVoltage=globals.MaxVoltage[z]
                                hostdata.append(MaxVoltage)
                                rt=UpdateHost(22,hostdata)
        
        #Send temperature to host
        if type==3:
                for z in range(0,numrf,1):
                        if RFList[z]==int(DevId):
                                if globals.Farenheit:
                                        value = value*1.8+32
                                        value = round(value,2)
                                hostdata.append(value)
                                if globals.Farenheit:
                                        hostdata.append(1)
                                else:
                                        hostdata.append(0)    
                                hostdata.append(DevId)
                                rt=UpdateHost(14,hostdata)
        
        #Send humidity to host
        if type==4:
                for z in range(0,numrf,1):
                        if RFList[z]==int(DevId):
                                if globals.Farenheit:
                                        value = value*1.8+32
                                        value = round(value,2)
                                hostdata.append(value)
                                if globals.Farenheit:
                                        hostdata.append(1)
                                else:
                                        hostdata.append(0)
                                hostdata.append(DevId)
                                hostdata.append(value2)
                                rt=UpdateHost(14,hostdata)
        return(0)

def BuildRFSensorList():
        try:
                thread.start_new_thread(BuildRFSensorListThread, ( ) )
        except:
                print "Error: unable to start thread"

def BuildRFSensorListThread():
        global RFList
        global numrf
        
        RecordSet = GetDataFromHost(21,[0])
        if RecordSet==False:
                print "No RF sensors defined on the server"
                return 1
        
        numrf = len(RecordSet)
        
        RFList = []
        for i in range(numrf):
                RFList.append(RecordSet[i][0])
            
        return 0

def main():
        globals.init()
        currvalue=''
        tempvalue=-999;
        
        # loop until the serial buffer is empty
        BuildRFSensorList()
        start_time = time.time()
        
        #try:
        while True:
                elapsed_time = time.time() - start_time
                # Poll for changes to RF settings
                if (elapsed_time > 600):
                        start_time = time.time()
                        BuildRFSensorList()
                # declare to variables, holding the com port we wish to talk to and the speed
                port = '/dev/ttyAMA0'
                baud = 9600
                
                # open a serial connection using the variables above
                ser = serial.Serial(port=port, baudrate=baud)
                
                # wait for a moment before doing anything else
                sleep(0.2)        
                while ser.inWaiting():
                        # read a single character
                        char = ser.read()
                        # check we have the start of a LLAP message
                        if char == 'a':
                                # start building the full llap message by adding the 'a' we have
                                llapMsg = 'a'
                                
                                # read in the next 11 characters form the serial buffer
                                # into the llap message
                                llapMsg += ser.read(11)
                                
                                # now we split the llap message apart into devID and data
                                devID = llapMsg[1:3]
                                data = llapMsg[3:]
                                
                                if globals.PrintToScreen: print data
                                                                
                                if data.startswith('BUTTON'):
                                        sensordata=data[5:].strip('-')
                                        if currvalue<>sensordata or currvalue=='':
                                                currvalue=sensordata
                                                ProcessMessage(currvalue, 0, devID,1)
                                
                                if data.startswith('BTN'):
                                        sensordata=data[2:].strip('-')
                                        if currvalue<>sensordata or currvalue=='':
                                                currvalue=sensordata
                                                ProcessMessage(currvalue, 0, devID,1)
                                
                                if data.startswith('TMPA'):
                                        sensordata=data[4:]
                                        currvalue=float(sensordata)
                                        ProcessMessage(currvalue, 0, devID,3)
                                
                                if data.startswith('TMPB'):
                                        sensordata=data[4:].strip('-')
                                        tempvalue=float(sensordata)
                                
                                if data.startswith('HUMB'):
                                        if tempvalue > -999:
                                                sensordata=data[4:].strip('-')
                                                currvalue=float(sensordata)
                                                ProcessMessage(tempvalue, currvalue, devID,4)
                                                tempvalue=-999
                                                
                                # check if battery level is being sent axxBATTn.nn-
                                if data.startswith('BATT'):
                                        sensordata=data[4:].strip('-')
                                        currvalue=sensordata 
                                        ProcessMessage(currvalue, 0, devID,2)
                #ser.close()
                sleep(0.2)
    #except:
        #        print "Error: unable to start thread"
           
if __name__ == "__main__":
        main()



   
   

