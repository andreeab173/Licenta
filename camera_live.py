from ultralytics import YOLO
import cv2
import pytesseract
import os

# Setăm calea către executabilul Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Încarcă modelul YOLO
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

    # Rulează predicția pe frame
    results = model.predict(frame, conf=0.25, verbose=False)

    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                # Crop pentru OCR
                plate_img = frame[y1:y2, x1:x2]

                # Convertim la alb-negru pentru OCR mai bun
                gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

                # Folosim pytesseract pentru a citi textul
                custom_config = r'--oem 3 --psm 7'  # Optimal pentru linii de text scurte
                text = pytesseract.image_to_string(gray, config=custom_config)

                # Curățăm textul (eliminăm spații inutile și caractere speciale)
                text = ''.join(filter(str.isalnum, text))

                if text:
                    print(f"🔍 Număr detectat: {text}")

                # Desenează box-ul și textul
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{text} ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Arătăm frame-ul
    cv2.imshow('Detectie Numar Inmatriculare + OCR', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Program încheiat cu succes!")
