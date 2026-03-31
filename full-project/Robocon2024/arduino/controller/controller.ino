#include <ESP32Servo.h>
#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <Arduino.h>

#define serialM Serial1
#define debug Serial
#define rx1pin 18
#define tx1pin 17
#define rx2pin 41
#define tx2pin 42
#define grip1 1
#define grip2 2
#define inball 16
#define outball 20
#define inball_grip 15
#define servo1 9
#define servo2 10

double lx = 250.0;
double ly = 250.0;
double r = 77;
double offset = 0;
double offsetang = 3;
double posx, posy, posz;
double w1, w2, w3, w4;

// For pos camera
double veloX, veloY, angVelo;

// int pixx, pixy;
int Team; // 0 = "blue", 1 = "red"
int Retry; // 1 is run retry mode
int Start = 0; // 1 Start mode
// For distance
double vx, vy, omega, dis, ang, t;

//Detection
double depth;
int detectionMode;
int coreX, coreY;

double errorx, errory, errorw, kpx, kpy, kpw, kix, kiy, kiw, kdx, kdy, kdw, px, ix, dx, py, iy, dy, pw, iw, dw, pidx, pidy, pidw;
double pre_errorx, pre_errory, pre_errorw;
double maxsp = 1500;
double minsp = -1500;
double maxspw = 1.57;
double minspw = -1.57;

int pwmch[5] = { 0, 1, 2, 3, 4 };
int pwmpin[5] = { 4, 5, 6, 7, 8};
int freq = 5000;
int resolution = 8;

bool getBall = false;

Servo servob, servot;

TaskHandle_t Task1;

void setup() {
  serialM.begin(115200, SERIAL_8N1, rx2pin, tx2pin);
  serialM.setTimeout(10);
  debug.begin(115200);
  debug.setTimeout(100);
  pinMode(grip1, OUTPUT);
  pinMode(grip2, OUTPUT);
  pinMode(inball, INPUT);
  pinMode(outball, INPUT);
  pinMode(inball_grip, INPUT);

  servob.attach(servo1);
  servot.attach(servo2);
  servob.write(45);  //open 140
  servot.write(0);

  for (int i = 0; i < 5; i++) {
    pinMode(pwmpin[i], OUTPUT);
    digitalWrite(pwmpin[i], 0);
  }

  grip(false);
  delay(2000);
  for (int i = 1; i < 5; i++) {
    run_speed(i, 0);
  }
  delay(5000);

  //create a task that will be executed in the Task1code() function, with priority 1 and executed on core 0
  xTaskCreatePinnedToCore(
    Task1code, /* Task function. */
    "Task1",   /* name of task. */
    10000,     /* Stack size of task */
    NULL,      /* parameter of the task */
    1,         /* priority of the task */
    &Task1,    /* Task handle to keep track of created task */
    1);        /* pin task to core 0 */
  delay(500);
}

void loop() {
  digitalWrite(pwmpin[1], 1);
  if (detectionMode != 0){
    find_object();
    if (detectionMode == 1){
      if(getBall == true){
        collect_ball();
        getBall = false;
       }
    }
  }

  if (Start == 2 ){
    debug.print("Test Run Started");
    motorMotion(vx, vy, omega, dis, ang, t);
    Start = 0;
  }
  
}

//Task1code: blinks an LED every 1000 ms
void Task1code(void* pvParameters) {
  // Serial.print("Task1 running on core ");
  // Serial.println(xPortGetCoreID());
  for (;;) {
    // if (serialM.available() > 0) {
    //   byte x = serialM.read();
    //   debug.print(x, HEX);
    //   debug.print(" ");
    // }
    if (debug.available() > 0) {
      String cmd = debug.readString();
//      debug.println(cmd);
      deserialJson(cmd);
    }
  }
}

void grip(bool release) {
  if (release == false) {
    digitalWrite(grip1, 0);
    digitalWrite(grip2, 1);
  } else {
    digitalWrite(grip1, 1);
    digitalWrite(grip2, 0);
  }
}

void deserialJson(String input) {
  JsonDocument doc;

  DeserializationError error = deserializeJson(doc, input);

  if (error) {
    debug.print(F("deserializeJson() failed: "));
    debug.println(error.f_str());
    return;
  }

  Team = doc["Team"]; // 0 = "blue", 1 = "red"
  Retry = doc["Retry"]; // 0
  Start = doc["Start"]; // 0
  
  vx = doc["Vx"]; // 0
  vy = doc["Vy"]; // 0
  omega = doc["Omega"]; // 0
  dis = doc["Dis"]; // 0
  ang = doc["Ang"]; // 0
  t = doc["Time"]; // 0

  depth = doc["Depth"];
  detectionMode = doc["DetectionMode"];
  JsonArray Pixel = doc["Pixel"];
  coreX = Pixel[0];
  coreY = Pixel[1];

  JsonArray Kx = doc["Kx"];
  kpx = Kx[0];  // 0.01
  kix = Kx[1];  // 0.1
  kdx = Kx[2];  // 0.1

  JsonArray Ky = doc["Ky"];
  kpy = Ky[0];  // 0.01
  kiy = Ky[1];  // 0
  kdy = Ky[2];  // 0

  JsonArray Kw = doc["Kw"];
  kpw = Kw[0];  // 0.01
  kiw = Kw[1];  // 0
  kdw = Kw[2];  // 0

  JsonArray Velocity = doc[F("Velocity")];
  veloY = Velocity[0];                 // -0.0007716716499999166
  double Velocity_1 = Velocity[1];  // -0.010633857920765877
  veloX = Velocity[2];                 // 0.0016034386353567243

  JsonArray Angular_velocity = doc[F("Angular velocity")];
  double Angular_velocity_0 = Angular_velocity[0];  // 0.00024088229110930115
  angVelo = Angular_velocity[1];                          // 0.0001808108063414693
  double Angular_velocity_2 = Angular_velocity[2];  // 0.0019626242574304342

}
