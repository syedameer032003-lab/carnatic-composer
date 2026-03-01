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


RAGA_DB = load_json("raga_database.json")
MOOD_DB = load_json("moods.json")
EMOTION_DB = load_json("emotions.json")
CHUNKS_DB = load_json("sandham_chunks.json")


# ==========================
# BASIC SANDHAM GENERATOR
# ==========================

def generate_line(target_beats):
    result = []
    current = 0

    while current < target_beats:
        beat = random.choice(list(CHUNKS_DB.keys()))
        beat = int(beat)

        if current + beat > target_beats:
            continue

        chunk = random.choice(CHUNKS_DB[str(beat)])
        result.append(chunk["text"])
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

st.title("Carnatic Sandham Composer")

# Raga
raga_names = [mela["name"] for mela in RAGA_DB["melakarta"].values()]
raga_name = st.selectbox("Select Raga", sorted(raga_names))

# Mood Category (top level keys)
mood_category = st.selectbox(
    "Select Mood Category",
    list(MOOD_DB["moods"].keys())
)

# Sub Mood (inside selected category)
mood = st.selectbox(
    "Select Specific Mood",
    MOOD_DB["moods"][mood_category]
)

# Emotion (flat list)
emotion = st.selectbox(
    "Select Emotion",
    EMOTION_DB["emotions"]
)

if st.button("Compose"):
    song = compose_song()

    st.subheader("Generated Structure")

    for section, lines in song.items():
        st.markdown(f"### {section}")
        for line in lines:
            st.write(line)
