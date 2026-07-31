---
type: protocol
title: Quantitative Lung Perfusion (Split Function)
chapter: pulmonary
order: 30
subtitle: Predicting postoperative lung function before resection, and differential function for transplant/LVRS
aliases: [quantitative lung perfusion, split lung function, differential lung function, predicted postoperative FEV1, ppoFEV1, ppoDLCO, lung resection workup, pneumonectomy, lobectomy, lung transplant perfusion, MAA quantification]
isotope_label: "⁹⁹ᵐTc-MAA"
modality: [Planar, SPECT]
evidence_level: High
review_status: physician-reviewed
last_updated: 2026-07-28
reading_time: "6 min"
tags: [pulmonary, perfusion, quantitative, surgery]
related_tracers: [maa]
related_protocols: [vq-scan-pe]
related_diseases: []
related_calculators: []
related_pitfalls: []
---

## Quick Answer

Quantitative perfusion scintigraphy with **⁹⁹ᵐTc-MAA** measures how much each lung (and region) contributes to total pulmonary blood flow, which stands in for **regional lung function**. Its main use is **predicting postoperative lung function before lung-cancer resection**: the **predicted postoperative FEV₁ (ppoFEV₁)** and **ppoDLCO** estimate what the patient will retain after surgery. A **ppoFEV₁ or ppoDLCO below ~40% predicted** marks **high perioperative risk** and prompts further testing (e.g. cardiopulmonary exercise testing). The same split-function data guide **lung transplant**, **lung volume reduction surgery (LVRS)**, and differential-function questions.

## Why it matters

A patient may have borderline whole-lung spirometry yet tolerate resection well if the diseased, to-be-removed lung contributes little function — or, conversely, be far riskier than spirometry suggests if the resected portion is doing most of the work. **Perfusion quantifies that regional contribution**, turning "how bad are the lungs overall" into "how much function remains after we take this part out."

## Technique

- **⁹⁹ᵐTc-MAA** perfusion imaging with **anterior and posterior planar** views; regional counts are combined as the **geometric mean** to correct for depth, and divided into lung halves or thirds (upper/middle/lower). **SPECT** improves regional (lobar) quantification.
- Each region's **percentage of total perfusion counts** is reported. Ventilation can be added, but **perfusion is the standard** for split-function prediction.

## Predicting postoperative function

{K} **ppoFEV₁ = preoperative FEV₁ × (fraction of perfusion contributed by the lung/region that REMAINS).** For a **pneumonectomy**, multiply preop FEV₁ by the **% perfusion of the non-operated lung**; for a **lobectomy**, use the fraction of remaining functional segments (segment-counting) or regional perfusion. Compute **ppoDLCO** the same way. **ppoFEV₁ or ppoDLCO < ~40% predicted → high risk** — proceed to cardiopulmonary exercise testing (VO₂max) rather than straight to surgery.

{H} Express results as **% predicted**, not absolute liters — risk thresholds are defined against predicted values, and a raw ppoFEV₁ in liters can mislead across body sizes.

## Worked example

A patient with preop FEV₁ 2.0 L (80% predicted) needs a **right pneumonectomy**; perfusion shows the **left lung contributes 55%**. ppoFEV₁ ≈ 2.0 × 0.55 = **1.1 L (~44% predicted)** — above the ~40% high-risk threshold, so resection is likely tolerable pending exercise testing. Had the left lung contributed only 40%, ppoFEV₁ would fall to ~0.8 L (~32% predicted), flagging **high risk**.

## Other uses

{D} The same split-function data inform **lung transplant** (differential function; which native lung to replace or the contribution of a single transplanted lung), **lung volume reduction surgery** (targeting the most destroyed, least-perfused regions), and rare **congenital/vascular** questions. In transplant and LVRS the question shifts from "predict what remains after removal" to "which regions are functionally worthless and safe to remove or bypass."

## High-Yield Pearls

- ppoFEV₁ = preop FEV₁ × fraction of perfusion to the **remaining** lung; the same math gives ppoDLCO.
- **ppoFEV₁ or ppoDLCO < ~40% predicted** = high perioperative risk → cardiopulmonary exercise testing.
- Use the **geometric mean** of anterior + posterior counts to correct for depth; SPECT sharpens lobar quantification.

## Common Pitfalls

- Reporting absolute liters instead of **% predicted** against risk thresholds.
- Using perfusion fractions from **planar** without geometric-mean correction (anterior-only over-weights anterior structures).
- Forgetting that **DLCO** is an independent predictor — a normal ppoFEV₁ with a low ppoDLCO still flags risk.

## Related Pages

- Perfusion agent: **⁹⁹ᵐTc-MAA**; base study: **V/Q scan & pulmonary embolism**.

## Self-Check

<details><summary><strong>Q1.</strong> Write the formula for predicted postoperative FEV₁ before a pneumonectomy.</summary>
<p><strong>Answer:</strong> <strong>ppoFEV₁ = preoperative FEV₁ × (% perfusion of the non-operated lung)</strong> — the fraction of total perfusion contributed by the lung that remains.</p>
</details>

<details><summary><strong>Q2.</strong> What ppoFEV₁ / ppoDLCO threshold flags high perioperative risk, and what is the next step?</summary>
<p><strong>Answer:</strong> Below <strong>~40% predicted</strong> → high risk; proceed to <strong>cardiopulmonary exercise testing (VO₂max)</strong> rather than directly to resection.</p>
</details>

<details><summary><strong>Q3.</strong> Why combine anterior and posterior planar counts as a geometric mean?</summary>
<p><strong>Answer:</strong> To <strong>correct for depth/attenuation</strong> so each region's perfusion fraction is accurate (a single projection over- or under-weights structures by depth).</p>
</details>

<details><summary><strong>Q4.</strong> A patient's ppoFEV₁ is adequate but ppoDLCO is ~35% predicted. Interpretation?</summary>
<p><strong>Answer:</strong> Still <strong>high risk</strong> — DLCO is an <strong>independent</strong> predictor of postoperative complications, so a low ppoDLCO flags risk even with an acceptable ppoFEV₁.</p>
</details>

## Key References

- ACCP / ERS-ESTS guidelines on physiologic evaluation before lung resection (ppoFEV₁, ppoDLCO, exercise testing).
- SNMMI/EANM guidance on quantitative lung perfusion scintigraphy and split-function calculation.
