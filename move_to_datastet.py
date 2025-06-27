import os
import shutil
#Dupa ce etichetez noile imagini cu manual.py acest fisier
#le muta in dataset
# Folderele sursă
image_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/captured_images'
label_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/manual_labels'

# Destinații dataset
train_image_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/dataset/images/train'
train_label_folder = 'C:/Users/barti/OneDrive/Desktop/IncercareLicenta/dataset/labels/train'

# Asigurăm că există destinațiile
os.makedirs(train_image_folder, exist_ok=True)
os.makedirs(train_label_folder, exist_ok=True)

# Mutăm imaginile
for file_name in os.listdir(image_folder):
    if file_name.endswith('.jpg') or file_name.endswith('.png'):
        src = os.path.join(image_folder, file_name)
        dst = os.path.join(train_image_folder, file_name)
        shutil.move(src, dst)
        print(f"🖼️ Mutat: {file_name} -> train images")

# Mutăm etichetele
for file_name in os.listdir(label_folder):
    if file_name.endswith('.txt'):
        src = os.path.join(label_folder, file_name)
        dst = os.path.join(train_label_folder, file_name)
        shutil.move(src, dst)
        print(f"📝 Mutat: {file_name} -> train labels")

print("\n🎉 Toate imaginile și etichetele au fost mutate în datasetul de antrenare!")
