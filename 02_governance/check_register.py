#!/usr/bin/env python3
"""Checks risk_register.csv: score = likelihood x impact, and bands match the scoring method.
Run from the repository root:  python 02_governance/check_register.py
Uses only the Python standard library."""
import csv
from pathlib import Path

PATH = Path(__file__).resolve().parent / "risk_register.csv"

def band(score):
    if score <= 4:
        return "Low"
    if score <= 9:
        return "Medium"
    if score <= 16:
        return "High"
    return "Critical"          # 20-25 on a 5x5 scale (17-19 cannot occur)

errors = 0
with open(PATH, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for r in rows:
    for prefix in ("initial", "residual"):
        l = int(r[f"{prefix}_likelihood"]); i = int(r[f"{prefix}_impact"]); s = int(r[f"{prefix}_score"])
        if not (1 <= l <= 5 and 1 <= i <= 5):
            print(f"{r['id']} {prefix}: likelihood/impact out of 1-5 range"); errors += 1
        if l * i != s:
            print(f"{r['id']} {prefix}: {l} x {i} = {l*i}, but file says {s}"); errors += 1
        if band(s) != r[f"{prefix}_band"]:
            print(f"{r['id']} {prefix}: band should be {band(s)}, file says {r[f'{prefix}_band']}"); errors += 1

print(f"Checked {len(rows)} risks.")
print("OK: all scores and bands are consistent." if errors == 0 else f"{errors} problem(s) found.")
print("\nResidual High/Critical risks:", ", ".join(r["id"] for r in rows if r["residual_band"] in ("High", "Critical")))
