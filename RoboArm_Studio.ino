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
int currentAngles[7]; // Current servo positions for smooth interpolation
int targetAngles[7]; // Target servo positions
int servoPins[] = { 2, 3, 4, 5, 6, 7, 8 }; // Servo pins - sequence from pin 2

// Interpolation parameters
const int INTERPOLATION_STEP = 1; // Degrees per step (smaller = smoother but slower)
const int STEP_DELAY = 15; // Milliseconds between steps (adjust for speed vs smoothness)

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
  
  // Initialize current and target positions to default (90° for most, 35° for gripper)
  for (int i = 0; i < 7; i++)
  {
    if (i == 6) { // Gripper
      currentAngles[i] = 35;
      targetAngles[i] = 35;
    } else {
      currentAngles[i] = 90;
      targetAngles[i] = 90;
    }
  }
  
  // Set initial positions
  servo1.write(currentAngles[0]);
  servo2.write(currentAngles[1]);
  servo3.write(currentAngles[2]);
  servo4.write(currentAngles[3]);
  servo5.write(currentAngles[4]);
  servo6.write(currentAngles[5]);
  servo7.write(currentAngles[6]);
  
  digitalWrite(13, LOW);
}

void loop()
{
  // Check for new commands from serial port
  if (Serial.available() > 0)
  {
    // Read target angle values
    for (int i = 0; i < 7; i++)
    {
      targetAngles[i] = Serial.parseInt(); // Read next int value
    }
    
    // DEBUG: Print received target angles
    Serial.print("RX: ");
    for (int i = 0; i < 7; i++)
    {
      Serial.print(targetAngles[i]);
      if (i < 6) Serial.print(",");
    }
    Serial.println();
  }
  
  // Smooth interpolation: gradually move current angles towards target angles
  bool isMoving = false;
  
  for (int i = 0; i < 7; i++)
  {
    if (currentAngles[i] != targetAngles[i])
    {
      isMoving = true;
      
      // Calculate the difference
      int diff = targetAngles[i] - currentAngles[i];
      
      // Move by INTERPOLATION_STEP degrees towards target
      if (abs(diff) <= INTERPOLATION_STEP)
      {
        // Close enough, snap to target
        currentAngles[i] = targetAngles[i];
      }
      else
      {
        // Move one step towards target
        if (diff > 0)
        {
          currentAngles[i] += INTERPOLATION_STEP;
        }
        else
        {
          currentAngles[i] -= INTERPOLATION_STEP;
        }
      }
    }
  }
  
  // Write current positions to servos ONLY when moving
  // This prevents jitter and unnecessary servo updates
  if (isMoving)
  {
    servo1.write(currentAngles[0]); // Root (Pin 2)
    servo2.write(currentAngles[1]); // Arm A1 (Pin 3)
    servo3.write(currentAngles[2]); // Arm A2 (Pin 4) - already calculated as opposite in Python
    servo4.write(currentAngles[3]); // Arm B (Pin 5)
    servo5.write(currentAngles[4]); // Wrist A (Pin 6)
    servo6.write(currentAngles[5]); // Wrist B (Pin 7)
    servo7.write(currentAngles[6]); // Gripper (Pin 8)
    
    // Add delay between steps for smooth movement
    delay(STEP_DELAY);
  }
  else
  {
    // Small delay when idle to prevent loop from running too fast
    delay(1);
  }
}
