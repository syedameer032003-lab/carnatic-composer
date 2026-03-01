import random
import json

# ======================================
# LOAD RAGA DATABASE (YOUR STRUCTURE)
# ======================================

with open("raga_database.json", "r", encoding="utf-8") as f:
    RAW_RAGA_DATA = json.load(f)

# Flatten melakarta structure
RAGA_DB = {}

for mela_no, data in RAW_RAGA_DATA["melakarta"].items():
    name = data["name"]
    RAGA_DB[name] = {
        "aroha": data["aroha"],
        "avaroha": data["avaroha"],
        "chakra": data["chakra"],
        "mela_number": mela_no
    }

# ======================================
# TALA DATABASE
# ======================================

TALA_DB = {
    "Adi": 8,
    "Rupaka": 6,
    "Misra_Chapu": 7,
    "Khanda_Chapu": 5
}

# ======================================
# ATOMIC SANDHAM CLUSTERS
# ======================================

CLUSTERS = {
    2: ["தன", "தத்", "தா"],
    3: ["தனன", "தத்த", "தய்ய"],
    4: ["தனதன", "தத்தன", "தானா"],
    5: ["தனதத்த", "தத்ததன"],
    6: ["தனதனன", "தத்ததத்த"]
}

# ======================================
# RAGA EMOTION PROFILE
# ======================================

def raga_emotion_profile(raga_data):

    scale = raga_data["aroha"]

    brightness = 0
    tension = 0

    for swara in scale:
        if "M2" in swara or "N3" in swara:
            brightness += 1
        if "R1" in swara or "D1" in swara:
            tension += 1

    if brightness > tension:
        tonal_bias = "bright"
    elif tension > brightness:
        tonal_bias = "heavy"
    else:
        tonal_bias = "balanced"

    return {
        "brightness": brightness,
        "tension": tension,
        "tonal_bias": tonal_bias
    }

# ======================================
# STRUCTURE DECISION
# ======================================

def decide_structure(polarity, motion, intensity, line_bias):

    if motion == "explosive":
        pallavi = 2
        charanam = 4

    elif motion == "fall_then_rise":
        pallavi = 4
        charanam = 8

    elif motion == "wave":
        pallavi = 4
        charanam = 6

    elif motion == "fall":
        pallavi = 3
        charanam = 4

    else:
        pallavi = 3
        charanam = 6

    if line_bias == "even":
        if pallavi % 2 != 0:
            pallavi += 1
        if charanam % 2 != 0:
            charanam += 1

    elif line_bias == "odd":
        if pallavi % 2 == 0:
            pallavi += 1
        if charanam % 2 == 0:
            charanam += 1

    elif line_bias == "adaptive":
        if motion in ["gradual_rise", "wave"] and intensity > 6:
            if pallavi % 2 == 0:
                pallavi += 1

    return {"pallavi": pallavi, "charanam": charanam}

# ======================================
# EMOTIONAL CURVE
# ======================================

def emotional_curve(motion, raga_profile):

    if motion == "gradual_rise":
        curve = ["base", "lift", "peak"]

    elif motion == "explosive":
        curve = ["peak", "stabilize"]

    elif motion == "fall_then_rise":
        curve = ["heavy", "relax", "lift", "peak"]

    elif motion == "wave":
        curve = ["base", "lift", "relax", "lift", "peak"]

    elif motion == "fall":
        curve = ["heavy", "drop"]

    else:
        curve = ["base", "lift", "peak"]

    if raga_profile["tonal_bias"] == "bright":
        curve.append("peak")

    if raga_profile["tonal_bias"] == "heavy":
        curve.insert(0, "heavy")

    return curve

# ======================================
# DYNAMIC BEAT DIVISION
# ======================================

def dynamic_division(total_beats, segments):

    divisions = []
    remaining = total_beats

    for i in range(segments - 1):
        min_required = 2 * (segments - i - 1)
        val = random.randint(2, remaining - min_required)
        divisions.append(val)
        remaining -= val

    divisions.append(remaining)
    return divisions

# ======================================
# RAGA DENSITY MODIFIER
# ======================================

def raga_density_modifier(pattern, raga_profile):

    if raga_profile["tonal_bias"] == "bright":
        pattern[-1] += 1

    if raga_profile["tonal_bias"] == "heavy":
        pattern[0] += 1

    return pattern

# ======================================
# OPTIONAL SPILL
# ======================================

def apply_spill(pattern, probability):

    if random.random() < probability:
        pattern[-1] += 1

    return pattern

# ======================================
# BUILD SANDHAM
# ======================================

def build_sandham(pattern):

    line = []

    for weight in pattern:
        options = CLUSTERS.get(weight)

        if not options:
            closest = min(CLUSTERS.keys(), key=lambda x: abs(x - weight))
            options = CLUSTERS[closest]

        line.append(random.choice(options))

    return " ".join(line)

# ======================================
# SECTION GENERATOR
# ======================================

def generate_section(line_count,
                     total_beats,
                     motion,
                     intensity,
                     raga_profile,
                     spill_probability):

    curve = emotional_curve(motion, raga_profile)
    section = []

    for i in range(line_count):

        stage = curve[min(i, len(curve) - 1)]

        segments = 3 if stage in ["base", "lift"] else 2
        pattern = dynamic_division(total_beats, segments)

        if stage == "lift":
            pattern[-1] += 1

        elif stage == "peak":
            pattern[-1] += min(2, intensity // 3)

        elif stage == "heavy":
            pattern[0] += 1

        elif stage == "relax":
            if pattern[-1] > 2:
                pattern[-1] -= 1

        pattern = raga_density_modifier(pattern, raga_profile)
        pattern = apply_spill(pattern, spill_probability)

        section.append(build_sandham(pattern))

    return section

# ======================================
# MASTER COMPOSE FUNCTION
# ======================================

def compose_song(polarity,
                 motion,
                 intensity,
                 raga_name,
                 tala_name,
                 line_bias="adaptive",
                 spill_probability=0.1):

    raga_data = RAGA_DB[raga_name]
    tala_beats = TALA_DB[tala_name]

    raga_profile = raga_emotion_profile(raga_data)

    structure = decide_structure(
        polarity,
        motion,
        intensity,
        line_bias
    )

    pallavi = generate_section(
        structure["pallavi"],
        tala_beats,
        motion,
        intensity,
        raga_profile,
        spill_probability
    )

    charanam = generate_section(
        structure["charanam"],
        tala_beats,
        motion,
        intensity,
        raga_profile,
        spill_probability
    )

    return {
        "pallavi": pallavi,
        "charanam": charanam
    }
