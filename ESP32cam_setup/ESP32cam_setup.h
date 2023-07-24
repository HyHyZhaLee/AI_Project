#include "esp_camera.h"
#include <WiFi.h>
#include <Arduino.h>
#include <EEPROM.h>
// WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
//            Ensure ESP32 Wrover Module or other board with PSRAM is selected
//            Partial images will be transmitted if image exceeds buffer size
//
//            You must select partition scheme from the board menu that has at least 3MB APP space.
//            Face Recognition is DISABLED for ESP32 and ESP32-S2, because it takes up from 15 
//            seconds to process single frame. Face Detection is ENABLED if PSRAM is enabled as well
// ===================
// Select camera model
// ===================
#define CAMERA_MODEL_AI_THINKER // Has PSRAM
#include "camera_pins.h"
#include <Preferences.h>

Preferences preferences;

void startCameraServer();
void setupLedFlash(int pin);
String ssid;
String password;

void flashing_led(int num, int freq = 100){
  for(int i = num; i>0; i--){
    analogWrite(LED_GPIO_NUM, 2);
    delay(freq);
    analogWrite(LED_GPIO_NUM, 0);
    delay(freq);
  }
  analogWrite(LED_GPIO_NUM, 0);
};

void saveWifiCredentials(String ssid, String password) {
  preferences.begin("credentials", false);
  preferences.putString("ssid", ssid); 
  preferences.putString("password", password);
  preferences.end();
}

bool check_savedWifi(){
  bool result = 0;
  // Kiểm tra xem đã lưu trữ thông tin Wi-Fi trước đó chưa
  preferences.begin("credentials", false);
 
  ssid = preferences.getString("ssid", ""); 
  password = preferences.getString("password", "");

  if (ssid == "" || password == ""){
    Serial.println("No values saved for ssid or password");
  }
  else {
    // Connect to Wi-Fi
    WiFi.begin(ssid.c_str(), password.c_str());
    Serial.print("Connecting to WiFi.");
    int timeout = 10; // Thời gian chờ kết nối (giây)
    while (WiFi.status() != WL_CONNECTED && timeout > 0) {
      flashing_led(1,500);
      Serial.print(".");
      timeout--;
    }
    Serial.println("");
    if(WiFi.status() == WL_CONNECTED) result = 1;
    else result = 0;      
  }
  return result;
}

void setupSmartConfig() {
  WiFi.beginSmartConfig();
  Serial.println("Waiting for SmartConfig.");
  // Chờ kết nối Wi-Fi
  while (!WiFi.smartConfigDone()) {
    flashing_led(1,1000);
    Serial.print(".");
  }  
  Serial.println("");
  Serial.println("SmartConfig done.");
}

void printSuccess(){
    startCameraServer();
    Serial.println("WiFi connected");
    Serial.print("Camera Ready! Use 'http://");
    Serial.print(WiFi.localIP());
    Serial.println("' to connect.");
    Serial.print("Or use URL: 'http://");
    Serial.print(WiFi.localIP());
    Serial.println(":81/stream' to ask for streaming in third-party app.");
    return;
}

void setupWifi(){
  Serial.println("");
  // Kiểm tra wifi có lưu chưa
  if(!check_savedWifi()){ 
    // tiến hành SmartConfig
    Serial.println("Cannot connect to saved wifi! Setup smart config...");
    preferences.clear();
    flashing_led(2);
    setupSmartConfig();
  }
  // Lưu trữ thông tin Wi-Fi
  ssid = WiFi.SSID().c_str();
  password = WiFi.psk().c_str();
  saveWifiCredentials(ssid, password);
  
  printSuccess();
}
