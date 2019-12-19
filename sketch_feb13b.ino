// Loading the ESP8266WiFi library and the PubSubClient library
#include <ESP8266WiFi.h>
#include "Nokia_5110.h"
#include <PubSubClient.h>

#define RST 4
#define CE 5
#define DC 12
#define DIN 13
#define CLK 14
#define PSHBTN 15

Nokia_5110 lcd = Nokia_5110(RST, CE, DC, DIN, CLK);

// Network credentials
const char* ssid = "Ericagui 2G";
const char* password = "gui4688erica";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.0.177";

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);

// Connect an LED to each GPIO of your ESP8266
const int ledGPIO5 = 10; //Gaveta 01
const int ledGPIO4 = 15; //Gaveta 02
const int ledGPIO3 = 10; //Gaveta 03
const int ledGPIO1 = 15; //Gaveta 04

//Global variable to set message
String message_to_send;
String topic_to_send;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  if(topic=="chamados/novochamado"){
      lcd.clear();
      lcd.print(messageTemp);
      igitalWrite(ledGPIO5, LOW);
      igitalWrite(ledGPIO4, LOW);
      igitalWrite(ledGPIO3, LOW);
      igitalWrite(ledGPIO1, LOW);
      
      if(messageTemp.startsWith("1")){
        topic_to_send = "gaveta/01";
        message_to_send = "OPEN01";
        digitalWrite(ledGPIO5, HIGH);
        lcd.clear();
        lcd.println(messageTemp);
      }
      else if(messageTemp.startsWith("2")){
        topic_to_send = "gaveta/02";
        message_to_send = "OPEN02";
        digitalWrite(ledGPIO4, LOW);
        lcd.clear();
        lcd.println(messageTemp);
      }
      else if(messageTemp.startsWith("3")){        
        topic_to_send = "gaveta/03";
        message_to_send = "OPEN03";
        digitalWrite(ledGPIO3, LOW);
        lcd.clear();
        lcd.println(messageTemp);
      }
      else if(messageTemp.startsWith("4")){
        topic_to_send = "gaveta/04";
        message_to_send = "OPEN04";
        digitalWrite(ledGPIO1, LOW);
        lcd.clear();
        lcd.println(messageTemp);
      }
  }
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");


    if (client.connect("ESP8266Client")) {
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      // You can subscribe to more topics (to control more LEDs in this example)
      client.subscribe("esp8266/4");
      client.subscribe("esp8266/5");
      client.subscribe("chamados/novochamado");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(ledGPIO4, OUTPUT);
  pinMode(ledGPIO5, OUTPUT);
  pinMode(ledGPIO3, OUTPUT);
  pinMode(ledGPIO1, OUTPUT);
  pinMode(PSHBTN, INPUT);
  
  
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
  
    client.connect("ESP8266Client");

    int limparTela;
    limparTela = digitalRead(PSHBTN);
    if (limparTela == 1)
    {
      client.publish(topic_to_send,message_to_send);
      lcd.clear();
      delay(20);
    }
}
