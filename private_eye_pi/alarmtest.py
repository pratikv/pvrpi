########################################################################
## alarmtest.py 1.00 Home Alarm System                                ##
## -------------------------------------------------------------------##
## Works conjunction with host at www.privateeyepi.com                ##
## Visit projects.privateeyepi.com for full details                   ##
##                                                                    ##
## J. Evans April 2013                                                ##
##                                                                    ##
########################################################################

import urllib2
global user
global password

# Usr and password that has been registered on www.privateeyepi.com website
user="ratneshsinghparihar@gmail.com"
password="kd200187"
       
def isNumber(x):
    # Test whether the contents of a string is a number
    try:
        val = int(x)
    except ValueError:
        return False
    return True

def find_all(a_str, sub):
    start = 0
    cnt=0
    while True:
        start = a_str.find(sub, start)
        if start == -1: 
            return cnt
        start += len(sub)
        cnt=cnt+1
    
def GetDataFromHost(function,opcode):
# Request data and receive reply (request/reply) from the server
 
    global user
    global password
    
    print "Sending request to server:"
    script_path = "https://www.privateeyepi.com/alarmhost.php?u="+user+"&p="+password+"&function="+str(function)
    i=0
    for x in opcode:
        script_path=script_path+"&opcode"+str(i)+"="+str(opcode[i])
        i=i+1
        
    print script_path 
    try:
        rt = urllib2.urlopen(script_path)
    except urllib2.HTTPError:
        return False
    print "Receiving reply from server:"
    temp=rt.read()
    print temp
    
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
        if find_all(x,"/FALSE")<>0:
            return False    
    return(c)

print "Your user="+user
print "Your password = "+password
if user=="" or password=="":
    print "User and Password not configured!"
    print "The system won't work without a user and password. Visit projects.privateeyepi.com/home for instructions."
else:
    RecordSet = GetDataFromHost(2,[0])

    if RecordSet==False:
        print "You do not have any alarm gpio settings (door,window, motion) configured in your Location seetings at www.privateeyepi.com"
    else:
        numgpio = len(RecordSet)
        
        if numgpio==0 or RecordSet[0][0]=="":
            print "You have not configured any GPIO ports. Visit www.privateeyepi.com and click on GPIO menu to configure."
            print "Visit projects.privateeyepi.com/home for instructions."
        else:
            print "You have configured "+str(numgpio)+" ports:"
                    
            for i in range(numgpio):
                gpio = RecordSet[i][0]
                RecordSet2 = GetDataFromHost(6,[gpio])
                if RecordSet2==False or RecordSet2[0][0]=="":
                    print "You have not configured Locations and linked to Zones for GPIO "+str(gpio)+". Visit www.privateeyepi.com to configure."
                    exit
                else:  
                    zonedesc=RecordSet2[0][0]
                    locationdesc = RecordSet2[0][1]
                    print "GPIO="+str(gpio)+", Locations="+locationdesc+", Zones="+zonedesc
            
            RecordSet = GetDataFromHost(5,[0])
            if RecordSet==False or RecordSet[0][0]=="":
                print "You have not configured any email addresses so you will not receive email alerts."
                print "Visit www.privateeyepi.com and click on Email menu to configure."
                exit
            else:   
                numrows = len(RecordSet)
                print "You have "+str(numrows)+ " email addresses configured:"        
                for i in range(numrows):
                    print RecordSet[i][0]
    
    RecordSet = GetDataFromHost(15,[0])
    if RecordSet<>False:
            print "You do have temperature sensors defined in Locations on www.privateeyepi.com"
            
    print "Hope that helps, otherwise email support@privateeyepi.com"
 
               
               
               
               
               
               
               
                
        

