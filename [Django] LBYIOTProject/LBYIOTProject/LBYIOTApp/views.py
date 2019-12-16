from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from threading import Thread
import datetime
import serial
import paho.mqtt.client as mqtt
import time
import json

# GLOBAL VARIABLE SETUP
ipadd = "10.200.180.1"
arduinoOneOutTopic = "/device/one/out"
arduinoOneInTopic = "/device/one/in"
arduinoTwoOutTopic = "/device/two/out"
arduinoTwoInTopic = "/device/two/in"
mqttMsg = ""
isProcessing = False
roadOneHasValue = False
roadTwoHasValue = False
roadOneValue = ""
roadTwoValue = ""
countdown = 0
roadOneState = False
roadTwoState = False
currentRoadState = 1

def on_connect(client, userdata, rc):
        print ("Connected with code"+ str(rc))     
   
def on_message(client, userdata, msg):
        global mqttMsg
        global isProcessing
        global roadOneHasValue
        global roadOneValue
        global roadTwoHasValue
        global roadTwoValue
        
        mqttMsg = msg.payload.decode()
        mqttTopic = str(msg.topic)
        #FOR DEBUGGING
        #print(countdown);
        #print ("Topic:", str(msg.topic))
        #print ("Message:", str(msg.payload.decode()))
        # GET BOTH VALUES BEFORE PROCEEDING
        
        if(mqttTopic == arduinoOneOutTopic and not roadOneHasValue):
                print("NIIIIIIIIIIICEEEE")
                roadOneHasValue = True
                roadOneValue = mqttMsg
                print(roadOneValue)
                print(roadOneHasValue)
                print(roadTwoHasValue)
                print(isProcessing)
                if(roadOneHasValue and roadTwoHasValue and not isProcessing):
                        print("WOOOOOOOOOOOOHHHH")
                        isProcessing = True
                        evaluate()
        elif(mqttTopic == arduinoTwoOutTopic and not roadTwoHasValue):
                print("OOOOOONNNNEEE")
                roadTwoHasValue = True
                roadTwoValue = mqttMsg
                print(roadTwoValue)
                print(roadOneHasValue)
                print(roadTwoHasValue)
                print(isProcessing)
                if(roadOneHasValue and roadTwoHasValue and not isProcessing):
                        print("WOOOOOOOOOOOOHHHH")
                        isProcessing = True
                        evaluate()
        
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ipadd,1883,60)
client.subscribe(arduinoOneOutTopic)
client.subscribe(arduinoTwoOutTopic)
#client.subscribe(arduinoOneInTopic)
#client.subscribe(arduinoTwoInTopic)
client.loop_start()
mqttc = mqtt.Client("Python Pub")
mqttc.connect(ipadd, 1883)

def readerFunction(request):
        global currentRoadState
        JSONer = {}

        JSONer['countdown'] = countdown
        if(currentRoadState == 1):
                #publish_change()
                JSONer['greenOne'] = 'green'
                JSONer['redOne'] = 'black'
                JSONer['greenTwo'] = 'black'
                JSONer['redTwo'] = 'red'
                
        elif(currentRoadState == 2):
                #publish_change()
                JSONer['greenOne'] = 'black'
                JSONer['redOne'] = 'red'
                JSONer['greenTwo'] = 'green'
                JSONer['redTwo'] = 'black'
        
        return HttpResponse(json.dumps(JSONer))
	# time.sleep(2)



def publish_change():
        global currentRoadState
        global isProcessing
        global roadOneHasValue
        global roadTwoHasValue
        if(currentRoadState == 1):
                '''
                if(roadTwoState and not roadOneState):
                        print("WOW1")
                        mqttc.publish(arduinoOneInTopic, "RED")                        
                        mqttc.publish(arduinoTwoInTopic, "GREEN")
                        print("WOW2")
                        currentRoadState = 2
                '''
                if(not roadTwoState and not roadOneState):
                        print("HANEEEP1")
                        #timer 5 sec
                        
                        mqttc.publish(arduinoOneInTopic, "RED")
                        mqttc.publish(arduinoTwoInTopic, "GREEN")
                        currentRoadState = 2
                        timer(5)
                        print("HANEEEP2")
                '''
                elif(roadTwoState and roadOneState):
                        print("TALAGA TOOLLL")
                        #timer 5 sec
                        timer(5)
                        mqttc.publish(arduinoOneInTopic, "RED")
                        mqttc.publish(arduinoTwoInTopic, "GREEN")
                        currentRoadState = 2
                '''
                
        elif(currentRoadState == 2):
                '''
                if(roadOneState and not roadTwoState):
                        print("WOW1")
                        mqttc.publish(arduinoTwoInTopic, "RED")
                        mqttc.publish(arduinoOneInTopic, "GREEN")
                        currentRoadState = 1
                        print("WOW2")
                '''
                if(not roadOneState and not roadTwoState):
                        print("HANEEEP1")
                        #timer 5 sec
                        timer(5)
                        mqttc.publish(arduinoTwoInTopic, "RED")
                        mqttc.publish(arduinoOneInTopic, "GREEN")
                        currentRoadState = 1
                        print("HANEEEP2")
                '''
                elif(roadOneState and roadTwoState):
                        print("TALAGA TOOLLL")
                        #timer 5 sec
                        timer(5)
                        mqttc.publish(arduinoTwoInTopic, "RED")
                        mqttc.publish(arduinoOneInTopic, "GREEN")
                        currentRoadState = 1
                '''
        isProcessing = False
        roadOneHasValue = False
        roadTwoHasValue = False


def switch(request):
        global roadOneState
        global roadTwoState
        global currentRoadState
        print("Switch states")
        if (roadOneState == True):
                roadOneState = False
                roadTwoState = True
                currentRoadState = 2
        elif (roadTwoState == True):
                roadTwoState = False
                roadOneState = True
                currentRoadState = 1
        #publish_change()
        return HttpResponse()

def evaluate():
        global roadOneState
        global roadTwoState
        if(roadOneValue == "CAR"):
                roadOneState = True
        elif(roadOneValue == "NONE"):
                roadOneState = False
        if(roadTwoValue == "CAR"):
                roadTwoState = True
        elif(roadTwoValue == "NONE"):
                roadTwoState = False

        #print("roadOneState: ", roadOneState)
        #print("roadTwoState: ", roadTwoState)
        #print("currentRoadState: ", currentRoadState)
        publish_change()

def timer(delay):
        global countdown
        for x in range(delay,0,-1):
                #update timer displayed in web
                countdown = x
                print(countdown)
                time.sleep(1);
                
def mainPage(request):
	curDateTime = datetime.datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
	return render(request, 'home.html', {'curDateTime': curDateTime})

def errorPage(request, url):
	template = loader.get_template('404.html')
	context = {
		'error_url': url,
	}
	return HttpResponse(template.render(context, request))
