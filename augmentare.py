import os
import cv2
import albumentations as A
from tqdm import tqdm
import shutil

# Folderele tale originale
image_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/dataset/images/train'
label_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/dataset/labels/train'

# Foldere de output
aug_image_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/dataset/images/train_aug'
aug_label_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/dataset/labels/train_aug'

# Creează folderele noi dacă nu există
os.makedirs(aug_image_folder, exist_ok=True)
os.makedirs(aug_label_folder, exist_ok=True)

# Transformări de augmentare
transform = A.Compose([
    A.RandomBrightnessContrast(p=0.5),
    A.HorizontalFlip(p=0.5),
    A.Rotate(limit=15, p=0.5),
    A.Blur(p=0.3),
    A.RandomGamma(p=0.5),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# Funcție de citire etichete
def read_label(path):
    boxes = []
    class_labels = []
    with open(path, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split()
            if len(parts) == 5:
                class_labels.append(int(parts[0]))
                boxes.append([float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])])
    return boxes, class_labels

# Loop prin toate imaginile
for filename in tqdm(os.listdir(image_folder)):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(image_folder, filename)
        label_path = os.path.join(label_folder, os.path.splitext(filename)[0] + '.txt')

        # Verificăm că există și eticheta
        if not os.path.exists(label_path):
            continue

        # Citim imaginea și eticheta
        image = cv2.imread(image_path)
        height, width = image.shape[:2]
        bboxes, class_labels = read_label(label_path)

        # Aplicăm augmentare de 5 ori
        for i in range(5):
            augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            aug_image = augmented['image']
            aug_bboxes = augmented['bboxes']
            aug_labels = augmented['class_labels']

            # Salvăm imaginea augmentată
            aug_image_name = f"{os.path.splitext(filename)[0]}_aug_{i}.jpg"
            aug_label_name = f"{os.path.splitext(filename)[0]}_aug_{i}.txt"

            cv2.imwrite(os.path.join(aug_image_folder, aug_image_name), aug_image)

            # Salvăm eticheta augmentată
            with open(os.path.join(aug_label_folder, aug_label_name), 'w') as f:
                for bbox, label in zip(aug_bboxes, aug_labels):
                    f.write(f"{label} {' '.join(map(str, bbox))}\n")

print("✅ Augmentare completă!")

# Dacă vrei, mutăm automat imaginile și în folderele de train existente
for file in os.listdir(aug_image_folder):
    shutil.move(os.path.join(aug_image_folder, file), os.path.join(image_folder, file))
for file in os.listdir(aug_label_folder):
    shutil.move(os.path.join(aug_label_folder, file), os.path.join(label_folder, file))

print("✅ Fișierele augmentate au fost mutate în folderele de train!")
