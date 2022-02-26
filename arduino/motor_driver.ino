#include <Servo.h>
Servo sabertooth;
int raspiSwitch = 0;
int raspiPin = 11;


void setup () 
{
  sabertooth.attach(13); // Use PWM pin 13 to control Sabertooth.
  pinMode(raspiPin, INPUT);
}

void loop() 
{  
  raspiSwitch = digitalRead(raspiPin);

  if (raspiSwitch == 0)
  {
    sabertooth.write(100);
  }
  else
  {
    sabertooth.write(135);
  }
}