import json
import random
import os
from config import DEFAULT_SIGNATURE, DEFAULT_ENTROPY
from memory_engine import update, penalty, boost

BASE_PATH = os.path.dirname(__file__)

def load_json(filename):
    with open(os.path.join(BASE_PATH, filename), encoding="utf-8") as f:
        return json.load(f)

RAGA_DB = load_json("raga_database.json")
CHUNKS = load_json("chunks.json")

TALA_DB = {
    "Adi": 8,
    "Rupaka": 6,
    "MisraChap": 7
}

# -------------------------
# Emotion Resolver
# -------------------------

FAMILY_KEYWORDS = {
    "romantic": ["love", "affection", "heart"],
    "tragic": ["sad", "loss", "grief"],
    "heroic": ["victory", "battle", "rise"],
    "tension": ["rage", "anger", "fear"],
    "calm": ["peace", "serene"],
    "celebration": ["joy", "festival"]
}

def resolve_emotion(emotion):
    e = emotion.lower()
    for family, words in FAMILY_KEYWORDS.items():
        for w in words:
            if w in e:
                return family
    return "romantic"

# -------------------------
# Raga Profile
# -------------------------

def raga_profile(raga_id):
    raga = RAGA_DB["melakarta"].get(str(raga_id))
    if not raga:
        return {"type": "neutral"}

    aroha = raga["aroha"]

    if "N3" in aroha:
        return {"type": "bright"}
    if "R1" in aroha:
        return {"type": "heavy"}

    return {"type": "soft"}

# -------------------------
# Structure
# -------------------------

def decide_structure():
    return {"pallavi": 2, "charanam": 4}

def dynamic_division(beats):
    divisions = []
    remaining = beats
    while remaining > 0:
        split = random.randint(2, min(4, remaining))
        divisions.append(split)
        remaining -= split
    return divisions

# -------------------------
# Build Line
# -------------------------

def build_line(pattern, entropy):
    line = []

    for beat_group in pattern:
        candidates = CHUNKS.get(str(beat_group), [])
        if not candidates:
            continue

        weighted = []

        for c in candidates:
            base = penalty("chunk_usage", c["text"], entropy)
            pref = boost("chunk_preference", c["text"])
            weight = base * pref
            weighted.append((c["text"], weight))

        total = sum(w for _, w in weighted)
        r = random.uniform(0, total)
        upto = 0

        chosen = weighted[0][0]

        for text, weight in weighted:
            if upto + weight >= r:
                chosen = text
                break
            upto += weight

        update("chunk_usage", chosen)
        line.append(chosen)

    return " ".join(line)

# -------------------------
# Main Composer
# -------------------------

def compose_song(
    emotion,
    raga_id,
    tala_name,
    signature=DEFAULT_SIGNATURE,
    entropy=DEFAULT_ENTROPY
):

    family = resolve_emotion(emotion)
    raga = raga_profile(raga_id)
    beats = TALA_DB.get(tala_name, 8)

    structure = decide_structure()

    pallavi = []
    charanam = []

    for _ in range(structure["pallavi"]):
        pattern = dynamic_division(beats)
        line = build_line(pattern, entropy)
        pallavi.append(line)

    for _ in range(structure["charanam"]):
        pattern = dynamic_division(beats)
        line = build_line(pattern, entropy)
        charanam.append(line)

    return {
        "emotion": emotion,
        "family": family,
        "raga_type": raga["type"],
        "structure": {
            "pallavi": pallavi,
            "charanam": charanam
        }
    }
