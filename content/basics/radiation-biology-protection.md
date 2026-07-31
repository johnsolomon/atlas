---
type: physics
title: Radiation Biology & Protection
chapter: physics
order: 40
subtitle: Stochastic vs deterministic effects, dose limits, and ALARA
aliases: [radiation biology, radiation protection, stochastic, deterministic, dose limits, ALARA, effective dose, tissue weighting, occupational dose, LNT, bremsstrahlung, inverse square]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "10 min"
tags: [physics, radiation-safety, basic-principles]
related_tracers: []
related_diseases: []
related_therapies: []
---

## Quick Answer

Radiation effects are either **stochastic** (probability of harm — chiefly cancer — rises with dose, **no threshold** under the linear-no-threshold model; severity is fixed) or **deterministic / tissue reactions** (occur **above a threshold**, with severity rising with dose — skin injury, marrow suppression, cataract). Protection follows **ALARA** (as low as reasonably achievable) using **time, distance, and shielding**, within regulatory **dose limits**. Diagnostic nuclear medicine operates in the **stochastic-risk** range; **therapy dosimetry** manages **deterministic organ limits** (marrow, kidney, lung, salivary).

## Key Quantities

| Quantity | Unit | Meaning |
|---|---|---|
| Absorbed dose | gray (Gy) | Energy deposited per unit mass |
| Equivalent dose | sievert (Sv) | Absorbed dose × **radiation weighting factor** (β/γ = 1; α = 20) |
| Effective dose | sievert (Sv) | Equivalent dose × **tissue weighting factors** — whole-body stochastic-risk scale |

**Effective dose** lets disparate procedures be compared on one stochastic-risk scale (e.g., an FDG-PET/CT vs a bone scan).

## Stochastic vs Deterministic

| | Stochastic | Deterministic (tissue reaction) |
|---|---|---|
| Threshold | **None** (LNT assumed) | **Yes** |
| Dose–effect | **Probability** ↑ with dose | **Severity** ↑ with dose above threshold |
| Latency | Years (cancer) | Hours–weeks (acute) or years (cataract) |
| Examples | Cancer, heritable effects | Skin erythema, marrow suppression, cataract, fertility, fetal effects |

## Dose Limits (Representative, ICRP-based)

- **Occupational:** ~**20 mSv/year** effective dose (averaged over defined periods); separate limits for **lens of the eye** (~20 mSv/yr under ICRP) and **extremities/skin** (~500 mSv/yr).
- **Public:** ~**1 mSv/year** effective dose.
- **Declared pregnancy:** additional constraint to protect the embryo/fetus (e.g., ~1 mSv over the declared term under some frameworks).

*(Exact limits are set by the applicable regulator — NRC/Agreement States or national body — verify locally; US NRC occupational limit is 50 mSv/yr, differing from ICRP's 20.)*

## ALARA in Practice

- **Time:** minimize time near sources.
- **Distance:** the **inverse-square law** — doubling distance quarters exposure — is the most powerful lever.
- **Shielding:** **lead** for gamma; for **beta emitters**, **low-Z material first** (acrylic/plastic) then lead, because lead alone generates penetrating **bremsstrahlung** X-rays.
- Plus **contamination control, dosimetry badges, and workflow design**.

## Worked Point

A tech stands 30 cm from a source reading 4 mR/hr. Stepping back to 90 cm (3×) drops exposure by **3² = 9×**, to ~0.44 mR/hr — distance beats most shielding for quick gains.

## Reporting / Practice Notes

- Frame diagnostic risk in **effective dose** terms; frame therapy limits in **absorbed dose to organs at risk**.
- Apply **ALARA** (time/distance/shielding) and document occupational dose (badges).
- Match **shielding to emission** (low-Z-then-lead for beta).

## Common Pitfalls

- Applying **deterministic-threshold thinking** to stochastic (no-threshold) cancer risk — or vice versa.
- **Shielding high-energy beta sources with lead alone** (generates bremsstrahlung).
- Confusing **NRC (50 mSv/yr)** with **ICRP (20 mSv/yr)** occupational limits.
- Neglecting the **inverse-square law** as the cheapest dose-reduction tool.

## Board Pearls

{K} Radiation effects split into **stochastic** (probability of cancer/heritable harm rises with dose, **no threshold** under LNT, severity fixed) and **deterministic/tissue reactions** (occur **above a threshold**, severity rises with dose — skin injury, marrow suppression, cataract). Diagnostic nuclear medicine lives in the **stochastic** range managed by **ALARA** (time, distance, shielding); **therapy dosimetry** manages **deterministic organ limits** (marrow, kidney, lung, salivary).

{H} **Effective dose** (Sv) weights equivalent dose by **tissue radiosensitivity**, letting disparate procedures compare on one stochastic-risk scale. The **inverse-square law** is the most powerful practical lever — tripling distance cuts exposure ~9×.

{D} Keep the dose chain straight: **absorbed dose (Gy)** → **equivalent dose (Sv)** (radiation weighting; α = 20) → **effective dose (Sv)** (tissue weighting). Representative limits: **ICRP ~20 mSv/yr occupational, ~1 mSv/yr public** — but the **US NRC uses 50 mSv/yr occupational**, so verify the applicable regulator. For **beta emitters**, shield with **low-Z first (acrylic) then lead**; lead alone generates penetrating **bremsstrahlung** and worsens the exposure it was meant to stop.

## Related Pages

- Physics: **PET/SPECT performance**, **radiation safety & patient release**; safety niches: contamination/accident management.

## Figure / Diagram Suggestions

- A **stochastic vs deterministic** dose–response pair (probability vs severity curves).
- An **inverse-square** exposure-vs-distance plot.
- A **beta-shielding** schematic (acrylic-then-lead vs bremsstrahlung from lead alone).

## Self-Check

<details><summary><strong>Q1.</strong> Classify radiation-induced cancer vs cataract as stochastic or deterministic, and state the defining difference.</summary>
<p><strong>Answer:</strong> Cancer is <strong>stochastic</strong> (no threshold; probability rises with dose); cataract is <strong>deterministic</strong> (threshold; severity rises with dose above it).</p>
</details>

<details><summary><strong>Q2.</strong> Why must a high-energy beta source be shielded with acrylic before lead?</summary>
<p><strong>Answer:</strong> Lead alone generates penetrating <strong>bremsstrahlung</strong> X-rays; a <strong>low-Z material (acrylic) first</strong> stops the betas with minimal bremsstrahlung, then lead attenuates residual photons.</p>
</details>

<details><summary><strong>Q3.</strong> A source reads 8 mR/hr at 25 cm. Approximately what is it at 100 cm?</summary>
<p><strong>Answer:</strong> Distance ×4 → exposure ÷16 → about <strong>0.5 mR/hr</strong> (inverse-square law).</p>
</details>

<details><summary><strong>Q4.</strong> What does effective dose (Sv) add beyond absorbed dose (Gy)?</summary>
<p><strong>Answer:</strong> It weights for <strong>radiation type</strong> (equivalent dose) and then <strong>tissue radiosensitivity</strong> (tissue weighting factors), giving a single <strong>whole-body stochastic-risk</strong> scale.</p>
</details>
