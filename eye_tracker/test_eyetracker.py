import os
import sys
sys.path.append("D:\BeamSDK-Windows64-1.1.0\API\python")


from eyeware.client import TrackerClient
import time
import numpy as np


tracker = TrackerClient()
while True:
    # Make sure that the connection with the tracker server (Eyeware application) is up and running.
    if tracker.connected:


        print("  * Gaze on Screen:")
        screen_gaze = tracker.get_screen_gaze_info()
        screen_gaze_is_lost = screen_gaze.is_lost
        print("      - Lost track:       ", screen_gaze_is_lost)
        # if not screen_gaze_is_lost:
        #     print("      - Screen ID:        ", screen_gaze.screen_id)
        #     print("      - Coordinates:       <x=%5.3f px,   y=%5.3f px>" % (screen_gaze.x, screen_gaze.y))
        #     print("      - Confidence:       ", screen_gaze.confidence)

        time.sleep(1 / 30)  # We expect tracking data at 30 Hz
    else:
        # Print a message every MESSAGE_PERIOD_IN_SECONDS seconds
        MESSAGE_PERIOD_IN_SECONDS = 2
        time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
        print("No connection with tracker server")
