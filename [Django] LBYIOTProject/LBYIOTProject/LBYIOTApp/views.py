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
ipadd = "10.200.180.9"
arduinoOneTopic = "/device/one"
arduinoTwoTopic = "/device/two"
arduinoAllTopic = "/device/all"
global mqttMsg

countdown = 0
roadOneState = False
roadTwoState = False
currentRoadState = 1

def on_connect(client, userdata, rc):
        print ("Connected with code"+ str(rc))     
   
def on_message(client, userdata, msg):        
        mqttMsg = msg.payload.decode()
        #FOR DEBUGGING
        print ("Topic:", str(msg.topic))
        print ("Message:", str(msg.payload.decode()))
        print(mqttRead)

        evaluate(msg);

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ipadd,1883,60)
client.subscribe(arduinoOneTopic)
client.subscribe(arduinoTwoTopic)
client.subscribe(arduinoAllTopic)
client.loop_start()
mqttc = mqtt.Client("Python Pub")
mqttc.connect(ipadd, 1883)

def readerFunction(request):          
        JSONer = {}

        print(countdown)
        JSONer['countdown'] = countdown
        if(currentRoadState == 1):
                JSONer['greenOne'] = 'green'
                JSONer['redOne'] = 'black'
                JSONer['greenTwo'] = 'black'
                JSONer['redTwo'] = 'red'
                
        elif(currentRoadState == 2):
                JSONer['greenOne'] = 'black'
                JSONer['redOne'] = 'red'
                JSONer['greenTwo'] = 'green'
                JSONer['redTwo'] = 'black'
        
        return HttpResponse(json.dumps(JSONer))
	# time.sleep(2)

def publish_change():
        if(currRoadState == 1):
                if(roadTwoState and not roadOneState):
                        mqttc.publish(arduinoTwoTopic, "GREEN")
                        mqttc.publish(arduinoOneTopic, "RED")
                        currRoadState = 2
                elif(roadTwoState and roadOneState):
                        #timer 3 sec
                        timer(3);
                        mqttc.publish(arduinoTwoTopic, "GREEN")
                        mqttc.publish(arduinoOneTopic, "RED")
                        currRoadState = 2
                elif(not roadTwoState and not roadOneState):
                        #timer 5 sec
                        timer(5);
                        mqttc.publish(arduinoTwoTopic, "GREEN")
                        mqttc.publish(arduinoOneTopic, "RED")
                        currRoadState = 2
        elif(currRoadState == 2):
                if(roadOneState and not roadTwoState):
                        mqttc.publish(arduinoOneTopic, "GREEN")
                        mqttc.publish(arduinoTwoTopic, "RED")
                        currRoadState = 1
                elif(roadOneState and roadTwoState):
                        #timer 3 sec
                        timer(3);
                        mqttc.publish(arduinoOneTopic, "GREEN")
                        mqttc.publish(arduinoTwoTopic, "RED")
                        currRoadState = 1
                elif(not roadOneState and not roadTwoState):
                        #timer 5 sec
                        timer(5);
                        mqttc.publish(arduinoOneTopic, "GREEN")
                        mqttc.publish(arduinoTwoTopic, "RED")
                        currRoadState = 1


def switch(request):
        print("Switch states")
        if (roadOneState == True):
                roadOneState = False
                roadTwoState = True
                currentRoadState = 2
        elif (roadTwoState == True):
                roadTwoState = False
                roadOneState = True
                currentRoadState = 1
                
        publish_change()
        return HttpResponse()

def evaluate(msg):
        if(str(msg.payload.decode()) == "CAR" and str(msg.topic()) == "/device/one"):
                roadOneState = True
        elif(str(msg.payload.decode()) == "NONE" and str(msg.topic()) == "/device/one"):
                roadOneState = False   
        elif(str(msg.payload.decode()) == "CAR" and str(msg.topic()) == "/device/two"):
                roadTwoState = True
        elif(str(msg.payload.decode()) == "NONE" and str(msg.topic()) == "/device/two"):
                roadTwoState = False

        publish_change()
        
def timer(delay):
        for x in range(delay,0,-1):
                #update timer displayed in web
                countdown = x
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
