import pyautogui, cv2, numpy as np
import pyaudio
import wave
import sys, os
import datetime, time
import requests, webbrowser
import argparse

parser = argparse.ArgumentParser(description='Records audio from the computer.')
parser.add_argument('--DEVICE', type=int, help='Index of the input device.')
parser.add_argument('--RECORDING_SECONDS', type=int, help='Index of the input device.')
parser.add_argument('--LOCATION', type=str, help='Index of the input device.')
parser.add_argument('--CHANNELS', type=int, help='Channel count of the input device')
parser.add_argument('--RATE', type=int, help='Rate of the recording')
parser.add_argument('--FORMAT', type=str, help='Format of the recording')
parser.add_argument('--CHUNK', type=int, help='Size of the chunks')

args = parser.parse_args()

INPUT_DEVICE = args.DEVICE
RECORD_SECONDS = args.RECORDING_SECONDS
WAVE_OUTPUT_FILENAME = args.LOCATION
FORMAT = args.FORMAT
CHANNELS = args.CHANNELS
RATE = args.RATE
CHUNK = args.CHUNK

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,input_device_index=INPUT_DEVICE)

    print("Recording audio sounds...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

record_audio()
