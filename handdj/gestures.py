import math


def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2 +
        (a.z - b.z) ** 2
    )


def finger_extended(hand, pip, tip):
    wrist = hand[0]

    tip_distance = distance(hand[tip], wrist)
    pip_distance = distance(hand[pip], wrist)

    return tip_distance > pip_distance * 1.15


def get_finger_states(hand):
    return {
        "index": finger_extended(hand, 6, 8),
        "middle": finger_extended(hand, 10, 12),
        "ring": finger_extended(hand, 14, 16),
        "pinky": finger_extended(hand, 18, 20),
    }


def identify_gesture(hand):
    fingers = get_finger_states(hand)

    index = fingers["index"]
    middle = fingers["middle"]
    ring = fingers["ring"]
    pinky = fingers["pinky"]

    # Open palm
    if index and middle and ring and pinky:
        return "OPEN_PALM"

    # Fist
    if not index and not middle and not ring and not pinky:
        return "FIST"

    # Pointing
    if index and not middle and not ring and not pinky:

        wrist = hand[0]
        index_tip = hand[8]

        dx = index_tip.x - wrist.x

        # Pointing right on the screen
        if dx > 0:
            return "POINT_RIGHT"

        # Pointing left on the screen
        else:
            return "POINT_LEFT"

    return "UNKNOWN"


class GestureStabilizer:

    def __init__(self, required_frames=8):
        self.required_frames = required_frames

        self.current_gesture = None
        self.frame_count = 0

        self.stable_gesture = "UNKNOWN"

    def update(self, detected_gesture):

        # Same gesture as previous frame
        if detected_gesture == self.current_gesture:
            self.frame_count += 1

        # New gesture
        else:
            self.current_gesture = detected_gesture
            self.frame_count = 1

        # Gesture has remained stable
        if self.frame_count >= self.required_frames:

            if detected_gesture != self.stable_gesture:

                self.stable_gesture = detected_gesture

                # Return the NEW gesture
                return detected_gesture

        # Nothing changed
        return None