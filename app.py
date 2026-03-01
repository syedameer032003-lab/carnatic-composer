
import streamlit as st
from composer_engine import compose_song
from voice_mapper import extract_rhythm_blueprint

st.title("Carnatic Sandham Studio")

emotion = st.text_input("Emotion", "love")
raga_id = st.text_input("Raga ID", "15")
tala = st.selectbox("Tala", ["Adi", "Rupaka", "MisraChap"])
entropy = st.slider("Entropy", 0.0, 1.0, 0.3)

if st.button("Compose"):
    song = compose_song(emotion, raga_id, tala, entropy=entropy)

    st.subheader("Pallavi")
    for line in song["structure"]["pallavi"]:
        st.write(line)

    st.subheader("Charanam")
    for line in song["structure"]["charanam"]:
        st.write(line)

st.divider()

st.header("Voice → Sandham")

audio = st.file_uploader("Upload humming", type=["wav", "mp3"])

if audio:
    blueprint = extract_rhythm_blueprint(audio)
    st.write(blueprint)
