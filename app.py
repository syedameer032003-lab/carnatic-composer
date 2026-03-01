import streamlit as st
import random
import json

# ===============================
# LOAD RAGA DATABASE (JSON FILE)
# ===============================

with open("raga_database.json", "r", encoding="utf-8") as f:
    RAGA_DB = json.load(f)

# ===============================
# TALA DATABASE
# ===============================

TALA_DB = {
    "Adi": 8,
    "Rupaka": 6,
    "Misra_Chapu": 7,
    "Khanda_Chapu": 5
}

# ===============================
# ATOMIC SANDHAM CLUSTERS
# ===============================

CLUSTERS = {
    2: ["தன", "தத்"],
    3: ["தனன", "தத்த"],
    4: ["தனதன", "தத்தன", "தானா"],
    5: ["தனதத்த", "தத்ததன"],
    6: ["தனதனன", "தத்ததத்த"]
}

# ===============================
# RAGA PROFILE ENGINE
# ===============================

def raga_profile(raga):

    brightness = 0
    tension = 0
    complexity = 0

    aroha = raga.get("aroha", [])
    janya = raga.get("janya", [])

    for swara in aroha:

        if "M2" in swara:
            brightness += 2
        if "N3" in swara:
            brightness += 1

        if "R1" in swara or "D1" in swara:
            tension += 2
        if "R3" in swara:
            tension += 1

    # Vakra adds rhythmic complexity
    if isinstance(janya, list):
        if any("Vakra" in j for j in janya):
            complexity += 2
    elif "Vakra" in str(janya):
        complexity += 2

    if brightness > tension:
        tonal_bias = "bright"
    elif tension > brightness:
        tonal_bias = "heavy"
    else:
        tonal_bias = "balanced"

    return {
        "tonal_bias": tonal_bias,
        "complexity": complexity
    }

# ===============================
# STRUCTURE DECISION
# ===============================

def decide_structure(motion):

    if motion == "explosive":
        return 2, 4
    if motion == "fall_then_rise":
        return 4, 8
    if motion == "wave":
        return 4, 6
    if motion == "fall":
        return 3, 4

    return 3, 6

def emotional_curve(motion, profile):

    if motion == "gradual_rise":
        base = ["base", "lift", "peak"]
    elif motion == "fall_then_rise":
        base = ["heavy", "relax", "lift", "peak"]
    elif motion == "wave":
        base = ["base", "lift", "relax", "lift", "peak"]
    elif motion == "fall":
        base = ["heavy", "drop"]
    else:
        base = ["base", "lift", "peak"]

    if profile["tonal_bias"] == "bright":
        base.append("peak")

    if profile["tonal_bias"] == "heavy":
        base.insert(0, "heavy")

    return base

# ===============================
# RHYTHM ENGINE
# ===============================

def dynamic_division(total_beats, segments):

    parts = []
    remaining = total_beats

    for i in range(segments - 1):
        min_left = 2 * (segments - i - 1)
        val = random.randint(2, remaining - min_left)
        parts.append(val)
        remaining -= val

    parts.append(remaining)
    return parts

def apply_raga_density(pattern, profile):

    if profile["tonal_bias"] == "bright":
        pattern[-1] += 1

    if profile["tonal_bias"] == "heavy":
        pattern[0] += 1

    if profile["complexity"] > 1 and len(pattern) > 2:
        pattern.insert(1, 2)

    return pattern

def build_sandham(pattern):

    words = []

    for weight in pattern:
        if weight in CLUSTERS:
            words.append(random.choice(CLUSTERS[weight]))
        else:
            nearest = min(CLUSTERS.keys(), key=lambda x: abs(x - weight))
            words.append(random.choice(CLUSTERS[nearest]))

    return " ".join(words)

def generate_section(lines, beats, motion, intensity, profile):

    curve = emotional_curve(motion, profile)
    result = []

    for i in range(lines):

        stage = curve[min(i, len(curve)-1)]
        segments = 3 if stage in ["base", "lift"] else 2

        pattern = dynamic_division(beats, segments)

        if stage == "lift":
            pattern[-1] += 1

        if stage == "peak":
            pattern[-1] += min(2, intensity // 3)

        if stage == "heavy":
            pattern[0] += 1

        pattern = apply_raga_density(pattern, profile)

        result.append(build_sandham(pattern))

    return result

# ===============================
# STREAMLIT UI
# ===============================

st.title("🎼 Carnatic Composition Engine")

raga_names = [r["name"] for r in RAGA_DB]
selected_raga_name = st.selectbox("Select Raga", raga_names)

selected_raga = next(r for r in RAGA_DB if r["name"] == selected_raga_name)

tala_name = st.selectbox("Select Tala", list(TALA_DB.keys()))

motion = st.selectbox(
    "Emotional Motion",
    ["gradual_rise", "fall_then_rise", "wave", "explosive", "fall", "static"]
)

intensity = st.slider("Intensity", 1, 10, 5)

if st.button("Compose"):

    profile = raga_profile(selected_raga)
    beats = TALA_DB[tala_name]

    pallavi_lines, charanam_lines = decide_structure(motion)

    pallavi = generate_section(
        pallavi_lines,
        beats,
        motion,
        intensity,
        profile
    )

    charanam = generate_section(
        charanam_lines,
        beats,
        motion,
        intensity,
        profile
    )

    st.subheader("🎵 Pallavi")
    for line in pallavi:
        st.write(line)

    st.subheader("🎵 Charanam")
    for line in charanam:
        st.write(line)
