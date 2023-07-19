#include "esp_camera.h"
#include <WiFi.h>
#include <Arduino.h>
#include <EEPROM.h>
//
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
//#define CAMERA_MODEL_WROVER_KIT // Has PSRAM
//#define CAMERA_MODEL_ESP_EYE // Has PSRAM
//#define CAMERA_MODEL_ESP32S3_EYE // Has PSRAM
//#define CAMERA_MODEL_M5STACK_PSRAM // Has PSRAM
//#define CAMERA_MODEL_M5STACK_V2_PSRAM // M5Camera version B Has PSRAM
//#define CAMERA_MODEL_M5STACK_WIDE // Has PSRAM
//#define CAMERA_MODEL_M5STACK_ESP32CAM // No PSRAM
//#define CAMERA_MODEL_M5STACK_UNITCAM // No PSRAM
#define CAMERA_MODEL_AI_THINKER // Has PSRAM
//#define CAMERA_MODEL_TTGO_T_JOURNAL // No PSRAM
//#define CAMERA_MODEL_XIAO_ESP32S3 // Has PSRAM
// ** Espressif Internal Boards **
//#define CAMERA_MODEL_ESP32_CAM_BOARD
//#define CAMERA_MODEL_ESP32S2_CAM_BOARD
//#define CAMERA_MODEL_ESP32S3_CAM_LCD

#include "camera_pins.h"

// ===========================
// Enter your WiFi credentials
// ===========================

void startCameraServer();
void setupLedFlash(int pin);

#include <EEPROM.h>

void saveWifiCredentials(const char* ssid, const char* password) {
  int ssidLength = strlen(ssid);
  int passLength = strlen(password);

  // Ghi độ dài của SSID và mật khẩu vào EEPROM (2 byte)
  EEPROM.write(0, ssidLength);
  EEPROM.write(1, passLength);

  // Ghi dữ liệu SSID và mật khẩu vào EEPROM (từ byte 2)
  for (int i = 0; i < ssidLength; i++) {
    EEPROM.write(i + 2, ssid[i]);
  }
  for (int i = 0; i < passLength; i++) {
    EEPROM.write(i + 2 + ssidLength, password[i]);
  }

  EEPROM.commit();
}

void setupSmartConfig() {
  // Kiểm tra xem đã lưu trữ thông tin Wi-Fi trước đó chưa
  int ssidLength = EEPROM.read(0);
  int passLength = EEPROM.read(1);

  if (ssidLength > 0 && passLength > 0) {
    char* ssid = new char[ssidLength + 1];
    char* password = new char[passLength + 1];

    // Đọc thông tin SSID và mật khẩu từ EEPROM
    for (int i = 0; i < ssidLength; i++) {
      ssid[i] = char(EEPROM.read(i + 2));
    }
    ssid[ssidLength] = '\0';

    for (int i = 0; i < passLength; i++) {
      password[i] = char(EEPROM.read(i + 2 + ssidLength));
    }
    password[passLength] = '\0';

    // Kết nối Wi-Fi với thông tin đã lưu trữ
    WiFi.begin(ssid, password);
    delete[] ssid;
    delete[] password;
    
    // Chờ kết nối Wi-Fi
    int timeout = 10; // Thời gian chờ kết nối (giây)
    while (WiFi.status() != WL_CONNECTED && timeout > 0) {
      delay(1000);
      timeout--;
    }

    if (WiFi.status() == WL_CONNECTED) {
      // Kết nối Wi-Fi thành công
      Serial.println("WiFi connected");
      startCameraServer();

      Serial.print("Camera Ready! Use 'http://");
      Serial.print(WiFi.localIP());
      Serial.println("' to connect");
      
      return;
    }
  }

  // Nếu chưa lưu trữ thông tin Wi-Fi hoặc kết nối không thành công,
  // tiến hành SmartConfig
  Serial.println("There is no saved wifi ID and password!");
  WiFi.beginSmartConfig();

  Serial.println("");
  Serial.println("Waiting for SmartConfig.");
  while (!WiFi.smartConfigDone()) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("SmartConfig done.");

  // Lưu trữ thông tin Wi-Fi
  const char* ssid = WiFi.SSID().c_str();
  const char* password = WiFi.psk().c_str();
  saveWifiCredentials(ssid, password);

  // Chờ kết nối Wi-Fi
  int timeout = 10; // Thời gian chờ kết nối (giây)
  while (WiFi.status() != WL_CONNECTED && timeout > 0) {
    delay(1000);
    timeout--;
  }

  if (WiFi.status() == WL_CONNECTED) {
    // Kết nối Wi-Fi thành công
    Serial.println("WiFi connected");
    startCameraServer();

    Serial.print("Camera Ready! Use 'http://");
    Serial.print(WiFi.localIP());
    Serial.println("' to connect");
  } else {
    // Kết nối Wi-Fi không thành công
    Serial.println("Failed to connect to WiFi");
  }
}

void setup() {
  Serial.begin(115200);
  EEPROM.begin(512);
  WiFi.mode(WIFI_AP_STA);
  Serial.setDebugOutput(true);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_UXGA;
  config.pixel_format = PIXFORMAT_JPEG; // for streaming
  //config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 1;
  
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if(config.pixel_format == PIXFORMAT_JPEG){
    if(psramFound()){
      config.jpeg_quality = 10;
      config.fb_count = 2;
      config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
      // Limit the frame size when PSRAM is not available
      config.frame_size = FRAMESIZE_SVGA;
      config.fb_location = CAMERA_FB_IN_DRAM;
    }
  } else {
    // Best option for face detection/recognition
    config.frame_size = FRAMESIZE_240X240;
#if CONFIG_IDF_TARGET_ESP32S3
    config.fb_count = 2;
#endif
  }

#if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
#endif

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  if(config.pixel_format == PIXFORMAT_JPEG){
    s->set_framesize(s, FRAMESIZE_QVGA);
  }

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

#if defined(CAMERA_MODEL_ESP32S3_EYE)
  s->set_vflip(s, 1);
#endif

// Setup LED FLash if LED pin is defined in camera_pins.h
#if defined(LED_GPIO_NUM)
  setupLedFlash(LED_GPIO_NUM);
#endif

  // Setup Smart Config and server
  setupSmartConfig();
}

void loop() {
  // Do nothing. Everything is done in another task by the web server
  delay(10000);
}
