#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <Arduino.h>
#include <Hash.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <Adafruit_Sensor.h>
#include <stdlib.h>
#include <DHT.h>


const char* ssid = "DesaiResidence";
const char* password = "Kookado111";

#define DHTPIN 3     // Digital pin connected to the DHT sensor
#define DHTTYPE    DHT11     // DHT 11

DHT dht(DHTPIN, DHTTYPE);

// current temperature & humidity, updated in loop()
float t = 0.0;
float h = 0.0;

// Create AsyncWebServer object on port 80
// AsyncWebServer server(80);

// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long previousMillis = 0;    // will store last time DHT was updated

// Updates DHT readings every 10 seconds
const long interval = 1000;

bool postStuff (String postData, String path);

bool dhtStuff (unsigned long previousMillis);

void setup()
{
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting...");
  }

  Serial.println("");
  Serial.println("connected IP address");
  Serial.println(WiFi.localIP());
}

void loop()
{
  //get measurements from dht sensor
  if (!dhtStuff(previousMillis)){
    delay(1000); 
  }

  // assemble the path for the POST message:
  String extension = "/api/post_value";
  String path = "http://192.168.0.20:5000" + extension;
  String contentType = "application/json";

  //turning float t to string
  String temp = String(t);
  String humid = String(h);
  String jsonString = "{\"temp\":" + temp + ",\"humid\":" + humid + "}";
  Serial.println(jsonString);
  //"{\"api_key\":\"tPmAT5Ab3j7F9\",\"sensor\":\"BME280\",\"value1\":\"24.25\",\"value2\":\"49.54\",\"value3\":\"1005.14\"}"

  //post data to server
  if (!postStuff(jsonString, path)){
    delay(1000);
  }

  delay(1000);
}

bool dhtStuff (unsigned long previousMillis) {
  unsigned long currentMillis = millis();
  bool okay = true;
  if ((currentMillis - previousMillis) >= interval) {
    // save the last time you updated the DHT values
    previousMillis = currentMillis;
    
    // Read temperature as Celsius (the default)
    float newT = dht.readTemperature();
    
    // if temperature read failed, don't change t value
    if (isnan(newT)) {
      Serial.println("Failed to read from DHT sensor!");
      okay = false;
    }
    else {
      t = newT;
      Serial.println(t);
    }
    
    // Read Humidity
    float newH = dht.readHumidity();
    // if humidity read failed, don't change h value
    if (isnan(newH)) {
      Serial.println("Failed to read from DHT sensor!");
      okay = false;
    }
    else {
      h = newH;
      Serial.println(h);
    }
    
    return okay;
  }
}

bool postStuff (String postData, String path){
  //post request
  Serial.println("making POST request");
  WiFiClient client;
  HTTPClient http;

  Serial.println(path.c_str());
  Serial.println(postData);
  
  http.begin(client, path.c_str());
  http.addHeader("Content-Type", "application/json");

  // send the POST request
  int httpCode = http.POST(postData);

  if (httpCode > 0) {
    // HTTP header has been send and Server response header has been handled
    Serial.printf("[HTTP] POST... code: %d\n", httpCode);

    // file found at server
    if (httpCode == HTTP_CODE_OK) {
      const String& payload = http.getString();
      Serial.println("received payload:\n<<");
      Serial.println(payload);
      Serial.println(">>\n");
    }
    return true;
  }
  
  else {
    Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    return false;
  }
}
