import streamlit as st
import random
from midiutil import MIDIFile
import io

st.set_page_config(layout="wide")

# =====================================================
# RAGA ENGINE (Same as before)
# =====================================================

R_OPTIONS = ["R1","R1","R1","R1","R2","R2","R2","R2","R3","R3","R3","R3"]
G_OPTIONS = ["G1","G2","G3","G1","G2","G3","G1","G2","G3","G1","G2","G3"]
D_OPTIONS = ["D1","D1","D1","D1","D2","D2","D2","D2","D3","D3","D3","D3"]
N_OPTIONS = ["N1","N2","N3","N1","N2","N3","N1","N2","N3","N1","N2","N3"]

def generate_72_melakarta():
    ragas = {}
    count = 1
    for m in ["M1","M2"]:
        for i in range(36):
            r = R_OPTIONS[i % 12]
            g = G_OPTIONS[i % 12]
            d = D_OPTIONS[i % 12]
            n = N_OPTIONS[i % 12]
            name = f"Melakarta_{count}"
            aroha = ["S", r, g, m, "P", d, n, "S'"]
            avaroha = ["S'", n, d, "P", m, g, r, "S"]
            ragas[name] = {
                "aroha": aroha,
                "avaroha": avaroha,
                "swara_set": list(set(aroha + avaroha)),
                "madhyama": m
            }
            count += 1
    return ragas

RAGAS = generate_72_melakarta()

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
# SHRUTI ENGINE (Adjustable)
# =====================================================

DEFAULT_CENT_MAP = {
    "S": 0,
    "R1": 90, "R2": 204, "R3": 294,
    "G1": 204, "G2": 294, "G3": 408,
    "M1": 498, "M2": 590,
    "P": 702,
    "D1": 792, "D2": 906, "D3": 996,
    "N1": 906, "N2": 996, "N3": 1110
}

def swara_to_midi(base_sa, swara):
    octave = 1 if "'" in swara else 0
    sw = swara.replace("'", "")
    base_note = base_sa + octave * 12
    return base_note

# =====================================================
# SANDHAM + MELODY
# =====================================================

BASE_CLUSTERS = ["தனதன","தத்தன","தானன","தந்தன"]

def generate_sandham(cycles, aksharas):
    total_units = cycles * aksharas
    pattern = random.choices(BASE_CLUSTERS, k=total_units)
    pattern[-1] = "தனதான"
    return " ".join(pattern)

def generate_melody(raga_name, total_notes):
    swaras = RAGAS[raga_name]["swara_set"]
    melody = [random.choice(swaras) for _ in range(total_notes)]
    melody[-1] = "S"
    return melody

# =====================================================
# MIDI EXPORT
# =====================================================

def create_midi(melody, base_sa, tempo):
    midi = MIDIFile(1)
    track = 0
    channel = 0
    time = 0
    midi.addTempo(track, time, tempo)

    for sw in melody:
        note = swara_to_midi(base_sa, sw)
        midi.addNote(track, channel, note, time, 1, 100)
        time += 1

    buffer = io.BytesIO()
    midi.writeFile(buffer)
    return buffer.getvalue()

# =====================================================
# UI
# =====================================================

st.title("Carnatic Composer — Stage 2 (Shruti + MIDI)")

with st.sidebar:
    raga_choice = st.selectbox("Raga", list(RAGAS.keys()))
    tala_choice = st.selectbox("Tala", list(TALAS.keys()))
    cycles = st.slider("Cycles", 1, 4, 2)
    tempo = st.slider("Tempo", 60, 160, 90)
    base_sa = st.slider("Base Sa (MIDI)", 48, 72, 60)

if st.button("Generate"):

    aksharas = TALAS[tala_choice]
    sandham = generate_sandham(cycles, aksharas)
    melody = generate_melody(raga_choice, cycles * aksharas)

    st.subheader("Sandham")
    st.text(sandham)

    st.subheader("Swara")
    st.text(" ".join(melody))

    st.subheader("Shruti Mapping (Cents)")
    for sw in melody[:10]:
        sw_clean = sw.replace("'", "")
        cents = DEFAULT_CENT_MAP.get(sw_clean, 0)
        st.write(f"{sw} → {cents} cents")

    midi_data = create_midi(melody, base_sa, tempo)
    st.download_button("Download MIDI", midi_data, "composition.mid")
