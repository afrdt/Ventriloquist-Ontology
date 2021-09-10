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

BLEService servoService("19B10000-E8F2-537E-4F6C-D104768A1214"); // create service

const int NUM_SERVOS = 5;
const int STARTING_PIN = 2;

// Array of BLE Characteristics
BLEByteCharacteristic sliderCharacteristics[] = {
  BLEByteCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite),
  BLEByteCharacteristic("19B10002-E8F2-537E-4F6C-D104768A1215", BLERead | BLEWrite),
  BLEByteCharacteristic("19B10003-E8F2-537E-4F6C-D104768A1216", BLERead | BLEWrite),
  BLEByteCharacteristic("19B10004-E8F2-537E-4F6C-D104768A1217", BLERead | BLEWrite),
  BLEByteCharacteristic("19B10005-E8F2-537E-4F6C-D104768A1218", BLERead | BLEWrite),
};

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
  BLE.poll();
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
