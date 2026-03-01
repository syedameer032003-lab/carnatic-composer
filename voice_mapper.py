import librosa
import numpy as np

def extract_rhythm_blueprint(audio_file, entropy=0.3):

    y, sr = librosa.load(audio_file)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    if len(onset_times) < 2:
        return []

    gaps = np.diff(onset_times)
    normalized = gaps / np.mean(gaps)

    blueprint = []

    for g in normalized:
        syllables = max(1, int(round(g * 4)))
        blueprint.append({"syllables": syllables})

    return blueprint
