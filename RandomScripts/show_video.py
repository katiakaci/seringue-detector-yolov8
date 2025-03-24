import cv2
from ultralytics import YOLO

model = YOLO("C:/Users/katia/Desktop/GitHub/MTI805-Projet/runs/detect/train2/weights/best.pt") # Changer train2 par le modèle souhaité

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame) # Détection
    annotated_frame = results[0].plot() # Annoter l'image
    cv2.imshow("Détection de seringue", annotated_frame) # Afficher l'image

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
