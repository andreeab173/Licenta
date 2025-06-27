from ultralytics import YOLO
import cv2
import pytesseract
import serial
import time
from thefuzz import fuzz  # Fuzzy matching!

# Configurare Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Număr permis
numar_permis = "CS10CSA"

# Conectare serială la Arduino
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
time.sleep(2)

# Încarcă modelul YOLO antrenat
model = YOLO('C:/Users/barti/runs/detect/train25/weights/best.pt')

# Pornește camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera nu a putut fi deschisă!")
    exit()

print("✅ Camera pornită! Apasă 'q' ca să oprești programul.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Nu s-a putut citi frame-ul de la cameră.")
        break

    # Predicție YOLO
    results = model.predict(frame, conf=0.25, verbose=False)

    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                # OCR pe zona de interes
                plate_img = frame[y1:y2, x1:x2]
                gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
                custom_config = r'--oem 3 --psm 7'
                text = pytesseract.image_to_string(gray, config=custom_config)
                text = ''.join(filter(str.isalnum, text)).strip().upper()

                if text:
                    print(f"🔍 Număr detectat: {text}")

                    # Fuzzy match
                    similarity = fuzz.ratio(text, numar_permis)
                    print(f"📊 Similaritate cu permis: {similarity}%")

                    if similarity > 80:  # Pragul de toleranță, reglezi cum vrei tu
                        command = "OPEN"
                    else:
                        command = "DENY"

                    # Trimite comanda la Arduino
                    arduino.write((command + '\n').encode())
                    time.sleep(0.1)

                    # Primește feedback de la Arduino
                    while arduino.in_waiting > 0:
                        feedback = arduino.readline().decode().strip()
                        print(f"🧩 Arduino: {feedback}")

                    # Desenează bounding box și text pe frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{text} ({conf:.2f})", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Afișează frame-ul
    cv2.imshow('Detectie Numar Inmatriculare + OCR', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
print("✅ Program încheiat cu succes!")
