from voice.audio_cleaning import clean_audio
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from app.resources import whisper_model
import queue

def record_audio(duration=5, filename="input.wav", fs=16000, channels=1):
    print("Speak now...")

    audio = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()

    audio = np.int16(audio * 32767)

    write(filename, fs, audio)



SAMPLE_RATE = 16000
BLOCK_SIZE = 1024

audio_queue = queue.Queue()


def callback(indata, frames, time, status):
    audio_queue.put(indata.copy())


def record_until_silence():

    silence_threshold = 0.01
    silence_frames = 0
    max_silence = 45  

    audio_buffer = []
    speaking_started = False

    with sd.InputStream(samplerate=SAMPLE_RATE,
                        channels=1,
                        callback=callback,
                        blocksize=BLOCK_SIZE):

        while True:
            audio = audio_queue.get()
            audio_float = audio[:, 0]

            volume = np.abs(audio_float).mean()

            if volume > silence_threshold:
                speaking_started = True
                silence_frames = 0
                audio_buffer.append(audio_float)

            else:
                if speaking_started:
                    silence_frames += 1
                    audio_buffer.append(audio_float)

            if speaking_started and silence_frames > max_silence:
                break


    return np.concatenate(audio_buffer)



def speech_to_text(file="input.wav", model=whisper_model()):
    result = model.transcribe(file, fp16=False, language="en", temperature=0, initial_prompt="Medical assistant conversation")
    return result["text"]