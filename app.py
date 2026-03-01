from composer_engine import compose_song
import json

# ======================================
# LOAD RAGA NAMES
# ======================================

with open("raga_database.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

RAGA_NAMES = [
    data["name"]
    for _, data in raw_data["melakarta"].items()
]

# ======================================
# SIMPLE CLI INTERFACE
# ======================================

def main():

    print("\n🎼 Carnatic Composition Engine\n")

    print("Available Ragas:")
    for i, raga in enumerate(RAGA_NAMES, start=1):
        print(f"{i}. {raga}")

    raga_choice = int(input("\nSelect Raga Number: "))
    raga_name = RAGA_NAMES[raga_choice - 1]

    print("\nAvailable Talas:")
    print("1. Adi")
    print("2. Rupaka")
    print("3. Misra_Chapu")
    print("4. Khanda_Chapu")

    tala_map = {
        1: "Adi",
        2: "Rupaka",
        3: "Misra_Chapu",
        4: "Khanda_Chapu"
    }

    tala_choice = int(input("\nSelect Tala Number: "))
    tala_name = tala_map[tala_choice]

    print("\nMotion Types:")
    print("1. gradual_rise")
    print("2. fall_then_rise")
    print("3. explosive")
    print("4. wave")
    print("5. fall")
    print("6. static")

    motion_map = {
        1: "gradual_rise",
        2: "fall_then_rise",
        3: "explosive",
        4: "wave",
        5: "fall",
        6: "static"
    }

    motion_choice = int(input("\nSelect Motion Number: "))
    motion = motion_map[motion_choice]

    intensity = int(input("\nEnter Intensity (1-10): "))

    print("\nLine Bias:")
    print("1. even")
    print("2. odd")
    print("3. adaptive")

    bias_map = {
        1: "even",
        2: "odd",
        3: "adaptive"
    }

    bias_choice = int(input("\nSelect Bias Number: "))
    line_bias = bias_map[bias_choice]

    # Compose
    song = compose_song(
        polarity="positive",
        motion=motion,
        intensity=intensity,
        raga_name=raga_name,
        tala_name=tala_name,
        line_bias=line_bias
    )

    print("\n🎵 PALLAVI:\n")
    for line in song["pallavi"]:
        print(line)

    print("\n🎵 CHARANAM:\n")
    for line in song["charanam"]:
        print(line)


if __name__ == "__main__":
    main()
