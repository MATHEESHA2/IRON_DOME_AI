#include <Servo.h>
#include <NewPing.h>

#define TRIGGER_PIN 7
#define ECHO_PIN 6
#define MAX_DISTANCE 400
#define SERVO_PIN 9
#define SCAN_SPEED_MS 20
#define ANGLE_MIN 0
#define ANGLE_MAX 180
#define DIST_THRESHOLD_CM 80

Servo scanServo;
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

unsigned long lastMove = 0;
int angle = ANGLE_MIN;
int dir = 1;

void setup() {
  Serial.begin(115200);
  scanServo.attach(SERVO_PIN);
  scanServo.write(angle);
  delay(500);
  Serial.println("START");
}

void loop() {
  unsigned long now = millis();
  if (now - lastMove >= SCAN_SPEED_MS) {
    lastMove = now;
    angle += dir;
    if (angle <= ANGLE_MIN) { angle = ANGLE_MIN; dir = 1; }
    if (angle >= ANGLE_MAX) { angle = ANGLE_MAX; dir = -1; }
    scanServo.write(angle);

    delay(20);

    unsigned int uS = sonar.ping();
    int cm = uS / US_ROUNDTRIP_CM;
    if (cm == 0) cm = MAX_DISTANCE;

    static unsigned long lastHeartbeat = 0;
    if (millis() - lastHeartbeat > 1000) {
      lastHeartbeat = millis();
      Serial.print("HB,");
      Serial.println(cm);
    }

    if (cm > 0 && cm < DIST_THRESHOLD_CM) {
      Serial.print("DETECTED,");
      Serial.print(angle);
      Serial.print(",");
      Serial.println(cm);
      delay(200);
    }
  }
}
