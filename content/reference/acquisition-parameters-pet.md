---
type: reference
title: Acquisition Parameters — PET
chapter: boards
order: 50
subtitle: Representative adult activity, uptake time, and acquisition by PET tracer
aliases: [PET protocol, PET acquisition, FDG dose, uptake time, PSMA protocol, DOTATATE protocol, amyloid PET, NaF, cardiac PET, bed time, weight-based activity]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "13 min"
tags: [reference, procedure, PET, quantitation]
related_tracers: [fdg, psma-11, dotatate]
related_diseases: []
related_therapies: []
related_calculators: [suv]
related_pitfalls: []
---

## Quick Answer

This is a **representative adult** PET-acquisition reference — tracer, typical activity, **uptake time**, and acquisition notes. For PET the parameters that most affect the result are the **uptake time** (fixed and consistent for quantitation), **patient preparation** (glucose for FDG; suppression vs promotion for cardiac), and **reconstruction/uptake-time matching** for serial **SUV**. Modern **TOF** scanners allow lower activities.

> ⚠️ Representative values for orientation — **verify against SNMMI/EANM procedure standards and local protocol**. Activity given in mCi (MBq); weight-based schemes (e.g. ~3–4 MBq/kg FDG) are increasingly standard.

## Oncology & General

| Tracer | Activity | Uptake time | Acquisition / prep |
|---|---|---|---|
| **¹⁸F-FDG (oncology)** | ~10–15 mCi (or ~3–4 MBq/kg; lower with TOF) | **~60 min** (55–75) | Fast 4–6 h, glucose < ~150–200; skull base→mid-thigh; ~1.5–3 min/bed (or continuous-bed) |
| **¹⁸F-FDG (brain)** | ~5–10 mCi | ~30–40 min | Quiet, dim room; dedicated brain acquisition |
| **¹⁸F-FES (breast, ER)** | ~6 mCi (222 MBq) | ~60–80 min | Hold ER-blocking therapy (false-negative) |
| **¹⁸F-NaF (bone)** | ~5–10 mCi | ~30–60 min | Low background; hydrate/void |
| **⁶⁸Ga/¹⁸F-FAPI** | agent-specific | ~10–60 min | Low liver/brain background |

## Prostate & Neuroendocrine

| Tracer | Activity | Uptake time | Notes |
|---|---|---|---|
| **⁶⁸Ga-PSMA-11** | ~1.8–2.2 mCi (~2 MBq/kg) | ~50–100 min | Furosemide/hydration to clear bladder for pelvic reads |
| **¹⁸F-DCFPyL (piflufolastat)** | ~9 mCi (333 MBq) | ~60 min | Sharper images; batch distribution |
| **¹⁸F-rhPSMA-7.3** | agent-specific | ~60 min | Low urinary excretion |
| **⁶⁸Ga-DOTATATE** | ~3–5 mCi (or weight-based) | ~45–90 min | Coordinate with somatostatin-analog timing |
| **⁶⁴Cu-DOTATATE** | ~4 mCi (148 MBq) | ~45–90 min | Longer half-life; delayed/centralized |

## Cardiac PET

| Study | Tracer | Activity | Acquisition / prep |
|---|---|---|---|
| **Perfusion** | **⁸²Rb** | ~30–60 mCi per rest/stress | **Dynamic list-mode** (~76 s half-life); pharmacologic stress; MBF/MFR |
| **Perfusion** | **¹³N-ammonia** | ~10–20 mCi | Dynamic; cyclotron; permits limited exercise |
| **Viability** | **¹⁸F-FDG** | ~10 mCi | **Promote** myocardial glucose (glucose ± insulin/clamp) + rest perfusion |
| **Sarcoid** | **¹⁸F-FDG** | ~10 mCi | **Suppress** myocardial glucose (high-fat/very-low-carb, fast, ± heparin) + rest perfusion |

## Neuro (Dementia)

| Tracer | Activity | Uptake time | Notes |
|---|---|---|---|
| **Amyloid** (florbetapir/florbetaben/flutemetamol) | ~10 mCi (370 MBq) | ~30–90 min (agent-specific) | Read by approved visual criteria (gray–white) |
| **Tau** (flortaucipir) | ~10 mCi | ~80 min | Regional/Braak-like distribution |
| **¹⁸F-FDG (dementia)** | ~5–10 mCi | ~30–40 min | Hypometabolism pattern |

## Cross-Cutting PET Principles

- **Uptake time must be fixed and consistent** across serial scans — it strongly affects **SUV** (and PERCIST comparisons).
- **Reconstruction** (OSEM iterations/subsets, PSF, TOF) changes SUV — use **matched** or **EARL-harmonized** reconstructions for cross-site/serial work.
- **Cross-calibration** (scanner ↔ dose calibrator ↔ clock) must be current for quantitative SUV.
- **Preparation is disease-specific** for cardiac FDG (suppress for sarcoid, promote for viability) and glucose-dependent for oncology FDG.

## Board-Level Synthesis

{K} For PET, **uptake time** (fixed ~60 min for FDG; agent-specific otherwise), **preparation** (glucose/fasting; suppress-vs-promote for cardiac FDG), and **reconstruction/uptake-time matching** are what determine a valid, comparable **SUV**. Modern **TOF** scanners permit **lower injected activities**.

{H} Two cardiac FDG preparations are opposite: **suppress** myocardial glucose for **sarcoid**, **promote** it for **viability**. **PSMA** pelvic reads benefit from **hydration/furosemide** to clear bladder activity; **DOTATATE** timing is coordinated with somatostatin-analog dosing.

{D} Activities are **representative and guideline-dependent** and increasingly **weight-based** (e.g. ~3–4 MBq/kg FDG, ~2 MBq/kg Ga-68-PSMA). Cross-site/serial **SUV** requires **matched or EARL-harmonized reconstruction** and current **cross-calibration**; uptake-time drift is a common, avoidable source of spurious SUV change.

## Related Pages

- Reference: **Acquisition parameters — SPECT & planar**, **FDG-PET preparation & physiologic uptake**, **quantitative thresholds & decision cutoffs**, **SUV harmonization (EARL)**.
- Physics: **PET & SPECT performance & reconstruction**.

## Figure / Diagram Suggestions

- A **tracer → activity → uptake-time → prep** PET protocol grid.
- A **cardiac-FDG suppress-vs-promote** side-by-side.

## Self-Check

<details><summary><strong>Q1.</strong> Why must FDG uptake time be fixed across serial oncologic scans?</summary>
<p><strong>Answer:</strong> SUV rises with uptake time; an inconsistent interval produces <strong>spurious SUV change</strong> and invalidates PERCIST-type comparison — keep ~60 min consistent.</p>
</details>

<details><summary><strong>Q2.</strong> How does cardiac FDG preparation differ between a sarcoid and a viability study?</summary>
<p><strong>Answer:</strong> <strong>Suppress</strong> myocardial glucose for sarcoid (high-fat/very-low-carb, fast, ± heparin); <strong>promote</strong> it for viability (glucose ± insulin/clamp).</p>
</details>

<details><summary><strong>Q3.</strong> What acquisition mode does Rb-82 cardiac PET require, and why?</summary>
<p><strong>Answer:</strong> <strong>Dynamic list-mode</strong> imaging begun immediately after infusion — because of Rb-82's <strong>~76-second half-life</strong> and to derive MBF/MFR.</p>
</details>

<details><summary><strong>Q4.</strong> What technique improves PSMA-PET pelvic evaluation, and why?</summary>
<p><strong>Answer:</strong> <strong>Hydration/furosemide</strong> to clear <strong>urinary bladder</strong> activity that would otherwise obscure pelvic disease/nodes.</p>
</details>
