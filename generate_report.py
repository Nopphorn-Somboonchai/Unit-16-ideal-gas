import math

def js_round(val):
    # Matches JavaScript Math.round(): floor(x + 0.5)
    return math.floor(val + 0.5)

def format_js_float(val):
    # Replicates JS .toString() for floats
    if val % 1 == 0:
        return str(int(val))
    else:
        # Standard float string
        return str(val)

def run_tests_for_r(R):
    results = []

    # 1. 16_2_2_boyle
    V1_boyle = 10 + (R % 20)
    P1_boyle = 1.0
    P2_boyle = 2 + (R % 3)
    V2_boyle = (P1_boyle * V1_boyle) / P2_boyle
    results.append({
        "id": "16_2_2_boyle",
        "params": f"V1 = {V1_boyle}, P1 = {P1_boyle}, P2 = {P2_boyle}",
        "answers": [f"{V2_boyle:.1f}", str(js_round(V2_boyle))]
    })

    # 2. 16_2_2_charles
    V1_charles = 2 + (R % 5)
    t1_charles = 27
    t2_charles = 127
    T1_charles = t1_charles + 273
    T2_charles = t2_charles + 273
    V2_charles = (V1_charles / T1_charles) * T2_charles
    results.append({
        "id": "16_2_2_charles",
        "params": f"V1 = {V1_charles}, t1 = {t1_charles}, t2 = {t2_charles}",
        "answers": [f"{V2_charles:.1f}", f"{V2_charles:.2f}"]
    })

    # 3. 16_2_2_combined
    V1_comb = 10
    P1_comb = 2
    V2_comb = 15 + (R % 10)
    P2_comb = (P1_comb * V1_comb * 600) / (300 * V2_comb)
    results.append({
        "id": "16_2_2_combined",
        "params": f"V1 = {V1_comb}, P1 = {P1_comb}, V2 = {V2_comb}",
        "answers": [f"{P2_comb:.1f}", format_js_float(P2_comb)]
    })

    # 4. 16_2_3_ideal1
    n_ideal1 = 2 + (R % 4)
    T_ideal1 = 300
    P_ideal1 = 1.0e5
    V_ideal1 = (n_ideal1 * 8.31 * T_ideal1) / P_ideal1
    results.append({
        "id": "16_2_3_ideal1",
        "params": f"n = {n_ideal1}, T = {T_ideal1}, P = {P_ideal1}",
        "answers": [f"{V_ideal1:.3f}", f"{V_ideal1:.4f}"]
    })

    # 5. 16_2_3_ideal2_N
    V_ideal2 = 2.0
    P_ideal2 = 1.0
    N_full = (P_ideal2 * 1e5 * V_ideal2 * 1e-3) / (1.38e-23 * 300)
    N_coeff = N_full / 1e22
    results.append({
        "id": "16_2_3_ideal2_N",
        "params": f"V = {V_ideal2}, P = {P_ideal2}",
        "answers": [f"{N_coeff:.1f}", f"{N_coeff:.2f}"]
    })

    # 6. 16_2_4_mol_mass
    n_mol = 1 + (R % 5)
    m_mol = n_mol * 32
    results.append({
        "id": "16_2_4_mol_mass",
        "params": f"n = {n_mol}",
        "answers": [str(m_mol)]
    })

    return results

def main():
    rolls = [1, 15, 40]
    md = "# Dynamic Quiz Verification Results (Unit 16.2 Ideal Gas)\n\n"
    md += "This report verifies the dynamically generated questions and their correct answers for students with Roll Numbers 1, 15, and 40 in Unit 16.2 Ideal Gas.\n\n"
    
    for r in rolls:
        md += f"## Roll Number (R) = {r}\n"
        md += "| Question ID | Generated Parameters | Computed Expected Answer |\n"
        md += "|---|---|---|\n"
        results = run_tests_for_r(r)
        for res in results:
            answers_str = " , ".join(res['answers'])
            md += f"| `{res['id']}` | `{res['params']}` | `{answers_str}` |\n"
        md += "\n"
        
    with open('exam_verification.md', 'w', encoding='utf-8') as f:
        f.write(md)
    print("exam_verification.md created")

if __name__ == '__main__':
    main()
