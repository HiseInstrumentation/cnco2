String commands;

void setup() 
{
  Serial.begin(9600);
}

void loop() 
{

  if(Serial.available()) {
      commands = Serial.readString();
      Serial.print("Got: ");
      Serial.println(commands);
  } 
}
