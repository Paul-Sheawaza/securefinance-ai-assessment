# Task 2: Governance and AI risk management (NIST AI RMF 1.0)

*Supporting document. The full risk register is in `risk_register.csv`; verify it with `python 02_governance/check_register.py`. Citations: NIST (2023), NIST AI 100-1. NIST is voluntary guidance, not law.*

## A1. Governance approach
| Function | Application to SecureFinance Africa |
|---|---|
| Govern | Adopt AI policies, document roles, set risk tolerance, require deployment approval, maintain an AI system inventory (GOVERN 1.6), train staff (GOVERN 2.2), manage vendors (GOVERN 6) and plan safe decommissioning (GOVERN 1.7). |
| Map | Document intended uses, data sources, affected groups, third-party dependencies and foreseeable harms (MAP 1.1, 4.1, 5.1). |
| Measure | Evaluate accuracy, group-level error rates, privacy, security, explanation quality and human-review effectiveness (MEASURE 2.3, 2.7-2.11). |
| Manage | Prioritise risks, choose a response (mitigate, transfer, avoid or accept), monitor after deployment and respond to incidents (MANAGE 1.2, 1.3, 4.1, 4.3). |

## A2. Governance responsibilities
| Role | Accountability and authority |
|---|---|
| Chief Risk Officer (chair of the AI Governance Committee) | Single accountable executive. Final sign-off to launch, restrict or withdraw the system (GOVERN 2.3). |
| AI Governance Committee | Approves risk tolerance and deployment conditions, accepts residual risks within policy, authorises restart after serious incidents. |
| AI/model lead | Owns model development, documentation, performance monitoring and controlled updates. |
| Data Protection Officer (DPO) | Owns NDPA obligations: impact assessments, data subject rights, retention, access and breach assessment. |
| Information security lead | Owns security testing, protection against manipulation, containment and security incident response. |
| Fraud operations manager | Owns reviewer training, meaningful human review, appeals and overrides. |
| Technology/vendor lead | Owns third-party due diligence, change notification and fallback. |
| Compliance lead | Tracks legal obligations, advises on reporting duties, checks uses stay in approved scope. |
| Independent reviewer | Not involved in building the model. Verifies validation, fairness and safeguard evidence before deployment is recommended (MEASURE 1.3; NIST, 2023, pp. 35-36). |

The fraud operations manager and information security lead may pause affected functionality immediately when harm is suspected. The committee decides on restart (MANAGE 2.4).

## A3. Scoring method
Risk score = Likelihood x Impact on a local 5x5 scale (NIST does not prescribe a scale or tolerance, p. 7).

| Score | Likelihood | Impact |
|---|---|---|
| 1 | Rare | Negligible: trivial, quickly corrected |
| 2 | Unlikely | Minor: limited, short-lived harm |
| 3 | Possible | Moderate: meaningful customer harm or disruption |
| 4 | Likely | Major: serious harm to many customers or the organisation |
| 5 | Almost certain | Severe: substantial financial or privacy harm, widespread exclusion |

**Bands:** 1-4 Low; 5-9 Medium; 10-16 High; 20-25 Critical. Initial ratings show exposure before safeguards; residual ratings estimate exposure after validated controls. With no test results, all ratings are preliminary judgements.

## A4. Measurement evidence
| Risk area | Proposed measurement |
|---|---|
| Bias and fairness | Compare false-positive and false-negative rates and outcomes across justified groups (MEASURE 2.11). |
| Performance | Precision, recall and verification error rates per use case; disaggregate by data segment (NIST, 2023, p. 14). |
| Privacy and security | Review collection, retention and access; test safeguards (MEASURE 2.7, 2.10). |
| Transparency | Check explanations reflect the decision and help reviewers (MEASURE 2.8, 2.9). |
| Human oversight | Sample review quality, override reasons, appeal outcomes and response times (MEASURE 3.3; NIST, 2023, p. 41). |
| Resilience | Test fallback, rollback and third-party outage response. |

## A6. Treatment, monitoring and review
| Area | Frequency | Trigger | Responsible |
|---|---|---|---|
| Security and availability | Continuous alerts; daily review | Suspected compromise, unauthorised access, critical outage | Information security lead |
| Model performance | Weekly in pilot; monthly when stable | Breach of an approved error limit or material decline | AI/model lead |
| Fairness | Monthly and after material changes | Unexplained group disparity or limit exceeded | Independent reviewer verifies; AI/model lead remediates |
| Human oversight | Weekly sampling in pilot; monthly after | Unsupported approvals, appeal backlogs, odd override patterns | Fraud operations manager |
| Privacy | Quarterly and on any processing change | Unapproved use, excess retention, inappropriate access | DPO |
| Full register | Monthly in pilot; quarterly after | Serious incident, new use case, major vendor change | Governance committee |

Numerical limits must be justified by validation evidence and documented before pilot approval.

## A7. Incident escalation (internal targets, not legal deadlines)
| Severity | Example | Escalation and response |
|---|---|---|
| Critical | Suspected sensitive-data compromise; widespread harmful restrictions | Escalate immediately to security, DPO/compliance and the CRO. Pause affected functions, preserve evidence, activate response plans. |
| High | Material group disparity, sustained model decline, repeated review failures | Notify the owner and committee chair the same working day. Restrict affected use and investigate. |
| Moderate | Isolated wrong flag or explanation failure, no wider harm | Record and assign within one working day. Correct the outcome and check for recurrence. |

For every incident: contain harm, identify affected customers, preserve logs, investigate causes, correct, validate recovery and hold a post-incident review (MANAGE 2.3, 4.3). Legal notification is decided separately by the Compliance lead and DPO (NDPA s.40).

## Deployment conditions
Full deployment should not be approved yet because R1, R5 and R7 keep High residual ratings. A limited pilot would require: (1) high risks within approved tolerance; (2) independently reviewed performance, fairness, privacy and security results; (3) effective human review and accessible appeals; (4) tested monitoring, fallback, rollback and incident response; (5) documented ownership and explicit approval of remaining risks.
