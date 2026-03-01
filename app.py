import streamlit as st
import json
import os
import traceback
from composer_engine import compose_song
from voice_mapper import extract_rhythm_blueprint

st.set_page_config(page_title="Carnatic Sandham Studio")
st.title("Carnatic Sandham Studio")

BASE_PATH = os.path.dirname(__file__)

# ----------------------------
# LOAD JSON FILES
# ----------------------------

def load_json(filename):
    with open(os.path.join(BASE_PATH, filename), encoding="utf-8") as f:
        return json.load(f)

RAGA_DB = load_json("raga_database.json")
EMOTION_DB = load_json("emotions.json")

# ----------------------------
# PREPARE DROPDOWNS
# ----------------------------

# Emotions (your structure)
emotion_list = sorted(EMOTION_DB["emotions"])

# Melakarta dropdown
melakarta_list = []
for key, value in RAGA_DB["melakarta"].items():
    melakarta_list.append(f"{key} - {value['name']}")

melakarta_list = sorted(melakarta_list, key=lambda x: int(x.split(" - ")[0]))

# ----------------------------
# INPUT SECTION
# ----------------------------

emotion = st.selectbox("Emotion", emotion_list)

raga_selection = st.selectbox("Raga (Melakarta)", melakarta_list)
raga_id = raga_selection.split(" - ")[0]

tala = st.selectbox("Tala", ["Adi", "Rupaka", "MisraChap"])

entropy = st.slider("Entropy", 0.0, 1.0, 0.3)

# ----------------------------
# COMPOSE
# ----------------------------

if st.button("Compose"):

    try:
        song = compose_song(
            emotion=emotion,
            raga_id=raga_id,
            tala_name=tala,
            entropy=entropy
        )

        st.subheader("Pallavi")
        for line in song["structure"]["pallavi"]:
            st.write(line)

        st.subheader("Charanam")
        for line in song["structure"]["charanam"]:
            st.write(line)

    except Exception as e:
        st.error("Error while composing")
        st.text(str(e))
        st.text(traceback.format_exc())

# ----------------------------
# VOICE SECTION
# ----------------------------

st.divider()
st.header("Voice → Sandham")

audio = st.file_uploader("Upload humming (wav recommended)", type=["wav"])

if audio is not None:
    try:
        blueprint = extract_rhythm_blueprint(audio)
        st.subheader("Detected Sandham Blueprint")
        st.write(blueprint)
    except Exception as e:
        st.error("Audio processing error")
        st.text(str(e))
        st.text(traceback.format_exc())
