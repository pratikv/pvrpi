#!/usr/bin/env python
"""
alarmfunctionsr.py 9.00 PrivateEyePi Common Functions
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
 V9.00 - Moving all versions to 9 for the rules release
 V9.01 - Added the PHOTO rule to send a photo as a rule action                                                             
 -----------------------------------------------------------------------------------
"""

import globals
import urllib2
import smtplib
import serial
import time
import sys
import thread
import RPi.GPIO as GPIO
import os, glob, time, operator
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from time import sleep
    
def find_all(a_str, sub):
        start = 0
        cnt=0
        while True:
                start = a_str.find(sub, start)
                if start == -1: 
                        return cnt
                start += len(sub)
                cnt=cnt+1
        
def isNumber(x):
        # Test whether the contents of a string is a number
        try:
                val = int(x)
        except ValueError:
                return False
        return True

def get_latest_photo(files):
    lt = operator.lt
    if not files:
        return None
    now = time.time()
    latest = files[0], now - os.path.getctime(files[0])
    for f in files[1:]:
        age = now - os.path.getctime(f)
        if lt(age, latest[1]):
            latest = f, age
    return latest[0]

def UpdateHostThread(function,opcode):
        try:
                thread.start_new_thread(UpdateHostThread, (function,opcode, ) )
        except:
                print "Error: unable to start thread"

def UpdateHost(function,opcode):
        # Sends data to the server 
        script_path = "https://www.privateeyepi.com/alarmhostr.php?u="+globals.user+"&p="+globals.password+"&function="+str(function)
        
        i=0
        for x in opcode:
            	script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
            	i=i+1
        
        if globals.PrintToScreen: print "Host Update: "+script_path 
        try:
                rt=urllib2.urlopen(script_path)
        except urllib2.HTTPError:
            	if globals.PrintToScreen: print "HTTP Error"
            	return False
        time.sleep(.2)
        temp=rt.read()
        if globals.PrintToScreen: print temp
        l = find_all(temp,"/n");
        RecordSet = temp.split(',')
        c=[]
        y=0
        c.append([])
        for x in RecordSet:
                if x=="/n":
                        y=y+1
                        if y < l:
                                c.append([])
                else:
                        if isNumber(x):
                                c[y].append(int(x))
                        else:
                                c[y].append(x)
        rt=ProcessActions(c)
        if rt==False:
                return(False)
        else:
            return(c)

def ProcessActions(ActionList):
        FalseInd=True
        for x in ActionList:
            if x[0]=="/EMAIL":
                    SendEmailAlertFromRule(x[1], x[2],0)
                    x.remove
            if x[0]=="/SEMAIL":
                    SendEmailAlert(x[1])
                    x.remove
            if x[0]=="/CHIME":
                    StartChimeThread()
                    x.remove
            if x[0]=="/rn588":
                    exit()
            if x[0]=="/FALSE":
                    FalseInd=False
            if x[0]=="/SIREN":
                    StartSirenThread(x[2])
                    x.remove
            if x[0]=="/PHOTO":
                    SendEmailAlertFromRule(x[1], x[2],1)
                    x.remove
            if x[0]=="/RELAYON":
                    SwitchRelay(1)
                    x.remove
            if x[0]=="/RELAYOFF":
                    SwitchRelay(0)
                    x.remove
            if x[0]=="/WRELAYON":
                    SwitchRFRelay(1)
                    x.remove
            if x[0]=="/WRELAYOFF":
                    SwitchRFRelay(0)
                    x.remove
        return(FalseInd)

def StartSirenThread(Zone):
        try:
                thread.start_new_thread(Siren, (Zone, ) )
        except:
                print "Error: unable to start thread"

def SwitchRelay(onoff):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(globals.RelayPin, GPIO.OUT) 
        GPIO.output(globals.RelayPin,onoff)
        
def SwitchRFRelay(onoff):
        # declare to variables, holding the com port we wish to talk to and the speed
        port = '/dev/ttyAMA0'
        baud = 9600
        
        # open a serial connection using the variables above
        ser = serial.Serial(port=port, baudrate=baud)
        
        # wait for a moment before doing anything else
        sleep(0.2)
        
        for i in range(0,3):
                if (onoff==True):       
                        ser.write('a{}RELAYAON-'.format(globals.WRelayPin))
                else:
                        ser.write('a{}RELAYAOFF'.format(globals.WRelayPin))
                time.sleep(2)
        ser.close
        
def Siren(Zone):
        GPIO.setmode(GPIO.BOARD)
        if globals.UseSiren == True:
                GPIO.setup(globals.SirenGPIOPin, GPIO.OUT) #Siren pin setup
        else:
                return
        
        if globals.SirenDelay>0:
                globals.SirenStartTime = time.time()
                while time.time() < globals.SirenStartTime + globals.SirenDelay:
                        if globals.BeepDuringDelay:
                                GPIO.output(globals.SirenGPIOPin,True)
                                time.sleep(1)
                                GPIO.output(globals.SirenGPIOPin,False)
                                time.sleep(4)
        
        GPIO.output(globals.SirenGPIOPin,True)
        globals.SirenStartTime = time.time()
        if globals.PrintToScreen: print "Siren Activated"
        while time.time() < globals.SirenStartTime + globals.SirenTimeout:
                time.sleep(5)
                if CheckForSirenDeactivation(Zone) == True:
                        break
        GPIO.output(globals.SirenGPIOPin,False)
        if globals.PrintToScreen: print "Siren Deactivated"
    
def CheckForSirenDeactivation(Zone):
        # Routine to fetch the location and zone descriptions from the server 
        RecordSet = GetDataFromHost(16,[Zone])
        if globals.PrintToScreen: print RecordSet
        ZoneStatus=RecordSet[0][0]
        if ZoneStatus=="FALSE":
                return (True)    

def StartChimeThread():
        try:
                thread.start_new_thread(SoundChime, ())
        except:
                print "Error: unable to start thread"

def SoundChime():
        if globals.ChimeDuration>0:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(globals.ChimeGPIOPin, GPIO.OUT) #Siren pin setup
                GPIO.output(globals.ChimeGPIOPin,True)
                time.sleep(globals.ChimeDuration)
                GPIO.output(globals.ChimeGPIOPin,False)
                    
def GetDataFromHost(function,opcode):
# Request data and receive reply (request/reply) from the server
 
        script_path = "https://www.privateeyepi.com/alarmhostr.php?u="+globals.user+"&p="+globals.password+"&function="+str(function)
        
        i=0
        for x in opcode:
                script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
                i=i+1
            
        if globals.PrintToScreen: print script_path 
        try:
                rt = urllib2.urlopen(script_path)
        except urllib2.HTTPError:
                return False
        temp=rt.read()
        if globals.PrintToScreen: print temp
        
        l = find_all(temp,"/n");
        RecordSet = temp.split(',')
        c=[]
        y=0
        c.append([])
        for x in RecordSet:
                if x=="/n":
                        y=y+1
                        if y < l:
                                c.append([])
                else:
                        if isNumber(x):
                                c[y].append(int(x))
                        else:
                                c[y].append(x)
        rt=ProcessActions(c)   
        if rt==False:
                return(False)
        else:
            return(c) 
        return(c)

def BuildMessage(SensorNumber):
        # Routine to fetch the location and zone descriptions from the server  
        
        RecordSet = GetDataFromHost(6,[SensorNumber])
        if globals.PrintToScreen: print RecordSet
        if RecordSet==False:
                return  
        zonedesc=RecordSet[0][0]
        locationdesc = RecordSet[0][1]
        messagestr="This is an automated email from your house alarm system. Alarm activated for Zone: "+zonedesc+" ("+locationdesc+")"
        return messagestr

def BuildMessageFromRule(SensorNumber, smartruleid):
        
    RecordSet = GetDataFromHost(7,[smartruleid, SensorNumber])
    if RecordSet==False:
        return

    numrows = len(RecordSet)  

    messagestr="This is an automated email from PrivateEyePi. Rule triggered for Zone(s): "+RecordSet[0][3]+", Location: "+RecordSet[0][4]+" and for rule "
    for i in range(0,numrows,1):
        if RecordSet[i][0]==1:
            messagestr=messagestr+"Alarm Activated"
        if RecordSet[i][0]==2:
            messagestr=messagestr+"Alarm Deactivated"
        if RecordSet[i][0]==3:
            messagestr=messagestr+"Circuit Open"
        if RecordSet[i][0]==4:
            messagestr=messagestr+"Circuit Closed"
        if RecordSet[i][0]==5:
            messagestr=messagestr+"Open for " + str(RecordSet[i][1]) + " Minutes"
        if RecordSet[i][0]==6:
            messagestr=messagestr+"Closed for " + str(RecordSet[i][1]) + " Minutes"
        if RecordSet[i][0]==7:
            messagestr=messagestr+"Where sensor value (" + str(RecordSet[i][5]) + ") is between " + str(RecordSet[i][1]) + " " + str(RecordSet[i][2])            
        if RecordSet[i][0]==8:
            messagestr=messagestr+"Tamper"
        if RecordSet[i][0]==9:
            messagestr=messagestr+"Day Of Week is between " + str(RecordSet[i][1]) + " and " + str(RecordSet[i][2]) 
        if RecordSet[i][0]==10:
            messagestr=messagestr+"Hour Of Day is between " + str(RecordSet[i][1]) + " and " + str(RecordSet[i][2])
        if RecordSet[i][0]==11:
            messagestr=messagestr+"Where secondary sensor value (" + str(RecordSet[i][6]) + ") is between " + str(RecordSet[i][1]) + " " + str(RecordSet[i][2])
        if i<numrows-1:
            messagestr=messagestr + " AND "    
    return messagestr

def SendEmailAlertFromRule(ruleid, SensorNumber, photo):
        try:
                thread.start_new_thread(SendEmailAlertThread, (SensorNumber, ruleid, True, photo, ) )
        except:
                print "Error: unable to start thread"

def SendEmailAlert(SensorNumber):
        try:
                thread.start_new_thread(SendEmailAlertThread, (SensorNumber,0 , False, False) )
        except:
                print "Error: unable to start thread"

def SendEmailAlertThread(SensorNumber, smartruleid, ruleind, photo):
    
        # Get the email addresses that you configured on the server
        RecordSet = GetDataFromHost(5,[0])
        if RecordSet==False:
                return
        
        numrows = len(RecordSet)
        
        if globals.smtp_server=="":
                return
        
        if ruleind:
                msgtext = BuildMessageFromRule(SensorNumber, smartruleid)
        else:
                msgtext = BuildMessage(SensorNumber)
                
        for i in range(numrows):
                # Define email addresses to use
                addr_to   = RecordSet[i][0]
                addr_from = globals.smtp_user #Or change to another valid email recognized under your account by your ISP      
                # Construct email
                
                if (photo==1):
                        files = 0
                        files = glob.glob(globals.photopath)
                        latestphoto = get_latest_photo(files)
                        msg = MIMEMultipart()
                else:
                        msg = MIMEText(msgtext)
                
                msg['To'] = addr_to
                msg['From'] = addr_from
                msg['Subject'] = 'Alarm Notification' #Configure to whatever subject line you want
                
                #attach photo
                if (photo==1):
                        msg.preamble = 'Multipart message.\n'  
                        part = MIMEText(msgtext) 
                        msg.attach(part)
                        part = MIMEApplication(open(latestphoto,"rb").read())
                        part.add_header('Content-Disposition', 'attachment', filename=latestphoto)
                        msg.attach(part)
                
                # Send the message via an SMTP server
                
                #Option 1 - No Encryption
                if globals.email_type==1:
                        s = smtplib.SMTP(globals.smtp_server)
                elif globals.email_type==2:
                #Option 2 - SSL
                        s = smtplib.SMTP_SSL(globals.smtp_server, 465)
                elif globals.email_type==3:
                #Option 3 - TLS
                        s = smtplib.SMTP(globals.smtp_server,587)
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                else:
                        s = smtplib.SMTP(globals.smtp_server)
                        
                
                s.login(globals.smtp_user,globals.smtp_pass)
                s.sendmail(addr_from, addr_to, msg.as_string()) 
                s.quit()
                if globals.PrintToScreen: print msg;

def SendCustomEmail(msgText, msgSubject):
    
        # Get the email addresses that you configured on the server
        RecordSet = GetDataFromHost(5,[0])
        if RecordSet==False:
                return
        
        numrows = len(RecordSet)
        
        if globals.smtp_server=="":
                return
                
        for i in range(numrows):
                # Define email addresses to use
                addr_to   = RecordSet[i][0]
                addr_from = globals.smtp_user #Or change to another valid email recognized under your account by your ISP      
                # Construct email
                msg = MIMEText(msgText)
                msg['To'] = addr_to
                msg['From'] = addr_from
                msg['Subject'] = msgSubject #Configure to whatever subject line you want
                
                # Send the message via an SMTP server
                #Option 1 - No Encryption
                if globals.email_type==1:
                        s = smtplib.SMTP(globals.smtp_server)
                elif globals.email_type==2:
                #Option 2 - SSL
                        s = smtplib.SMTP_SSL(globals.smtp_server, 465)
                elif globals.email_type==3:
                #Option 3 - TLS
                        s = smtplib.SMTP(globals.smtp_server,587)
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                else:
                        s = smtplib.SMTP(globals.smtp_server)
                        
                s.login(globals.smtp_user,globals.smtp_pass)
                s.sendmail(addr_from, addr_to, msg.as_string())
                s.quit()
                if globals.PrintToScreen: print msg;

