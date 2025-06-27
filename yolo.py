from ultralytics import YOLO

# Încarcă modelul pre-antrenat YOLOv8
model = YOLO("yolov8n.pt")

# Antrenează modelul pe dataset-ul tău
model.train(data="data.yaml", epochs=50, imgsz=640)
