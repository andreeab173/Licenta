from ultralytics import YOLO
import cv2

# Încarcă modelul antrenat
model = YOLO('C:/Users/barti/runs/detect/train21/weights/best.pt')

# Pornește camera (0 este webcam-ul default)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera nu a putut fi deschisă!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Nu s-a putut citi frame-ul de la cameră.")
        break

    # Rulează predicția pe frame-ul de la cameră
    results = model.predict(frame, show=True, conf=0.05)

    # Verificăm dacă există detecții
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                # Coordonatele bounding box-ului
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                # Confidență
                conf = float(box.conf[0])
                # Clasa detectată
                cls = int(box.cls[0])

                # Desenăm box-ul și label-ul pe frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Numar ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Arată frame-ul
    cv2.imshow('Detectie Numar Inmatriculare', frame)

    # Oprește dacă apăsăm 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Eliberează resursele
cap.release()
cv2.destroyAllWindows()
