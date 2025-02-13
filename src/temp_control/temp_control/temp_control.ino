/**
  Copyright 2025, Hise Scientific Instrumentation, LLC
  All Rights Reserved
  Range 5C-60C

  Serial Commands at Baud 115200

  start target_temp     // Start the heating/cooling cycles to obtain target temperature in C
  stop                  // Stop the heating/cooling cycle, idle


  Dev Notes:
    - Could introduce a general temp offset value.

**/

// Control
#define RUNNING 1
#define STOPPED 0
#define HEATING 1
#define COOLING 0

// Sampling
#define NUMSAMPLES 20

// Pins
#define PIN_HEAT 6
#define PIN_COOL 5
#define PIN_ENABLE 4
#define PIN_TEMP A0

// Calculations
#define aref_voltage 3.349
#define rRef 11600  // 9kOhm

String commands;
float current_temp = 0;
float target_temp = 0;
int status = STOPPED;

int pelt_pwr_level = 255;

int is_heating = 0;
int is_cooling = 0;

// Temperature reading
int samples[NUMSAMPLES], n;
float average;
float rTherm, logrTherm, tempTherm;

// Usage instructions
void showUsage()
{
  Serial.println(F("Usage:"));
  Serial.println(F("\tstart target_temp_in_C"));
  Serial.println(F("\tstop"));
}

/*
  Stop the heating/cooling cycle
*/
void stop() 
{
  analogWrite(PIN_COOL, 0);
  analogWrite(PIN_HEAT, 0);
}

/*
  Establish the voltage level of the peltier.
*/
void adjustPeltPower()
{
  float t = abs(current_temp - target_temp);
  pelt_pwr_level = (((int)t * 20) + 155);
  pelt_pwr_level = min(pelt_pwr_level,255);  
}

/*
  Turn on heating
*/
void heat() 
{
  adjustPeltPower();
  
  if(is_heating == 0) {
    is_heating = 1;
    analogWrite(PIN_COOL, 0);
    analogWrite(PIN_HEAT, pelt_pwr_level);
  }
  is_cooling = 0;
}

/*
  Turn on cooling
*/
void cool() 
{
  if(is_cooling == 0) {
    is_cooling = 1;
    analogWrite(PIN_HEAT, 0);
    analogWrite(PIN_COOL, pelt_pwr_level);
  }
  is_heating = 0;
}

/*
  Get the current temperature
*/
float getCurrentTemperature() 
{ 
  
  average = 0;

  for (n = 1; n < NUMSAMPLES; n++) {
    samples[n] = analogRead(PIN_TEMP);
    average += samples[n];
  }

  average /= NUMSAMPLES;
  
  rTherm = rRef / (1024 / average - 1);
  
  logrTherm = rTherm;
  
  // Thermistor specific
  tempTherm = 0.000000000000000000000000312559 * pow(logrTherm , 6) 
            - 0.000000000000000000044153755786 * pow(logrTherm , 5) 
            + 0.00000000000000252921232833742 * pow(logrTherm , 4) 
            - 0.0000000000759528833550828 * pow(logrTherm , 3) 
            + 0.00000130404854263673 * pow(logrTherm , 2) 
            - 0.0137601358467662 * pow(logrTherm , 1) 
            + 96.356373987591;

  return (tempTherm);
}

/*
  Controller initialization
*/
void setup() 
{
  Serial.begin(115200);

  pinMode(PIN_COOL, OUTPUT);
  pinMode(PIN_HEAT, OUTPUT);
  pinMode(PIN_ENABLE, OUTPUT);

  digitalWrite(PIN_ENABLE, HIGH);  // No idea what this does, try to remove

  // This string must start with CNCO2 and each temp controller should have a number
  Serial.println(F("CNCO2 HEATER 1"));
  delay(1000);
  stop();
}

/*
  Main Loop
*/
void loop() 
{
  if (Serial.available()) {
    
    commands = Serial.readString();
    commands.trim();

    if (commands.substring(0, 5) == "start") {
      
      String t_temp;
      t_temp = commands.substring(6);
      t_temp.trim();

      if (t_temp == "") {
        showUsage();
      } else {
        Serial.print(F("Setting target temp: "));
        Serial.print(t_temp);
        Serial.println(F("C"));
  
        target_temp = t_temp.toFloat();
  
        Serial.println(F("Starting"));
        Serial.println(F("Targ  \tCurr  \tPwr"));
        status = RUNNING;
      }
    } else if (commands == "stop") {
      Serial.println(F("Stopping"));
      stop();
      status = STOPPED;
    } else {
      showUsage();
    }
    delay(1000);
  }

  if (status == RUNNING) {
    current_temp = getCurrentTemperature();

    char buff[30];

    char s_target_temp[8];
    char s_current_temp[8];

    dtostrf(current_temp, 6, 2, s_current_temp);
    dtostrf(target_temp, 6, 2, s_target_temp);

    delay(500);

    if(current_temp < target_temp) {
      heat();
    } else {
      cool();
    }

    sprintf(buff, "%s\t%s\t%d\t%d", s_target_temp, s_current_temp, pelt_pwr_level); 
    Serial.println(buff);

  } else {
    current_temp = getCurrentTemperature();
    Serial.print(F("Idle: "));
    Serial.print(current_temp);
    Serial.println(F("C"));
    delay(1000); 
  }

}
 
