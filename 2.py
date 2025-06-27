from ultralytics import YOLO
import cv2
import os
from datetime import datetime

# Încarcă modelul antrenat
model = YOLO('C:/Users/barti/runs/detect/train21/weights/best.pt')

# Creează folder pentru imagini salvate, dacă nu există
save_dir = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/captured_images'
os.makedirs(save_dir, exist_ok=True)

# Pornește camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera nu a putut fi deschisă!")
    exit()

print("✅ Camera pornită. Apasă 'q' ca să oprești.")

image_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Nu s-a putut citi frame-ul de la cameră.")
        break

    # Rulează predicția pe frame
    results = model.predict(frame, conf=0.10, verbose=False)

    # Verificăm dacă există detecții
    detected = False
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                # Desenează box și text
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Numar ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Dacă detectăm, salvăm imaginea
    if detected:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(save_dir, f"detected_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        image_count += 1
        print(f"💾 Imagine salvată: {filename}")
    #daca vreau doar sa fac poze ca sa mai antrenez modeul inca o data , sterg partea de sus si adaug urmatoarea 
    # Salvăm fiecare frame pentru dataset rapid
    #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    #filename = os.path.join(save_dir, f"captured_{timestamp}.jpg")
    #cv2.imwrite(filename, frame)
    #image_count += 1
    #print(f"💾 Imagine salvată: {filename}")

    # Arată fereastra cu camera
    cv2.imshow('Detectie Numar Inmatriculare', frame)

    # Dacă apeși 'q', oprește
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Eliberează resursele
cap.release()
cv2.destroyAllWindows()

print(f"✅ Program terminat. Total imagini salvate: {image_count}")
