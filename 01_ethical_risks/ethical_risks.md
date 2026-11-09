# Task 1: Ethical risk assessment

*Draft for the AICS-201 Assessment 01 repository. Ratings match `02_governance/risk_register.csv` (R1 to R5). Replace with your own final wording so the repo and the report agree.*

Five ethical risks were assessed, each described by cause, affected stakeholders, likely consequences and a proportionate control.

## R1: Algorithmic bias (High)
- **Cause:** Historical fraud labels may record who was investigated, not who was guilty, and may under-represent informal-sector and thin-file customers. Proxy variables such as location or device type can stand in for protected characteristics. NIST identifies systemic, statistical and human-cognitive sources of bias (NIST, 2023, p. 18).
- **Stakeholders:** Under-represented and newly banked customers, investigators, SecureFinance.
- **Consequences:** Repeated verification failures, frozen accounts and false flags, compounding at scale.
- **Control:** Audit labels against investigation outcomes; compare group error rates before launch and after each major change; review proxies; set a disparity threshold that triggers retraining.

## R2: Privacy and excessive data processing (High)
- **Cause:** Identity checks may collect national ID numbers, biometrics and transaction histories. Risks include over-collection, indefinite retention, broad staff access, function creep and vendor sharing.
- **Stakeholders:** Customers, staff with access, vendors.
- **Consequences:** Identity theft and financial loss that cannot be reset like a password, loss of control over personal data, and enforcement under the Nigeria Data Protection Act 2023.
- **Control:** Impact assessment before launch; documented purpose and lawful basis; data minimisation; retention limits; encryption; role-based access; vendor due diligence; breach procedure.

## R3: Unfair outcomes and unequal redress (High)
- **Cause:** Rules assume a typical customer, for example treating short histories as suspicious, and digital-only appeals exclude people with limited connectivity or disabilities. Unlike R1, this concerns rules and redress, not only model error.
- **Stakeholders:** Newly banked and irregular-income customers, people with disabilities or limited digital access.
- **Consequences:** Disproportionate restrictions and little practical route to correct errors, deepening financial exclusion.
- **Control:** Define fairness objectives per use case; evaluate outcome and error gaps; offer alternative verification routes; provide accessible appeals reviewed by someone with authority to reverse the decision.

## R4: Limited transparency (Medium)
- **Cause:** Complex models and generic outputs such as "high risk" give no usable reason, and customers may not know AI is involved.
- **Stakeholders:** Customers with adverse outcomes, investigators, auditors.
- **Consequences:** Errors cannot be spotted or contested, and opacity creates legal risk under the Act's rules on automated decisions.
- **Control:** Disclose AI use; give plain-language, case-specific reasons; keep model documentation and decision records. Explanations give reason categories, not exact thresholds, balancing transparency against fraud prevention.

## R5: Ineffective human oversight (High)
- **Cause:** Automation bias, heavy workloads, limited training, restricted evidence or no authority to override.
- **Stakeholders:** Customers, analysts, compliance officers.
- **Consequences:** The human in the loop becomes a formality, and incorrect flags become harmful decisions with unclear ownership. Because the design assumes a person makes the final call, this control carries particular weight.
- **Control:** Mandatory review of high-impact outcomes; reviewer training, evidence, time and override authority; recorded reasons; monitoring of override rates, since near-total agreement with the model is a warning sign; escalation and suspension procedures.

Together, these risks show that accuracy, privacy, fairness, transparency and oversight must be managed as one system, because weakness in one undermines the others.
