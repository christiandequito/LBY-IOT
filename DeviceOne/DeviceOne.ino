const char mqtt_arduino_one_out[] = "/device/one/out"; 
const char mqtt_arduino_one_in[] = "/device/one/in"; 
//const char mqtt_arduino_two[] = "/device/two"; ------------------CHANGE----------------

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

void connectionSetup();
void reconnect();
void pub(const char* topic, char* msg);
void mqttLoop();

void setup() {
  // put your setup code here, to run once:
  pinMode(r1_redLight, OUTPUT);
  pinMode(r1_greenLight, OUTPUT);
  pinMode(r2_redLight, OUTPUT);
  pinMode(r2_greenLight, OUTPUT);
  pinMode(d1_trigPin,OUTPUT);
  pinMode(d1_echoPin,INPUT);
  pinMode(d2_trigPin,OUTPUT);
  pinMode(d2_echoPin,INPUT);
  Serial.begin(9600);
  //initially light up road 1
  connectionSetup();
}

void loop() {
  reconnect();
  
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
    String s = "CAR";
    char cStringArr[10]; 
    s.toCharArray(cStringArr, s.length() + 1);
    if(prevState != s){
      prevState = s;
      pub(mqtt_arduino_one_out, cStringArr);
    }
    
  }else if(!checkDistance(r1distance) && !checkDistance(r2distance)){
    //                            ------------------CHANGE----------------
    String s = "NONE";
    char cStringArr[10];
    s.toCharArray(cStringArr, s.length() + 1);
//    pub(mqtt_arduino_one_out, cStringArr);
    if(prevState != s){
      prevState = s;
      pub(mqtt_arduino_one_out, cStringArr);
    }
  }

  mqttLoop();
  delay(2000);
}

//check if distance is within the threshold
boolean checkDistance(int distance){
  if(distance>4&&distance<8){
    return true;
  }else{
    return false;
  }
}

// hindi ba dapat parang cross sila?
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

//timer
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
