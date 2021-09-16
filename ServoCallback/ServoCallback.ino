#include <Servo.h>

/*
  Callback LED

  This example creates a BLE peripheral with service that contains a
  characteristic to control an LED. The callback features of the
  library are used.

  The circuit:
  - Arduino MKR WiFi 1010, Arduino Uno WiFi Rev2 board, Arduino Nano 33 IoT,
    Arduino Nano 33 BLE, or Arduino Nano 33 BLE Sense board.

  You can use a generic BLE central app, like LightBlue (iOS and Android) or
  nRF Connect (Android), to interact with the services and characteristics
  created in this sketch.

  This example code is in the public domain.
*/

#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

BLEService servoService("19B10000-E8F2-537E-4F6C-D104768A1214"); // create service

const int NUM_SERVOS = 5;
const int STARTING_PIN = 2;

// Array of BLE Characteristics
BLEByteCharacteristic sliderCharacteristics[] = {
  BLEByteCharacteristic("7c962495-dd04-496a-87a8-2f837bc3eedd", BLERead | BLEWrite),
  BLEByteCharacteristic("84e1e552-67a4-4a29-8553-b597c731554f", BLERead | BLEWrite),
  BLEByteCharacteristic("9bb9e2bc-5799-49ce-a1cf-8385de906f7f", BLERead | BLEWrite),
  BLEByteCharacteristic("577f2be7-5c69-4591-87bc-67fbf914aeb4", BLERead | BLEWrite),
  BLEByteCharacteristic("c614f8b8-f751-4197-9eda-53652d882deb", BLERead | BLEWrite),
};

BLEByteCharacteristic aXBLE = BLEByteCharacteristic("19B10001-E8F2-537E-4F6C-D204768A1214", BLERead | BLEWrite);
BLEByteCharacteristic aYBLE = BLEByteCharacteristic("19B10001-E8F2-537E-4F6C-E204768A1214", BLERead | BLEWrite);
BLEByteCharacteristic aZBLE = BLEByteCharacteristic("19B10001-E8F2-537E-4F6C-F204768A1214", BLERead | BLEWrite);
BLEByteCharacteristic gXBLE = BLEByteCharacteristic("19B10001-E8F2-537E-4F6C-G204768A1214", BLERead | BLEWrite);
BLEByteCharacteristic gYBLE = BLEByteCharacteristic("19B10001-E8F2-537E-4F6C-E104768A1214", BLERead | BLEWrite);
BLEByteCharacteristic gZBLE = BLEByteCharacteristic("19B10001-E8F2-537E-4F6C-A204768A1214", BLERead | BLEWrite); 

// Array of servos
Servo servos[] = {Servo(), Servo(), Servo(), Servo(), Servo()};


void setup() {
  //  Serial.begin(9600);
  for (int i = 0; i < NUM_SERVOS;  i++) {
    servos[i].attach(STARTING_PIN + i);  // attaches the servo on pin 9 to the servo object
  }

  //  while (!Serial);

  // begin initialization
  if (!BLE.begin()) {
    //    Serial.println("starting BLE failed!");

    while (1);
  }

  // set the local name peripheral advertises
  BLE.setLocalName("ServoCallback");
  
  // set the UUID for the service this peripheral advertises
  BLE.setAdvertisedService(servoService);

  // add the characteristic to the service
  for (int i = 0; i < NUM_SERVOS;  i++) {
    servoService.addCharacteristic(sliderCharacteristics[i]);
  }

  servoService.addCharacteristic(aXBLE);
  aXBLE.writeValue(0);

  // add service
  BLE.addService(servoService);

  // assign event handlers for connected, disconnected to peripheral
  BLE.setEventHandler(BLEConnected, blePeripheralConnectHandler);
  BLE.setEventHandler(BLEDisconnected, blePeripheralDisconnectHandler);

  // assign event handlers for characteristic
  sliderCharacteristics[0].setEventHandler(BLEWritten, servo0Activated);
  sliderCharacteristics[0].setValue(0);
  sliderCharacteristics[1].setEventHandler(BLEWritten, servo1Activated);
  sliderCharacteristics[1].setValue(0);
  sliderCharacteristics[2].setEventHandler(BLEWritten, servo2Activated);
  sliderCharacteristics[2].setValue(0);
  sliderCharacteristics[3].setEventHandler(BLEWritten, servo3Activated);
  sliderCharacteristics[3].setValue(0);
  sliderCharacteristics[4].setEventHandler(BLEWritten, servo4Activated);
  sliderCharacteristics[4].setValue(0);

  // start advertising
  BLE.advertise();

  //  Serial.println(("Bluetooth device active, waiting for connections..."));
}

void loop() {
  // poll for BLE events
//  float aX, aY, aZ, gX, gY, gZ;
  
  BLE.poll();
//  if (IMU.accelerationAvailable()) {
//    IMU.readAcceleration(aX, aY, aZ);
//    aXBLE.writeValue(aX);
//  }
//  delay(100);
}

void blePeripheralConnectHandler(BLEDevice central) {
  // central connected event handler
  //  Serial.print("Connected event, central: ");
  //  Serial.println(central.address());
}

void blePeripheralDisconnectHandler(BLEDevice central) {
  // central disconnected event handler
  //  Serial.print("Disconnected event, central: ");
  //  Serial.println(central.address());
}

void servoActivated(int index) {
  //  Serial.print("Servo ");
  //  Serial.print(index);
  //  Serial.print(", Value: ");
  //  Serial.println(sliderCharacteristics[index].value());
  servos[index].write(sliderCharacteristics[index].value());
}

void servo0Activated(BLEDevice central, BLECharacteristic characteristic) {
  servoActivated(0);
}

void servo1Activated(BLEDevice central, BLECharacteristic characteristic) {
  servoActivated(1);
}

void servo2Activated(BLEDevice central, BLECharacteristic characteristic) {
  servoActivated(2);
}

void servo3Activated(BLEDevice central, BLECharacteristic characteristic) {
  servoActivated(3);
}

void servo4Activated(BLEDevice central, BLECharacteristic characteristic) {
  servoActivated(4);
}
