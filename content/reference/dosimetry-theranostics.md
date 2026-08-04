---
type: pitfall
title: Dosimetry in Theranostics
chapter: dosimetry-safety
order: 20
subtitle: "How absorbed dose is estimated for radioligand therapy: MIRD, organs at risk, and post-therapy imaging"
aliases: [dosimetry, MIRD, absorbed dose, organ at risk, tumor dosimetry, PRRT dosimetry, Lu-177 dosimetry]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "5 min"
tags: [theranostics, physics, dosimetry]
related_tracers: [psma-11, dotatate]
related_protocols: []
related_diseases: []
---

## Quick Answer

Dosimetry estimates the radiation **absorbed dose (in gray, Gy)** delivered to tumors and to normal organs at risk during radioligand therapy. The standard framework is **MIRD**, which combines the time-integrated activity in a region (how much isotope is there and for how long) with tissue-specific dose factors. For Lu-177 therapies, serial post-therapy SPECT/CT (using Lu-177's imageable gammas) enables patient-specific dosimetry; the **kidneys, salivary glands, and bone marrow** are the principal organs at risk.

## Why it matters

Radioligand therapy can be delivered as **fixed activity** (the common regulatory-approved approach, e.g. 7.4 GBq per cycle) or **dosimetry-guided** (tailoring activity to keep organs at risk under threshold while maximizing tumor dose). Dosimetry supports safety (avoiding renal/marrow toxicity), may allow more cycles or higher activity in tolerant patients, and is increasingly expected for personalized therapy and trials.

## The MIRD framework (conceptually)

Absorbed dose to a target region = **time-integrated activity** in source regions × **S-values** (dose per unit cumulated activity, specific to the isotope and the source→target geometry).

The two inputs:

1. **Time-integrated activity (cumulated activity):** how much activity accumulates in a region and how long it stays — obtained from serial imaging at several time points to build a time–activity curve, then integrated.
2. **S-value / dose factor:** the physical conversion from cumulated activity to dose for a given isotope and anatomy (reference phantoms or, better, patient-specific voxel dosimetry).

## Data acquisition

- **Lu-177 (β⁻ + γ):** quantitative **SPECT/CT** at multiple post-therapy time points; the imageable gamma makes true patient-specific dosimetry feasible.
- **Y-90 (pure β):** **bremsstrahlung SPECT** or **Y-90 PET** (exploiting the small internal pair-production branch) to verify distribution; quantitative dosimetry is harder than for Lu-177.
- **Alpha emitters (Ac-225):** direct imaging is very difficult; dosimetry relies on surrogate imaging and models.

## Organs at risk

| Therapy | Key organs at risk |
|---|---|
| ¹⁷⁷Lu-PSMA | Kidneys, salivary/lacrimal glands, bone marrow |
| ¹⁷⁷Lu-DOTATATE | Kidneys (amino-acid protected), bone marrow |
| ⁹⁰Y radioembolization | Normal liver, lungs (via shunt), GI tract (non-target) |
| Ra-223 | Bone marrow |

## Dose = time-integrated activity × S-value

{K} The MIRD framework computes absorbed dose (gray) from two inputs: **time-integrated activity** (how much isotope is in a region and for how long — from serial imaging) times the **S-value** (isotope- and geometry-specific dose per unit cumulated activity). Fixed-activity regimens dominate approved practice, but dosimetry-guided dosing personalizes therapy and can allow more cycles in tolerant patients.

## Lu-177's built-in advantage, and the organs at risk

{K} Lu-177's **imageable gamma** lets every therapy cycle double as a **post-therapy SPECT/CT dosimetry** scan — a quality check pure-beta (Y-90) and alpha (Ac-225) emitters lack. Dose-limiting organs differ by agent: **kidneys/salivary (PSMA), kidneys/marrow (DOTATATE), marrow (Ra-223), liver/lungs (Y-90)** — and renal dose is cumulative across cycles.

## The accuracy nuances

{D} Single-time-point imaging poorly estimates time-integrated activity; multi-time-point sampling is more accurate. Reference-phantom S-values can misestimate dose in atypical anatomy — voxel-based methods are preferred where available. Y-90 dosimetry relies on bremsstrahlung SPECT or the small internal-pair-production PET signal; alpha-emitter dosimetry is hardest because directly imaging alphas is difficult. Lesional dosimetry (I-124 PET) supports a ~85 Gy response threshold that empiric activities often miss in bone.

## High-Yield Pearls

- Lu-177's gamma emission is a built-in advantage: every therapy cycle can double as a dosimetry and quality-assurance scan.
- Renal dose is cumulative — amino acid infusion (DOTATATE) reduces renal retention; track function across cycles.

## Common Pitfalls

- Single-time-point imaging poorly estimates the time-integrated activity; multi-time-point sampling is more accurate.
- Applying reference-phantom S-values to patients with atypical anatomy can misestimate dose — voxel-based methods are preferred where available.

## Self-Check

<details><summary><strong>Q1.</strong> State the two inputs to the MIRD absorbed-dose calculation.</summary>
<p><strong>Answer:</strong> <strong>Time-integrated (cumulated) activity</strong> in a region (from serial imaging) × the <strong>S-value</strong> (isotope- and geometry-specific dose per unit cumulated activity).</p>
</details>

<details><summary><strong>Q2.</strong> Why does Lu-177 permit patient-specific post-therapy dosimetry that Y-90 and Ac-225 do not easily allow?</summary>
<p><strong>Answer:</strong> Lu-177 emits an <strong>imageable gamma</strong>, so each cycle can double as a quantitative <strong>SPECT/CT dosimetry</strong> scan; Y-90 relies on bremsstrahlung/small PET signal and alpha emitters are very hard to image directly.</p>
</details>

<details><summary><strong>Q3.</strong> Name the principal organs at risk for ¹⁷⁷Lu-PSMA and for ¹⁷⁷Lu-DOTATATE.</summary>
<p><strong>Answer:</strong> PSMA → <strong>kidneys, salivary/lacrimal glands, bone marrow</strong>; DOTATATE → <strong>kidneys (amino-acid protected), bone marrow</strong>. Renal dose is cumulative across cycles.</p>
</details>

<details><summary><strong>Q4.</strong> Why is single-time-point imaging a limitation for dosimetry?</summary>
<p><strong>Answer:</strong> It <strong>poorly estimates the time-integrated activity</strong> (the area under the time–activity curve); multi-time-point sampling is more accurate.</p>
</details>

## Key References

- MIRD Committee pamphlets, SNMMI.
- EANM dosimetry committee guidance for ¹⁷⁷Lu-labeled radioligand therapy.
