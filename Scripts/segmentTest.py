import cv2
from ultralytics import YOLO

model = YOLO("best.pt")
results = model.predict(source="test2.jpg", conf=0.75)

for r in results:
    img = r.orig_img.copy()
    for seg, cls, conf in zip(r.masks.xy, r.boxes.cls, r.boxes.conf):
        seg = seg.astype(int)
        cv2.polylines(img, [seg], isClosed=True, color=(0, 255, 0), thickness=2)
        x, y = seg[0][0], seg[0][1]  # top-left corner of mask
        label = f"{model.names[int(cls)]} {conf:.2f}"
        cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    cv2.imwrite("output_with_labels.jpg", img)
