// RoboArm Studio - Arduino Control Code
// Emre Kalem | Eskisehir, Turkiye | 2025
// Controls 7 servos via serial communication
// Hardware: Arduino Uno R4 with Sensor Shield attached on top

#include <Servo.h>

Servo servo1; // Servo objects
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;

int angleValues[7]; // Array to store angle values - 7 servos
int servoPins[] = { 2, 3, 4, 5, 6, 7, 8 }; // Servo pins - sequence from pin 2

/* 
Pin 2 = Root (Servo 0)
Pin 3 = Arm A1 (Servo 1)
Pin 4 = Arm A2 (Servo 2) - coupled with Pin 3, rotates in opposite direction
Pin 5 = Arm B (Servo 3)
Pin 6 = Wrist A (Servo 4)
Pin 7 = Wrist B (Servo 5)
Pin 8 = Gripper (Servo 6)
*/

void setup()
{
  Serial.begin(9600); // Start serial communication

  // Set servo pin modes
  for (int i = 0; i < 7; i++)
  {
    pinMode(servoPins[i], OUTPUT);
  }

  // Attach servo objects
  servo1.attach(servoPins[0]);
  servo2.attach(servoPins[1]);
  servo3.attach(servoPins[2]);
  servo4.attach(servoPins[3]);
  servo5.attach(servoPins[4]);
  servo6.attach(servoPins[5]);
  servo7.attach(servoPins[6]);
  digitalWrite(13, LOW);
}

void loop()
{
  // Python server sends gradual commands for smooth movements
  // Each command contains 7 integer values separated by spaces (one per servo)
  // Smooth movements are handled server-side with gradual interpolation
  if (Serial.available() > 0) // If data is available from serial port
  {
    // Read angle values
    for (int i = 0; i < 7; i++)
    {
      angleValues[i] = Serial.parseInt(); // Read next int value
    }

    // Move servos
    // Note: Python code already sends servo2 (Pin 4) calculated as opposite of servo1 (Pin 3)
    // So we use the received values directly
    // Smooth movements are achieved by sending intermediate positions from Python server
    servo1.write(angleValues[0]); // Root (Pin 2)
    servo2.write(angleValues[1]); // Arm A1 (Pin 3)
    servo3.write(angleValues[2]); // Arm A2 (Pin 4) - already calculated as opposite in Python
    servo4.write(angleValues[3]); // Arm B (Pin 5)
    servo5.write(angleValues[4]); // Wrist A (Pin 6)
    servo6.write(angleValues[5]); // Wrist B (Pin 7)
    servo7.write(angleValues[6]); // Gripper (Pin 8)
    
  }
}
