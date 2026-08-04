---
type: physics
title: Quality Control Procedures
chapter: instrumentation
order: 20
subtitle: Gamma camera, SPECT, PET/CT, dose calibrator, and generator QC, cadence and pass criteria
aliases: [quality control, QC, uniformity, flood, center of rotation, COR, bar phantom, spatial resolution, linearity, dose calibrator constancy linearity accuracy geometry, NEMA, normalization, blank scan, Mo-99 breakthrough, aluminum]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "15 min"
tags: [instrumentation, physics, quality-control, basic-principles]
related_tracers: []
related_diseases: []
related_therapies: []
related_calculators: []
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

A defined **quality-control program** keeps imaging quantitative and detects failures before they mimic disease. The essentials: **gamma camera** — daily **uniformity** and energy peak, periodic **spatial resolution/linearity** (bar phantom) and **SPECT center-of-rotation (COR)**; **PET/CT** — daily **normalization/blank** and cross-calibration; **dose calibrator** — daily **constancy**, periodic **linearity, accuracy, geometry**; **generator** — **Mo-99 breakthrough (≤ 0.15 µCi/mCi)** and **aluminum (≤ 10 µg/mL)**. Each test has a cadence and an acceptance criterion; failing one has a characteristic artifact.

## Gamma Camera (SPECT) QC

| Test | Cadence | What it detects / criterion |
|---|---|---|
| **Energy peak (photopeak)** | **Daily** | Correct window centering; drift causes count loss/artifact |
| **Uniformity (flood)** | **Daily** | Non-uniform detector response → ring/patchy SPECT artifacts; integral/differential uniformity (commonly ≤ ~5% for CFOV) |
| **Spatial resolution & linearity (bar phantom)** | **Weekly** | Four-quadrant bar phantom; smallest resolved bars = resolution; bar straightness = linearity |
| **Center of rotation (COR)** | **Weekly–monthly** | SPECT reconstruction alignment; COR error → "tuning-fork"/doughnut ring artifacts and blurring |
| **Tomographic uniformity / sensitivity** | Periodic | System sensitivity (cpm/µCi) and SPECT uniformity |

**Extrinsic** floods include the collimator (test the clinical system); **intrinsic** floods are without the collimator (test the detector). A **non-uniformity** projects as a **ring artifact** at the corresponding radius on SPECT — the single most important reason daily uniformity is mandatory.

## PET/CT QC

| Test | Cadence | Purpose |
|---|---|---|
| **Daily normalization / blank scan** | **Daily** | Detector-block stability; drift degrades uniformity/quantitation |
| **Calibration / well-counter cross-calibration** | Periodic | Keeps **SUV** quantitative (scanner ↔ dose calibrator ↔ clock) |
| **CT QC** | Per CT program | Attenuation-map accuracy, CT number/water |
| **NEMA NU-2 performance** | Acceptance/annual | Resolution, sensitivity, scatter fraction, **NECR**, image quality |

A miscalibrated **cross-calibration** (scanner, dose calibrator, and clock must agree) silently biases **SUV** — a quantitation error, not a visual one.

## Dose Calibrator QC

The instrument behind **every administered activity** — its QC is non-negotiable:

| Test | Cadence | Method / criterion |
|---|---|---|
| **Constancy** | **Daily** | Long-lived reference source (Cs-137, Co-57); reading stable within ~±5–10% |
| **Accuracy** | **Annual** (and at install) | NIST-traceable source(s); within ~±5% (±10% action) |
| **Linearity** | **Quarterly** | Decay method or shield (Calicheck) method across the activity range |
| **Geometry** | **At installation** | Volume/container-dependence correction factors |

## Well Counter & Survey Instruments

- **Well counter:** daily **constancy** and energy calibration; efficiency for quantitative counting (blood dosimetry, wipe tests).
- **Survey / GM meters:** **annual calibration**, daily **battery/constancy** check; used for contamination and exposure surveys and package/area monitoring.

## Generator & Radiopharmaceutical QC

| Test | Limit | Note |
|---|---|---|
| **Mo-99 breakthrough** | **≤ 0.15 µCi Mo-99 / mCi Tc-99m** | Radionuclidic purity, at administration |
| **Aluminum (Al³⁺)** | **≤ 10 µg/mL** | Column breakthrough (colorimetric strip); excess disrupts labeling/colloids |
| **Radiochemical purity** | typically **≥ 90–95%** | Chromatography; free-pertechnetate / hydrolyzed-reduced species |
| **Sterility/endotoxin** | Per USP | Compounded and PET products |

## Failure → Artifact Map

| QC failure | Characteristic artifact |
|---|---|
| Non-uniformity | **Ring** artifact on SPECT (at the defect radius) |
| COR error | **Doughnut / tuning-fork** blurring, point-source ring |
| Wrong photopeak/energy | Count loss, degraded contrast |
| Collimator–isotope mismatch | **Septal-penetration star** (e.g. low-energy collimator with I-131) |
| Cross-calibration error | Biased **SUV** (silent quantitative error) |
| Mo-99 breakthrough | Added dose, degraded images, high-energy contamination |

## Board-Level Synthesis

{K} The **daily** anchors are **gamma-camera uniformity + energy peak**, **PET normalization/blank**, and **dose-calibrator constancy**. The **periodic** anchors are **bar-phantom resolution/linearity** and **SPECT COR** (weekly–monthly), and **dose-calibrator linearity (quarterly)/accuracy (annual)/geometry (install)**.

{H} A **non-uniformity projects as a ring artifact** at the corresponding SPECT radius, and a **COR error** causes doughnut/tuning-fork blurring — the two failures most likely to mimic or obscure disease, and the reason their QC is frequent.

{D} Two limits anchor generator radionuclidic/chemical purity: **Mo-99 breakthrough ≤ 0.15 µCi/mCi** and **aluminum ≤ 10 µg/mL**. The **dose calibrator** underlies every administered activity — daily **constancy**, quarterly **linearity**, annual **accuracy**, and **geometry** at install — and PET **cross-calibration** (scanner ↔ dose calibrator ↔ clock) keeps **SUV** trustworthy, a quantitation error that is invisible on the image.

## Related Pages

- Physics: **Radiation detection & instrumentation**, **counting statistics & ROC** (chi-square/constancy), **radiopharmaceuticals & production** (generator QC).
- Pitfalls: **Pearls, pitfalls & normal variants** (artifacts).

## Figure / Diagram Suggestions

- A **QC cadence** calendar (daily/weekly/quarterly/annual by instrument).
- A **failure → artifact** plate (ring, doughnut, septal-penetration star).
- A **dose-calibrator four-test** schematic (constancy/accuracy/linearity/geometry).

## Self-Check

<details><summary><strong>Q1.</strong> Which gamma-camera QC tests are performed daily, and what artifact does a uniformity failure cause?</summary>
<p><strong>Answer:</strong> Daily <strong>uniformity (flood)</strong> and <strong>energy-peak</strong> checks; a non-uniformity projects as a <strong>ring artifact</strong> at the corresponding radius on SPECT.</p>
</details>

<details><summary><strong>Q2.</strong> What are the four dose-calibrator QC tests and their cadences?</summary>
<p><strong>Answer:</strong> <strong>Constancy (daily)</strong>, <strong>linearity (quarterly)</strong>, <strong>accuracy (annual)</strong>, and <strong>geometry (at installation)</strong>.</p>
</details>

<details><summary><strong>Q3.</strong> State the Mo-99 breakthrough and aluminum limits for a Tc-99m generator eluate.</summary>
<p><strong>Answer:</strong> <strong>Mo-99 ≤ 0.15 µCi per mCi Tc-99m</strong> (at administration) and <strong>aluminum ≤ 10 µg/mL</strong>.</p>
</details>

<details><summary><strong>Q4.</strong> A SPECT study shows a doughnut/tuning-fork blurring artifact. Which QC parameter is likely off?</summary>
<p><strong>Answer:</strong> The <strong>center of rotation (COR)</strong> — misalignment causes point-source ring/doughnut and tomographic blurring.</p>
</details>
