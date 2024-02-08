
import pyautogui, cv2, numpy as np
from screeninfo import get_monitors
import soundfile as sf
import sounddevice as sd
import sys, os
import datetime, time
import requests, webbrowser
import threading

## configuration start ##

# time settings
start_hour = 11
start_minute = 11
start_seconds = 1

end_hour = 11
end_minute = 11
end_seconds = 5

# output settings
audio_output_location = f"output_audio\\{str(datetime.datetime.now().date().day)}_{str(datetime.datetime.now().date().month)}_{str(datetime.datetime.now().date().year)}.wav"
video_output_location = f"output_video\\{str(datetime.datetime.now().date().day)}_{str(datetime.datetime.now().date().month)}_{str(datetime.datetime.now().date().year)}.avi"

# monitor settings
monitor_info = get_monitors()[0]
x = monitor_info.width
y = monitor_info.height

# video settings
framerate = 24.0
resolution = (x, y)
codec = cv2.VideoWriter_fourcc(*"XVID")

# audio settings
samplerate = 44100
duration = ((end_hour * 60 * 60) + (end_minute * 60) + end_seconds) - ((start_hour * 60 * 60) + (start_minute * 60) + start_seconds)
print(duration)
exit()
print(sd.query_devices())
loopback_device = 1

# configuration end ##

def get_time():
    current_time = datetime.datetime.now().time()

    # Retrieve hours, minutes, and seconds
    hours = int(current_time.hour)
    minutes = int(current_time.minute)
    seconds = int(current_time.second)

    # Print the values
    print("Hours:", hours)
    print("Minutes:", minutes)
    print("Seconds:", seconds)

    return hours, minutes, seconds

out = cv2.VideoWriter(video_output_location, codec, framerate, resolution)
cv2.namedWindow("Live", cv2.WINDOW_NORMAL) # debug
cv2.resizeWindow("Live", 480, 270) # debug


def record_screen():
    while True:

        img = pyautogui.screenshot()
        frame = np.array(img)
    
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        
        cv2.imshow('Live', frame) # debug
        
        if cv2.waitKey(1) == ord('a'):
            break
    out.release()
    cv2.destroyAllWindows()

def record_audio():
    print(f"Recording for {duration} seconds...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate,channels=2, device=loopback_device)
    sd.wait()  # Wait until recording is finished

    # Save the recording
    sf.write(audio_output_location, myrecording, samplerate)

record_audio()
