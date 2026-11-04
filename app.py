"""Webcam-based communication: recognize a custom gesture, display and speak phrase."""
import time
from collections import Counter, deque

import cv2
import mediapipe as mp
import pyttsx3

from gesture_utils import extract_landmarks
from translator import load_bundle, predict_gesture

CONFIDENCE_THRESHOLD = 0.75
STABLE_FRAMES = 8

bundle = load_bundle()
speech = pyttsx3.init()
speech.setProperty("rate", 145)

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise RuntimeError("Cannot open webcam. Check camera permission.")

history = deque(maxlen=STABLE_FRAMES)
current_phrase = "Show a gesture"
confidence = 0.0

with mp.solutions.hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
) as hands:
    while True:
        ok, frame = camera.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        confidence = 0.0

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand, mp.solutions.hands.HAND_CONNECTIONS
            )
            label, confidence = predict_gesture(extract_landmarks(hand), bundle)
            if confidence >= CONFIDENCE_THRESHOLD:
                history.append(label)
                if len(history) == STABLE_FRAMES:
                    common_label, votes = Counter(history).most_common(1)[0]
                    if votes >= STABLE_FRAMES - 1:
                        current_phrase = common_label
            else:
                history.clear()
        else:
            history.clear()

        cv2.putText(frame, "COMMUNICATION ASSISTANT", (10, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Message: {current_phrase[:45]}", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        cv2.putText(frame, f"Confidence: {confidence * 100:.1f}%", (10, 112),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, "S: Speak | C: Clear | Q: Quit",
                    (10, frame.shape[0] - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 1)
        cv2.imshow("Communication Assistant", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            if current_phrase != "Show a gesture":
                speech.say(current_phrase)
                speech.runAndWait()
        elif key == ord("c"):
            current_phrase = "Show a gesture"
            history.clear()
        elif key == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()
