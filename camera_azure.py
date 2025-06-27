from ultralytics import YOLO
import cv2
import pytesseract
import serial
import time
import requests

# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
model = YOLO('C:/Users/barti/runs/detect/train25/weights/best.pt')
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
time.sleep(2)

# Numere permise (manuale)
numere_permise = {"CS10CSA"}

# URL aplicație Azure
AZURE_URL = "https://parcare-andreea-gfevcue8e6ayfsba.centralus-01.azurewebsites.net/detect"

# === START CAMERA ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera nu a putut fi deschisă.")
    exit()

print("✅ Camera pornită. Apasă 'q' pentru oprire.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Eroare la citirea camerei.")
        break

    results = model.predict(frame, conf=0.25, verbose=False)

    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                plate_img = frame[y1:y2, x1:x2]

                # OCR
                gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
                custom_config = r'--oem 3 --psm 7'
                text = pytesseract.image_to_string(gray, config=custom_config)
                text = ''.join(filter(str.isalnum, text)).strip().upper()

                if text and 6 <= len(text) <= 7:
                    print(f"🔍 Număr detectat: {text}")

                    # Trimite către aplicația web de pe Azure
                    try:
                        response = requests.post(AZURE_URL, data={'number': text})
                        print(f"🌐 Trimis către Azure: {response.status_code} - {response.text}")
                    except Exception as e:
                        print(f"⚠️ Eroare trimitere către Azure: {e}")

                    # Comandă către Arduino
                    command = "OPEN" if text in numere_permise else "DENY"
                    print(f"🚀 Trimit comanda către Arduino: {command}")
                    arduino.write((command + '\n').encode())
                    time.sleep(0.1)

                    # Feedback de la Arduino
                    while arduino.in_waiting > 0:
                        feedback = arduino.readline().decode().strip()
                        print(f"🧩 Arduino: {feedback}")

                    # Bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{text} ({conf:.2f})", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Detectie Numar Inmatriculare', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === CLEANUP ===
cap.release()
cv2.destroyAllWindows()
arduino.close()
print("✅ Program încheiat.")
