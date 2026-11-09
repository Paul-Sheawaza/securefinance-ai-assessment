#!/usr/bin/env python3
"""
AICS-201 Assessment 01 - Task 4: Algorithmic fairness and explainability
Fictional organisation: SecureFinance Africa (fraud-detection module)

What this script does (all data is SYNTHETIC; no real customer records):
  1. Builds the 80-record synthetic dataset from a documented pattern-count table.
  2. Applies a transparent weighted screening rule (integer arithmetic).
  3. Computes confusion matrices and fairness measures per group.
  4. Quantifies uncertainty (stratified bootstrap + Fisher exact test).
  5. Reviews individual decisions exactly (feature contributions, counterfactuals)
     and measures how much each group's flags depend on one feature.
  6. Compares three candidate corrections across ALL relevant outcomes.
  7. Writes CSV/TXT results and a chart.

Run from the repository root:   python src/fairness_analysis.py
Only numpy, pandas and matplotlib are required. Fairlearn is used for an
optional cross-check if it happens to be installed.
"""
import json
import math
import platform
from itertools import product
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
SEED = 42
N_BOOT = 10_000

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RES_DIR = ROOT / "results"
FIG_DIR = ROOT / "figures"
for d in (DATA_DIR, RES_DIR, FIG_DIR):
    d.mkdir(exist_ok=True)

FEATURES = ["unusual_velocity", "device_anomaly", "limited_history"]

# Screening rule in HUNDREDTHS so comparisons are exact integers (no float error):
#   score = 40*V + 35*D + 25*H   -> flag if score >= 50   (i.e. 0.40, 0.35, 0.25, 0.50)
BASELINE = {"weights": {"unusual_velocity": 40, "device_anomaly": 35, "limited_history": 25},
            "threshold": 50}

# Pattern-count table that DEFINES the synthetic dataset.
# Key: (group, actual_fraud). Value: {(V, D, H): number_of_records}.
# Each (group, label) cell holds exactly 20 records. Groups are fictional audit groups.
SPEC = {
    ("A", 1): {(1, 1, 0): 6, (1, 1, 1): 6, (0, 1, 1): 3, (1, 0, 1): 3, (0, 1, 0): 1, (1, 0, 0): 1},
    ("A", 0): {(0, 1, 1): 1, (1, 0, 1): 1, (1, 1, 0): 2, (0, 0, 1): 2, (0, 0, 0): 8, (0, 1, 0): 3, (1, 0, 0): 3},
    ("B", 1): {(1, 1, 0): 5, (1, 1, 1): 5, (0, 1, 1): 3, (1, 0, 1): 3, (0, 0, 1): 1, (0, 1, 0): 1, (1, 0, 0): 1, (0, 0, 0): 1},
    ("B", 0): {(0, 1, 1): 5, (1, 0, 1): 3, (0, 0, 1): 4, (0, 0, 0): 4, (0, 1, 0): 2, (1, 0, 0): 2},
}

# Expected baseline confusion counts (sanity check on the construction).
EXPECTED = {"A": dict(tp=18, fn=2, fp=4, tn=16), "B": dict(tp=16, fn=4, fp=8, tn=12)}

LOG = []


def out(text=""):
    print(text)
    LOG.append(str(text))


# --------------------------------------------------------------------------
# 1. Dataset
# --------------------------------------------------------------------------
def build_dataset():
    rows = []
    for group in ("A", "B"):
        counter = 0
        for fraud in (1, 0):                       # records 001-020 fraud, 021-040 legitimate
            for pattern, n in SPEC[(group, fraud)].items():
                for _ in range(n):
                    counter += 1
                    v, d, h = pattern
                    rows.append({"record_id": f"{group}{counter:03d}", "group": group,
                                 "unusual_velocity": v, "device_anomaly": d,
                                 "limited_history": h, "actual_fraud": fraud})
    return pd.DataFrame(rows)


def apply_rule(df, weights, threshold):
    score = sum(df[f] * w for f, w in weights.items())     # integer hundredths
    return score, (score >= threshold).astype(int)


# --------------------------------------------------------------------------
# 2. Metrics
# --------------------------------------------------------------------------
def safe_div(a, b):
    return float("nan") if b == 0 else a / b


def group_metrics(df, flag_col):
    rows = []
    for g, sub in df.groupby("group"):
        tp = int(((sub[flag_col] == 1) & (sub.actual_fraud == 1)).sum())
        fn = int(((sub[flag_col] == 0) & (sub.actual_fraud == 1)).sum())
        fp = int(((sub[flag_col] == 1) & (sub.actual_fraud == 0)).sum())
        tn = int(((sub[flag_col] == 0) & (sub.actual_fraud == 0)).sum())
        n = len(sub)
        rows.append({"group": g, "n": n, "tp": tp, "fn": fn, "fp": fp, "tn": tn,
                     "fpr": safe_div(fp, fp + tn), "tpr": safe_div(tp, tp + fn),
                     "fnr": safe_div(fn, tp + fn), "flag_rate": (tp + fp) / n,
                     "precision": safe_div(tp, tp + fp), "accuracy": (tp + tn) / n})
    return pd.DataFrame(rows).set_index("group")


def disparity(m):
    a, b = m.loc["A"], m.loc["B"]
    return {"fpr_gap": abs(a.fpr - b.fpr), "tpr_gap": abs(a.tpr - b.tpr),
            "fnr_gap": abs(a.fnr - b.fnr), "flag_rate_gap": abs(a.flag_rate - b.flag_rate),
            "accuracy_gap": abs(a.accuracy - b.accuracy),
            "equalized_odds_difference": max(abs(a.tpr - b.tpr), abs(a.fpr - b.fpr)),
            "fpr_ratio_B_over_A": safe_div(b.fpr, a.fpr)}


# --------------------------------------------------------------------------
# 3. Uncertainty
# --------------------------------------------------------------------------
def fisher_exact_two_sided(a, b, c, d):
    """Two-sided Fisher exact p-value for the 2x2 table [[a, b], [c, d]]."""
    row1, row2, col1 = a + b, c + d, a + c
    total = row1 + row2

    def prob(x):
        return math.comb(row1, x) * math.comb(row2, col1 - x) / math.comb(total, col1)

    p_obs = prob(a)
    lo, hi = max(0, col1 - row2), min(row1, col1)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs * (1 + 1e-9)))


def bootstrap_gaps(df, rng):
    """Stratified bootstrap: resample each (group, label) cell with replacement."""
    def rates(group, fraud):
        v = df[(df.group == group) & (df.actual_fraud == fraud)]["flag"].to_numpy()
        return rng.choice(v, size=(N_BOOT, len(v)), replace=True).mean(axis=1)

    fpr_a, fpr_b = rates("A", 0), rates("B", 0)
    tpr_a, tpr_b = rates("A", 1), rates("B", 1)
    pct = lambda x: (float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5)))
    return {"fpr_A": pct(fpr_a), "fpr_B": pct(fpr_b), "tpr_A": pct(tpr_a), "tpr_B": pct(tpr_b),
            "fpr_gap_B_minus_A": pct(fpr_b - fpr_a), "tpr_gap_A_minus_B": pct(tpr_a - tpr_b),
            "share_of_resamples_FPR_B_above_A": float((fpr_b > fpr_a).mean())}


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(SEED)

    # ---- 1. dataset and baseline rule ----
    df = build_dataset()
    df["score"], df["flag"] = apply_rule(df, BASELINE["weights"], BASELINE["threshold"])
    df["score_display"] = df["score"] / 100
    df[["record_id", "group", "unusual_velocity", "device_anomaly", "limited_history",
        "actual_fraud", "score_display", "flag"]].rename(columns={"score_display": "score"}) \
        .to_csv(DATA_DIR / "synthetic_transactions.csv", index=False)

    out("=" * 72)
    out("TASK 4 - FAIRNESS AND EXPLAINABILITY ANALYSIS (SYNTHETIC DATA ONLY)")
    out("=" * 72)
    out(f"Records: {len(df)}  | Groups: {sorted(df.group.unique())}  | Seed: {SEED}")
    out(f"Rule: score = 0.40*V + 0.35*D + 0.25*H ; flag if score >= 0.50 (integer arithmetic)")

    # ---- 2. baseline metrics ----
    m = group_metrics(df, "flag")
    for g, exp in EXPECTED.items():                      # construction sanity check
        got = {k: int(m.loc[g, k]) for k in exp}
        assert got == exp, f"Construction check failed for group {g}: {got} != {exp}"
    out("\n--- Confusion matrices and rates (baseline rule) ---")
    out(m.round(3).to_string())
    m.round(4).to_csv(RES_DIR / "metrics_by_group.csv")

    disp = disparity(m)
    overall_acc = float(((df.flag == df.actual_fraud).mean()))
    out("\n--- Group disparities (absolute) ---")
    for k, v in disp.items():
        out(f"{k:28s}: {v:.3f}")
    out(f"{'overall_accuracy':28s}: {overall_acc:.3f}")
    pd.Series({**disp, "overall_accuracy": overall_acc}).round(4) \
        .to_csv(RES_DIR / "disparity_summary.csv", header=["value"], index_label="measure")

    # optional cross-check with Fairlearn (if installed)
    try:
        from fairlearn.metrics import equalized_odds_difference
        fl = equalized_odds_difference(df.actual_fraud, df.flag, sensitive_features=df.group)
        out(f"\nFairlearn cross-check, equalized_odds_difference: {fl:.3f} "
            f"(script value {disp['equalized_odds_difference']:.3f})")
    except ImportError:
        out("\nFairlearn not installed: cross-check skipped (not required).")

    # ---- 3. uncertainty ----
    a, b = m.loc["A"], m.loc["B"]
    p_fpr = fisher_exact_two_sided(int(b.fp), int(b.tn), int(a.fp), int(a.tn))
    p_tpr = fisher_exact_two_sided(int(a.tp), int(a.fn), int(b.tp), int(b.fn))
    ci = bootstrap_gaps(df, rng)
    out("\n--- Uncertainty (n = 20 per group-label cell) ---")
    out(f"Fisher exact p-value, FPR B vs A (8/20 vs 4/20): {p_fpr:.3f}")
    out(f"Fisher exact p-value, TPR A vs B (18/20 vs 16/20): {p_tpr:.3f}")
    for k, v in ci.items():
        out(f"{k:36s}: " + (f"[{v[0]:.3f}, {v[1]:.3f}]" if isinstance(v, tuple) else f"{v:.3f}"))
    rows = [{"quantity": k, "ci_low": v[0], "ci_high": v[1]} for k, v in ci.items() if isinstance(v, tuple)]
    rows += [{"quantity": "fisher_p_FPR_B_vs_A", "ci_low": p_fpr, "ci_high": p_fpr},
             {"quantity": "fisher_p_TPR_A_vs_B", "ci_low": p_tpr, "ci_high": p_tpr}]
    pd.DataFrame(rows).round(4).to_csv(RES_DIR / "uncertainty.csv", index=False)

    # ---- 4. why the gap exists: feature prevalence by group and label ----
    prev = df.groupby(["group", "actual_fraud"])[FEATURES].mean().round(3)
    out("\n--- Feature prevalence by group and ground truth (1 = fraud) ---")
    out(prev.to_string())
    prev.to_csv(RES_DIR / "feature_prevalence.csv")

    # ---- 5. explainability ----
    out("\n--- Individual decision review: record B021 ---")
    rec = df[df.record_id == "B021"].iloc[0]
    contrib = pd.DataFrame({
        "feature": FEATURES,
        "value": [int(rec[f]) for f in FEATURES],
        "contribution": [rec[f] * BASELINE["weights"][f] / 100 for f in FEATURES]})
    total = contrib.contribution.sum()
    out(contrib.to_string(index=False))
    out(f"Total score: {total:.2f} | threshold 0.50 | flagged: {bool(rec.flag)} | "
        f"actual_fraud: {int(rec.actual_fraud)} -> {'false positive' if rec.flag and not rec.actual_fraud else 'other'}")
    cf = []
    for f in FEATURES:
        s = int(rec.score - rec[f] * BASELINE["weights"][f])
        cf.append({"counterfactual": f"set {f} to 0", "new_score": s / 100,
                   "flag_after_change": int(s >= BASELINE["threshold"])})
    cf = pd.DataFrame(cf)
    out("\nCounterfactual check (one feature changed at a time):")
    out(cf.to_string(index=False))
    contrib.assign(total_score=total).to_csv(RES_DIR / "explain_B021_contributions.csv", index=False)
    cf.to_csv(RES_DIR / "explain_B021_counterfactuals.csv", index=False)

    # flag dependence on limited_history (decision-review at group level)
    w0 = dict(BASELINE["weights"]); w0["limited_history"] = 0
    _, flag_no_h = apply_rule(df, w0, BASELINE["threshold"])
    df["h_dependent_flag"] = ((df.flag == 1) & (flag_no_h == 0)).astype(int)
    dep_rows = []
    for g, sub in df.groupby("group"):
        flagged = sub[sub.flag == 1]
        hdep = flagged[flagged.h_dependent_flag == 1]
        other = flagged[flagged.h_dependent_flag == 0]
        dep_rows.append({"group": g, "flagged": len(flagged), "flags_dependent_on_limited_history": len(hdep),
                         "share_dependent": len(hdep) / len(flagged),
                         "precision_of_dependent_flags": hdep.actual_fraud.mean(),
                         "precision_of_other_flags": other.actual_fraud.mean()})
    dep = pd.DataFrame(dep_rows).set_index("group")
    out("\n--- Flags that disappear if limited_history is ignored ---")
    out(dep.round(3).to_string())
    dep.round(4).to_csv(RES_DIR / "flag_dependence_limited_history.csv")

    # ---- 6. candidate corrections, tested on ALL outcomes ----
    scenarios = {
        "baseline": (BASELINE["weights"], 50),
        "M1_remove_limited_history": ({**BASELINE["weights"], "limited_history": 0}, 50),
        "M2_limited_history_weight_0.10": ({**BASELINE["weights"], "limited_history": 10}, 50),
        "M3_raise_threshold_to_0.65": (BASELINE["weights"], 65),
    }
    srows = []
    for name, (w, t) in scenarios.items():
        _, fl = apply_rule(df, w, t)
        tmp = df.assign(flag_s=fl)
        mm = group_metrics(tmp, "flag_s")
        dd = disparity(mm)
        srows.append({"scenario": name,
                      "fpr_A": mm.loc["A", "fpr"], "fpr_B": mm.loc["B", "fpr"],
                      "tpr_A": mm.loc["A", "tpr"], "tpr_B": mm.loc["B", "tpr"],
                      "fpr_gap": dd["fpr_gap"], "tpr_gap": dd["tpr_gap"],
                      "equalized_odds_difference": dd["equalized_odds_difference"],
                      "total_false_positives": int(mm.fp.sum()), "total_missed_fraud": int(mm.fn.sum())})
    sc = pd.DataFrame(srows).set_index("scenario")
    out("\n--- Candidate corrections compared on all outcomes ---")
    out(sc.round(3).to_string())
    out("Note: M2 and M3 flag the same records here because every feature is binary.")
    sc.round(4).to_csv(RES_DIR / "mitigation_scenarios.csv")

    # ---- 7. chart ----
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    x = np.arange(2)
    w = 0.34
    fpr = [m.loc["A", "fpr"], m.loc["B", "fpr"]]
    fnr = [m.loc["A", "fnr"], m.loc["B", "fnr"]]
    # bootstrap CIs for FPR; FNR CI = 1 - TPR CI (reversed)
    fpr_err = np.array([[fpr[0] - ci["fpr_A"][0], fpr[1] - ci["fpr_B"][0]],
                        [ci["fpr_A"][1] - fpr[0], ci["fpr_B"][1] - fpr[1]]])
    fnr_lo = [1 - ci["tpr_A"][1], 1 - ci["tpr_B"][1]]
    fnr_hi = [1 - ci["tpr_A"][0], 1 - ci["tpr_B"][0]]
    fnr_err = np.array([[fnr[0] - fnr_lo[0], fnr[1] - fnr_lo[1]], [fnr_hi[0] - fnr[0], fnr_hi[1] - fnr[1]]])
    ax[0].bar(x - w / 2, fpr, w, yerr=fpr_err, capsize=4, label="False-positive rate", color="#c0504d")
    ax[0].bar(x + w / 2, fnr, w, yerr=fnr_err, capsize=4, label="False-negative rate", color="#4f81bd")
    ax[0].set_xticks(x, ["Group A", "Group B"])
    ax[0].set_ylim(0, 0.85)
    ax[0].set_ylabel("Rate")
    ax[0].set_title("Baseline error rates by group\n(bars = observed, whiskers = 95% bootstrap interval)", fontsize=10)
    for i, (p, q) in enumerate(zip(fpr, fnr)):
        # place value labels just above the upper whisker so they never overlap it
        ax[0].text(i - w / 2, p + fpr_err[1][i] + 0.015, f"{p:.0%}", ha="center", va="bottom", fontsize=9)
        ax[0].text(i + w / 2, q + fnr_err[1][i] + 0.015, f"{q:.0%}", ha="center", va="bottom", fontsize=9)
    ax[0].legend(loc="upper left", fontsize=8)

    labels = ["Baseline", "M1 remove\nlimited history", "M2 weight 0.10\n(= M3 threshold 0.65)"]
    keys = ["baseline", "M1_remove_limited_history", "M2_limited_history_weight_0.10"]
    xx = np.arange(len(keys))
    ww = 0.2
    ax[1].bar(xx - 1.5 * ww, sc.loc[keys, "fpr_A"], ww, label="FPR A", color="#e6b8b7")
    ax[1].bar(xx - 0.5 * ww, sc.loc[keys, "fpr_B"], ww, label="FPR B", color="#c0504d")
    ax[1].bar(xx + 0.5 * ww, sc.loc[keys, "tpr_A"], ww, label="TPR A", color="#b8cce4")
    ax[1].bar(xx + 1.5 * ww, sc.loc[keys, "tpr_B"], ww, label="TPR B", color="#4f81bd")
    ax[1].set_xticks(xx, labels, fontsize=8)
    ax[1].set_ylim(0, 1.05)
    ax[1].set_title("Candidate corrections: fewer false flags,\nbut fraud detection also falls", fontsize=10)
    ax[1].legend(fontsize=8, ncol=2, loc="upper right")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.text(0.5, 0.02, "Synthetic example only - illustrative, not evidence about a real system",
             ha="center", fontsize=9)
    fig.savefig(FIG_DIR / "error_rates_and_corrections.png", dpi=200)
    out("\nChart saved: figures/error_rates_and_corrections.png")

    # ---- environment record ----
    env = {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
           "matplotlib": matplotlib.__version__, "seed": SEED, "bootstrap_resamples": N_BOOT}
    (RES_DIR / "run_environment.json").write_text(json.dumps(env, indent=2))
    out("Environment: " + json.dumps(env))
    (RES_DIR / "analysis_output.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
