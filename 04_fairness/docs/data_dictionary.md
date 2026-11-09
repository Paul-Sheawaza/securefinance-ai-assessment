# Data dictionary and dataset construction

**All records are fictional and synthetic.** No real customer, transaction, identity or financial data was used. The groups (A and B) are fictional audit groups, not real demographic populations.

File: `data/synthetic_transactions.csv` (80 rows, 8 columns)

| Column | Type | Description |
|---|---|---|
| `record_id` | text | Fictional identifier. Prefix = group; numbers 001-020 are fraudulent records, 021-040 are legitimate records. |
| `group` | text | Fictional audit group: `A` or `B`. **Not an input to the screening rule.** |
| `unusual_velocity` | 0/1 | Indicator of unusual transaction frequency (V). |
| `device_anomaly` | 0/1 | Indicator of an unusual device-related signal (D). |
| `limited_history` | 0/1 | Indicator of limited account history (H). |
| `actual_fraud` | 0/1 | **Stipulated** ground truth: 1 = fraud, 0 = legitimate. In real data this label must be validated (see limitations). |
| `score` | decimal | Screening score = 0.40 x V + 0.35 x D + 0.25 x H. |
| `flag` | 0/1 | Screening output: 1 if `score` >= 0.50, otherwise 0. |

## Screening rule

```
score = 0.40*V + 0.35*D + 0.25*H
flag  = 1 if score >= 0.50 else 0
```

The script uses integer hundredths (40, 35, 25 and threshold 50) so the comparison is exact and free of floating-point error.

Only four feature combinations reach the threshold: V+D (0.75), V+H (0.65), D+H (0.60) and V+D+H (1.00). Single features (0.40, 0.35, 0.25) and no features (0) do not.

## How the dataset was constructed

The dataset is not random. It is built from the pattern-count table below (defined in `SPEC` in `src/fairness_analysis.py`). Each cell holds exactly 20 records. Pattern notation is V D H (1 = present).

| Group | Truth | Pattern counts (V D H : records) | Records |
|---|---|---|---|
| A | Fraud | 110: 6, 111: 6, 011: 3, 101: 3, 010: 1, 100: 1 | 20 |
| A | Legitimate | 011: 1, 101: 1, 110: 2, 001: 2, 000: 8, 010: 3, 100: 3 | 20 |
| B | Fraud | 110: 5, 111: 5, 011: 3, 101: 3, 001: 1, 010: 1, 100: 1, 000: 1 | 20 |
| B | Legitimate | 011: 5, 101: 3, 001: 4, 000: 4, 010: 2, 100: 2 | 20 |

### Design assumption (the mechanism being demonstrated)

Limited account history is equally common among fraudulent records in both groups (60%) but much more common among **legitimate** records in Group B (60%) than in Group A (20%). The rule treats limited history as a fraud signal, so legitimate Group B customers are flagged more often. Group membership is never used by the rule: the disparity is produced by a feature acting as a proxy.

This pattern is a deliberate construction to demonstrate the evaluation method. The numerical results are properties of this constructed example. They are not findings about SecureFinance Africa's real system or any real population.

## Hand-check of the baseline results

| Group | TP | FN | FP | TN | FPR = FP/(FP+TN) | TPR = TP/(TP+FN) |
|---|---|---|---|---|---|---|
| A | 18 | 2 | 4 | 16 | 4/20 = 20% | 18/20 = 90% |
| B | 16 | 4 | 8 | 12 | 8/20 = 40% | 16/20 = 80% |

The script asserts these counts when it runs. If the dataset is changed, the assertion fails and tells you the construction no longer matches the documented design.
