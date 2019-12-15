#include <SPI.h>
#include <Ethernet.h> 
#include <PubSubClient.h> 

// MAC Address of the Gizduino-IOT, replace the '?' with your group number
byte mac[] = {0xDE,0xED,0xBA,0xFE,0xFE,0x01}; 
//IPAddress ip(192, 168, 0, 37);
// IP Address of your Broker Computer, replace the '??' with the last octet
const IPAddress server(192, 168, 1, 7); 
const char deviceID[] = "ArduinoOne";

EthernetClient ethClient; 
PubSubClient client(ethClient);

// MQTT topic on the broker (Uncomment only one)
//extern const char mqtt_arduino_one[]; 
extern const char mqtt_arduino_two[]; 
//------------------CHANGE----------------
const char mqtt_controller[] = "/web/control";

//char msg[64];
char msg[64];
char topic[32];

void callback(char* topic, byte* payload, unsigned int length) { 
  memcpy(msg, payload, length);
  msg[length] = '\0';
  //FOR DEBUGGING
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(msg);

  if(strcmp(msg, "GREEN")==0){
    green();
  }else if(strcmp(msg, "RED")==0){
    red();
  }
} 

void reconnect() {
  if(!client.connected()){
    // Loop until connection is completed
    while (!client.connected()) {
      Serial.print("Attempting MQTT connection..."); 
      if (client.connect("arduinoClient")) { 
        Serial.println("Connected"); 
        client.publish("outTopic", "Connected"); 
        //                            ------------------CHANGE----------------
        client.subscribe(mqtt_arduino_two);
        
      } else { 
        Serial.print("Failed, rc="); 
        Serial.print(client.state()); 
        Serial.println(" try again in 3 seconds");
        delay(2000); 
      } 
    } 
  }
}

void connectionSetup() {
  Serial.begin(9600);

  client.setClient(ethClient);
  client.setServer(server, 1883);
  client.setCallback(callback);
  Ethernet.begin(mac);
  print_local_IP();
}

void print_local_IP(){
  Serial.print("My IP address: "); 
  for (byte nCtr = 0; nCtr < 4; nCtr++){
    Serial.print(Ethernet.localIP()[nCtr], DEC); 
    Serial.print(".");
  }
  Serial.println(); 
}  

void mqttLoop(){
  client.loop();
}

void pub(const char* topic, char* msg){
  client.publish(topic, msg);
} 