from ultralytics import YOLO

model = YOLO("yolo26n.pt")

model.predict(
    source=0,
    show=True,
    device="mps"
)