---
type: physics
title: Radiation Detection & Instrumentation
chapter: instrumentation
order: 10
subtitle: Gamma cameras, collimators, PET detectors, dose calibrators, and quality control
aliases: [gamma camera, scintillation detector, collimator, photomultiplier, NaI crystal, CZT, dose calibrator, well counter, PET detector, LSO, BGO, coincidence, quality control, uniformity, center of rotation]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "13 min"
tags: [instrumentation, physics, quality-control, basic-principles]
related_tracers: []
related_protocols: []
related_diseases: []
related_calculators: []
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

Nuclear medicine detects the photons emitted by radiopharmaceuticals. The **gamma camera** (scintillation crystal + photomultipliers + a **collimator** that defines direction) produces planar and SPECT images from single gammas. **PET** instead detects the two 511-keV photons from positron annihilation in **coincidence**, needing no physical collimator — giving higher sensitivity and resolution. **Dose calibrators** and **well counters** quantify activity, and a defined **quality-control** program keeps all of it accurate.

## The Gamma Camera (SPECT)

A **sodium-iodide (NaI(Tl))** crystal (or CZT semiconductor) converts gamma photons to light/charge; **photomultiplier tubes** (or direct readout) localize and quantify each event via **Anger logic**. Because gammas travel in all directions, a **collimator** (lead septa) accepts only photons traveling in a defined direction — the fundamental **resolution/sensitivity trade-off** in SPECT:

- **Low-energy high-resolution** vs **high-sensitivity** collimators trade counts for sharpness.
- Higher-energy isotopes (I-131) need **medium/high-energy** collimators.
- **CZT (solid-state)** cameras improve energy resolution and enable compact, high-sensitivity cardiac systems.

## PET Detection

Positron annihilation yields **two 511-keV photons ~180° apart**. Detecting both within a **coincidence window** defines the line of response — **electronic collimation** — which is why PET is far more sensitive than SPECT. **Detector crystals** (LSO/LYSO, historically BGO) are chosen for high stopping power and fast timing. **Time-of-flight (TOF)** uses the tiny arrival-time difference to localize the annihilation along the line, improving signal-to-noise (especially in larger patients).

## Detector Materials at a Glance

| Detector | Used in | Note |
|---|---|---|
| NaI(Tl) | Gamma cameras | Good light yield; standard SPECT crystal |
| CZT (CdZnTe) | Solid-state cameras | Direct conversion; better energy resolution; cardiac/dedicated systems |
| LSO/LYSO | PET | Fast, dense — enables TOF |
| BGO | (older) PET | Dense but slower timing |

## Non-Imaging Instruments

- **Dose calibrator:** an **ionization chamber** measuring administered activity before every dose — the daily accuracy check behind therapy and diagnostics.
- **Well counter:** high-sensitivity counting of small samples (blood dosimetry, wipe tests).
- **Survey / GM meters:** contamination and exposure monitoring for radiation safety.

## Quality Control (Representative)

| Instrument | QC (typical cadence) |
|---|---|
| Gamma camera | **Daily** uniformity/energy peak; periodic resolution, linearity, SPECT **center-of-rotation** |
| PET/CT | **Daily** normalization/blank; periodic calibration; CT QC |
| Dose calibrator | **Daily** constancy; periodic accuracy, linearity, geometry |

## The Collimator Is the SPECT Bottleneck

In SPECT, the **collimator** — not the crystal — sets the resolution/sensitivity trade-off, because it discards all photons except those traveling in a defined direction. PET needs **no physical collimator** (coincidence = electronic collimation), which is why PET has fundamentally higher sensitivity and resolution than SPECT.

## Matching the Collimator to the Isotope

Use a **collimator energy rating matched to the isotope**: **low-energy** for Tc-99m (140 keV) and Tl-201; **medium/high-energy** for I-131 (364 keV) and Ga-67. A low-energy collimator with a high-energy isotope produces **septal-penetration artifacts** (star/streak patterns) that mimic or obscure disease.

## Reporting / QC Impact

- Daily **uniformity** and **energy-peak** checks catch non-uniformities that project as **ring/patchy** SPECT artifacts.
- Periodic **center-of-rotation**, resolution, and linearity checks preserve reconstruction fidelity.
- PET/CT daily **normalization/blank** and cross-calibration keep **SUV** quantitative.
- The **dose calibrator** stands behind every administered activity — its daily **constancy** check is non-negotiable; geometry/linearity errors propagate directly into patient dose.

## Common Pitfalls

- **Non-uniformity / center-of-rotation** errors producing SPECT ring/artifact patterns.
- **Low-energy collimator with a high-energy isotope** → septal-penetration artifacts.
- **CT-based attenuation misregistration** on hybrid systems from patient motion/respiration.
- Uncorrected **dose-calibrator** errors propagating into administered activity.

## Board Pearls

{K} The **collimator is the resolution-limiting element of SPECT** (it discards most photons); PET's **coincidence detection removes it**, giving PET fundamentally higher sensitivity and resolution. **TOF** further improves PET signal-to-noise.

{H} **Match collimator energy to the isotope** — a low-energy collimator with **I-131 (364 keV)** causes **septal-penetration (star) artifacts**. The **dose calibrator** is the instrument behind every administered activity; its daily constancy check is non-negotiable.

{D} **Daily gamma-camera uniformity/energy-peak** checks catch non-uniformities that become **ring/patchy SPECT artifacts**; **center-of-rotation**, resolution, and linearity checks preserve reconstruction fidelity. On **PET/CT**, daily normalization/blank and cross-calibration keep SUV quantitative, and **CT–emission misregistration** (motion/respiration) is the classic hybrid artifact.

## Related Pages

- Related: **Physics of nuclear medicine**, **SPECT/PET & hybrid imaging**, **radiopharmaceuticals & production**.
- Pitfalls: **Pearls, pitfalls & normal variants** (free-pertechnetate, collimator artifacts).

## Figure / Diagram Suggestions

- A **gamma-camera** cross-section (collimator → crystal → PMTs → Anger logic).
- **SPECT collimator** vs **PET coincidence** (physical vs electronic collimation).
- A **QC artifact** plate (non-uniformity ring, septal-penetration star, misregistration defect).

## Self-Check (Board-Style)

<details><summary><strong>Q1.</strong> Why does PET have higher sensitivity and resolution than SPECT?</summary>
<p><strong>Answer:</strong> PET uses <strong>coincidence detection (electronic collimation)</strong> and needs no physical collimator, whereas SPECT's <strong>lead collimator discards most photons</strong> — the collimator is SPECT's fundamental resolution/sensitivity bottleneck.</p>
</details>

<details><summary><strong>Q2.</strong> An I-131 scan shows star/streak artifacts. What instrumentation error is likely?</summary>
<p><strong>Answer:</strong> Use of a <strong>low-energy collimator with a high-energy isotope</strong> (I-131, 364 keV) → <strong>septal penetration</strong>. Use a medium/high-energy collimator.</p>
</details>

<details><summary><strong>Q3.</strong> What does the dose calibrator's daily constancy check protect against?</summary>
<p><strong>Answer:</strong> Errors in the measured <strong>administered activity</strong> — which would directly affect patient dose and quantitation; constancy (with linearity/accuracy/geometry) keeps it reliable.</p>
</details>

<details><summary><strong>Q4.</strong> What does time-of-flight (TOF) add to PET?</summary>
<p><strong>Answer:</strong> It uses the <strong>arrival-time difference</strong> of the two 511-keV photons to localize the annihilation <strong>along the line of response</strong>, improving signal-to-noise (notably in larger patients).</p>
</details>
