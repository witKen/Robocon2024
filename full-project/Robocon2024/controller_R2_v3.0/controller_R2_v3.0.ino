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
#define servo1 9
#define servo2 10

double lx = 250.0;
double ly = 250.0;
double r = 77;
double offset = 0;  //42
double offsetang = 3;
double posx, posy, posz;
double vx, vy, w, w1, w2, w3, w4;

int Team;       // 0 = "blue", 1 = "red"
int Retry;      // 1 is run retry mode
int Calibrate;  // 1 call calibrate camera
int Start;      // 1 start mode
float Vx, Vy, Omega, Dis, Ang, Ta, depth;
int pixx, pixy;
bool find_ball;
int detect;

double errorx, errory, errorw, kpx, kpy, kpw, kix, kiy, kiw, kdx, kdy, kdw, px, ix, dx, py, iy, dy, pw, iw, dw, pidx, pidy, pidw;
double pre_errorx, pre_errory, pre_errorw;
double maxsp = 1500;
double minsp = -1500;
double maxspw = 1.57;
double minspw = -1.57;

int pwmch[4] = { 0, 1, 2, 3 };
int pwmpin[4] = { 4, 5, 6, 7 };
int freq = 5000;
int resolution = 8;

Servo servob, servot;

TaskHandle_t Task1;
// TaskHandle_t Task2;

void setup() {
  serialM.begin(115200, SERIAL_8N1, rx1pin, tx1pin);
  serialM.setTimeout(10);
  debug.begin(115200);
  debug.setTimeout(100);
  pinMode(grip1, OUTPUT);
  pinMode(grip2, OUTPUT);
  pinMode(inball, INPUT);
  pinMode(outball, INPUT);

  servob.attach(servo1);
  servot.attach(servo2);
  servob.write(45);  //open 140
  servot.write(0);

  for (int i = 0; i < 4; i++) {
    // ledcSetup(pwmch[i], freq, resolution);
    // ledcAttachPin(pwmpin[i], pwmch[i]);
    // ledcWrite(pwmch[i], 0);
    pinMode(pwmpin[i], OUTPUT);
    digitalWrite(pwmpin[i], 0);
  }

  //  kpx = 0.5;
  //  kix = 0;
  //  kdx = 0;
  //  kpy = 0.5;
  //  kiy = 0;
  //  kdy = 0;
  //  kpw = 0.01;
  //  kiw = 0;
  //  kdw = 0;

  grip(false);
  delay(2000);
  serialM.flush();
  for (int i = 1; i < 5; i++) {
    run_speed(i, 0);
  }
  delay(5000);

  //  find_ball = true;
  //  motorMotion(1500, 0, 0, 6200, 0, 2 );
  //  motorMotion(0, -1500, 0, 3800, 0, 2);
  //  motorMotion(1500, 0, 0, 3700, 0, 2);
  //  motorMotion(0,0,45,1000,90,2);
  //  motorMotion(1000,0,0,3200,0,2);


  //  float lp1[] = {0, 0};
  //  float lp2[] = { -10, 10};

  //  float rp[] = {1, 2};
  //  dis_point_line(lp1, lp2, rp);

  //create a task that will be executed in the Task1code() function, with priority 1 and executed on core 0
  xTaskCreatePinnedToCore(
    Task1code, /* Task function. */
    "Task1",   /* name of task. */
    10000,     /* Stack size of task */
    NULL,      /* parameter of the task */
    0,         /* priority of the task */
    &Task1,    /* Task handle to keep track of created task */
    0);        /* pin task to core 0 */
  delay(500);
  // //create a task that will be executed in the Task2code() function, with priority 1 and executed on core 1
  // xTaskCreatePinnedToCore(
  //                   Task2code,   /* Task function. */
  //                   "Task2",     /* name of task. */
  //                   10000,       /* Stack size of task */
  //                   NULL,        /* parameter of the task */
  //                   1,           /* priority of the task */
  //                   &Task2,      /* Task handle to keep track of created task */
  //                   1);          /* pin task to core 1 */
  //   delay(500);
}

void loop() {
//  if (digitalRead(outball) == 1) {
//    for (int i = 0; i < 4; i++) {
//      digitalWrite(pwmpin[i], 1);
//    }
//    grip(true);
//  }
  if (digitalRead(inball) == 1) {
    for (int i = 0; i < 4; i++) {
      digitalWrite(pwmpin[i], 0);
    }
    grip(false);
  }
  delay(100);

  if (detect == 1) {
    ball_detect();
    detect = 0;
  }

  if (Start == 2) {
    motorMotion(Vx, Vy, Omega, Dis, Ang, Ta);
    //      motorMotion(0, -1500, 0, 3800, 0, 2);
    //      motorMotion(1500, 0, 0, 3700, 0, 2);
    //      motorMotion(0, 0, 45, 1000, 90, 2);

    //      find_ball = true;
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
      debug.println(cmd);
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

  //{ "Team": 0,"Start": 2, "Retry": 0, "Vx": 500, "Vy": 0, "Omega": 0, "Dis": 3000, "Ang": 0,"Time": 5, "DetectionMode": 0, "Depth": 0,"Pixel": [0,0], "Angular_velocity": [0,0,0], "Velocity": [0,0,0]}
  JsonDocument doc;

  DeserializationError error = deserializeJson(doc, input);

  if (error) {
    debug.print(F("deserializeJson() failed: "));
    debug.println(error.f_str());
    return;
  }

  Team = doc["Team"];    // 0 = "blue", 1 = "red"
  Retry = doc["Retry"];  // 0
  Start = doc["Start"];  // 0
  Vx = doc["Vx"];
  Vy = doc["Vy"];
  Omega = doc["Omega"];
  Dis = doc["Dis"];  // 0
  Ang = doc["Ang"];  // 0
  Ta = doc["Time"];  // 0
  detect = doc["DetectionMode"];
  depth = doc["Depth"];

  JsonArray Pixel = doc["Pixel"];
  pixx = Pixel[0];  // 0
  pixy = Pixel[1];  // 0

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
  vy = Velocity[0];                 // -0.0007716716499999166
  double Velocity_1 = Velocity[1];  // -0.010633857920765877
  vx = Velocity[2];                 // 0.0016034386353567243

  JsonArray Angular_velocity = doc[F("Angular velocity")];
  double Angular_velocity_0 = Angular_velocity[0];  // 0.00024088229110930115
  w = Angular_velocity[1];                          // 0.0001808108063414693
  double Angular_velocity_2 = Angular_velocity[2];  // 0.0019626242574304342

  //  JsonArray Position = doc[F("Position")];
  //  posx = Position[0] ;  // -0.00020906013378407806
  //  posy = Position[2] ;  // 0.000754627282731235
  //  posz = Position[1] ;  // -0.00004609348616213538
}
