---
type: reference
title: Oncology Response Criteria — RECIST & PERCIST
chapter: reporting
order: 50
subtitle: Anatomic and metabolic response frameworks, and where each applies
aliases: [RECIST, RECIST 1.1, PERCIST, PERCIST 1.0, SULpeak, metabolic response, Choi criteria, iRECIST, pseudoprogression, complete metabolic response, response assessment]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "10 min"
tags: [reporting, oncology, response, standards]
related_tracers: [fdg]
related_diseases: []
related_therapies: []
related_calculators: [suv]
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

Tumor response is scored with the framework that matches the biology and modality. **RECIST 1.1** is the **anatomic (size-based)** standard on CT/MRI. **PERCIST 1.0** is the **metabolic (FDG)** standard, using **SUL-peak** of the hottest lesion against a **liver** reference. Disease- and therapy-specific frameworks refine these: **Choi** (GIST — density + size), **iRECIST** (immunotherapy pseudoprogression), **Deauville/Lugano** (lymphoma), and **RECIP** (PSMA-PET). Matching the right criterion — and comparing like-with-like — is what makes a response call valid.

## Why Different Criteria

Size change (RECIST) can lag or misrepresent biology: **GIST** responds by becoming hypodense without shrinking, **immunotherapy** can cause transient pseudoprogression, and **metabolic** change often precedes anatomic change. Each framework encodes the response signal that best predicts benefit for its setting.

## RECIST 1.1 (Anatomic)

- **Target lesions:** up to 5 measurable lesions (≤ 2 per organ); sum of **longest diameters** (short axis for nodes).
- **Response categories:**

| Category | Definition (summary) |
|---|---|
| Complete response (CR) | Disappearance of all target lesions |
| Partial response (PR) | **≥ 30% decrease** in sum of diameters |
| Progressive disease (PD) | **≥ 20% increase** (and ≥ 5 mm absolute) or **new lesions** |
| Stable disease (SD) | Neither PR nor PD |

Non-target lesions and new lesions are also assessed.

## PERCIST 1.0 (Metabolic, FDG)

- Measures **SUL-peak** (SUV normalized to **lean body mass**) of the **single hottest** lesion, against a **normal-liver reference** (mean liver SUL + tolerance).
- **Same scanner/protocol and uptake time** across serial scans (metabolic change is highly technique-sensitive).
- **Categories:** **complete metabolic response (CMR)**, **partial metabolic response (PMR, ≥ 30% SUL-peak decrease)**, **stable metabolic disease (SMD)**, **progressive metabolic disease (PMD, ≥ 30% increase or new lesions)**.

Metabolic response frequently **precedes** anatomic (RECIST) change.

## Disease/Therapy-Specific Frameworks

| Framework | Setting | Signal |
|---|---|---|
| **Choi** | GIST (imatinib) | ≥ 10% size **or** ≥ 15% CT-density decrease |
| **iRECIST** | Immunotherapy | Requires **confirmation** of progression (pseudoprogression) |
| **Deauville / Lugano** | Lymphoma | 5-point uptake vs blood pool/liver |
| **RECIP 1.0 (PROMISE)** | PSMA-PET (prostate) | Tumor-volume change + new lesions |
| **PERCIST** | Broad FDG oncology | SUL-peak metabolic response |

## The Immunotherapy Caveat

Checkpoint-inhibitor therapy can produce **pseudoprogression** (transient enlargement/new inflammatory uptake before response) and **immune-related** FDG-avid inflammation. **iRECIST** addresses this by requiring **confirmation** of progression on a follow-up scan (unconfirmed progression = "iUPD"; confirmed = "iCPD"), preventing premature "failure" calls.

## Common Pitfalls

- **Mismatching** the criterion to the setting (e.g. size-only RECIST for GIST, missing a Choi response).
- Comparing **PERCIST across different scanners/protocols/uptake times** (metabolic change is technique-sensitive — like PERCIST-forbidden).
- Calling **immunotherapy progression** without confirmation (pseudoprogression).
- Ignoring **new lesions**, which define progression across frameworks.

## Board Pearls

{K} Use the framework that fits the biology: **RECIST 1.1** (anatomic size) on CT/MRI; **PERCIST 1.0** (metabolic **SUL-peak** of the hottest lesion vs a **liver** reference) for FDG. **Metabolic response often precedes anatomic change.**

{H} **GIST** needs **Choi** (density + size, not size alone); **immunotherapy** needs **iRECIST** (confirm progression — pseudoprogression); **lymphoma** uses **Deauville/Lugano**; **PSMA-PET** uses **RECIP**. Matching the criterion to the setting is half the job.

{D} **PERCIST demands like-with-like:** same scanner/protocol/uptake time across serial scans (metabolic values are technique-sensitive), SUL normalized to **lean body mass**, and a **normal-liver** reference. **New lesions define progression** in every framework, and **immune-related inflammation/pseudoprogression** must be confirmed before calling failure.

## Related Pages

- Reference: **Lymphoma staging & response (Lugano/Deauville)**, **PSMA-PET reporting (PROMISE/PSMA-RADS)**.
- Therapy: **Theranostics response criteria** (RECIP/PROMISE/PCWG3).
- Disease: **Sarcoma & GIST** (Choi), **melanoma** (immunotherapy response); tracer: **FDG**.

## Figure / Diagram Suggestions

- A **criterion selector** by setting (RECIST / PERCIST / Choi / iRECIST / Deauville / RECIP).
- A **metabolic-before-anatomic** timeline (SUL falls before size).
- An **iRECIST** confirmation flow (iUPD → confirm → iCPD).

## Self-Check (Board-Style)

<details><summary><strong>Q1.</strong> A GIST on imatinib is unchanged in size but markedly hypodense. Which criterion captures the response, and how?</summary>
<p><strong>Answer:</strong> <strong>Choi criteria</strong> — a ≥ 10% size <strong>or</strong> ≥ 15% CT-density decrease counts as response; size-only RECIST would miss it.</p>
</details>

<details><summary><strong>Q2.</strong> What does PERCIST measure, and what reference organ anchors it?</summary>
<p><strong>Answer:</strong> The <strong>SUL-peak</strong> (lean-body-mass-normalized SUV) of the <strong>single hottest lesion</strong>, referenced to <strong>normal liver</strong> — with a ≥ 30% decrease defining partial metabolic response.</p>
</details>

<details><summary><strong>Q3.</strong> On immunotherapy, a lesion enlarges with new FDG-avid nodes at week 8. How should progression be handled?</summary>
<p><strong>Answer:</strong> Treat as <strong>unconfirmed</strong> (possible pseudoprogression/irAE) — <strong>iRECIST</strong> requires <strong>confirmation on a follow-up scan</strong> before calling confirmed progression.</p>
</details>

<details><summary><strong>Q4.</strong> Why must serial PERCIST studies use the same scanner and uptake time?</summary>
<p><strong>Answer:</strong> Metabolic (SUL) values are <strong>highly technique-sensitive</strong> (reconstruction, uptake time, calibration); comparing mismatched protocols invalidates the response call.</p>
</details>
