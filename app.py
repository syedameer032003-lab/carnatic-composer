import streamlit as st
import random

st.set_page_config(layout="wide")

# =====================================================
# MELAKARTA RAGA NAMES
# =====================================================

MELAKARTA_NAMES = [
"Kanakangi","Ratnangi","Ganamurti","Vanaspati","Manavati","Tanarupi",
"Senavati","Hanumatodi","Dhenuka","Natakapriya","Kokilapriya","Rupavati",
"Gayakapriya","Vakulabharanam","Mayamalavagowla","Chakravakam","Suryakantam",
"Hatakambari","Jhankaradhwani","Natabhairavi","Keeravani","Kharaharapriya",
"Gourimanohari","Varunapriya","Mararanjani","Charukesi","Sarasangi",
"Harikambhoji","Dheerasankarabharanam","Naganandini","Yagapriya",
"Ragavardhini","Gangeyabhushani","Vagadheeswari","Shulini","Chalanata",
"Salagam","Jalarnavam","Jhalavarali","Navaneetam","Pavani","Raghupriya",
"Gavambodhi","Bhavapriya","Subhapantuvarali","Shadvidamargini","Suvarnangi",
"Divyamani","Dhavalambari","Namanarayani","Kamavardhini","Ramapriya",
"Gamanashrama","Vishwambari","Shamalangi","Shanmukhapriya",
"Simhendramadhyamam","Hemavati","Dharmavati","Neetimati","Kantamani",
"Rishabhapriya","Latangi","Vachaspati","Mechakalyani","Chitrambari",
"Sucharitra","Jyotiswarupini","Dhatuvardhini","Nasikabhushani","Kosalam",
"Rasikapriya"
]

# =====================================================
# SWARA OPTIONS
# =====================================================

R_OPTIONS = ["R1","R1","R1","R1","R2","R2","R2","R2","R3","R3","R3","R3"]
G_OPTIONS = ["G1","G2","G3","G1","G2","G3","G1","G2","G3","G1","G2","G3"]
D_OPTIONS = ["D1","D1","D1","D1","D2","D2","D2","D2","D3","D3","D3","D3"]
N_OPTIONS = ["N1","N2","N3","N1","N2","N3","N1","N2","N3","N1","N2","N3"]

# =====================================================
# RAGA ENGINE
# =====================================================

def generate_72_melakarta():
    ragas = {}
    count = 0
    for m in ["M1","M2"]:
        for i in range(36):
            r = R_OPTIONS[i % 12]
            g = G_OPTIONS[i % 12]
            d = D_OPTIONS[i % 12]
            n = N_OPTIONS[i % 12]

            name = MELAKARTA_NAMES[count]

            aroha = ["S", r, g, m, "P", d, n, "S'"]
            avaroha = ["S'", n, d, "P", m, g, r, "S"]

            ragas[name] = {
                "number": count + 1,
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
# TRANSITION ENGINE
# =====================================================

def raga_similarity(r1, r2):
    s1 = set(RAGAS[r1]["swara_set"])
    s2 = set(RAGAS[r2]["swara_set"])
    shared = len(s1.intersection(s2))
    same_m = 2 if RAGAS[r1]["madhyama"] == RAGAS[r2]["madhyama"] else 0
    return shared + same_m

def suggest_ragas(base_raga):
    scores = {}
    for r in RAGAS:
        if r != base_raga:
            scores[r] = raga_similarity(base_raga, r)
    sorted_ragas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [r[0] for r in sorted_ragas[:3]]

# =====================================================
# SANDHAM ENGINE
# =====================================================

BASE_CLUSTERS = ["தனதன","தத்தன","தானன","தந்தன"]

def generate_sandham(cycles, aksharas):
    total_units = cycles * aksharas
    pattern = random.choices(BASE_CLUSTERS, k=total_units)
    pattern[-1] = "தனதான"
    return " ".join(pattern)

# =====================================================
# MELODY ENGINE
# =====================================================

def generate_melody(raga_name, total_notes):
    swaras = RAGAS[raga_name]["swara_set"]
    melody = [random.choice(swaras) for _ in range(total_notes)]
    melody[-1] = "S"
    return melody

# =====================================================
# UI
# =====================================================

st.title("Carnatic Structured Composer")

with st.sidebar:
    tala_choice = st.selectbox("Tala", list(TALAS.keys()))
    num_sections = st.slider("Number of Sections", 1, 5, 3)

st.subheader("Section Configuration")

sections = []
first_raga = st.selectbox("First Section Raga", list(RAGAS.keys()))

for i in range(num_sections):
    st.markdown(f"### Section {i+1}")
    name = st.text_input(f"Section Name {i+1}", f"Section_{i+1}")
    cycles = st.slider(f"Cycles (Section {i+1})", 1, 4, 2, key=f"cycles{i}")

    if i == 0:
        raga = first_raga
        auto_raga = False
        st.write(f"Raga: {raga} (Fixed)")
    else:
        auto_raga = st.checkbox(f"Auto Raga Suggest (Section {i+1})", True, key=f"auto{i}")
        if auto_raga:
            raga = None
            st.write("Will auto-select based on previous section")
        else:
            raga = st.selectbox(f"Manual Raga (Section {i+1})", list(RAGAS.keys()), key=f"manual{i}")

    sections.append({
        "name": name,
        "raga": raga,
        "cycles": cycles,
        "auto_raga": auto_raga
    })

if st.button("Generate Full Song"):

    prev_raga = first_raga
    aksharas = TALAS[tala_choice]

    for idx, sec in enumerate(sections):

        if idx != 0 and sec["auto_raga"]:
            suggestions = suggest_ragas(prev_raga)
            sec_raga = suggestions[0]
        else:
            sec_raga = sec["raga"]

        sandham = generate_sandham(sec["cycles"], aksharas)
        melody = generate_melody(sec_raga, sec["cycles"] * aksharas)

        st.markdown(f"## {sec['name']}")
        st.write(f"Raga: {sec_raga} (Melakarta {RAGAS[sec_raga]['number']})")
        st.write("Tala:", tala_choice)

        st.subheader("Sandham")
        st.text(sandham)

        st.subheader("Swara Output")
        st.text(" ".join(melody))

        st.subheader("Aroha")
        st.text(" ".join(RAGAS[sec_raga]["aroha"]))

        st.subheader("Avaroha")
        st.text(" ".join(RAGAS[sec_raga]["avaroha"]))

        prev_raga = sec_raga
