import pyaudio
import numpy as np
import time
from playsound import playsound
import random

FORMAT = pyaudio.paInt16
CHANNELS: int = 1
RATE: int = 16000
CHUNK: int = 1024
THRESHOLD: int = 110
PAUSE_DURATION: float = 0.4

audio_detection = pyaudio.PyAudio()

stream = audio_detection.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

adlibs: list[str] = ["goddamn.mp3", "oh-my-god.mp3", "yeah.mp3", "its-lit.mp3", "straight-up.mp3", "stroke-my-cactus.mp3"]

def play_adlib() -> None:
    adlib: str = "./adlibs/" + random.choice(adlibs)
    playsound(adlib, block=False)

print("Travis is awake!!")
pause_start_time = None
while True:
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)

    rms_value = np.sqrt(np.mean(np.abs(audio_data ** 2)))

    if rms_value < THRESHOLD:
        if pause_start_time is None:
            pause_start_time = time.time()
        
        elif time.time() - pause_start_time >= PAUSE_DURATION:
            play_adlib()
            pause_start_time = None

    else:
        pause_start_time = None

stream.stop_stream()
stream.close()
audio_detection.terminate()