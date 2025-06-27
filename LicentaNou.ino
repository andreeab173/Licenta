#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

// Inițializări LCD și Servo
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo myservo;

// Definiri pinii
const int BUZZER = 5;
const int SERVO_PIN = 4;

// Variabile comunicare serială
String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(9600);  // Inițializează comunicarea serială
  lcd.init();          // Inițializează LCD-ul
  lcd.backlight();     // Aprinde backlight-ul LCD

  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);  // Oprește buzzer-ul la start

  myservo.attach(SERVO_PIN);  // Atașează servo pe pinul 4
  myservo.write(100);         // Inițial, bariera închisă

  // Mesaj inițial LCD
  lcd.setCursor(0, 0);
  lcd.print(" ARDUINO PARKING ");
  lcd.setCursor(0, 1);
  lcd.print(" SYSTEM READY! ");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Verificare date pe serial
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
      Serial.println(">>> Comanda primita: OPEN");
      lcd.setCursor(0, 1);
      lcd.print("Acces permis!");

      myservo.write(0);      // Ridică bariera
      delay(3000);           // 3 secunde deschisă
      myservo.write(100);    // Închide bariera
      Serial.println(">>> Bariera a fost ridicata!");

    } else if (inputString == "DENY") {
      Serial.println(">>> Comanda primita: DENY");
      lcd.setCursor(0, 1);
      lcd.print("Acces interzis!");

      tone(BUZZER, 1000);    // Pornește buzzer-ul
      delay(1000);           // Sună 1 secundă
      noTone(BUZZER);        // Oprește buzzer-ul
      Serial.println(">>> Acces interzis! Buzzer activat.");

    } else {
      Serial.print(">>> Comanda necunoscuta: ");
      Serial.println(inputString);
    }

    // Resetăm pentru următorul mesaj
    inputString = "";
    stringComplete = false;
  }
}
