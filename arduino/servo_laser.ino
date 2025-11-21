
#include <Servo.h>
Servo panServo;
Servo tiltServo;

const int PAN_PIN = 9;
const int TILT_PIN = 10;
const int LASER_PIN = 7;
const int SAFETY_PIN = 2;

int panDeg = 90;
int tiltDeg = 90;

void setup() {
  Serial.begin(115200);
  panServo.attach(PAN_PIN);
  tiltServo.attach(TILT_PIN);
  pinMode(LASER_PIN, OUTPUT);
  pinMode(SAFETY_PIN, INPUT_PULLUP);
  digitalWrite(LASER_PIN, LOW);
  panServo.write(panDeg);
  tiltServo.write(tiltDeg);
  Serial.println("ARDUINO:READY");
}

void loop() {
  if (Serial.available()) {
    String s = Serial.readStringUntil('\n');
    s.trim();
    if (s.startsWith("PAN:")) {
      int v = s.substring(4).toInt();
      panDeg = constrain(v, 0, 180);
      panServo.write(panDeg);
      Serial.print("ACK:PAN:");
      Serial.println(panDeg);
    } else if (s.startsWith("TILT:")) {
      int v = s.substring(5).toInt();
      tiltDeg = constrain(v, 0, 180);
      tiltServo.write(tiltDeg);
      Serial.print("ACK:TILT:");
      Serial.println(tiltDeg);
    } else if (s.startsWith("FIRE")) {
      // safety: only fire if safety button pressed (active LOW)
      if (digitalRead(SAFETY_PIN) == LOW) {
        digitalWrite(LASER_PIN, HIGH);
        delay(150);
        digitalWrite(LASER_PIN, LOW);
        Serial.println("ACK:FIRE");
      } else {
        Serial.println("ERR:SAFETY_OFF");
      }
    }
  }
}
