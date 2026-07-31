---
type: physics
title: MIRD Dosimetry — Framework & Worked Examples
chapter: dosimetry-safety
order: 10
subtitle: Cumulated activity, S-values, and organ-dose calculation, step by step
aliases: [MIRD, dosimetry, cumulated activity, time-integrated activity, residence time, S value, absorbed dose, OLINDA, effective half-life, marrow dose, kidney dose, BED, worked example]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "16 min"
tags: [physics, dosimetry, therapy, quantitation, basic-principles]
related_tracers: []
related_diseases: []
related_therapies: [dosimetry-theranostics]
related_calculators: [decay, dosimetry, effective-dose]
related_pitfalls: []
---

## Quick Answer

The **MIRD schema** computes absorbed dose as **D = Ã × S**: the **cumulated (time-integrated) activity Ã** in a source region times the **S-value** (mean dose to a target per unit cumulated activity in the source). For a mono-exponentially clearing region, **Ã = 1.443 × T_eff × A₀(region)**, where **1.443 = 1/ln2** and **T_eff** combines physical and biological half-lives. S-values come from anatomic models (OLINDA/EXM, MIRD pamphlets). Therapy dosimetry then respects **organ-at-risk limits** — classically **~2 Gy marrow**, **~23 Gy kidney (BED)**, and lung limits for Y-90.

## The Core Equation

**D (target ← source) = Ã(source) × S(target ← source)**

Summed over all source regions:

**D(target) = Σ_source Ã(source) × S(target ← source)**

- **Ã** = cumulated activity = ∫ A(t) dt (units: MBq·h or µCi·h) — the **total number of decays** in the source region.
- **S** = dose per unit cumulated activity (mGy/MBq·h) — encodes emission energy, geometry (absorbed fraction), and target mass.

## Cumulated Activity (Ã) and Residence Time (τ)

For a region that takes up a fraction and clears **mono-exponentially**:

**Ã = 1.443 × T_eff × A₀(region)**

- **1.443 = 1/ln2** (the mean lifetime factor).
- **T_eff** from **1/T_eff = 1/T_physical + 1/T_biological**.
- **Residence time τ = Ã / A₀** (hours) — a normalized way to tabulate uptake.

Real kinetics are measured from **serial imaging/blood sampling** (multi-time-point SPECT/CT for Lu-177), fitting the time–activity curve and integrating it — the labor-intensive heart of patient-specific dosimetry.

## The S-Value

**S(target ← source) = (Σᵢ Δᵢ φᵢ) / m_target**

- **Δᵢ** = mean energy emitted per decay for emission *i*.
- **φᵢ** = absorbed fraction (fraction of energy *i* deposited in the target).
- **m_target** = target mass.

For **non-penetrating radiation (α, β)**, energy is deposited **locally** (self-dose φ ≈ 1 within the source; ≈ 0 to distant targets) — the reason β/α therapy dose is dominated by **self-dose**. For **penetrating γ**, φ < 1 and cross-organ doses matter. S-values are tabulated for reference phantoms and scaled to patient organ mass.

## Worked Example 1 — Effective Half-Life & Cumulated Activity

A ¹⁷⁷Lu-DOTATATE administration; consider an organ with **biological half-life 20 h** for Lu-177 (**physical T½ = 6.65 d = 159.6 h**):

1. **1/T_eff = 1/159.6 + 1/20 = 0.00627 + 0.0500 = 0.0563 h⁻¹ → T_eff = 17.8 h.**
2. If the organ's peak activity A₀(region) = **500 MBq**:
   **Ã = 1.443 × 17.8 h × 500 MBq = 12,843 MBq·h.**
3. **Residence time τ = Ã / A₀ = 1.443 × T_eff = 25.7 h.**

The biological clearance dominates T_eff here — a physically long-lived nuclide can deliver far less dose than its physical half-life implies when biological clearance is fast (see effective half-life).

## Worked Example 2 — Organ Absorbed Dose

Using Ã from above and a (illustrative) organ **S-value = 0.15 mGy/(MBq·h)**:

**D = Ã × S = 12,843 MBq·h × 0.15 mGy/(MBq·h) ≈ 1,930 mGy ≈ 1.9 Gy.**

Add contributions from **other source regions** (cross-dose) via their Ã × S(target ← source) terms for the total organ dose. In practice, software (OLINDA/EXM, patient-specific voxel dosimetry) performs the summation across the reference phantom.

## Organ-at-Risk Limits (Therapy)

| Organ | Classic limit | Context |
|---|---|---|
| **Bone marrow** | ~ **2 Gy** | Historically dose-limiting (e.g. I-131 therapy blood dosimetry) |
| **Kidney** | ~ **23 Gy** (up to ~27–40 with modifiers) as **BED** | Dose-limiting for PRRT — hence amino-acid renoprotection |
| **Lung** | ≤ **30 Gy single / 50 Gy cumulative** | Y-90 radioembolization (from MAA lung-shunt) |

**Biologically effective dose (BED)** corrects absorbed dose for **dose rate and repair** — important because a given Gy delivered slowly (radionuclide therapy) differs biologically from the same Gy delivered acutely (external beam). This is why kidney tolerance is expressed as BED for PRRT.

## Patient-Specific vs Fixed-Activity

Most therapy is delivered at **fixed/empiric activity** (e.g. 7.4 GBq Lu-177-DOTATATE × 4; 200 mCi I-131). **Dosimetry-guided** dosing — serial SPECT/CT (or I-124 PET), time–activity fitting, S-value/voxel dose — is used where the therapeutic ratio is tight (extensive disease, renal impairment, pediatrics) and is an active area (personalized dosimetry improved Y-90 outcomes in DOSISPHERE-01).

## Board-Level Synthesis

{K} **D = Ã × S.** Cumulated activity **Ã = 1.443 × T_eff × A₀(region)** (1.443 = 1/ln2); **T_eff** combines physical and biological half-lives; the **S-value** = mean-energy × absorbed-fraction ÷ target mass. Sum Ã × S over all source regions for the total organ dose.

{H} For **α/β (non-penetrating)** emitters, dose is dominated by **self-dose** (absorbed fraction ≈ 1 within the source; ≈ 0 at distance); for **γ**, cross-organ dose matters. This is the physical reason particle emitters are therapeutic and γ emitters are for imaging.

{D} Therapy respects **organ-at-risk limits** — ~**2 Gy marrow**, ~**23 Gy kidney (BED)**, and Y-90 **lung** limits — expressed where relevant as **BED** to account for dose rate and repair (a radionuclide-therapy Gy is not an external-beam Gy). Most therapy is **fixed-activity**; **patient-specific dosimetry** (serial SPECT/CT, OLINDA/voxel methods) is reserved for tight-therapeutic-ratio settings.

## Related Pages

- Physics: **Physics of nuclear medicine** (effective half-life, LET), **dosimetry & theranostics**.
- Therapy: the radionuclide-therapy pages (Lu-177-DOTATATE/PSMA, I-131, Y-90).
- Calculators: **decay**, **dosimetry**, **effective dose**.

## Figure / Diagram Suggestions

- A **D = Ã × S** schematic (time–activity curve → cumulated activity → S-value → dose).
- A **self-dose vs cross-dose** absorbed-fraction diagram (β/α vs γ).
- An **organ-at-risk limits** panel (marrow/kidney/lung with BED note).

## Self-Check

<details><summary><strong>Q1.</strong> Write the MIRD dose equation and define each term.</summary>
<p><strong>Answer:</strong> <strong>D = Ã × S</strong> — Ã is the <strong>cumulated (time-integrated) activity</strong> (total decays in the source), and S is the <strong>dose to the target per unit cumulated activity</strong> (mean energy × absorbed fraction ÷ target mass).</p>
</details>

<details><summary><strong>Q2.</strong> An organ has a physical T½ of 159.6 h and biological T½ of 20 h. What is the effective half-life?</summary>
<p><strong>Answer:</strong> 1/T_eff = 1/159.6 + 1/20 = 0.0563 h⁻¹ → <strong>T_eff ≈ 17.8 h</strong> — biological clearance dominates.</p>
</details>

<details><summary><strong>Q3.</strong> Why is dose from a beta-emitting radiopharmaceutical dominated by self-dose?</summary>
<p><strong>Answer:</strong> Beta particles are <strong>non-penetrating</strong> — the absorbed fraction is ≈ 1 within the source region and ≈ 0 at a distance, so energy is deposited locally (little cross-organ dose).</p>
</details>

<details><summary><strong>Q4.</strong> Why is kidney tolerance in PRRT expressed as biologically effective dose (BED) rather than absorbed dose?</summary>
<p><strong>Answer:</strong> BED corrects for <strong>dose rate and tissue repair</strong> — a Gy delivered slowly by a radionuclide differs biologically from the same Gy delivered acutely by external beam, so BED better predicts renal tolerance.</p>
</details>
