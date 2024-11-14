#define aref_voltage 3.349
#define NUMSAMPLES 20

int samples[NUMSAMPLES], n;

const int tempPin = A0;
const int rRef = 5610;

float average;
float rTherm, logrTherm, tempTherm;

/**
 * Reads temperature from thermistor
 */
void thermTE()
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
              
  Serial.println(tempTherm, 1);
  delay(150);  
}

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
