
import streamlit as st
import json
from composer_engine import compose_song

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(page_title="Carnatic Composition Engine", layout="wide")

st.title("🎼 Carnatic Commercial Composition Engine")

# ======================================
# LOAD RAGA DATABASE
# ======================================

@st.cache_data
def load_ragas():
    with open("raga_database.json", "r", encoding="utf-8") as f:
        raw = json.load(f)

    ragas = []
    for _, data in raw["melakarta"].items():
        ragas.append(data["name"])

    return sorted(ragas)

RAGA_NAMES = load_ragas()

# ======================================
# UI CONTROLS
# ======================================

col1, col2 = st.columns(2)

with col1:
    raga_name = st.selectbox("Select Raga", RAGA_NAMES)

    tala_name = st.selectbox(
        "Select Tala",
        ["Adi", "Rupaka", "Misra_Chapu", "Khanda_Chapu"]
    )

    motion = st.selectbox(
        "Select Emotional Motion",
        ["gradual_rise", "fall_then_rise", "explosive",
         "wave", "fall", "static"]
    )

with col2:
    intensity = st.slider("Intensity", 1, 10, 6)

    line_bias = st.selectbox(
        "Line Bias",
        ["adaptive", "even", "odd"]
    )

    spill_probability = st.slider(
        "Spill Probability",
        0.0, 0.5, 0.1
    )

# ======================================
# GENERATE BUTTON
# ======================================

if st.button("Generate Composition"):

    song = compose_song(
        polarity="positive",
        motion=motion,
        intensity=intensity,
        raga_name=raga_name,
        tala_name=tala_name,
        line_bias=line_bias,
        spill_probability=spill_probability
    )

    st.subheader("🎵 Pallavi")

    for line in song["pallavi"]:
        st.write(line)

    st.subheader("🎵 Charanam")

    for line in song["charanam"]:
        st.write(line)
