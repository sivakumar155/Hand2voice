
import time
import os
import csv
import cv2
import mediapipe as mp

from communication_phrases import PHRASES
from gesture_utils import extract_landmarks

DATASET = "dataset/hand_landmarks.csv"
os.makedirs("dataset", exist_ok=True)

if not os.path.exists(DATASET):
    with open(DATASET, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label"] + [f"feature_{i}" for i in range(63)])

print("\nCUSTOM GESTURE DATA COLLECTION")
for key, phrase in PHRASES.items():
    print(f"  {key}: {phrase}")
print("\nShow the chosen gesture, then hold its number key to collect.")
print("Collect 100-200 varied samples per phrase. Press X to deselect; Q to quit.")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam. Check macOS camera permission.")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
selected_key = None
last_save = 0.0
saved_count = 0

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
) as hands:
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        features = None

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            features = extract_landmarks(hand)

        phrase = PHRASES.get(selected_key, "Select a phrase key (1-9 or 0)")
        cv2.putText(frame, phrase[:42], (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        cv2.putText(frame, f"Session samples: {saved_count}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, "Hold 1-9/0 to collect | X deselect | Q quit",
                    (10, frame.shape[0] - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1)
        cv2.imshow("Communication Gesture Collection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("x"):
            selected_key = None
        elif key != 255:
            char = chr(key)
            if char in PHRASES:
                selected_key = char

        if selected_key and features is not None and time.time() - last_save >= 0.12:
            with open(DATASET, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([PHRASES[selected_key]] + features.tolist())
            saved_count += 1
            last_save = time.time()

cap.release()
cv2.destroyAllWindows()
print(f"Finished. Added {saved_count} samples to {DATASET}")
