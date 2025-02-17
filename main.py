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
# test

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
        print(rms_value)

        if rms_value < THRESHOLD:
            
            if pause_start_time is None:
                pause_start_time = time.time()
            
            elif time.time() - pause_start_time >= PAUSE_DURATION:
                play_adlib(CURATED_ADLIBS)
                pause_start_time = None

        else:
            pause_start_time = None

    stream.stop_stream()
    stream.close()
    audio_detection.terminate()




HINDSIGHT: int = 5 # how far to look back in prms values
DIFFERENCE_THRESHOLD: int = -50 # ∆v
ALT_PAUSE_DURATION: float = 2

def process_prms_values(prms_values = list[float], rms = float, last_time = time) -> bool:
    '''
    Takes prms values, the current rms value, and timestamp of previous adlib.
    Determines if it's time to play an adlib.
    Prints out status messages.
    '''

    avg: float = sum(prms_values) / len(prms_values)
    diff: float = rms - avg
    
    prms_values.pop(0)
    prms_values.append(rms)

    if diff <= DIFFERENCE_THRESHOLD and time.time() - last_time >= ALT_PAUSE_DURATION:
        to_lib = True
        iflib: str = "ADLIB"

    elif diff <= DIFFERENCE_THRESHOLD:
        to_lib = False
        iflib: str = "_____"

    else:
        to_lib = False
        iflib: str= "     "

    if diff < 0:
        strdiff:str = "-" + str(-diff)[:5]
    else:
        strdiff:str = " " + str(diff)[:5]

    print(f"{iflib} diff: {str(strdiff)}, " + ("#" * int(-diff)))
    #print(f"{iflib} : Avg: {avg}, RMS: {rms}, diff: {diff}")
    return to_lib

def alt_awaken_travis():
    print("Alt-Travis is awake!!")
    prms_values = []
    last_time = time.time()

    while len(prms_values) < HINDSIGHT:
        prms_values.append(0)


    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        rms_value = np.sqrt(np.mean(np.abs(audio_data ** 2)))


        if process_prms_values(prms_values, rms_value, last_time):
            #print(f"{time.time() - last_time} >= {ALT_PAUSE_DURATION}")
            play_adlib(CURATED_ADLIBS)

            last_time = time.time()

                


    stream.stop_stream()
    stream.close()
    audio_detection.terminate()


    



if __name__ == "__main__":
    print("Awakening Travis...")
    print(f"Detected in adlib folder: {ADLIBS}")
    alt_awaken_travis()