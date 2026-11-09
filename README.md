# SecureFinance Africa: AI Ethics, Governance and Legal Compliance Assessment

**ICDFA AICS-201 | AI Ethics, Governance and Legal Frameworks | Assignment 01**
Author: Paul Sheawaza Yohanna | Student ID: 2026/AICDF/16788 | Submitted: 11-09-2026

This repository supports my assessment report for a fictional organisation, SecureFinance Africa, which plans to deploy an AI platform for identity verification, fraud detection and financial risk assessment in Nigeria. It contains the risk register, the analysis files, the synthetic dataset, the reproducible methods and the supporting documentation referred to in the PDF report.

> **Data statement.** Everything here is fictional or synthetic. No real customer records, passwords, financial identifiers or confidential information are used. No live production system or third-party service was assessed.

## How the repository maps to the report

| Folder | Content | Report location |
|---|---|---|
| `01_ethical_risks/` | Five ethical risks (R1 to R5) with cause, stakeholders, consequences and controls | Task 1, section 4 |
| `02_governance/` | NIST AI RMF governance approach, **risk register** (`risk_register.csv`, 9 risks) and a checker script | Task 2, section 5, Appendix A |
| `03_legal_compliance/` | Binding vs non-binding instruments; NDPA, EU AI Act, UNESCO and OECD analysis | Task 3, section 6, Appendix B |
| `04_fairness/` | **Synthetic dataset, Python analysis, results, chart** and its own README | Task 4, section 7, Appendix C |
| `docs/` | Assumptions and AI-use declaration | Sections 2 and 10 |
| `references.md` | Reference list | References |

## Reproducing the analysis

Requires Python 3.10 or later.

```bash
# 1. Check the risk register arithmetic (standard library only)
python 02_governance/check_register.py

# 2. Reproduce the fairness evaluation
cd 04_fairness
pip install -r requirements.txt
python src/fairness_analysis.py
```

Step 2 rebuilds the synthetic dataset, recalculates every fairness measure, uncertainty estimate and explainability output, and regenerates the chart. The random seed is fixed, so results are identical on every run. Details are in `04_fairness/README.md`.

## Headline results

- **Risk register:** 9 risks. Before controls: 1 Critical, 6 High, 2 Medium. After proposed controls, R1 (bias), R5 (human oversight) and R7 (cyberattack) remain High.
- **Fairness example (synthetic):** false-positive rate 20% (Group A) vs 40% (Group B); equalized-odds difference 0.20; the gap is not statistically established at n = 20 per cell (Fisher exact p = 0.30).
- **Recommendation:** no full deployment now; a limited Nigerian pilot only once the listed conditions are met; EU-facing use deferred.

## Notes for the assessor

- Linked evidence is public (or shared with the authorised assessor) and the submission URL was tested before the deadline.
- I can demonstrate or explain any analysis in this repository on request.
- AI assistance is declared in `docs/ai_use_declaration.md` and in the report.
