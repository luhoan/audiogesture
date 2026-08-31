import math


def distance(a, b):
    """Distance between two MediaPipe landmarks."""

    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2 +
        (a.z - b.z) ** 2
    )


def finger_extended(hand, pip, tip):
    """
    Determines whether a finger is extended.

    A simple first approximation:
    the fingertip should be farther from
    the wrist than the PIP joint.
    """

    wrist = hand[0]

    tip_distance = distance(hand[tip], wrist)
    pip_distance = distance(hand[pip], wrist)

    return tip_distance > pip_distance * 1.15


def get_finger_states(hand):
    """
    Returns the state of the four main fingers.

    True  = extended
    False = folded
    """

    index = finger_extended(hand, 6, 8)
    middle = finger_extended(hand, 10, 12)
    ring = finger_extended(hand, 14, 16)
    pinky = finger_extended(hand, 18, 20)

    return {
        "index": index,
        "middle": middle,
        "ring": ring,
        "pinky": pinky,
    }


def identify_gesture(hand):
    """
    Convert hand landmarks into a gesture name.
    """

    fingers = get_finger_states(hand)

    index = fingers["index"]
    middle = fingers["middle"]
    ring = fingers["ring"]
    pinky = fingers["pinky"]

    # ✋ Open palm
    if index and middle and ring and pinky:
        return "OPEN_PALM"

    # ✊ Fist
    if not index and not middle and not ring and not pinky:
        return "FIST"

    # 👉 Pointing
    if index and not middle and not ring and not pinky:

        # We'll distinguish left/right later.
        return "POINT"

    return "UNKNOWN"

