import re

def main():
    file_path = 'h:\\05-Physics\\Unit 16\\Unit 16.1\\index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix regeneratePractice to use R instead of practiceRNG
    content = content.replace(
        "const rng = isRandom ? practiceRNG : null;\n      const instance = generateQuestionInstance(template, rng);",
        "const R = isRandom ? Math.floor(Math.random() * 40) + 1 : null;\n      const instance = generateQuestionInstance(template, R);"
    )

    # 1. 16_1_1_q2_celsius_to_kelvin
    content = content.replace(
        "const t = rng ? roundHalfEven(-150 + rng.random() * 550, 2) : values[Math.floor(Math.random() * values.length)];",
        "const t = rng ? roundHalfEven(-150 + (rng * 13.5), 2) : values[Math.floor(Math.random() * values.length)];"
    )

    # 2. 16_1_1_q3_kelvin_to_celsius
    content = content.replace(
        "const T = rng ? roundHalfEven(5 + rng.random() * 600, 2) : values[Math.floor(Math.random() * values.length)];",
        "const T = rng ? roundHalfEven(5 + (rng * 14.2), 2) : values[Math.floor(Math.random() * values.length)];"
    )

    # 3. 16_1_2_q2_metal_specific_heat
    content = content.replace(
        "const m = rng ? roundHalfEven(1.0 + rng.random() * 4.0, 1) : 2.0;\n          const Q = rng ? Math.round(1000 + rng.random() * 9000) : 2500;\n          const T1 = rng ? Math.round(15 + rng.random() * 15) : 25;\n          const dT = rng ? Math.round(10 + rng.random() * 30) : 20;",
        "const m = rng ? roundHalfEven(1.0 + (rng * 0.1), 1) : 2.0;\n          const Q = rng ? Math.round(1000 + (rng * 200)) : 2500;\n          const T1 = rng ? Math.round(15 + (rng % 15)) : 25;\n          const dT = rng ? Math.round(10 + (rng % 30)) : 20;"
    )

    # 4. 16_1_2_q5_pool_heat
    content = content.replace(
        "const m = rng ? (roundHalfEven(0.5 + rng.random() * 2.5, 2) * 1e6) : 1e6;\n          const dT = rng ? Math.round(1 + rng.random() * 4) : 2;",
        "const m = rng ? (roundHalfEven(0.5 + (rng * 0.05), 2) * 1e6) : 1e6;\n          const dT = rng ? Math.round(1 + (rng % 4)) : 2;"
    )

    # 5. 16_1_3_q1_ice_melting_heat
    content = content.replace(
        "const m = rng ? roundHalfEven(0.5 + rng.random() * 9.5, 1) : 2.0;",
        "const m = rng ? roundHalfEven(0.5 + (rng * 0.2), 1) : 2.0;"
    )

    # 6. 16_1_3_q2_ice_to_steam
    content = content.replace(
        "const m = rng ? roundHalfEven(0.1 + rng.random() * 2.9, 2) : 0.5;",
        "const m = rng ? roundHalfEven(0.1 + (rng * 0.07), 2) : 0.5;"
    )

    # 7. 16_1_3_q5_ice_to_steam_full
    content = content.replace(
        "const m = rng ? roundHalfEven(0.5 + rng.random() * 2.5, 1) : 2.0;\n          const T_start = rng ? -Math.round(2 + rng.random() * 18) : -5;",
        "const m = rng ? roundHalfEven(0.5 + (rng * 0.06), 1) : 2.0;\n          const T_start = rng ? -Math.round(2 + (rng % 18)) : -5;"
    )

    # 8. 16_1_4_q3_metal_in_ice_calculation
    content = content.replace(
        "const m1 = rng ? Math.round(100 + rng.random() * 400) : 300;\n          const T_metal = rng ? Math.round(200 + rng.random() * 250) : 400;\n          const m2 = rng ? Math.round(100 + rng.random() * 400) : 300;\n          const T_final = rng ? roundHalfEven(2.0 + rng.random() * 10, 1) : 5.0;",
        "const m1 = rng ? Math.round(100 + (rng * 10)) : 300;\n          const T_metal = rng ? Math.round(200 + (rng * 6)) : 400;\n          const m2 = rng ? Math.round(100 + (rng * 8)) : 300;\n          const T_final = rng ? roundHalfEven(2.0 + (rng * 0.2), 1) : 5.0;"
    )

    # Make sure we don't have any leftover rng.random()
    if 'rng.random()' in content:
        print("WARNING: There are still rng.random() calls in the file!")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("All templates updated to use dynamic R.")

if __name__ == '__main__':
    main()
