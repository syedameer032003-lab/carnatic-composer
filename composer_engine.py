import streamlit as st
import json
import random
import os


# ==========================
# SAFE JSON LOADER
# ==========================

def load_json(file):
    if not os.path.exists(file):
        st.error(f"Missing file: {file}")
        st.stop()

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================
# LOAD DATABASES
# ==========================

RAGA_DB = load_json("raga_database.json")
MOOD_DB = load_json("moods.json")          # NO "moods" wrapper expected
EMOTION_DB = load_json("emotions.json")   # Must contain {"emotions": [...]}
CHUNKS_DB = load_json("sandham_chunks.json")


# ==========================
# RAGA HELPERS
# ==========================

def get_raga_names():
    return [
        raga["name"]
        for raga in RAGA_DB["melakarta"].values()
    ]


# ==========================
# SANDHAM GENERATOR
# ==========================

def generate_line(target_beats):
    result = []
    current = 0

    beat_options = list(CHUNKS_DB.keys())

    while current < target_beats:
        beat = int(random.choice(beat_options))

        if current + beat > target_beats:
            continue

        chunk_list = CHUNKS_DB[str(beat)]

        # Supports both formats:
        # ["தனனா"]  OR  [{"text": "தனனா"}]
        chunk = random.choice(chunk_list)

        if isinstance(chunk, dict):
            result.append(chunk["text"])
        else:
            result.append(chunk)

        current += beat

    return " ".join(result)


def compose_song():
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
            section_lines.append(generate_line(beats))
        song[section] = section_lines

    return song


# ==========================
# STREAMLIT UI
# ==========================

st.title("Carnatic Emotion-Based Sandham Composer")

# Raga
raga_name = st.selectbox("Select Raga", sorted(get_raga_names()))

# Mood (top-level keys directly)
mood_category = st.selectbox("Select Mood Category", list(MOOD_DB.keys()))
mood = st.selectbox("Select Specific Mood", MOOD_DB[mood_category])

# Emotion
emotion = st.selectbox("Select Emotion", EMOTION_DB["emotions"])

# Creativity control
entropy = st.slider("Creativity (Entropy)", 0.0, 1.0, 0.5)

# ==========================
# COMPOSE BUTTON
# ==========================

if st.button("Compose Song"):
    song = compose_song()

    st.subheader("Generated Structure")
    st.write(f"Raga: {raga_name}")
    st.write(f"Mood: {mood}")
    st.write(f"Emotion: {emotion}")
    st.write("")

    for section, lines in song.items():
        st.markdown(f"### {section}")
        for line in lines:
            st.write(line)
