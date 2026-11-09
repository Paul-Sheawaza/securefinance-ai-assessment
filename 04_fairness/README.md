# Task 4: Algorithmic fairness and explainability evaluation

**AICS-201 AI Ethics, Governance and Legal Frameworks | Assessment 01 | SecureFinance Africa (fictional)**

This folder contains the reproducible evidence for Task 4 of the assessment. It demonstrates a practical method for detecting potentially unfair outcomes in the fraud-detection module of a fictional AI platform.

> **Data statement.** All data is synthetic. No real customer records, passwords, financial identifiers or confidential information were used. Group labels A and B are fictional audit groups. Results describe the constructed example only and make no claim about any real system or population.

## Contents

```
task4_fairness/
├── README.md                      this file
├── requirements.txt               Python dependencies
├── data/
│   └── synthetic_transactions.csv 80 synthetic records
├── src/
│   └── fairness_analysis.py       complete analysis (builds data, computes everything)
├── results/
│   ├── analysis_output.txt        full console output of the run
│   ├── metrics_by_group.csv       confusion matrices, FPR, TPR, FNR, flag rate, precision, accuracy
│   ├── disparity_summary.csv      group gaps and equalized-odds difference
│   ├── uncertainty.csv            bootstrap 95% intervals and Fisher exact p-values
│   ├── feature_prevalence.csv     feature rates by group and ground truth (proxy mechanism)
│   ├── explain_B021_contributions.csv   exact score contributions for record B021
│   ├── explain_B021_counterfactuals.csv one-feature-at-a-time counterfactual checks
│   ├── flag_dependence_limited_history.csv flags that depend on one feature, by group
│   ├── mitigation_scenarios.csv   candidate corrections compared on all outcomes
│   └── run_environment.json       Python and library versions, seed
├── figures/
│   └── error_rates_and_corrections.png
└── docs/
    └── data_dictionary.md         variables, scoring rule, dataset construction table
```

## How to reproduce

```bash
python -m venv .venv && source .venv/bin/activate     # optional
pip install -r requirements.txt
python src/fairness_analysis.py
```

The script rebuilds the dataset, recalculates every result, overwrites the files in `data/`, `results/` and `figures/`, and prints the same output saved in `results/analysis_output.txt`. The random seed is fixed (`SEED = 42`, 10,000 bootstrap resamples), so repeated runs give identical numbers.

Tested with Python 3.12, numpy 2.5, pandas 3.0 and matplotlib 3.11 (see `results/run_environment.json`). Fairlearn is **not** required. If it is installed, the script cross-checks its equalized-odds difference against Fairlearn's.

## What the analysis does

1. **Dataset.** 80 fictional transactions (40 per group; 20 fraud and 20 legitimate per group) built from a documented pattern-count table.
2. **Screening rule.** `score = 0.40 x unusual_velocity + 0.35 x device_anomaly + 0.25 x limited_history`; flag if score >= 0.50. Group is not an input.
3. **Fairness measures.** False-positive rate (primary harm: legitimate customers wrongly flagged), true-positive rate and false-negative rate (missed fraud), flag rate, and equalized-odds difference (the larger of the TPR gap and FPR gap).
4. **Uncertainty.** Stratified bootstrap intervals and Fisher exact tests, because each denominator is only 20.
5. **Explainability and decision review.** Exact additive feature contributions for individual records, one-feature counterfactuals, and a group-level measure of how many flags depend on a single feature.
6. **Candidate corrections.** Three changes tested on all outcomes (both group FPRs, both group TPRs, total false positives, total missed fraud), so an improvement on one measure cannot hide a worse result on another.

## Headline results (baseline)

| Measure | Group A | Group B |
|---|---|---|
| False-positive rate | 20% | 40% |
| True-positive rate | 90% | 80% |
| Flag rate | 55% | 60% |
| Accuracy | 85% | 70% |

Equalized-odds difference = 0.20. The Fisher exact p-value for the FPR difference is 0.30, and the bootstrap 95% interval for the FPR gap (B minus A) spans -0.10 to +0.45. The observed gap is consistent with a real disparity but is **not statistically established** at this sample size. See `results/uncertainty.csv`.

## Limitations

- The dataset is small, deliberately structured and not representative of real customers.
- The ground-truth labels are stipulated. In practice, fraud labels can reflect past investigation decisions rather than proven fraud, and must be audited.
- The rule is transparent by design, so the explanations are exact. A trained model would need post-hoc explanation methods, with their own accuracy limits.
- Only one binary group split is tested. Real assessments need intersecting groups and attention to multiple comparisons.
- Collecting group attributes to test fairness must itself be reconciled with data-minimisation duties (Nigeria Data Protection Act 2023, s.24).
- The correction scenarios are illustrations on this dataset, not validated recommendations.

## AI-assistance declaration

> AI tools were used to help review and structure this analysis and to assist with drafting code. The student reviewed, ran and understands all code and results, and is responsible for the analysis and conclusions. 

## References

- Fairlearn contributors (n.d.) *Performing a Fairness Assessment*. Fairlearn documentation. https://fairlearn.org/main/user_guide/assessment/perform_fairness_assessment.html
- Fairlearn contributors (n.d.) *Common fairness metrics*. Fairlearn documentation. https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html
- Phillips, P.J., Hahn, C.A., Fontana, P.C., Yates, A.N., Greene, K., Broniatowski, D.A. and Przybocki, M.A. (2021) *Four Principles of Explainable Artificial Intelligence*, NISTIR 8312. National Institute of Standards and Technology. https://doi.org/10.6028/NIST.IR.8312
- National Institute of Standards and Technology (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1
