/**
  Copyright 2025, Hise Scientific Instrumentation, LLC
  All Rights Reserved
  Range 5C-60C

  Serial Commands at Baud 115200

  start target_temp     // Start the heating/cooling cycles to obtain target temperature in C
  ambient ambient_temp  // Set the ambient temperature in C
  stop                  // Stop the heating/cooling cycle, idle

**/

// Control
#define RUNNING 1
#define STOPPED 0

// Sampling
#define NUMSAMPLES 20

// Pins
#define PIN_HEAT 6
#define PIN_COOL 5
#define PIN_ENABLE 4
#define PIN_TEMP A0

// Heat control
#define HEAT_DUR_SEC 1

// Calculations
#define aref_voltage 3.349
#define rRef 11600  // 9kOhm


String commands;
float current_temp = 0;
float target_temp = 0;
float ambient_temp = -100;
int status = STOPPED;

int heat_dur_sec = 1;
int heat_pwr_level = 255;

// Temperature reading
int samples[NUMSAMPLES], n;
float average;
float rTherm, logrTherm, tempTherm;

/*
  Stop the heating/cooling cycle
*/
void stop() {
  analogWrite(PIN_COOL, 0);
  analogWrite(PIN_HEAT, 0);
}

void getHeatCoolPower(int temp_diff)
{

  switch (temp_diff) {
    case 5:
      heat_dur_sec = 1;
      heat_pwr_level = 255;
      break;
    case 4:
      heat_dur_sec = 1;
      heat_pwr_level = 255;
      break;
    case 3:
      heat_dur_sec = 1;
      heat_pwr_level = 255;
      break;
    case 2:
      heat_dur_sec = 1;
      heat_pwr_level = 225;
      break;
    default:
      heat_dur_sec = 1;
      heat_pwr_level = 225;
      break;
    }
  
}

/*
  Turn on heating
*/
void heat(bool suppress) {
  getHeatCoolPower(heat_dur_sec);
  //Serial.print("PW: ");
  //Serial.println(heat_pwr_level);
  analogWrite(PIN_COOL, 0);
  if (!suppress) {
    analogWrite(PIN_HEAT, heat_pwr_level);
  }

  delay(heat_dur_sec * 1000);
  analogWrite(PIN_HEAT, 0);
}

/*
  Turn on cooling
*/
void cool(bool suppress) {
  getHeatCoolPower(heat_dur_sec);
  //Serial.print("PW: ");
  //Serial.println(heat_pwr_level);
  analogWrite(PIN_HEAT, 0);
  if (!suppress) {
    analogWrite(PIN_COOL, heat_pwr_level);
  } 
  delay(heat_dur_sec * 1000);
  analogWrite(PIN_COOL, 0);
}

/*
  Get the current temperature
*/
float get_current_temperature() { 
  average = 0;

  for (n = 1; n < NUMSAMPLES; n++) {
    samples[n] = analogRead(PIN_TEMP);
    average += samples[n];
  }

  average /= NUMSAMPLES;

  rTherm = rRef / (1024 / average - 1);

  logrTherm = rTherm;
  
 
  /*
  tempTherm = 0.000000000000000000000000312559145621717 * pow(logrTherm , 6) 
            - 0.000000000000000000044153755786489 * pow(logrTherm , 5) 
            + 0.00000000000000252921232833742 * pow(logrTherm , 4) 
            - 0.0000000000759528833550828 * pow(logrTherm , 3) 
            + 0.00000130404854263673 * pow(logrTherm , 2) 
            - 0.0137601358467662 * pow(logrTherm , 1) 
            + 96.356373987591;
  */
  
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
void setup() {
  Serial.begin(115200);

  pinMode(PIN_COOL, OUTPUT);
  pinMode(PIN_HEAT, OUTPUT);
  pinMode(PIN_ENABLE, OUTPUT);

  digitalWrite(PIN_ENABLE, HIGH);  // No idea what this does, try to remove

  Serial.println(F("CNCO2 HEATER 1"));
  delay(1000);
  stop();
}

void loop() {
  bool suppress = false;
  
  if (Serial.available()) {
    commands = Serial.readString();
    commands.trim();

    if (commands.substring(0, 5) == "start") {
      String t_temp;
      t_temp = commands.substring(6);
      t_temp.trim();

      if (t_temp == "") {
        t_temp = "0";
      }

      Serial.print(F("Setting target temp: "));
      Serial.print(t_temp);
      Serial.println(F("C"));

      target_temp = t_temp.toFloat();
      if(ambient_temp == -100) {
        ambient_temp = get_current_temperature();
      }

      
      Serial.println(F("Starting"));
      Serial.println(F("Amb   \tTarg  \tCurr  \tDelay  \tPwr  \tS"));
      status = RUNNING;
    } else if (commands.substring(0, 7) == "ambient") {
      String a_temp;
      a_temp = commands.substring(8);
      a_temp.trim();

      if (a_temp == "") {
        a_temp = "30";
      }

      ambient_temp = a_temp.toFloat();

      Serial.print(F("Ambient Temp: "));
      Serial.print(ambient_temp);
      Serial.println(F("C"));

    } else if (commands == "stop") {
      Serial.println(F("Stopping"));
      stop();
      status = STOPPED;
    } else {
      Serial.print(F("Unknown Command '"));
      Serial.print(commands);
      Serial.println(F("'"));
      Serial.println(F("Usage:"));
      Serial.println(F("\tstart target_temp_in_C"));
      Serial.println(F("\tambient ambient_temp_in_C"));
      Serial.println(F("\tstop"));
    }
    delay(1000);
  }

  if (status == RUNNING) {
    current_temp = get_current_temperature();

    char buff[30];

    char s_ambient_temp[8];
    char s_target_temp[8];
    char s_current_temp[8];

    
    dtostrf(current_temp, 6, 2, s_current_temp);
    dtostrf(ambient_temp, 6, 2, s_ambient_temp);
    dtostrf(target_temp, 6, 2, s_target_temp);


    delay(500);

    int temp_diff = abs(target_temp - current_temp);

    heat_dur_sec = temp_diff;
    
    if(temp_diff < 1) {
      heat_dur_sec = 1;
    } else if (temp_diff > 5) {
      heat_dur_sec = 5;
    }

    if (current_temp < target_temp) {
      // Move this logic to inside heat function
      if (current_temp >= (ambient_temp - 1)) {
        suppress = false;
      } else {
        suppress = true;
      }

      heat(suppress);

      
    } else {
      // Move this logic to inside cool function
      if (current_temp >= (ambient_temp + 1)) {
        suppress = true;
      } else {
        suppress = false;
      }

      cool(suppress);      
    }

    if(suppress) {
      sprintf(buff, "%s\t%s\t%s\t%d\t%d\tY", s_ambient_temp, s_target_temp, s_current_temp, heat_dur_sec, heat_pwr_level); 
    } else {
      sprintf(buff, "%s\t%s\t%s\t%d\t%d\tN", s_ambient_temp, s_target_temp, s_current_temp, heat_dur_sec, heat_pwr_level); 
    }

    Serial.println(buff);

  } else {
    current_temp = get_current_temperature();
    Serial.print(F("Idle: "));
    Serial.print(current_temp);
    Serial.println(F("C"));
    delay(1000); }

}
 
