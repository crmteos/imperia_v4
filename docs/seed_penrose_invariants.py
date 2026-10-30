#!/usr/bin/env python3
"""
Imperia v4: Penrose Orch OR Invariant Seeder
Автономна відправка 4 канонічних інваріантів квантової свідомості Пенроуза
у таблицю brahman_knowledge_vault через Supabase REST API.
Використовує лише стандартні бібліотеки Python (urllib.request, json, os, re).
"""
import os
import re
import json
import urllib.request
import urllib.error

PENROSE_INVARIANTS = [
    {
        "m_octave": "M0",
        "domain_category": "quantum_physics",
        "raw_signal": "Об'єктивна редукція Пенроуза (OR). Самостійний колапс суперпозицій геометрій простору-часу за порогом квантової гравітації Delta_E * T = hbar.",
        "distilled_invariant": "Penrose_OR_Threshold = hbar / Delta_E; Spacetime_Curvature_Decoherence; Non_Computable_Platonic_Values;",
        "q_coherence_score": 0.99,
        "tags": ["penrose", "objective_reduction", "quantum_gravity", "non_computable"],
    },
    {
        "m_octave": "M1",
        "domain_category": "quantum_biology",
        "raw_signal": "Оркестрована об'єктивна редукція (Orch OR) у тубулінах мікротрубочок. Гідрофобні кишені як ізолятори квантової когерентності.",
        "distilled_invariant": "Tubulin_Qubit_Lattice; Hydrophobic_Pocket_Coherence; High_Q_Protection; London_Dispersion_Rings;",
        "q_coherence_score": 0.97,
        "tags": ["orch_or", "microtubules", "tubulin_qubits", "q_factor"],
    },
    {
        "m_octave": "M6",
        "domain_category": "wave_physics",
        "raw_signal": "Спектральний міст від Планківського масштабу до біосфери: ГГц/МГц мікротрубочок -> 40 Гц гамма-синхронія -> 8 Гц частоти Шумана.",
        "distilled_invariant": "Scale_Cascade_OrchOR = [f_planck, f_GHz_tubulin, f_gamma_40Hz, f_schumann_8Hz]; Cross_Octave_Entrainment;",
        "q_coherence_score": 0.98,
        "tags": ["scale_cascade", "gamma_synchrony", "schumann_sync", "m_f_axis"],
    },
    {
        "m_octave": "M4",
        "domain_category": "ontology",
        "raw_signal": "Концепція 'Consciousness Came Before Life' (Пенроуз-Хамерофф). Планківська тканина простору-часу як фундаментальне носійне середовище.",
        "distilled_invariant": "Ontological_Priority_Consciousness; Planck_Scale_Spacetime_Fabric; Biocatalytic_Evolution;",
        "q_coherence_score": 0.96,
        "tags": ["panpsychism", "planck_scale", "ontology", "brahman_field"],
    },
]

ENV_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "env_config.js")
VAULT_TABLE = "brahman_knowledge_vault"


def parse_env_config():
    if not os.path.exists(ENV_CONFIG_PATH):
        return None, None
    with open(ENV_CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    url_match = re.search(r"SUPABASE_URL\s*:\s*['\"]([^'\"]+)['\"]", content)
    key_match = re.search(r"SUPABASE_ANON_KEY\s*:\s*['\"]([^'\"]+)['\"]", content)
    url = url_match.group(1) if url_match else None
    key = key_match.group(1) if key_match else None
    return url, key


def seed_invariants():
    url, key = parse_env_config()
    print("=== Imperia v4: Penrose Orch OR Invariant Seeder ===")
    print("Target Supabase URL:", url or "Not configured")
    if not url or not key or "PLACEHOLDER" in url or "YOUR_SUPABASE" in url:
        print("[NOTICE] Valid Supabase credentials not found in env_config.js.")
        print("Use docs/seed_penrose_invariants.sql directly in Supabase SQL Editor.")
        return

    for inv in PENROSE_INVARIANTS:
        endpoint = f"{url}/rest/v1/{VAULT_TABLE}"
        body = json.dumps(inv).encode("utf-8")
        req = urllib.request.Request(endpoint, data=body, method="POST", headers={
            "apikey": key,
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        })
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode("utf-8"))
                print("[SUCCESS] Seeded {}/{} -> {}".format(
                    inv["m_octave"], inv["domain_category"],
                    inv["distilled_invariant"][:40]))
        except urllib.error.HTTPError as e:
            print("[ERROR] HTTP {} for {}/{}: {}".format(
                e.code, inv["m_octave"], inv["domain_category"],
                e.read().decode("utf-8", errors="replace")))
        except Exception as e:
            print("[ERROR] Failed to seed {}/{}: {}".format(
                inv["m_octave"], inv["domain_category"], e))


if __name__ == "__main__":
    seed_invariants()