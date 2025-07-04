#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

// Inițializări
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo myservo;

// Pini
const int BUZZER = 5;
const int SERVO_PIN = 4;
const int RGB_RED = 9;
const int RGB_GREEN = 10;
const int RGB_BLUE = 11;
const int BUTON_MANUAL = 6;

// Variabile pentru serial
String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();

  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);

  pinMode(RGB_RED, OUTPUT);
  pinMode(RGB_GREEN, OUTPUT);
  pinMode(RGB_BLUE, OUTPUT);

  pinMode(BUTON_MANUAL, INPUT_PULLUP);

  myservo.attach(SERVO_PIN);
  myservo.write(100);

  lcd.setCursor(0, 0);
  lcd.print(" ARDUINO PARKING ");
  lcd.setCursor(0, 1);
  lcd.print(" SYSTEM READY! ");
  delay(2000);
  lcd.clear();
}

void loop() {
  if (digitalRead(BUTON_MANUAL) == LOW) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Mod manual activat");
    lcd.setCursor(0, 1);
    lcd.print("Bariera ridicata!");

    setRGB(0, 0, 255);  // Albastru

    myservo.write(0);
    delay(3000);
    myservo.write(100);
    delay(2000);
    return;
  }

  if (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }

  if (stringComplete) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Numar: ");
    lcd.print(inputString);

    if (inputString == "OPEN") {
      lcd.setCursor(0, 1);
      lcd.print("Acces permis!");

      setRGB(0, 255, 0);  // Verde

      tone(BUZZER, 1500);  // ✅ Buzzer activ doar la acces permis
      delay(300);
      noTone(BUZZER);

      myservo.write(0);
      delay(3000);
      myservo.write(100);

    } else if (inputString == "DENY") {
      lcd.setCursor(0, 1);
      lcd.print("Acces interzis!");

      setRGB(255, 0, 0);  // Roșu
      noTone(BUZZER);     // 🔕 Fără buzzer

    } else {
      lcd.setCursor(0, 1);
      lcd.print("Comanda necunosc.");
    }

    inputString = "";
    stringComplete = false;
  }
}

void setRGB(int r, int g, int b) {
  analogWrite(RGB_RED, 255 - r);
  analogWrite(RGB_GREEN, 255 - g);
  analogWrite(RGB_BLUE, 255 - b);
}
