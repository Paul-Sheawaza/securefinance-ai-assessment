# Task 3: Legal and regulatory compliance matrix

*Supporting document. Verify NDPA wording against the official text on https://ndpc.gov.ng/ and the EU AI Act provisions in the AI Act Explorer before relying on them. This is analysis for an assessment, not legal advice.*

## B1. Binding law and non-binding principles
| Instrument | Status | When it affects SecureFinance |
|---|---|---|
| Nigeria Data Protection Act 2023 (NDPA) | Binding national law | Now. Applies where a controller operates in Nigeria, processing occurs in Nigeria, or a foreign controller processes data of a person in Nigeria (s.2(2)). |
| EU AI Act (Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744) | Binding EU regulation with effect beyond the EU | Conditionally, where the Article 2 circumstances are met: placing the system on the EU market or putting it into service there, or a third-country provider's or deployer's outputs being used in the EU. |
| UNESCO Recommendation on the Ethics of AI (2021) | Non-binding; states are recommended to apply it "on a voluntary basis" (para 2) | A benchmark for ethical design and governance. |
| OECD AI Principles (2019, revised 2024) | Non-binding Council Recommendation | A benchmark for trustworthy AI. Creates no Nigerian legal obligation. |

## B2. NDPA 2023 obligations and controls (binding now)
| Provision | When it applies and effect on SecureFinance | Proposed control |
|---|---|---|
| **s.24-25: principles and lawful basis.** Fair, lawful, transparent processing; specified purposes; data minimisation; limited retention; accuracy; security; accountability (s.24(3)). A lawful basis is needed (s.25); legitimate interests cannot override data subjects' rights or exceed their reasonable expectations (s.25(2)). | Applies to all three modules from first collection. Fraud monitoring and risk profiling need a documented basis. Reusing data for new purposes (function creep) must pass the compatibility test in s.24(4). | Record purpose and lawful basis per module; minimise collection; set retention and deletion schedules; accuracy checks and a correction route. |
| **s.27: information to data subjects.** Customers must be told the lawful basis, recipients, retention, complaint rights and the existence of automated decision-making and profiling, its significance and the right to object and challenge (s.27(1)(g)). | Applies at onboarding and whenever processing changes. A generic privacy policy omitting AI profiling would fall short. | Plain-language privacy and AI-use notice at onboarding. |
| **s.28: data privacy impact assessment.** Required before processing likely to result in high risk. If high risk remains, consult the Commission before processing (s.28(2)). | Biometric verification plus financial profiling and consequential recommendations is a strong case for assessment before deployment. Internal approval cannot replace consultation where s.28(2) is triggered. | Documented assessment covering all three modules and their combined effects; record safeguards and residual risk; privacy-lead review; no processing until any required consultation has occurred; reassess on material change. |
| **s.30 and s.65: sensitive personal data.** Biometric data used to uniquely identify a person is sensitive and may be processed only on a listed ground, such as consent. | Applies to selfie templates used in identity verification. | Obtain valid consent or another s.30 ground; limit template retention; offer a non-biometric alternative route. |
| **s.37: automated decision-making.** Right not to be subject to a decision based solely on automated processing with legal or similarly significant effects. Exceptions (contract necessity, written law, consent) still require safeguards: human intervention, the right to express a view and to contest (s.37(3)). Section 65 defines this as a decision "without any human involvement". | Where analysts genuinely make the final call, s.37(1) may not be triggered. If analysts merely endorse model outputs, a regulator could treat decisions as solely automated in substance. This is an argument, not settled law, because the Act does not define "involvement". | Genuine review with authority to override; reviewer training; sampling of review quality; accessible appeals; s.37(3) safeguards adopted regardless. |
| **s.29 and s.39: processors and security.** Processors bound by written agreement; controllers apply appropriate technical and organisational measures (for example encryption, pseudonymisation, regular testing). | Applies to cloud, identity-verification and model vendors, and to security risk (R7) and vendor risk (R8). | Written processor agreements; vendor due diligence; encryption; access controls; security testing. |
| **s.40: breach notification.** Processors notify the controller. The controller notifies the Commission within 72 hours of becoming aware of a breach likely to result in risk, and immediately informs affected individuals where risk is high, in plain language, or publicly where direct contact is disproportionate or not feasible. All breaches are recorded (s.40(8)). | The 72 hours run from awareness, not from when the breach occurred. The Commission threshold is risk; the individual threshold is high risk. | Breach procedure recording awareness time, affected data, risk assessment and notification decisions; assigned roles; templates; evidence preservation; prompt vendor escalation. |
| **s.41-43: cross-border transfers.** Data may leave Nigeria only if the recipient is subject to adequate protection or a s.43 condition applies; record the basis (s.41(2)). | Applies if models, logs or vendors sit outside Nigeria, or if EU expansion moves data across borders. | Map data flows; choose hosting and contracts accordingly; record the basis for each transfer. |
| **s.32 and s.44: DPO and registration.** Controllers of major importance designate a Data Protection Officer and register with the Commission. | Assumed to apply, pending the Commission's thresholds. | Designate the DPO; register; notify significant changes within 60 days (s.44(3)). |

**Enforcement.** Compliance orders, including orders to stop processing (s.47). For controllers of major importance, penalties can reach the greater of 10 million naira or 2% of annual gross revenue (s.48). Damages claims (s.51); principal officers may be held culpable (s.53).

## B3. EU AI Act classification by module (only if in scope)
| Module | Likely classification | Reasoning |
|---|---|---|
| Identity verification (one-to-one) | Not high-risk on the biometrics ground alone | Annex III point 1(a) excludes biometric verification whose sole purpose is to confirm a claimed identity. The exclusion is specific; other intended uses must be assessed separately, and Nigerian sensitive-data rules still apply. |
| Fraud detection | Likely excepted | Annex III point 5(b) excludes AI used to detect financial fraud. The Commission's draft guidelines read this narrowly: fraud detection should be the main intended use. If fraud outputs feed a creditworthiness decision, that use is assessed separately. |
| Financial risk assessment (creditworthiness or limits) | High-risk | Annex III point 5(b) covers evaluating the creditworthiness of natural persons or establishing a credit score. Human review does not remove a system from the listed category. Because creditworthiness assessment involves profiling, the Article 6(3) derogation is unlikely to be available. |

**Timing.** Annex III high-risk obligations apply from 2 December 2027 under Regulation (EU) 2026/1744 (in force 27 July 2026), replacing 2 August 2026. **Roles.** SecureFinance must identify whether it is provider, deployer or both; provider duties include risk management, data governance, documentation, record-keeping, human oversight, accuracy and robustness, quality management, conformity assessment and registration; deployers have separate duties.

## B4. UNESCO principles applied (non-binding)
| Principle | Application | Proposed safeguard |
|---|---|---|
| Proportionality and Do No Harm (paras 25-26) | Verification and monitoring should not collect or analyse more than needed. Para 26 says AI should not be used for social scoring, so risk scoring should stay tied to its financial purpose. | Assess less intrusive options; document why each data category is necessary; limit scoring to stated purposes. |
| Fairness and non-discrimination (paras 28-29) | Errors and policies should not systematically disadvantage groups; effective remedy should be available. | Test group-level outcomes; investigate disparities; alternative verification routes. |
| Privacy and data protection (paras 32-34) | Algorithmic systems require adequate privacy impact assessments. | Data minimisation, access restrictions, retention controls, impact assessments. |
| Transparency and explainability (paras 38, 40) | People should be informed when AI informs a decision and be able to get reasons and make submissions to someone able to review and correct it. | Clear AI-use notices; meaningful reasons; accessible review. |
| Human oversight and accountability (paras 35-36, 42-43) | Responsibility stays with people and the organisation, with auditability and traceability. | Accountable owners; meaningful overrides; decision logs. |

## B5. OECD principles applied (non-binding)
| Principle | Application to SecureFinance |
|---|---|
| Inclusive growth, sustainable development and well-being | Assess whether the platform widens access rather than excluding customers with limited financial histories or digital access. |
| Respect for the rule of law, human rights and democratic values, including fairness and privacy | Evaluate discrimination and privacy risks; use data safeguards; keep routes for redress. |
| Transparency and explainability | Tell customers about AI involvement and give information that helps them understand and challenge outcomes. |
| Robustness, security and safety | Test normal and foreseeable misuse; maintain monitoring, fallback and the ability to override or withdraw unsafe functions. |
| Accountability | Assign owners, document changes and keep traceability for investigating outputs and incidents. |
