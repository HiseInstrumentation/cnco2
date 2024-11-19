String commands;
float current_temp = 0;

void setup() 
{
  Serial.begin(115200);
  delay(1000);
  Serial.println("CNCO2 HEATER 1");
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
      if(commands == "start") {
        Serial.println("Starting");
      }
      if(commands == "stop") {
        Serial.println("Stopping");
      }

      Serial.println(current_temp);
      delay(1000);
  } 



}
