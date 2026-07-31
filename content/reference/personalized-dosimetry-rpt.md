---
type: practice
title: Personalized vs Fixed-Activity Dosimetry
chapter: dosimetry-safety
order: 25
subtitle: Why radioligand therapy is still dosed like chemotherapy — and how evidence and AI are changing that
aliases: [personalized dosimetry, fixed activity dosing, dosimetry guided therapy, single time point dosimetry, DOSISPHERE, dose response RPT, tumor absorbed dose, theranostic dosimetry personalization, AI dosimetry]
isotope_label: "¹⁷⁷Lu · ⁹⁰Y"
modality: [PET, SPECT]
evidence_level: Moderate
review_status: physician-reviewed
last_updated: 2026-07-29
reading_time: "7 min"
tags: [dosimetry, theranostics, personalization, future]
related_tracers: []
related_protocols: []
related_diseases: []
related_pitfalls: []
---

## Quick Answer

Almost every external-beam radiation oncologist prescribes in **absorbed dose (Gray)**, yet most radioligand therapy (RPT) is still given as a **fixed administered activity** — the same number of gigabecquerels to every patient, regardless of how much radiation actually reaches the tumor or the organs at risk. This is a striking inconsistency: RPT *is* radiotherapy, and **absorbed dose varies several-fold between patients** given identical activity. **Dosimetry** measures the dose actually delivered (from post-therapy SPECT/CT or PET), and **personalized, dosimetry-guided dosing** adjusts activity to hit a tumor-dose target while respecting organ limits. The evidence that this matters is strongest in **⁹⁰Y radioembolization** (DOSISPHERE-01 showed personalized dosimetry improved response in HCC) and is accumulating for **PRRT and Lu-PSMA**. The historical barrier is **practical**, not conceptual: classical dosimetry requires **multiple SPECT/CT time points** and laborious segmentation. **Single-time-point protocols and AI-automated segmentation/dosimetry** are collapsing that burden — which is why automated dosimetry is widely seen as the change that will finally make personalized RPT routine.

## Why fixed activity leaves benefit on the table

{K} Give ten patients the same activity of ¹⁷⁷Lu-PSMA and the **tumor and kidney absorbed doses will differ widely** — driven by tumor burden, receptor density, renal function, and clearance kinetics. Fixed dosing therefore **under-treats** some patients (tumor dose below the threshold for response) while risking **avoidable toxicity** in others (organ dose near tolerance). Because RPT delivers **ionizing radiation**, the same **dose–response and dose–toxicity** relationships that govern external-beam therapy apply — which is the core argument that activity, not absorbed dose, is the wrong prescription unit.

## What the evidence shows

{H} Personalization is best proven where dosimetry is most tractable:

| Setting | Evidence | Takeaway |
|---|---|---|
| **⁹⁰Y radioembolization (HCC)** | **DOSISPHERE-01** (personalized vs standard dosimetry) | Personalized tumor-dose targeting **improved response** |
| **PRRT (¹⁷⁷Lu-DOTATATE)** | Dose–effect analyses; prospective dosimetry trials | Higher **tumor absorbed dose** associates with better outcome; renal dose tracks toxicity |
| **¹⁷⁷Lu-PSMA** | Emerging dose–response data | Wide inter-patient dose variation; personalization under active study |

{D} The counter-argument is honest: for β-emitters like ¹⁷⁷Lu, registration trials used **fixed activity** and showed benefit, prospective **outcome** trials proving personalized dosing is *superior* are still maturing, and dosimetry adds cost and complexity. The field is moving toward personalization, but the level-1 evidence base is still being built outside radioembolization.

## The practical bottleneck — and how it falls

{H} Classical dosimetry is demanding: **serial SPECT/CT** at several time points (e.g. ~4, 24, 96 h), image registration, organ and tumor **segmentation**, time–activity curve fitting, and dose calculation — per cycle, per patient. Two developments dismantle this:

- **Single-time-point (STP) dosimetry** — validated simplifications estimate absorbed dose from **one** post-therapy scan, cutting patient visits and workload with acceptable accuracy for many organs.
- **AI-automated segmentation and dosimetry** — deep learning contours organs and lesions and computes voxel dose in minutes, removing the manual step that made routine dosimetry impractical.

Together these turn dosimetry from a research-lab exercise into something a busy service can actually run every cycle — the operational key to personalization at scale.

## High-Yield Pearls

- RPT is radiotherapy, yet most is dosed as **fixed activity**, not **absorbed dose** — a several-fold inter-patient dose variation.
- **Dosimetry** measures delivered dose (post-therapy SPECT/CT/PET); **personalized dosing** targets tumor dose within organ limits.
- **DOSISPHERE-01** (⁹⁰Y in HCC) is the strongest evidence that personalized dosimetry improves response.
- The barrier was **practical** (multi-time-point SPECT/CT + manual segmentation) — **single-time-point** protocols and **AI automation** are removing it.
- Higher **tumor absorbed dose** generally tracks better outcomes; **kidney/marrow** dose tracks toxicity.

## Common Pitfalls

- Treating **administered activity** as if it were the delivered **dose** — they diverge widely.
- Assuming fixed dosing is optimal because registration trials used it — that shows *efficacy*, not *optimality*.
- Ignoring **single-time-point/AI** options and dismissing dosimetry as too laborious for routine use.

## Related Pages

- Framework: **Dosimetry in theranostics**, **MIRD dosimetry — worked examples**; evidence: **DOSISPHERE / Y-90 radioembolization**; frontier: **AI & machine learning in nuclear medicine**.

## Self-Check

<details><summary><strong>Q1.</strong> Why is dosing radioligand therapy by fixed administered activity considered a mismatch with how radiation is normally prescribed?</summary>
<p><strong>Answer:</strong> RPT delivers ionizing radiation, so the meaningful quantity is <strong>absorbed dose (Gy)</strong> — and identical activity yields <strong>several-fold different absorbed doses</strong> between patients, so activity is a poor surrogate for the actual tumor/organ dose.</p>
</details>

<details><summary><strong>Q2.</strong> Which trial and setting provide the strongest evidence that personalized dosimetry improves outcomes?</summary>
<p><strong>Answer:</strong> <strong>DOSISPHERE-01</strong> — personalized vs standard dosimetry in <strong>⁹⁰Y radioembolization for HCC</strong>, showing improved response with personalized tumor-dose targeting.</p>
</details>

<details><summary><strong>Q3.</strong> What has historically made routine dosimetry impractical, and what two developments are changing that?</summary>
<p><strong>Answer:</strong> The need for <strong>multiple post-therapy SPECT/CT time points plus manual segmentation</strong>; <strong>single-time-point protocols</strong> and <strong>AI-automated segmentation/dosimetry</strong> collapse that burden.</p>
</details>

<details><summary><strong>Q4.</strong> Give the general dose relationships that motivate personalization in PRRT.</summary>
<p><strong>Answer:</strong> Higher <strong>tumor absorbed dose</strong> tends to improve outcomes, while <strong>kidney (and marrow)</strong> absorbed dose tracks toxicity — so personalization aims to raise tumor dose while keeping organs at risk within tolerance.</p>
</details>

## Key References

- DOSISPHERE-01 (Garin E, et al., Lancet Gastroenterol Hepatol 2021) — personalized dosimetry in ⁹⁰Y radioembolization for HCC.
- MIRD/EANM dosimetry guidance; validation studies of single-time-point dosimetry and AI-automated organ/lesion segmentation for RPT.
