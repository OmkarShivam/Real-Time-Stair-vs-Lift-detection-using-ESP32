#include <Wire.h>
#include <WiFi.h>
#include <Adafruit_BMP280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

const char* ssid = "wifi";
const char* password = "password";
const int portNumber = 8080;  // Change this to your desired port number

const int MPU_ADDRESS = 0x68; // MPU6050 I2C address
const float ACCEL_SCALE = 16384.0; // Accelerometer sensitivity scale factor
const float GYRO_SCALE = 131.0; // Gyroscope sensitivity scale factor

Adafruit_BMP280 bmp; // I2C
WiFiServer server(portNumber);
IPAddress staticIP(192, 168, 137, 242); // Desired static IP address
IPAddress gateway(192, 168, 137, 1);    // Your gateway IP address
IPAddress subnet(255, 255, 255, 0);   // Your subnet mask
IPAddress dns(8, 8, 8, 8);            // Your DNS server

const int redLedPin = 5;    // GPIO pin connected to the red LED
const int greenLedPin = 4;  // GPIO pin connected to the green LED
const int buttonPin = 2;    // GPIO pin connected to the push button

const char* activity = "Stairs";  // Initial state is stairs

// Function prototypes
void initializeMPU();
void writeRegister(uint8_t regAddress, uint8_t regValue);
float readAccelData();
float readGyroData();

void setup() {
  Serial.begin(9600);
  Wire.begin();
  initializeMPU();

  pinMode(buttonPin, INPUT_PULLUP);  // Internal pull-up resistor for the button

  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);

  // Initialize LEDs
  digitalWrite(redLedPin, HIGH);   // Turn on red LED
  digitalWrite(greenLedPin, LOW);  // Turn off green LED

  delay(1000);

  if (!bmp.begin(0x76)) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    while (1);
  }

  WiFi.config(staticIP, gateway, subnet, dns);  // Set static IP configuration
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  server.begin();
  Serial.println("Server started");
  Serial.print("Server IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Server port: ");
  Serial.println(portNumber);  // Print the assigned port number

  Serial.println(F("BMP280 sensor found"));
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,    /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,   /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,     /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500);/* Standby time. */

  Serial.println(F("BMP280 sensor initialized"));
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");

    while (client.connected()) {
      float accelX, accelY, accelZ;
      float gyroX, gyroY, gyroZ;

      accelX = readAccelData();
      accelY = readAccelData();
      accelZ = readAccelData();
      gyroX = readGyroData();
      gyroY = readGyroData();
      gyroZ = readGyroData();

      float altitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);
      Serial.print(F("Altitude = "));
      Serial.print(altitude);
      Serial.println(F(" meters"));

      // Get current timestamp
      unsigned long currentMillis = millis();

      // Check the state of the push button
      if (digitalRead(buttonPin) == LOW) {
        // Button is pressed, change activity to "Lift"
        activity = "Stairs";
        // Update LEDs accordingly
        digitalWrite(redLedPin, HIGH);     // Turn off red LED
        digitalWrite(greenLedPin, LOW);  // Turn on green LED
        delay(500);
      } else {
        // Button is not pressed, activity remains as "Stairs"
        activity = "Lift";
        // Update LEDs accordingly
        digitalWrite(redLedPin, LOW);    // Turn on red LED
        digitalWrite(greenLedPin, HIGH);   // Turn off green LED
        delay(500);
      }

      // Send data for each sensor reading separately
      client.print(String(currentMillis) + "," + String(accelX) + "," + String(accelY) + "," + String(accelZ) + "," +
                   String(gyroX) + "," + String(gyroY) + "," + String(gyroZ) + "," +
                   String(altitude) + "," + String(activity) + "\n");

      delay(1000); // Collect data every second
    }

    client.stop();
    Serial.println("Client disconnected");
  }
}

void initializeMPU() {
  // Wake up MPU6050 and set configurations
  writeRegister(0x6B, 0b00000000); // Power Management Register
  writeRegister(0x1B, 0x08); // Setting +/- 500 dps range for gyroscope
  writeRegister(0x1C, 0x08); // Setting +/- 4g range for accelerometer
}

void writeRegister(uint8_t regAddress, uint8_t regValue) {
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(regAddress);
  Wire.write(regValue);
  Wire.endTransmission();
}

float readAccelData() {
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x3B); // Starting register for Accel Readings
  Wire.endTransmission();
  Wire.requestFrom(MPU_ADDRESS, 6);

  if (Wire.available() >= 6) {
    int16_t rawAccel = Wire.read() << 8 | Wire.read();
    return static_cast<float>(rawAccel) / ACCEL_SCALE;
  }
  return 0.0;
}

float readGyroData() {
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(0x43); // Starting register for Gyro Readings
  Wire.endTransmission();
  Wire.requestFrom(MPU_ADDRESS, 6);

  if (Wire.available() >= 6) {
    int16_t rawGyro = Wire.read() << 8 | Wire.read();
    return static_cast<float>(rawGyro) / GYRO_SCALE;
  }
  return 0.0;
}
