import streamlit as st
import json
import random


# ==========================
# LOAD JSON SAFELY
# ==========================

def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


RAGA_DB = load_json("raga_database.json")
MOOD_DB = load_json("moods.json")
EMOTION_DB = load_json("emotions.json")
CHUNKS_DB = load_json("sandham_chunks.json")


# ==========================
# EMOTION → SANDHAM BIAS
# ==========================

EMOTION_WEIGHT_MAP = {
    "joy": ["bright", "flow"],
    "sad": ["soft", "stretch"],
    "anger": ["sharp", "heavy"],
    "romantic": ["soft", "flow"],
    "devotional": ["stretch", "soft"],
    "fear": ["tense", "sharp"],
    "energetic": ["bright", "heavy"],
    "melancholy": ["soft"],
}


# ==========================
# SELECT RAGA
# ==========================

def get_raga_names():
    names = []
    for mela_no, mela in RAGA_DB["melakarta"].items():
        names.append(mela["name"])
    return sorted(names)


def get_raga_by_name(name):
    for mela in RAGA_DB["melakarta"].values():
        if mela["name"] == name:
            return mela
    return None


# ==========================
# SANDHAM ENGINE
# ==========================

def generate_line(target_beats, emotion):
    allowed_moods = EMOTION_WEIGHT_MAP.get(emotion, [])

    result = []
    current = 0

    while current < target_beats:
        beat_choices = list(CHUNKS_DB.keys())
        beat = random.choice(beat_choices)

        if current + int(beat) > target_beats:
            continue

        possible_chunks = CHUNKS_DB[str(beat)] if isinstance(beat, str) else CHUNKS_DB[beat]

        if allowed_moods:
            filtered = [c for c in possible_chunks if c["mood"] in allowed_moods]
            if filtered:
                chunk = random.choice(filtered)
            else:
                chunk = random.choice(possible_chunks)
        else:
            chunk = random.choice(possible_chunks)

        result.append(chunk["text"])
        current += int(beat)

    return " ".join(result)


# ==========================
# COMPOSER ENGINE
# ==========================

def compose_song(raga, mood, emotion, entropy):
    structure = {
        "Pallavi": 2,
        "Anupallavi": 2,
        "Charanam": 4
    }

    song = {}

    for section, lines in structure.items():
        section_lines = []
        for _ in range(lines):
            beats = random.choice([8, 12, 16])
            line = generate_line(beats, emotion)
            section_lines.append(line)
        song[section] = section_lines

    return song


# ==========================
# STREAMLIT UI
# ==========================

st.title("Carnatic Emotion-Based Sandham Composer")

raga_name = st.selectbox("Select Raga", get_raga_names())
mood = st.selectbox("Select Mood", MOOD_DB["moods"])
emotion = st.selectbox("Select Emotion", EMOTION_DB["emotions"])

entropy = st.slider("Creativity (Entropy)", 0.0, 1.0, 0.5)

if st.button("Compose"):
    raga = get_raga_by_name(raga_name)

    song = compose_song(
        raga=raga,
        mood=mood,
        emotion=emotion,
        entropy=entropy
    )

    st.subheader("Generated Structure")

    for section, lines in song.items():
        st.markdown(f"### {section}")
        for line in lines:
            st.write(line)
