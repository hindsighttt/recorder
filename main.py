import pyautogui, cv2, numpy as np
from screeninfo import get_monitors
import pyaudio
import wave
import sys, os
import datetime, time
import requests, webbrowser
import threading
import keyboard

## Uncomment the line below if you want to list the audio devices ##
# audio = pyaudio.PyAudio()
# info = audio.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#     if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#         print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
# audio.terminate()


## configuration start ##

# time settings
start_hour = 14
start_minute = 13
start_seconds = 30

end_hour = 14
end_minute = 13
end_seconds = 50

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
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = ((end_hour * 60 * 60) + (end_minute * 60) + end_seconds) - ((start_hour * 60 * 60) + (start_minute * 60) + start_seconds)
WAVE_OUTPUT_FILENAME = audio_output_location
INPUT_DEVICE = 1

# configuration end ##

def get_time():
    current_time = datetime.datetime.now().time()

    hours = int(current_time.hour)
    minutes = int(current_time.minute)
    seconds = int(current_time.second)

    return hours, minutes, seconds

def start_recording():
    
    print('Starting the audio recorder...')
    print('SCREEN RECORDER NULL.')
    os.system(f'python record_audio.py -DEVICE {INPUT_DEVICE} -RECORDING_SECONDS {RECORD_SECONDS} -LOCATION {WAVE_OUTPUT_FILENAME} -CHANNELS {CHANNELS} -RATE {RATE} -FORMAT {FORMAT} -CHUNK {CHUNK}')
    time.sleep(3)

    os.system('cls')
    print('AUDIO RECORDER OK.')
    print('Starting the screen recorder...')
    os.system(f'python record_screen.py -LOCATION {video_output_location} -RECORDING_SECONDS {RECORD_SECONDS} -X {x} -Y {y} -CODEC {codec} -FRAMERATE {framerate}')
    time.sleep(3)

    os.system('cls')
    print('AUDIO RECORDER OK.')
    print('SCREEN RECORDER OK.')

def check_time():
    start = False
    while start != True:
        hours, minutes, seconds = get_time()
        if hours < start_hour and minutes < start_minute and seconds < start_seconds:
            print(f'{hours}:{minutes}:{seconds}: Waiting for start time...')
            start = False
        elif hours >= start_hour and minutes >= start_minute and seconds >= start_seconds:
            start = True
            break
def combine_video(vidname, audname, outname, fps=framerate):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)

if __name__ == "__main__":
    start_recording()
    time.sleep(RECORD_SECONDS)
    combine_video(video_output_location, audio_output_location, f"output\\{str(datetime.datetime.now().date().day)}_{str(datetime.datetime.now().date().month)}_{str(datetime.datetime.now().date().year)}.mp4")
