import streamlit as st
import json
import random

st.set_page_config(layout="wide")

# =====================================================
# LOAD JSON DATABASE
# =====================================================

with open("raga_database.json", "r", encoding="utf-8") as f:
    RAGA_DB = json.load(f)["melakarta"]

# =====================================================
# BUILD RAGA LIST
# =====================================================

def build_raga_list():
    ragas = []
    for mela_num, data in RAGA_DB.items():
        ragas.append({
            "label": f"{data['name']} (Mela {mela_num})",
            "mela": mela_num,
            "type": "Melakarta",
            "name": data["name"],
            "data": data
        })
        for j_name, j_data in data["janya"].items():
            ragas.append({
                "label": f"{data['name']} - {j_name}",
                "mela": mela_num,
                "type": "Janya",
                "name": f"{data['name']} - {j_name}",
                "data": j_data
            })
    return ragas

ALL_RAGAS = build_raga_list()

# =====================================================
# TALA ENGINE
# =====================================================

TALAS = {
    "Adi": 8,
    "Rupaka": 6,
    "Misra Chapu": 7,
    "Khanda Chapu": 5
}

# =====================================================
# SANDHAM TEMPLATES
# =====================================================

SANDHAM_TEMPLATES = [
    [4,4,4,4],
    [3,3,2],
    [5,5,6],
    [7,7]
]

BASE_CLUSTERS = ["தனதன","தத்தன","தானன","தந்தன"]

def generate_sandham(cycles, aksharas):
    total = cycles * aksharas
    pattern = random.choices(BASE_CLUSTERS, k=total)
    pattern[-1] = "தனதான"
    return pattern

# =====================================================
# MELODY ENGINE (Scale Driven for Now)
# =====================================================

def generate_melody(raga_data, total_notes, mood):

    scale = raga_data["aroha"]
    if scale[-1] == "S'":
        scale = scale[:-1]

    melody = []
    current_index = 0

    for i in range(total_notes):

        progress = i / total_notes
        direction = 1 if progress < 0.5 else -1

        if mood == "Devotional":
            leap_prob = 0.05
        elif mood == "Romantic":
            leap_prob = 0.15
        elif mood == "Heroic":
            leap_prob = 0.25
        else:
            leap_prob = 0.1

        r = random.random()

        if r < 0.7:
            new_index = current_index + direction
        elif r < 0.9:
            new_index = current_index
        else:
            new_index = current_index + random.choice([-2,2])

        new_index = max(0, min(len(scale)-1, new_index))

        melody.append(scale[new_index])
        current_index = new_index

    melody[-1] = "S"
    return melody

# =====================================================
# UI
# =====================================================

st.title("Carnatic Composer — JSON Master Engine")

with st.sidebar:
    tala_choice = st.selectbox("Tala", list(TALAS.keys()))
    mood = st.selectbox("Mood", ["Devotional","Romantic","Heroic","Melancholic"])
    chakra_filter = st.selectbox("Chakra Filter", ["All"] + list(range(1,13)))
    search = st.text_input("Search Raga")

# FILTERING
filtered_ragas = []

for r in ALL_RAGAS:

    mela_data = RAGA_DB[str(r["mela"])]

    if chakra_filter != "All" and mela_data["chakra"] != chakra_filter:
        continue

    if search.lower() not in r["label"].lower():
        continue

    filtered_ragas.append(r)

raga_labels = [r["label"] for r in filtered_ragas]

selected_label = st.selectbox("Select Raga", raga_labels)

selected_raga = next(r for r in filtered_ragas if r["label"] == selected_label)

cycles = st.slider("Cycles", 1, 4, 2)

if st.button("Generate Composition"):

    aksharas = TALAS[tala_choice]
    sandham_pattern = generate_sandham(cycles, aksharas)
    melody = generate_melody(selected_raga["data"], cycles*aksharas, mood)

    st.subheader("Raga Info")
    st.write(f"Name: {selected_raga['label']}")
    st.write(f"Type: {selected_raga['type']}")
    st.write(f"Mela: {selected_raga['mela']}")
    st.write(f"Chakra: {RAGA_DB[str(selected_raga['mela'])]['chakra']}")

    st.subheader("Sandham")
    st.text(" ".join(sandham_pattern))

    st.subheader("Melody")
    st.text(" ".join(melody))

    st.subheader("Aroha")
    st.text(" ".join(selected_raga["data"]["aroha"]))

    st.subheader("Avaroha")
    st.text(" ".join(selected_raga["data"]["avaroha"]))
