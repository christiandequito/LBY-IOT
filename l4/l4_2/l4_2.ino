#include <SPI.h>
#include <Ethernet.h> 
#include <PubSubClient.h>
// MAC Address of the Gizduino-IOT, replace the '?' with your group number
byte mac[] = {0xDE,0xED,0xBA,0xFE,0xFE,0x02}; 
// IP Address of the Gizduino-IOT, replace the '?' with your group number 
//IPAddress ip(10, 200, 180, 180);
// IP Address of your Broker Computer, replace the '??' with the last octet
IPAddress server(10, 200, 180, 12); 

int r1_redLight = 2;
int r1_greenLight = 3;
int r2_redLight = 4;
int r2_greenLight = 5;
int d1_trigPin = 6;
int d1_echoPin = 7;
int d2_trigPin = 8;
int d2_echoPin = 9;
int roadOneState;
int roadTwoState;
String prevState = "";

char message[64];
char topic[32];

void callback(char* topic, byte* payload, unsigned int length) {   
  memcpy(message, payload, length);
  message[length] = '\0';
  //FOR DEBUGGING
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message);

  if(strcmp(message, "GREEN")==0){
    green();
  }else if(strcmp(message, "RED")==0){
    red();
  }
}

EthernetClient ethClient; 
PubSubClient client(ethClient); 

const char mqtt_arduino_two_out[] = "/device/two/out";
const char mqtt_arduino_two_in[] = "/device/two/in";

void reconnect() {  
// Loop until connection is completed  
  while (!client.connected()) {    
    Serial.print("Attempting MQTT connection...");     
    if (client.connect("arduinoClient2")) {      
      Serial.println("Connected");       
      client.publish("outTopic", "Hello world!");       
      client.subscribe(mqtt_arduino_two_in);     
    } else {       
      Serial.print("Failed, rc=");       
      Serial.print(client.state());      
      Serial.println(" try again in 3 seconds");      
      delay(3000);     
    }   
  } 
}

void setup(){   
  Serial.begin(9600);   
  client.setClient(ethClient);  
  client.setServer(server, 1883); // 1883 is the default port of MQTT  
  client.setCallback(callback);   
  Ethernet.begin(mac);  
  print_local_IP();
  
  
  pinMode(r1_redLight, OUTPUT);
  pinMode(r1_greenLight, OUTPUT);
  pinMode(r2_redLight, OUTPUT);
  pinMode(r2_greenLight, OUTPUT);
  pinMode(d1_trigPin,OUTPUT);
  pinMode(d1_echoPin,INPUT);
  pinMode(d2_trigPin,OUTPUT);
  pinMode(d2_echoPin,INPUT);
  
}  

void loop(){  
  if(!client.connected()){    
    reconnect();  
  }
  
  digitalWrite(d1_trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(d1_trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(d1_trigPin, LOW);
  
  int r1distance;
  int r2distance;
  long duration;
  
  duration = pulseIn(d1_echoPin, HIGH);
  r1distance = duration*0.034/2;

  Serial.print("D1 Distance : ");
  Serial.println(r1distance); 

  digitalWrite(d2_trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(d2_trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(d2_trigPin, LOW);

  duration = pulseIn(d2_echoPin, HIGH);
  r2distance = duration*0.034/2;
  Serial.print("D2 Distance: ");
  Serial.println(r2distance);

  if(checkDistance(r1distance) || checkDistance(r2distance)){
    //                            ------------------CHANGE----------------
    String sCar = "CAR";
    char cStringArr[10]; 
    sCar.toCharArray(cStringArr, sCar.length() + 1);
//    client.publish(mqtt_arduino_two_out, cStringArr);
    if(prevState != sCar){
      prevState = sCar;
      client.publish(mqtt_arduino_two_out, cStringArr);
    }
    
  }else if(!checkDistance(r1distance) && !checkDistance(r2distance)){
    //                            ------------------CHANGE----------------
    String sNone = "NONE";
    char cStringArr[10];
    sNone.toCharArray(cStringArr, sNone.length() + 1);
//    client.publish(mqtt_arduino_two_out, cStringArr);
    if(prevState != sNone){
      prevState = sNone;
      client.publish(mqtt_arduino_two_out, cStringArr);
    }
  }
  
  client.loop();
  delay(200);
}

//check if distance is within the threshold
boolean checkDistance(int distance){
  if(distance > 3 && distance < 9){
    return true;
  } else {
    return false;
  }
}

void green(){
  digitalWrite(r1_redLight, LOW);
  digitalWrite(r1_greenLight, HIGH);
  digitalWrite(r2_redLight, LOW);
  digitalWrite(r2_greenLight, HIGH);
}

void red(){
  digitalWrite(r1_redLight, HIGH);
  digitalWrite(r1_greenLight, LOW);
  digitalWrite(r2_redLight, HIGH);
  digitalWrite(r2_greenLight, LOW);
}

void delayTime(int timeGo){

  for(int i=0; i<timeGo; i++){
    delay(1000);
    Serial.print(timeGo-i + " ");
    //switch states lang
    int temp = roadOneState;
    roadOneState = roadTwoState;
    roadTwoState = temp;
  }
    
}

void print_local_IP(){
  Serial.print("My IP address: "); 
  for (byte nCtr = 0; nCtr < 4; nCtr++){
    Serial.print(Ethernet.localIP()[nCtr], DEC); 
    Serial.print(".");
  }
  Serial.println(); 
} 
