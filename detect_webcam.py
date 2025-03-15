import cv2
from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO("runs/detect/train/weights/best.pt")  # Update path if needed

# Open webcam (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()  # Capture frame-by-frame
    if not ret:
        print("Failed to grab frame")
        break

    # Run YOLO inference
    results = model(frame, conf=0.7)  # Adjust confidence threshold if needed

    # Draw bounding boxes
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert to integers
            conf = box.conf[0].item()  # Get confidence score
            cls = int(box.cls[0].item())  # Get class index
            
            # Draw rectangle around detected object
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame, f"Syringe {conf:.2f}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
            )

    # Show the result in a window
    cv2.imshow("Syringe Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
