#!/usr/bin/env python3
"""
ETL Script: Global H3 Territory Passport Generation
Generates global database of territory passports based on H3 indices.
"""
import json, csv, math, os

H3_GLOBAL_HUBS = {
    "872b101ffffff": {"name": "Kyiv Central Hub", "country": "UA", "macro_region": "Eastern Europe"},
    "872b101ffff": {"name": "Lviv Western Hub", "country": "UA", "macro_region": "Western Europe"},
    "872b102ffffff": {"name": "Odesa Port Cluster", "country": "UA", "macro_region": "Maritime East"},
    "872b103ffffff": {"name": "Kharkiv Eastern Hub", "country": "UA", "macro_region": "Eastern Europe"},
    "872b104ffffff": {"name": "Dnipro Central Cluster", "country": "UA", "macro_region": "Industrial East"},
    "8829b52001fffff": {"name": "Tokyo Eastern Gateway", "country": "JP", "macro_region": "East Asia"},
    "850b5a0ffffffff": {"name": "London Financial Hub", "country": "GB", "macro_region": "Western Europe"},
    "850b6e0ffffffff": {"name": "New York Global Node", "country": "US", "macro_region": "North America"},
}
def compute_q_node(lat, lng, base_q=0.90, jitter_amount=0.08):
    """
    Compute Q-node coherence metric in [0.00, 1.00].
    Base Q depends on macro-region importance; jitter adds controlled noise.
    """
    jitter = (math.sin(lat * 1000) * 0.01 + math.cos(lng * 1000) * 0.01) * jitter_amount
    q = base_q - abs(jitter)
    return round(max(0.0, min(1.0, q)), 2)


def compute_E_tensor(q_node, warna_class):
    """
    Compute 4D environment tensor E = [E_lang, E_geo, E_hist, E_soc]^T.
    Values in [0.0, 1.0], normalized by Q-factor and warna class.
    """
    base_tensors = {
        "Brahman":    [0.95 * q_node, 0.91 * q_node, 0.98 * q_node, 0.89 * q_node],
        "Kshatriya":  [0.82 * q_node, 0.95 * q_node, 0.88 * q_node, 0.78 * q_node],
        "Vaishya":    [0.85 * q_node, 0.92 * q_node, 0.90 * q_node, 0.88 * q_node],
        "Shudra":     [0.88 * q_node, 0.85 * q_node, 0.92 * q_node, 0.90 * q_node],
    }
    tensor = base_tensors.get(warna_class, [0.80 * q_node] * 4)
    for i in range(4):
        jitter = round((math.sin(i * 37 + int(q_node * 100)) % 1 - 0.5) * 0.1, 3)
        tensor[i] = round(max(0.0, min(1.0, tensor[i] + jitter)), 3)
    return tensor


def compute_warna_class(q_node, E_tensor):
    """
    Determine warna_class based on Q-node and E-tensor profiles.
    """
    e_lang, e_geo, e_hist, e_soc = E_tensor
    max_e = max(e_lang, e_geo, e_hist, e_soc)

    if max_e >= 0.90 and q_node >= 0.88:
        return "Brahman"
    elif e_lang >= 0.85 and e_geo >= 0.85:
        return "Kshatriya"
    elif e_hist >= 0.85 and e_soc >= 0.80:
        return "Vaishya"
    else:
        return "Shudra"


def compute_jitterbug_state(E_tensor, q_node):
    """
    Determine jitterbug state based on E-tensor geometry and Q coherence.
    """
    e_lang, e_geo, e_hist, e_soc = E_tensor
    mean_e = (e_lang + e_geo + e_hist + e_soc) / 4
    if mean_e == 0:
        return "Tetrahedron"
    variations = [abs(e - mean_e) for e in E_tensor]
    avg_variation = sum(variations) / 4
    if avg_variation < 0.12:
        return "Cuboctahedron"
    elif q_node > 0.85:
        return "Cuboctahedron"
    else:
        return "Tetrahedron"


def h3_roll_up_algorithm(passports_data, target_resolution=7):
    """
    H3 Roll-Up Algorithm: Compute weighted averages from finer to coarser resolutions.
    """
    rolled_up = {}
    for h3_index, passport in passports_data.items():
        try:
            prefix = h3_index[:4] if len(h3_index) >= 4 else h3_index
            if prefix not in rolled_up:
                rolled_up[prefix] = {
                    "q_factors": [], "E_tensors": [], "jitters": [],
                    "warna_classes": [], "jitterbug_states": [],
                    "count": 0, "h3_indices": [],
                }
            rolled_up[prefix]["q_factors"].append(passport.get("q_factor", 0.5))
            rolled_up[prefix]["E_tensors"].append(passport.get("E_tensor", [0.5, 0.5, 0.5, 0.5]))
            rolled_up[prefix]["jitters"].append(passport.get("jitter", 0.05))
            rolled_up[prefix]["warna_classes"].append(passport.get("warna_class", "Shudra"))
            rolled_up[prefix]["jitterbug_states"].append(passport.get("jitterbug_state", "Tetrahedron"))
            rolled_up[prefix]["count"] += 1
            rolled_up[prefix]["h3_indices"].append(h3_index)
        except Exception:
            continue

    result = {}
    for prefix, group in rolled_up.items():
        q_weights = group["q_factors"]
        total_weight = sum(q_weights) if q_weights else 1
        E_sum = [0, 0, 0, 0]
        for E_group in group["E_tensors"]:
            for i in range(4):
                E_sum[i] += E_group[i] / total_weight if total_weight > 0 else 0
        warna_counts = {}
        for wc in group["warna_classes"]:
            warna_counts[wc] = warna_counts.get(wc, 0) + 1
        dominant_warna = max(warna_counts, key=warna_counts.get) if warna_counts else "Shudra"
        jitterbug_counts = {}
        for jb in group["jitterbug_states"]:
            jitterbug_counts[jb] = jitterbug_counts.get(jb, 0) + 1
        dominant_jitterbug = max(jitterbug_counts, key=jitterbug_counts.get) if jitterbug_counts else "Tetrahedron"
        avg_jitter = sum(group["jitters"]) / len(group["jitters"]) if group["jitters"] else 0.0

        result[prefix] = {
            "q_factor": round(sum(q_weights) / len(q_weights), 2) if q_weights else 0.5,
            "E_tensor": [round(v, 3) for v in E_sum],
            "warna_class": dominant_warna,
            "jitterbug_state": dominant_jitterbug,
            "avg_jitter": round(avg_jitter, 3),
            "h3_indices": group["h3_indices"][:8],
            "count": group["count"],
            "resolution": 7,
            "roll_up_from": "resolutions 8-8 (fine-grain aggregated)",
        }
    return result


def main():
    print("=" * 60)
    print("Imperia v4 Global H3 Territory Passport ETL Pipeline")
    print("=" * 60)

    passports_data = {}
    csv_rows = []

    print("\n[1/3] Generating global H3 territory passports...")
    import random
    for h3_index, hub_info in H3_GLOBAL_HUBS.items():
        lat = hub_info.get("lat", 50.0)
        lng = hub_info.get("lng", 30.0)
        country = hub_info["country"]
        macro_region = hub_info["macro_region"]

        q_node = compute_q_node(lat, lng)

        # Estimate warna class for E tensor computation
        warna_class = compute_warna_class(q_node, [0.8, 0.8, 0.8, 0.8])
        E_tensor = compute_E_tensor(q_node, warna_class)
        jitterbug_state = compute_jitterbug_state(E_tensor, q_node)
        jitter = round(random.random() * 0.05, 3)

        passport = {
            "h3_index": h3_index,
            "name": hub_info["name"],
            "country": country,
            "macro_region": macro_region,
            "q_factor": q_node,
            "E_tensor": E_tensor,
            "jitter": jitter,
            "warna_class": warna_class,
            "jitterbug_state": jitterbug_state,
        }

        passports_data[h3_index] = passport
        csv_rows.append({
            "h3_index": h3_index,
            "name": hub_info["name"],
            "country": country,
            "macro_region": macro_region,
            "q_factor": q_node,
            "E_lang": E_tensor[0],
            "E_geo": E_tensor[1],
            "E_hist": E_tensor[2],
            "E_soc": E_tensor[3],
            "jitter": jitter,
            "warna_class": warna_class,
            "jitterbug_state": jitterbug_state,
        })

    print("\n[2/3] Applying H3 Roll-Up algorithm...")
    rolled_up = h3_roll_up_algorithm(passports_data, target_resolution=7)

    for prefix, rollup in rolled_up.items():
        passports_data[prefix] = rollup
        csv_rows.append({
            "h3_index": prefix,
            "name": f"Roll-Up Group {prefix}",
            "country": "Aggregated",
            "macro_region": macro_region,
            "q_factor": rollup["q_factor"],
            "E_lang": rollup["E_tensor"][0],
            "E_geo": rollup["E_tensor"][1],
            "E_hist": rollup["E_tensor"][2],
            "E_soc": rollup["E_tensor"][3],
            "jitter": rollup["avg_jitter"],
            "warna_class": rollup["warna_class"],
            "jitterbug_state": rollup["jitterbug_state"],
        })

    print("\n[3/3] Saving output files...")
    os.makedirs("docs", exist_ok=True)

    json_output = {
        "system_version": "3.0.0-global-h3-etl",
        "data_source": "OpenStreetMap / Uber H3 Spatial Layer Engine - Global",
        "binding_logic": "Mapping core Q-telemetry and 4D E-tensors to native map feature IDs",
        "h3_layer_passports": passports_data,
        "roll_up_aggregations": rolled_up,
        "generation_info": {
            "total_passports": len(passports_data),
            "global_hubs": len(H3_GLOBAL_HUBS),
            "roll_up_groups": len(rolled_up),
            "metrics": ["Q_factor", "E_tensor_4D", "jitter", "warna_class", "jitterbug_state"],
        }
    }

    with open("docs/territory_passports.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Written: docs/territory_passports.json ({len(passports_data)} passports)")

    csv_fieldnames = [
        "h3_index", "name", "country", "macro_region",
        "q_factor", "E_lang", "E_geo", "E_hist", "E_soc",
        "jitter", "warna_class", "jitterbug_state"
    ]
    with open("docs/territory_passports.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"  ✅ Written: docs/territory_passports.csv ({len(csv_rows)} rows)")

    print("\n" + "=" * 60)
    print("ETL Pipeline Complete!")
    print("=" * 60)
    print(f"\nGenerated {len(passports_data)} global territory passports")
    print(f"  JSON: docs/territory_passports.json")
    print(f"  CSV:  docs/territory_passports.csv")
    print(f"\nH3 Roll-Up groups: {len(rolled_up)} aggregated resolutions")
    print("\nCanonical metrics computed per passport:")
    print("  • Q_node in [0.00, 1.00] - Dobrotnist/Coherence")
    print("  • E = [E_lang, E_geo, E_hist, E_soc]^T - 4D tensor srodovyshcha")
    print("  • jitter - Deviation/ noi\u0441utvorennya")
    print("  • warna_class - Brahman / Kshatriya / Vaishya / Shudra")
    print("  • jitterbug_state - Tetrahedron / Cuboctahedron")


if __name__ == "__main__":
    main()