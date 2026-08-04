---
type: reference
title: Quantitative Thresholds & Decision Cutoffs
chapter: boards
order: 10
subtitle: The numbers that change management, with their evidence and their caveats
aliases: [thresholds, cutoffs, decision values, Krenning, Deauville, PERCIST, H/CL, MFR, TID, lung shunt, dose limits, Mo-99 breakthrough, patient release, medical event]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "16 min"
tags: [reference, synthesis, quantitation, standards]
related_tracers: []
related_diseases: []
related_therapies: []
related_calculators: [suv, summed-scores, lung-shunt, effective-dose]
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

Most nuclear-medicine decisions turn on a small number of **quantitative cutoffs** — but almost none are absolute. They are **protocol-, software-, tracer-, and population-dependent**, and several (TID, MFR, drainage T½) require **lab-specific normal values**. This page collects the thresholds that actually change management, each with **what it decides**, its **evidence**, and the **caveat** that keeps it from being applied blindly. Read the number and the caveat together — the caveat is the expertise.

## Theranostics — Selection

| Parameter | Cutoff | Decides | Caveat |
|---|---|---|---|
| **Krenning score** | **≥ 3** (uptake ≥ liver) | SSTR-avidity sufficient for **¹⁷⁷Lu-DOTATATE** | Visual, reference-organ-dependent; higher-grade disease needs paired FDG |
| **PSMA positivity** | Uptake **> liver** at ≥ 1 site, no dominant FDG-discordant disease | Eligibility for **¹⁷⁷Lu-PSMA-617** (VISION-type) | Agent- and criteria-specific; FDG/PSMA discordance predicts poorer benefit |
| **Dual-tracer discordance** | FDG-positive / target-negative | Dedifferentiation → poorer PRRT/RLT benefit | Qualitative; changes plan more than any single SUV |

The selection principle is that **uptake intensity is a surrogate for target expression**, which predicts response — so these are *imaging* eligibility decisions, not purely histologic ones.

## Oncology — Response

| Framework | Cutoff | Decides | Caveat |
|---|---|---|---|
| **Deauville** | 1–3 vs 4–5 (vs blood pool/liver) | Complete metabolic response vs residual | Interim de-escalation may require 1–2; protocol-specific |
| **PERCIST** | **≥ 30% SUL-peak** decrease (PMR) | Metabolic response of hottest lesion | Same scanner/uptake-time; SUL (lean mass); liver reference |
| **RECIST 1.1** | **≥ 30%** ↓ (PR) / **≥ 20% (+≥5 mm)** or new lesion (PD) | Anatomic response | Size lags biology; misleading for GIST/immunotherapy |
| **Choi (GIST)** | ≥ 10% size **or** ≥ 15% CT-density ↓ | GIST response to imatinib | Metabolic/FDG change precedes even Choi |
| **Seminoma residual** | **> 3 cm**, imaged **≥ 6 weeks** post-chemo | FDG worth performing (viable vs fibrosis) | Not valid for NSGCT (teratoma FDG-negative) |

## Cardiac — Perfusion, Flow, Function

| Parameter | Cutoff | Decides | Caveat |
|---|---|---|---|
| **Ischemic burden** | commonly **> 10%** ischemic myocardium | flagged as high-risk / prompts discussion | **ISCHEMIA** reframed this — burden alone does not mandate revascularization |
| **Myocardial flow reserve (MFR)** | **< 2.0** abnormal (broadly) | balanced/microvascular disease; prognosis | Tracer/software/lab-specific — validate locally |
| **Transient ischemic dilation (TID)** | ~ **1.2** upper-limit-of-normal | high-risk marker | Protocol/software/normal-database-dependent |
| **Summed scores** | SSS 0–3 normal; 4–8 mild; 9–13 moderate; ≥ 14 severe | severity/extent | Software normal-database-dependent |

## Amyloid (ATTR)

| Parameter | Cutoff | Decides | Caveat |
|---|---|---|---|
| **Perugini grade** | **2–3** (+ negative monoclonal screen) | ATTR without biopsy (> 99% specific) | AL can be avid — monoclonal screen is mandatory |
| **H/CL ratio** | **≥ 1.5 at 1 h** (~1.3 at 3 h) | supports ATTR | SPECT must confirm myocardial (not blood-pool/rib) uptake |

## Thyroid

| Parameter | Cutoff | Decides | Caveat |
|---|---|---|---|
| **Ablation activity** | **30 mCi (1.1 GBq)** non-inferior to 100 mCi | low/intermediate-risk remnant ablation | HiLo/ESTIMABL1; higher activities for high-risk/structural disease |
| **TSH stimulation** | **> 30 mIU/L** | adequate uptake for RAI | Withdrawal or rhTSH; exclude iodine load |
| **Radioiodine age** | **avoided < 5 y**; low/calculated 5–10 y | pediatric therapy safety | Specialized-center dosimetry |

## Renal & GI

| Parameter | Cutoff | Decides | Caveat |
|---|---|---|---|
| **Diuretic drainage T½** | < 10 min non-obstructed; > 20 min obstructed; 10–20 equivocal | obstruction assessment | Only valid with hydration/empty bladder/adequate function; protocol (F+20 etc.) matters |
| **Gastric retention** | **> 60% at 2 h** and/or **> 10% at 4 h** | gastroparesis | Standardized meal + 4-h imaging required |
| **Gallbladder EF (CCK)** | **< 38%** | biliary dyskinesia | Standardize CCK infusion (rapid infusion → false-low) |

## Pulmonary / Radioembolization

| Parameter | Cutoff | Decides | Caveat |
|---|---|---|---|
| **Lung dose (Y-90)** | ≤ **30 Gy** single / ≤ **50 Gy** cumulative | deliverable ⁹⁰Y activity | Derived from MAA lung-shunt fraction |
| **Tumor-absorbed dose (glass, HCC)** | ~ **≥ 120 Gy** target | response likelihood | DOSISPHERE-01; personalized dosimetry |

## Radiation Safety & Regulatory (US NRC)

These are US NRC values (board-relevant); **ICRP recommendations differ** (e.g. ICRP occupational effective dose ~20 mSv/yr averaged).

| Parameter | Value (NRC) | Note |
|---|---|---|
| **Occupational** TEDE | **50 mSv/yr (5 rem)** | Lens **150 mSv**; skin/extremity **500 mSv** |
| **Declared-pregnant worker** | **5 mSv (0.5 rem)** over gestation | ~0.5 mSv/month, ALARA |
| **Public** | **1 mSv/yr (100 mrem)** | ≤ 2 mrem/hr in unrestricted areas |
| **Patient release** (10 CFR 35.75) | TEDE to others **≤ 5 mSv** | Common surrogates: **≤ 33 mCi I-131** or **≤ 7 mR/hr at 1 m**; written instructions if > 1 mSv |
| **Mo-99 breakthrough** | **≤ 0.15 µCi Mo-99 / mCi Tc-99m** | At administration (0.15 kBq/MBq) |
| **Aluminum** (Tc eluate) | **≤ 10 µg/mL** | Column breakthrough |
| **Radiochemical purity** | typically **≥ 90–95%** | Agent-specific |
| **Written directive** | any **therapy** dose; **I-131 > 30 µCi** | Required before administration |
| **Medical event** | dose differs by **≥ 0.5 Sv** EDE (or ≥ 0.5 Sv organ) **and ≥ 20%**, or wrong patient/drug/route/site | Reportable |

## Physics — Half-Lives (Reference)

| Nuclide | t½ | Nuclide | t½ |
|---|---|---|---|
| Tc-99m | 6.0 h | Ga-68 | 68 min |
| F-18 | 110 min | Rb-82 | 76 s |
| I-123 | 13.2 h | N-13 | 10 min |
| I-131 | 8.0 d | C-11 | 20 min |
| In-111 | 2.8 d | Lu-177 | 6.65 d |
| Tl-201 | 73 h | Y-90 | 64.1 h |
| Mo-99 | 66 h | Ac-225 | 10.0 d |
| Cu-64 | 12.7 h | Ra-223 | 11.4 d |

**Effective half-life:** 1/t½(eff) = 1/t½(physical) + 1/t½(biological) — the number that actually governs dose and release timing.

## How to Use These

{K} Every cutoff answers a **specific decision**, and almost every one carries a **caveat** that determines whether it applies: **Krenning ≥ 3** gates PRRT but needs paired FDG in higher grade; **Deauville 1–3** is a complete metabolic response *except* where an interim de-escalation protocol demands 1–2; **> 10% ischemic myocardium** is high-risk *but* ISCHEMIA showed burden alone does not mandate revascularization; **H/CL ≥ 1.5** supports ATTR *only* with a negative monoclonal screen and SPECT confirmation.

{H} Several thresholds are **not portable** — **MFR, TID, drainage T½, and summed-score bands** depend on tracer, software, and the lab's normal database; **PERCIST** demands the same scanner/uptake-time. Quoting a universal cutoff without local validation is a classic error.

{D} The **regulatory** numbers are jurisdiction-specific: the values above are **US NRC**; **ICRP** differs (occupational ~20 mSv/yr averaged). Patient-release, written-directive, and medical-event definitions are the ones most often tested and most often misremembered — and the **Mo-99 (0.15) / aluminum (10)** breakthrough limits anchor generator QC.

## Related Pages

- Reference: **Oncology response criteria (RECIST/PERCIST)**, **PSMA-PET reporting (PROMISE/PSMA-RADS)**, **Lugano/Deauville**, **ATA thyroid risk**.
- Physics/safety: **Physics of nuclear medicine**, **radiation biology & protection**, **radiation safety & patient release**.

## Figure / Diagram Suggestions

- A one-page **threshold-with-caveat** matrix by domain.
- A **decision-cutoff → management** flow for the top theranostic/cardiac numbers.

## Self-Check

<details><summary><strong>Q1.</strong> A referring oncologist quotes "MFR &lt; 2.0 = disease" from a paper using a different scanner. What is your caveat?</summary>
<p><strong>Answer:</strong> MFR thresholds are <strong>tracer-, software-, and lab-specific</strong>; the ~2.0 figure is a broad guide that must be <strong>validated against local normal values</strong> before being applied as a hard cutoff.</p>
</details>

<details><summary><strong>Q2.</strong> Grade-3 PYP uptake is present. Which single result determines whether this is diagnostic of ATTR, and what confirms the uptake is myocardial?</summary>
<p><strong>Answer:</strong> A <strong>negative monoclonal-protein screen</strong> (AL can be avid); <strong>SPECT</strong> confirms myocardial rather than blood-pool/rib uptake.</p>
</details>

<details><summary><strong>Q3.</strong> What is the US NRC patient-release limit, and two common surrogate criteria used to satisfy it?</summary>
<p><strong>Answer:</strong> TEDE to any other individual <strong>≤ 5 mSv</strong>; surrogates include <strong>≤ 33 mCi I-131</strong> retained activity or <strong>≤ 7 mR/hr at 1 m</strong>, with written instructions if the projected dose &gt; 1 mSv.</p>
</details>

<details><summary><strong>Q4.</strong> Why is "&gt; 10% ischemic myocardium = revascularize" an oversimplification?</summary>
<p><strong>Answer:</strong> <strong>ISCHEMIA</strong> showed that in stable CAD, ischemia burden alone did not identify a survival benefit from routine invasive management — the number flags risk and prompts discussion, it does not mandate revascularization.</p>
</details>
