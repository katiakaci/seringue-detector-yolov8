import cv2
import numpy as np
from ultralytics import YOLO

# Define hue ranges for basic colors (in OpenCV, the Hue has a range from 0 to 179. Not 360)
def classify_hue(h, s, v):
    if v < 50:
        return "dark"

    # Let lightly saturated colors still get a label, but flag them
    if s < 50:
        if v > 200:
            return "white"
        elif 130 <= h <= 165:
            return "pale purple"
        elif 10 <= h < 25:
            return "peach"
        else:
            return "gray"

    if h < 10 or h > 170:
        return "red"
    elif 10 <= h < 20:
        return "peach"
    elif 20 <= h < 30:
        return "orange"
    elif 30 <= h < 45:
        return "yellow"
    elif 45 <= h < 85:
        return "green"
    elif 85 <= h < 127:
        return "blue"
    elif 127 <= h <= 170:
        return "purple"
    else:
        return "unknown"



model = YOLO("best.pt")
results = model.predict(source="ValidateSyringe23.jpg", conf=0.75)

for r in results:
    img = r.orig_img.copy()
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for seg, cls, conf in zip(r.masks.xy, r.boxes.cls, r.boxes.conf):
        seg = seg.astype(np.int32)

        # Create mask
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [seg], 255)

        # Apply mask to HSV image
        h_values = hsv_img[:, :, 0][mask == 255]
        s_values = hsv_img[:, :, 1][mask == 255]
        v_values = hsv_img[:, :, 2][mask == 255]

        # Compute average hue, sat, val
        avg_h = np.mean(h_values)
        avg_s = np.mean(s_values)
        avg_v = np.mean(v_values)

        # Classify color
        color_label = classify_hue(avg_h, avg_s, avg_v)

        # Draw & label
        cv2.polylines(img, [seg], isClosed=True, color=(0, 255, 0), thickness=2)
        x, y = seg[0][0], seg[0][1]
        label_text = f"{model.names[int(cls)]} {conf:.2f} - {color_label} (H={avg_h:.0f}°)"
        cv2.putText(img, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    cv2.imwrite("output_with_labels.jpg", img)
