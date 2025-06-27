from ultralytics import YOLO
import cv2
import os
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#DE ASTA NU AM NEVOIE !!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Încarcă modelul tău YOLO antrenat
model = YOLO('C:/Users/barti/runs/detect/train21/weights/best.pt')

# Foldere input/output
image_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/captured_images'
label_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/auto_labels'
os.makedirs(label_folder, exist_ok=True)

# Rulează predicție pe fiecare imagine
for image_name in os.listdir(image_folder):
    if image_name.endswith('.jpg') or image_name.endswith('.png'):
        image_path = os.path.join(image_folder, image_name)
        results = model.predict(image_path, conf=0.05, verbose=False)

        # Pregătește fișierul label
        label_path = os.path.join(label_folder, os.path.splitext(image_name)[0] + '.txt')

        with open(label_path, 'w') as f:
            for r in results:
                boxes = r.boxes
                if boxes is not None:
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        x_center, y_center, width, height = box.xywhn[0]  # Normalized (YOLO format)

                        # Scrie în format YOLO: class x_center y_center width height
                        f.write(f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        print(f"✅ Etichetă creată pentru: {image_name}")

print("🎉 Toate imaginile au fost etichetate automat!")
