import cv2
from ultralytics import YOLO
import os
from datetime import datetime

model = YOLO("C:/Users/katia/Desktop/GitHub/MTI805-Projet/runs/detect/train_yolov8x_50_epoch/weights/best.pt") # Changer train_yolov8n par le modèle souhaité

# Dossier pour sauvegarder les seringues détectées
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAVE_DIR = os.path.join(ROOT_DIR, "captures_seringues")
os.makedirs(SAVE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame) # Détection
    annotated_frame = results[0].plot() # Annoter l'image

    # Vérifier les détections
    for box in results[0].boxes:
        conf = box.conf[0].item()
        if conf > 0.8:  # Seulement si > 80%
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            syringe_crop = frame[y1:y2, x1:x2]  # Recadrer la seringue

            # Sauvegarde l'heure exacte à laquelle le médicament a été donné
            timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mm%Ss")
            filename = os.path.join(SAVE_DIR, f"{timestamp}.jpg")
            cv2.imwrite(filename, syringe_crop)
            # print(f"Seringue sauvegardée : {filename}")

    # Afficher l'image annotée
    cv2.imshow("Détection de seringue", annotated_frame)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
