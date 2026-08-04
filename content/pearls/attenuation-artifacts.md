---
type: pattern
title: Attenuation & Misregistration Artifacts
chapter: pearls
order: 50
subtitle: When the correction, the CT, or the patient, not the tracer, creates the finding
aliases: [attenuation artifact, attenuation correction artifact, misregistration, halo artifact, truncation artifact, CT contrast artifact, breast attenuation, diaphragmatic attenuation, respiratory mismatch]
review_status: physician-reviewed
last_updated: 2026-07-28
reading_time: "6 min"
tags: [pattern, artifacts, instrumentation, pearls]
related_tracers: [fdg, sestamibi]
related_diseases: []
related_protocols: []
related_calculators: []
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

Many false findings on hybrid imaging come from the **attenuation-correction (AC) process** and from **misregistration between the emission and CT data**, not from tracer distribution. Dense material (metal, iodinated contrast, calcium), **breathing motion**, and **patient positioning** can create apparent uptake where there is none or erase real uptake. The universal defense is to **compare the attenuation-corrected and non-attenuation-corrected (NAC) images and inspect the fused CT**: an artifact behaves differently across those datasets than true disease.

## Why AC can lie

{K} PET and SPECT reconstruct quantitative images by using the **CT (or a transmission map) to correct for photon attenuation**. That correction assumes the emission and attenuation data describe the **same anatomy in the same place**. When they do not — because the patient breathed, moved, or has dense material the CT over-weights — the algorithm **redistributes counts incorrectly**, producing spurious hot or cold regions. The corrected image is only as trustworthy as the alignment and the CT it was built from.

## The core artifacts

**Misregistration (respiratory mismatch).** The classic example is a **curvilinear cold or hot band at the lung base/dome of the diaphragm/liver**, where CT (a fast breath-hold snapshot) and PET (averaged over many breaths) capture the diaphragm in different positions. A hepatic-dome lesion can be shifted into lung or vice versa. Checking the NAC images and the fused display — where the mislocation is obvious — resolves it.

**Dense-material (CT contrast, metal, calcium) over-correction.** High-attenuation material makes the CT assign excessive attenuation to that voxel, so AC **over-corrects and creates apparent uptake** on the AC image that is **absent on NAC**. Culprits: **IV/oral CT contrast**, hip prostheses and dental hardware, pacemakers, chemo ports, and contrast in the renal collecting system. The tell is focal "uptake" that vanishes on the NAC series and co-locates with dense material on CT.

**Halo artifact.** A **rim of apparent decreased activity around an intensely avid focus** (e.g. a brightly avid tumour or the bladder), an over-/under-correction reconstruction effect that can mimic or obscure adjacent disease.

**Truncation artifact.** When the patient's body extends **beyond the CT field of view** (arms at the sides, large body habitus), the missing anatomy is under-corrected, producing streaks or falsely altered peripheral activity.

## Cardiac SPECT MPI attenuation

{H} On myocardial perfusion SPECT, soft-tissue attenuation creates **fixed** apparent perfusion defects that mimic infarct: **anterior/anterolateral (breast)** attenuation in women and **inferior/inferolateral (diaphragm)** attenuation in men. Two tools separate artifact from scar: **gated wall-motion** (an attenuation artifact has **normal wall motion and thickening**; true scar is hypokinetic/akinetic) and **attenuation correction** or **prone/upright imaging** that redistributes the soft tissue. A fixed defect with preserved motion is the signature of attenuation, not infarction.

{D} Other MPI pitfalls in the same family: **patient motion** (blurring, "hurricane" sign), **subdiaphragmatic activity** (bowel/liver) creating reconstruction ramp artifacts adjacent to the inferior wall, and **breast-position variation** between stress and rest that mimics a reversible defect. Recognising these prevents both false-positive catheterisations and missed disease.

## The universal workflow

- {H} **Always review NAC alongside AC images.** Artifact-driven "uptake" from dense material disappears on NAC; true disease persists on both.
- **Inspect the fused CT** for metal, contrast, and diaphragm alignment.
- For cardiac SPECT, **read the gated cine** and use AC/prone imaging before calling a fixed inferior or anterior defect.
- When registration is poor, consider **re-processing or repeating** rather than over-interpreting.

## Self-Check

<details><summary><strong>Q1.</strong> Why can attenuation correction create a false hot spot from CT contrast or metal?</summary>
<p><strong>Answer:</strong> Dense material makes the CT assign excessive attenuation to that voxel, so AC <strong>over-corrects and adds apparent counts</strong>. The spurious "uptake" is present on the AC image but <strong>absent on the non-attenuation-corrected (NAC)</strong> series and co-locates with the dense material on CT.</p>
</details>

<details><summary><strong>Q2.</strong> What causes the curvilinear defect at the lung base/diaphragm, and how is it recognised?</summary>
<p><strong>Answer:</strong> <strong>Respiratory misregistration</strong> — CT (breath-hold) and PET (free-breathing average) capture the diaphragm in different positions, mislocating activity between liver dome and lung base. The fused display and NAC images reveal the mismatch.</p>
</details>

<details><summary><strong>Q3.</strong> On cardiac SPECT, how do you distinguish breast/diaphragm attenuation from true infarct?</summary>
<p><strong>Answer:</strong> A fixed defect with <strong>preserved wall motion and thickening on the gated images</strong> (plus resolution with attenuation correction or prone/upright imaging) indicates <strong>attenuation</strong>; true scar shows <strong>abnormal (hypo/akinetic)</strong> motion.</p>
</details>

<details><summary><strong>Q4.</strong> What single habit defends against most attenuation/misregistration artifacts?</summary>
<p><strong>Answer:</strong> <strong>Reviewing the non-attenuation-corrected images alongside the AC images and inspecting the fused CT</strong> — artifacts behave differently across those datasets than true tracer uptake.</p>
</details>

## Key References
- SNMMI/EANM guidance on PET/CT and SPECT/CT attenuation correction, misregistration, and artifact recognition.
- Nuclear cardiology literature on soft-tissue attenuation, gated wall-motion analysis, and attenuation-correction/prone imaging for MPI.
