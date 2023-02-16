#include <Servo.h>
Servo sabertooth;
int raspiSwitch = 0;
int raspiSwitchSlow = 0;
int raspiPin = 11;
int raspiPin2 = 12;
bool FAST = false;
bool SLOW = false;


void setup () {
  sabertooth.attach(13); // Use PWM pin 13 to control Sabertooth.
  pinMode(raspiPin, INPUT);
  pinMode(raspiPin2, INPUT);
}

void loop() {  
  raspiSwitch = digitalRead(raspiPin);
  raspiSwitchSlow = digitalRead(raspiPin2);

  FAST = (raspiSwitch == 1);
  SLOW = (raspiSwitchSlow == 1);

  if (SLOW && !(FAST)){
    sabertooth.write(115);
  }
  else if (!(SLOW || FAST)){
    sabertooth.write(100);
  }
  else{
    sabertooth.write(135);
  }

  /*
  old:
  if (raspiSwitch == 0)
  {
    sabertooth.write(100);
  }
  else
  {
    sabertooth.write(135);
  }
  */
}