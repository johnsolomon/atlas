---
type: protocol
title: FDG PET/CT in Oncology
chapter: oncology
order: 10
subtitle: SUV and its dependencies, PERCIST vs RECIST, and the physiologic and inflammatory pitfalls
aliases: [FDG oncology, SUV, SUVmax, PERCIST, RECIST, oncology PET, uptake time, partial volume, response assessment, staging]
isotope_label: "¹⁸F-FDG"
modality: [PET]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "6 min"
tags: [oncology, FDG, PET, response, SUV]
related_tracers: [fdg]
related_protocols: []
related_diseases: [lymphoma, head-neck-cancer]
related_calculators: []
related_pitfalls: [theranostics-response-criteria]
---

## Quick Answer

FDG PET/CT is the core oncologic imaging study for staging, restaging, treatment-response assessment, and radiotherapy planning across most solid and hematologic malignancies. Interpretation rests on recognizing physiologic and inflammatory uptake, understanding what **SUV** does and does not mean (it depends on uptake time, blood glucose, reconstruction, and lesion size), and applying the right **response framework** — **PERCIST** (metabolic) or **RECIST** (anatomic), and disease-specific criteria such as Deauville/Lugano in lymphoma.

## SUV and its dependencies

The standardized uptake value normalizes lesion activity to injected dose and body size (usually body weight, SUVbw; lean-body-mass SUL is used in PERCIST). It is a semiquantitative surrogate for metabolism, **not an absolute biological constant**, and is sensitive to:

- **Uptake time** — SUV rises with longer post-injection intervals; keep it consistent (~60 min).
- **Blood glucose** — hyperglycemia competes with FDG and lowers tumor SUV/sensitivity.
- **Reconstruction and scanner** — different algorithms/settings change SUV; compare only matched protocols.
- **Partial-volume effect** — small lesions (below ~2–3× resolution) have underestimated SUV.

{K} SUV is comparable across serial scans **only** when technique is held constant — same scanner, protocol, uptake time, and reference region. Treat SUV as a semiquantitative surrogate, not an absolute number.

## Response assessment: PERCIST vs RECIST

- **RECIST** measures anatomic tumor size on CT (unidimensional). It can misclassify metabolically responding tumors that have not yet shrunk, or scar that remains measurable.
- **PERCIST** measures the metabolic response using SUL peak of the most active lesion against a consistent reference (typically liver), classifying complete/partial metabolic response, stable, and progressive metabolic disease.
- **Disease-specific criteria** exist where they perform better — e.g. **Deauville/Lugano** for lymphoma.

Metabolic change often precedes anatomic change, which is why PET-based criteria detect response earlier.

{H} **PERCIST specifics (board favorite):** measure **SULpeak** (lean-body-mass–normalized, in a 1.2 cm spherical VOI) of the single most active lesion; the reference is a **1.5–3 cm sphere in normal right-lobe liver** (use blood pool if the liver is abnormal). **Complete metabolic response** = lesion activity falls to **≤ liver background**; **partial** = **≥30% decline** in SULpeak; **progressive** = **≥30% increase** or a **new** FDG-avid lesion. Measurable target requires lesion SUL **> 1.5× liver SUL + 2 SD**.

## High-yield board facts

{H} Learn the normal distribution and the two classic pitfall lists cold — most oncology PET questions turn on distinguishing physiologic/benign uptake from tumor, or remembering which cancers are FDG-low.

| Category | Must-know |
|---|---|
| Normal high uptake | Brain cortex, myocardium (variable), liver/spleen (liver = reference), renal collecting system/ureters/bladder (excreted), bowel, Waldeyer ring/tonsils, thymus (children/rebound), marrow, brown fat, muscle |
| Classic false **positives** (benign-avid) | Infection/abscess, granulomatous disease (sarcoid, TB, fungal), post-surgical/post-radiation inflammation, brown fat, skeletal muscle, bowel, thyroiditis, reactive nodes, **G-CSF** marrow/splenic uptake, talc pleurodesis, healing fracture |
| Classic false **negatives** (FDG-low tumors) | Well-differentiated **neuroendocrine**, some low-grade lymphomas, **prostate** adenocarcinoma, **renal cell** (variable), **HCC** (variable), **mucinous** adenocarcinoma (colorectal/ovarian), **lepidic/BAC** adenocarcinoma, **lobular** breast carcinoma, sub-cm lesions (partial volume), hyperglycemia-suppressed |
| Prep thresholds | Fast **4–6 h**; glucose **<150–200 mg/dL**; uptake **~60 min** (kept constant); SPN heuristic **SUV ~2.5** |

## Patient preparation (detail)

Preparation is what makes FDG-PET interpretable, and most avoidable pitfalls trace back to it:

- **Fasting 4–6 hours**; only water. Withhold IV dextrose and glucose-containing fluids.
- **Blood glucose** checked before injection — most protocols require it below ~150–200 mg/dL; hyperglycemia competes with FDG and lowers tumor uptake/sensitivity. Manage diabetics per protocol (timing of insulin/oral agents; avoid recent short-acting insulin driving FDG into muscle).
- **Uptake time ~60 min** (kept consistent across serial scans), rest in a warm, quiet room to minimize muscle and brown-fat uptake.
- Avoid strenuous activity for 24 h (muscle uptake); consider warming and, per local policy, measures to reduce brown fat.
- Note recent **G-CSF, chemotherapy, radiation, or surgery** — all alter uptake and interpretation timing.

## Immunotherapy-era response & pitfalls

Checkpoint-inhibitor and targeted therapies complicate FDG interpretation. **Pseudoprogression** and **immune-related adverse events** (sarcoid-like mediastinal/hilar nodes, thyroiditis, hypophysitis, colitis, pneumonitis) produce FDG-avid findings that mimic or coexist with tumor progression. Immune-adapted response frameworks (e.g. **iPERCIST / imPERCIST**) address the fact that a transient uptake increase or new lesions may not equal true progression — confirmation on follow-up or biopsy is often needed. Recognizing the pattern of immune-related uptake prevents both false calls of progression and missed treatment toxicity.

## High-Yield Pearls

- Report the uptake time, glucose, and injected activity — they are prerequisites for interpreting SUV.
- Know the normal FDG distribution (brain, myocardium, liver/spleen, bowel, urinary tract) cold; deviations drive both findings and pitfalls.
- Metabolic response (PERCIST) may lead anatomic response (RECIST) — choose the framework the question demands.

## Common Pitfalls

- Brown fat, muscle, and bowel uptake mistaken for nodal/metastatic disease.
- Post-treatment inflammation — surgery, radiation, infection, G-CSF marrow stimulation — causing false positives; timing of imaging matters.
- FDG-low tumors (some low-grade, mucinous, neuroendocrine) under-called.
- Comparing SUV across non-matched scans/scanners as though equivalent.

## Related Pages

- Tracer: **FDG**; physics: **SUV harmonization & EARL**; reporting: **Oncology response criteria (RECIST/PERCIST)**; pitfalls: **Incidental findings on FDG-PET**.

## Self-Check

<details><summary><strong>Q1.</strong> Name four factors that change SUV independent of tumor biology.</summary>
<p><strong>Answer:</strong> <strong>Uptake time, blood glucose, reconstruction/scanner, and lesion size (partial-volume effect)</strong>.</p>
</details>

<details><summary><strong>Q2.</strong> When does PERCIST detect response that RECIST misses?</summary>
<p><strong>Answer:</strong> When <strong>metabolic change precedes anatomic shrinkage</strong> — a responding tumor's SUL falls before its size does (or residual scar stays measurable).</p>
</details>

<details><summary><strong>Q3.</strong> A checkpoint-inhibitor patient shows new FDG-avid hilar nodes. What must you consider before calling progression?</summary>
<p><strong>Answer:</strong> <strong>Immune-related adverse events / sarcoid-like reaction and pseudoprogression</strong> — confirm on follow-up/biopsy; immune-adapted criteria (iPERCIST/imPERCIST) address this.</p>
</details>

<details><summary><strong>Q4.</strong> Why must you report uptake time, glucose, and injected activity?</summary>
<p><strong>Answer:</strong> They are <strong>prerequisites for interpreting SUV</strong> and for valid serial comparison (SUV is a semiquantitative surrogate, not an absolute constant).</p>
</details>

<details><summary><strong>Q5.</strong> Name five malignancies that are classically FDG-low (false-negative risk).</summary>
<p><strong>Answer:</strong> Any five of: <strong>well-differentiated neuroendocrine tumors, prostate adenocarcinoma, renal cell carcinoma, hepatocellular carcinoma, mucinous adenocarcinoma, lepidic/BAC lung adenocarcinoma, lobular breast carcinoma, and some low-grade lymphomas</strong>.</p>
</details>

<details><summary><strong>Q6.</strong> In PERCIST, what is the reference region and the threshold for partial metabolic response?</summary>
<p><strong>Answer:</strong> Reference = <strong>normal right-lobe liver</strong> (1.5–3 cm sphere; blood pool if liver abnormal); partial metabolic response = <strong>≥30% decline in SULpeak</strong> of the most active lesion.</p>
</details>
