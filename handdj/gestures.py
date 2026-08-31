import math
import time

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
    """
    determine whether each finger is extended

    mediaPipe landmarks:
    Thumb:  4
    Index:  8
    Middle: 12
    Ring:   16
    Pinky:  20
    """

    # For the thumb, compare x position of the tip
    # to the thumb's lower joint.
    thumb = abs(hand[4].x - hand[2].x) > 0.05

    # For the other fingers, compare the fingertip
    # to the PIP joint.
    index = hand[8].y < hand[6].y
    middle = hand[12].y < hand[10].y
    ring = hand[16].y < hand[14].y
    pinky = hand[20].y < hand[18].y

    return {
        "thumb": thumb,
        "index": index,
        "middle": middle,
        "ring": ring,
        "pinky": pinky,
    }


def identify_gesture(hand):
    fingers = get_finger_states(hand)

    index = fingers["index"]
    middle = fingers["middle"]
    ring = fingers["ring"]
    pinky = fingers["pinky"]
    thumb = fingers["thumb"]

    # Open palm
    if thumb and index and middle and ring and pinky:
        return "OPEN_PALM"

    # Fist
    if not thumb and not index and not middle and not ring and not pinky:
        return "FIST"

    # Pointing right
    if index and not middle and not ring and not pinky:
        wrist = hand[0]
        index_tip = hand[8]

        dx = index_tip.x - wrist.x

        if dx > 0:
            return "POINT_RIGHT"
        else:
            return "POINT_LEFT"

    # Thumbs up
    if thumb and not index and not middle and not ring and not pinky:
        wrist = hand[0]
        thumb_tip = hand[4]

        dy = thumb_tip.y - wrist.y

        if dy < 0:
            return "THUMBS_UP"

    # Thumbs down
    if thumb and not index and not middle and not ring and not pinky:
        wrist = hand[0]
        thumb_tip = hand[4]

        dy = thumb_tip.y - wrist.y

        if dy > 0:
            return "THUMBS_DOWN"

    # Pinch
    if thumb and index:
        thumb_tip = hand[4]
        index_tip = hand[8]

        distance = ((thumb_tip.x - index_tip.x) ** 2 +
                    (thumb_tip.y - index_tip.y) ** 2) ** 0.5

        if distance < 0.08:
            return "PINCH"

    return "UNKNOWN"

class GestureStabilizer:

    def __init__(self, required_frames=8, action_cooldown=0.8):

        self.required_frames = required_frames
        self.action_cooldown = action_cooldown

        self.current_gesture = None
        self.frame_count = 0

        self.stable_gesture = "UNKNOWN"

        self.last_action_time = 0

    def update(self, detected_gesture):

        current_time = time.time()

        # New gesture
        if detected_gesture != self.current_gesture:

            self.current_gesture = detected_gesture
            self.frame_count = 1

        # Same gesture
        else:

            self.frame_count += 1

        # Gesture is stable
        if self.frame_count >= self.required_frames:

            # Repeatable gestures
            repeatable = {
                "POINT_LEFT",
                "POINT_RIGHT",
                "THUMBS_UP",
                "THUMBS_DOWN",
            }

            if detected_gesture in repeatable:

                if current_time - self.last_action_time >= self.action_cooldown:

                    self.last_action_time = current_time

                    return detected_gesture

            # Non-repeatable gestures
            else:

                if detected_gesture != self.stable_gesture:

                    self.stable_gesture = detected_gesture

                    return detected_gesture

        return None