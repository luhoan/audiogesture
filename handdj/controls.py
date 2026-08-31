import Quartz

is_playing = False

# macOS media key codes
MEDIA_KEYS = {
    "VOLUME_UP": 0,
    "VOLUME_DOWN": 1,
    "MUTE": 7,
    "PLAY_PAUSE": 16,
    "NEXT": 17,
    "PREVIOUS": 18,
}

def media_key(key):
    key_code = MEDIA_KEYS[key]

    def send_event(down):
        # 0xA = key down
        # 0xB = key up
        state = 0xA if down else 0xB

        event = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
            Quartz.NSSystemDefined,
            (0, 0),
            0xA00 if down else 0xB00,
            0,
            0,
            None,
            8,
            (key_code << 16) | (state << 8),
            -1,
        )

        if event is None:
            raise RuntimeError("Could not create macOS media event.")

        cg_event = event.CGEvent()

        if cg_event is None:
            raise RuntimeError("Could not convert media event to CGEvent.")

        Quartz.CGEventPost(
            Quartz.kCGHIDEventTap,
            cg_event
        )

    send_event(True)

    # Give macOS a moment between key-down and key-up.
    import time
    time.sleep(0.05)

    send_event(False)


GESTURE_KEYS = {
    "POINT_LEFT": "PREVIOUS",
    "OPEN_PALM": "PAUSE",
    "FIST": "PLAY",
    "POINT_RIGHT": "NEXT",

    "THUMBS_UP": "VOLUME_UP",
    "THUMBS_DOWN": "VOLUME_DOWN",
    "PINCH": "MUTE",
}

def execute_gesture(gesture):

    if gesture == "POINT_LEFT":
        print("Gesture: POINT_LEFT -> PREVIOUS")
        media_key("PREVIOUS")

    elif gesture == "POINT_RIGHT":
        print("Gesture: POINT_RIGHT -> NEXT")
        media_key("NEXT")

    elif gesture == "OPEN_PALM":
        print("Gesture: OPEN_PALM -> PLAY/PAUSE")
        media_key("PLAY_PAUSE")

    elif gesture == "FIST":
        print("Gesture: FIST -> PLAY/PAUSE")
        media_key("PLAY_PAUSE")

    elif gesture == "THUMBS_UP":
        print("Gesture: THUMBS_UP -> VOLUME UP")
        media_key("VOLUME_UP")

    elif gesture == "THUMBS_DOWN":
        print("Gesture: THUMBS_DOWN -> VOLUME DOWN")
        media_key("VOLUME_DOWN")

    elif gesture == "PINCH":
        print("Gesture: PINCH -> MUTE")
        media_key("MUTE")