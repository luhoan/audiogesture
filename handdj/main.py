import cv2
import mediapipe as mp
from pathlib import Path

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gestures import identify_gesture, GestureStabilizer


# Find the model next to this Python file
MODEL_PATH = Path(__file__).parent / "hand_landmarker.task"


# Configure MediaPipe
base_options = python.BaseOptions(
    model_asset_path=str(MODEL_PATH),
    delegate=python.BaseOptions.Delegate.CPU,
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
)

detector = vision.HandLandmarker.create_from_options(options)

stabilizer = GestureStabilizer(required_frames=8)

# Open MacBook camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open camera.")


while True:
    success, frame = cap.read()

    if not success:
        print("Could not read camera frame.")
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # OpenCV: BGR
    # MediaPipe: RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame,
    )

    # Detect hands
    result = detector.detect(mp_image)

    # Draw the 21 landmarks
    if result.hand_landmarks:

        for hand in result.hand_landmarks:

            gesture = identify_gesture(hand)
            new_gesture = stabilizer.update(gesture)

            cv2.putText(
                frame,
                f"Detected: {gesture}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Stable: {stabilizer.stable_gesture}",
                (30, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            height, width, _ = frame.shape

            for landmark in hand:

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1,
                )

    cv2.imshow("HandDJ", frame)

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()