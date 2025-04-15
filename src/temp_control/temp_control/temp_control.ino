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

#define MODE_DEBUG 0
#define MODE_RUN 1
#define MODE_FIXED 0
#define MODE_WAVE 1

String commands;
float current_temp = 0;
float target_temp = 20;
float mode = MODE_FIXED;
float w_period = 360;
float w_amp = 5;
int status = STOPPED;
int op_mode = MODE_RUN;

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
  Serial.println(F("\tstart (Starts controller to reach target temp)"));
  Serial.println(F("\ttarget target_temp_in_C (Set the target temperature)"));
  Serial.println(F("\tmode [fixed|wave] (Define the operation mode)"));
  Serial.println(F("\tamp target_amp_in_C (The maximum amplitude of temp change in wave mode)"));
  Serial.println(F("\tperiod seconds (Seconds between waves in wave mode)"));
  Serial.println(F("\tstop (Stops the controller and returns to ambient temp)"));
  Serial.println(F("\tdebug on (Turns on debug mode)"));
  Serial.println(F("\tdebug off (Turns off debug mode)"));
  Serial.println(F("\tstat (Get the current temperature status)"));
  
}

/*
  Stop the heating/cooling cycle
*/
void stop() 
{
  analogWrite(PIN_COOL, 0);
  analogWrite(PIN_HEAT, 0);
  is_heating = 0;
  is_cooling = 0;
}

/*
  Establish the voltage level of the peltier.
*/
void adjustPeltPower()
{
  float t = abs(current_temp - target_temp);
  pelt_pwr_level = (((int)t * 20) + 155);

  pelt_pwr_level = (((int)t * 31) + 100);

  if(pelt_pwr_level > 255) {
    pelt_pwr_level = 255;
  } else if (pelt_pwr_level < 100) {
    pelt_pwr_level = 100;
  }

}

void showCurrentStatus() {
  char buff[60];
  char s_target_temp[8];
  char s_current_temp[8];
  char s_amp[8];
  char s_period[8];
  char t_status[2];
  char t_mode[6];
    
  dtostrf(current_temp, 6, 2, s_current_temp);
  dtostrf(target_temp, 6, 2, s_target_temp);
  dtostrf(w_period, 6, 2, s_period);
  dtostrf(w_amp, 6, 2, s_amp);

  if(mode == MODE_FIXED) {
    strcpy(t_mode, "Fixed");
  } else {
    strcpy(t_mode, "Wave");    
  }

  if(is_heating == 1) {
    strcpy(t_status,"H");
  } else if (is_cooling == 1) {
    strcpy(t_status,"C");
  } else {
    strcpy(t_status,"O");
  }

  sprintf(buff, "%s\t%s\t%d\t%s\t%s\t%s\t%s", s_target_temp, s_current_temp, pelt_pwr_level, t_status, s_amp, s_period, t_mode); 
  Serial.println(buff);
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
  
  adjustPeltPower();
  
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
  Serial.println(F("CNCO2 TRAY 3"));
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

    if (commands == "start") {
      
        if(op_mode == MODE_DEBUG) {
          Serial.println(F("Starting"));
          Serial.println(F("Targ  \tCurr  \tPwr"));
        }
        
        status = RUNNING;
        Serial.println(F("ready"));
      
    } else if (commands.substring(0, 6) == "target") {
      
      String t_temp;
      t_temp = commands.substring(7);
      t_temp.trim();

      if (t_temp == "") {
        showUsage();
      } else {
        target_temp = t_temp.toFloat();
      
        if(op_mode == MODE_DEBUG) {
          Serial.print(F("Setting target temp: "));
          Serial.print(t_temp);
          Serial.println(F("C"));
        }
      }

      Serial.println(F("ready"));
    } else if (commands.substring(0, 4) == "mode") {
      if(commands.substring(6) == "fixed") {
        mode = MODE_FIXED;  
      } else {
        mode = MODE_WAVE;
      }
      Serial.println(F("ready"));
    } else if (commands.substring(0, 3) == "amp") {

      String t_amp;
      t_amp = commands.substring(4);
      t_amp.trim();
      
      w_amp = t_amp.toFloat();
      
      Serial.println(F("ready"));
    } else if (commands.substring(0, 6) == "period") {

      String t_period;
      t_period = commands.substring(7);
      t_period.trim();
      
      w_period = t_period.toFloat();
      
      Serial.println(F("ready"));
    } else if (commands == "stop") {
      Serial.println(F("ready"));
      stop();
      status = STOPPED;
    } else if (commands == "debug on") {
      op_mode = MODE_DEBUG;
    } else if (commands == "debug off") {
      op_mode = MODE_RUN;
    } else if (commands == "stat") {
      showCurrentStatus(); 
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

    sprintf(buff, "%s\t%s\t%d", s_target_temp, s_current_temp, pelt_pwr_level); 
    if(op_mode == MODE_DEBUG) {
      Serial.println(buff);
    }

  } else {
    current_temp = getCurrentTemperature();
    if(op_mode == MODE_DEBUG) {
      Serial.print(F("Idle: "));
      Serial.print(current_temp);
      Serial.println(F("C"));
    }
    delay(1000); 
  }

}
 
