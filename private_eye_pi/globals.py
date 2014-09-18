#!/usr/bin/env python
"""
globals.py 9.00 PrivateEyePi Globals Parameters
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
 V2.00 - Added generic poll interval
 V3.00 - Incorporated rules functionality
 V4.00 - Added siren rule action, chime, siren beep delay
 v9.00 - Rules release     
 v10.00 - Added support for flexible sensor voltages                                                        
 -----------------------------------------------------------------------------------
"""

def init():
        global PrintToScreen
        global user
        global password
        global RFPollInterval
        global smtp_server
        global smtp_user
        global smtp_pass
        global Farenheit
        global DallasSensorNumbers
        global DallasSensorDirectory
        global TemperaturePollInterval
        global GenericPollInterval
        global GPIOPollInterval
        global UseSiren
        global SirenGPIOPin
        global SirenTimeout
        global SirenStartTime
        global Armed
        global RemoteZoneDescription
        global ArmPin
        global DisarmPin
        global ArmDisarm
        global GPIO 
        global ChimeDuration
        global SirenPollInterval
        global SirenDelay
        global BeepDuringDelay
        global ButtonBList
        global ButtonBId
        global dht22_gpio
        global dht22_pin_no
        global auto_dht22
        global auto_alarm
        global auto_rfsensor
        global auto_dallas
        global install_directory
        global email_type
        global ChimeGPIOPin
        global photopath
        global RelayPin
        global WRelayPin
        global VoltageList
        global MaxVoltage
        
        #User and password that has been registered on www.privateeyepi.com website
        user="ratneshsinghparihar@gmail.com"     #Enter your email address
        password="kd200187" #Enter your password here
        
        # Set this to True if you want to send outputs to the screen
        # This is useful for debugging
        PrintToScreen=True
        
        # If you want to receive email alerts define SMTP email server details
        # This is the SMTP server, username and password trequired to send email through your internet service provider
        smtp_server="" # usually something like smtp.yourisp.com
        smtp_user=""   # usually the main email address of the account holder
        smtp_pass=""   # usually your email address password
        email_type=1   # 1 for No Encryption, 
                       # 2 for SSL and 
                       # 3 and TLS
        
        # Set the path to the photos that get attached to emails when
        # a rule is triggered to send photos
        photopath = "/home"
        
        #Indicator to record temperature in Farenheit
        Farenheit=False
                
        #Temperature settings
        #if you are using the dht22 temperature and humidity sensor set the gpio number and the pin number here
        # note!! the GPIO number and the pin number are not the same e.g GPIO4=RPIPin7
        dht22_gpio=4
        dht22_pin_no=7
        
        DallasSensorNumbers = []
        DallasSensorDirectory = []
        
        #Set the directory and sensor numbers for the Dallas temperature gauge
        DallasSensorNumbers.append(7) #sensor number defined in the number field in the GPIO settings
        #DallasSensorNumbers.append(80) #add more sensors..
        #DallasSensorNumbers.append() #add more sensors..
        
        DallasSensorDirectory.append("10-000B006318b6") #directory name on RPI in the /sys/bus/w1/devices directory 
        #DallasSensorDirectory.append("28-000005020815") #add another directory 
        #DallasSensorDirectory.append("") #add another directory

        #Auto restart settings
        auto_dallas = True
        auto_alarm = False
        auto_dht22 = False
        auto_rfsensor = False
        install_directory = "/home" #The PrivateEyePi software directory

        # Set this to true if you want to connect an external siren. Put siren activation and deactivation code in the Siren function.
        UseSiren = False
        SirenGPIOPin = 18
        SirenDelay=30 #The amount of time the siren will delay before it sounds
        BeepDuringDelay = True #if your want the siren to beep during the SirenDelay period
        SirenTimeout = 30 #siren will timeout after 30 seconds
        ChimeGPIOPin = 18
        ChimeDuration = 5
     
        #Arm/Disarm zone from a switch
        ArmDisarm=False # set this to True if you want to arm/disarm using switches
        RemoteZoneDescription="" #The description of the zone you want to arm/disarm
        ArmPin=13
        DisarmPin=15
        Armed = False

        #Configure your button B sensors here
        #Button B is the second button on the RF Switch
        ButtonBList = []
        ButtonBId = []
        #ButtonBList.append(80) # this is the device ID of the sensor 
        #ButtonBId.append(90)   # sensor number defined in the number field in the GPIO settings
        
        #ButtonBList.append(81)
        #ButtonBId.append(90)
        #...add more button B sensors by copying the above two lines and updating the numbers in brackets....
        
        #Relay pin configuration for the relay ON/OFF rule action
        #RelayPin=12 
        #WRelayPin=99
        
        #Configure alternate voltages here. This is for wireless sensors that have a voltage
        #that is not the standard 3V. This voltage setting is used for the battery display
        #on the dashboard so the system knows what the maximum voltage is for the display
        #The below example will set the maximum voltage for Device ID 81 to 9V
        VoltageList = []
        MaxVoltage = []
        #VoltageList.append(81)
        #MaxVoltage.append(9)
        #...add more max voltages by copying the above two lines and updating the numbers in brackets....
        
