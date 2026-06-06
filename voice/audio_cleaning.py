import librosa

def clean_audio(file):
    y, sr = librosa.load(file, sr=16000)
    y = librosa.effects.preemphasis(y)
    return y