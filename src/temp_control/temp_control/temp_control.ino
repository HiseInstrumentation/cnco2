/**
  Range 5C-60C

**/

#define RUNNING 1
#define STOPPED 0

#define aref_voltage 3.349
#define NUMSAMPLES 20

#define PIN_HEAT 6
#define PIN_COOL 5
#define PIN_ENABLE 4

#define HEAT_DUR_SEC 0
#define COOL_DUR_SEC 5

// Control
String commands;
float current_temp = 0;
float target_temp = 0;
int status = STOPPED;

// Temperature reading
int samples[NUMSAMPLES], n;
const int tempPin = A0;
// const int rRef = 5610;
const int rRef = 9000; // 9kOhm
float average;
float rTherm, logrTherm, tempTherm;


void stop() {
  analogWrite(PIN_COOL, 0);
  analogWrite(PIN_HEAT, 0);

}

void heat() {
  Serial.println("Heating");
  analogWrite(PIN_COOL, 0);
  analogWrite(PIN_HEAT, 255);
  delay(HEAT_DUR_SEC * 1000);
  analogWrite(PIN_HEAT, 0);
}

void cool() {
  Serial.println("Cooling");
  analogWrite(PIN_HEAT, 0);
  analogWrite(PIN_COOL, 255);
  delay(COOL_DUR_SEC * 1000);
  analogWrite(PIN_COOL, 0);
}

float get_current_temperature()
{

  average = 0;
  for (n = 1; n < NUMSAMPLES; n++) {
    samples[n] = analogRead(tempPin);
    average += samples[n];
  }

  average /= NUMSAMPLES;
  rTherm = rRef / (1024 / average - 1);
  logrTherm = log10(rTherm);

  tempTherm = .07191332 * pow(logrTherm, 6) - 1.791422 * pow(logrTherm, 5) + 18.67046 * pow(logrTherm, 4)
            - 105.4027 * pow(logrTherm, 3) + 350.9841 * pow(logrTherm, 2) - 729.505 * logrTherm + 833.2693;
              
  return (tempTherm);
}


void setup() 
{
  Serial.begin(115200);
  
  pinMode(PIN_COOL, OUTPUT);
  pinMode(PIN_HEAT, OUTPUT);
  pinMode(PIN_ENABLE, OUTPUT);

  digitalWrite(PIN_ENABLE, HIGH); // No idea what this does, try to remove

  Serial.println("CNCO2 HEATER 1");
  delay(1000);
  stop();

}


void loop() 
{

  /*
    Commands:
      start target_temp
      stop
  */
  if(Serial.available()) {
      commands = Serial.readString();
      commands.trim();

      if(commands.substring(0,5) == "start") {
        String t_temp;        
        t_temp = commands.substring(6);
        t_temp.trim();
        Serial.print("Setting target temp: ");
        Serial.print(t_temp);
        Serial.println("C");

        if(t_temp == "") {
          t_temp = "0";
        }

        target_temp = t_temp.toFloat();

        Serial.println("Starting");
        status = RUNNING;
      }

      if(commands == "stop") {
        Serial.println("Stopping");
        stop();
        status = STOPPED;
      }
      delay(1000);
  } 


  if(status == RUNNING) {
    current_temp = get_current_temperature();

    Serial.print("Target temp: ");
    Serial.println(target_temp);
    Serial.print("Curent Temp: ");
    Serial.println(current_temp);
    delay(500);

    if(current_temp < target_temp) {
      heat();
    } else {
      cool();
    }

  } else {
    current_temp = get_current_temperature();
    Serial.print("Idle: ");
    Serial.print(current_temp);
    Serial.println("C");
    delay(500);
  }


}
