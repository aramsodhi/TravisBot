import pyaudio, time, random, os
from os.path import isfile, join
import numpy as np
from playsound import playsound

# sound processing stuff
FORMAT = pyaudio.paInt16
CHANNELS: int = 1
RATE: int = 16000
CHUNK: int = 1024
THRESHOLD: int = 110
PAUSE_DURATION: float = 0.4

# file name stuff
ADLIB_FOLDER: str = "adlibs"
ADLIBS: list[str] = [f for f in os.listdir("adlibs") if f.endswith(".mp3")] # default list, every mp3 file in ADLIB_FOLDER

CURATED_ADLIBS: list[str] = ["goddamn.mp3", "oh-my-god.mp3", "yeah.mp3", "its-lit.mp3", "straight-up.mp3", "stroke-my-cactus.mp3"] 



audio_detection = pyaudio.PyAudio()

stream = audio_detection.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)


def play_adlib(fromAdlibs: list[str] = ADLIBS) -> None:
    '''
    Plays an adlib from a list of file names. 
    
    Files must be inside the adlib folder. ("adlibs")

    File list defaults to an automatically-generated list of every file in the folder.
    '''

    adlib: str = "./adlibs/" + random.choice(fromAdlibs)
    #print(f"> Playing {adlib}")
    playsound(adlib, block=False)

def awaken_travis():
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
                play_adlib(ADLIBS)
                pause_start_time = None

        else:
            pause_start_time = None

    stream.stop_stream()
    stream.close()
    audio_detection.terminate()

if __name__ == "__main__":
    print("Awakening Travis...")
    print(f"Detected in adlib folder: {ADLIBS}")
    awaken_travis()