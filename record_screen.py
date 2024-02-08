import pyautogui, cv2, numpy as np
from screeninfo import get_monitors
import sys, os
import datetime, time
import requests, webbrowser
import argparse

parser = argparse.ArgumentParser(description='Records the screen.')
parser.add_argument('-LOCATION', type=str, help='Output location of the recording.')
parser.add_argument('-RECORDING_SECONDS', type=int, help='Length of the recording.')
parser.add_argument('-X', type=int, help='Width of the screen.')
parser.add_argument('-Y', type=int, help='Height of the screen.')
parser.add_argument('-CODEC', type=str, help='Codec of the recording.')
parser.add_argument('-FRAMERATE', type=float, help='Framerate of the recording.')

args = parser.parse_args()
framerate = args.FRAMERATE
resolution = (args.X, args.Y)
codec = args.CODEC
video_output_location = args.LOCATION
RECORD_SECONDS = args.RECORDING_SECONDS

def record_screen():

    out = cv2.VideoWriter(video_output_location, codec, framerate, resolution)
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL) # debug
    cv2.resizeWindow("Live", 480, 270) # debug

    start_time = time.time()  # Record the start time
    end_time = start_time + RECORD_SECONDS

    while time.time() < end_time:

        img = pyautogui.screenshot()
        frame = np.array(img)
    
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        
        cv2.imshow('Live', frame) # debug
        
        if cv2.waitKey(1) == ord('a'):
            break

    out.release()
    cv2.destroyAllWindows()

record_screen()