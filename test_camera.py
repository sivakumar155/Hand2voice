
import cv2
import mediapipe as mp

print("OpenCV:", cv2.__version__)
print("MediaPipe:", mp.__version__)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera not accessible")
    exit()

hands = mp.solutions.hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

draw = mp.solutions.drawing_utils

while True:
    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            draw.draw_landmarks(
                frame,
                hand,
                mp.solutions.hands.HAND_CONNECTIONS
            )

        cv2.putText(
            frame, "HAND DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 0), 2
        )

    cv2.imshow("Hand Detection Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

hands.close()
camera.release()
cv2.destroyAllWindows()
