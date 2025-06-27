import cv2
import os
#imi deschide imaginile de le fac cu 2.py si ma lasa sa le etichetez
# Setăm folderele
image_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/captured_images'
label_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/manual_labels'
os.makedirs(label_folder, exist_ok=True)

# Variabile globale pentru coordonate
points = []

# Callback pentru mouse
def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"📍 Punct selectat: {x}, {y}")

def process_image(image_path, label_path):
    global points
    points = []

    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    cv2.imshow('Eticheteaza: Click colt stanga sus si dreapta jos', img)
    cv2.setMouseCallback('Eticheteaza: Click colt stanga sus si dreapta jos', click_event)

    print("🔎 Click colt stanga sus și apoi dreapta jos al plăcuței, apoi apasă ENTER.")

    while True:
        cv2.imshow('Eticheteaza: Click colt stanga sus si dreapta jos', img)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # ENTER
            break

    cv2.destroyAllWindows()

    if len(points) != 2:
        print("⚠️ Trebuie exact 2 click-uri (colt stanga sus si dreapta jos)!")
        return

    # Calculăm coordonate YOLO
    x1, y1 = points[0]
    x2, y2 = points[1]

    x_center = ((x1 + x2) / 2) / w
    y_center = ((y1 + y2) / 2) / h
    bbox_width = abs(x2 - x1) / w
    bbox_height = abs(y2 - y1) / h

    # Salvăm în format YOLO
    with open(label_path, 'w') as f:
        f.write(f"0 {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")

    print(f"✅ Eticheta salvată: {label_path}")

# Procesăm toate imaginile
for image_name in os.listdir(image_folder):
    if image_name.endswith('.jpg') or image_name.endswith('.png'):
        image_path = os.path.join(image_folder, image_name)
        label_name = os.path.splitext(image_name)[0] + '.txt'
        label_path = os.path.join(label_folder, label_name)

        print(f"\n🔨 Procesăm imaginea: {image_name}")
        process_image(image_path, label_path)

print("\n🎉 Toate imaginile au fost etichetate!")

