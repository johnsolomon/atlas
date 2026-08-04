---
type: reference
title: Radionuclides & Tracers at a Glance
chapter: radiopharmacy
order: 8
subtitle: Side-by-side comparison of the major radionuclides (emission, half-life, production) and radiopharmaceuticals (target, modality, use, and matched therapy)
aliases: [radionuclide comparison, isotope table, half-life table, tracer comparison, radiopharmaceutical table, emission table, production generator cyclotron reactor, PET isotopes, SPECT isotopes, therapy isotopes]
review_status: physician-reviewed
last_updated: 2026-08-03
reading_time: "6 min"
tags: [reference, radiopharmacy, physics, tracers]
related_tracers: [fdg, psma-11, dotatate]
related_protocols: []
related_calculators: [decay]
---

## Quick Answer

Two lookup tables for fast comparison. The first sorts the **radionuclides** by what they emit, how long they last, and how they are made, which is what determines whether an isotope images, treats, or both. The second sorts the **radiopharmaceuticals** by target, modality, and primary use, with the matched therapy for the theranostic pairs. For the interactive, filterable version organized by mechanism class, see the **[Radiopharmaceutical Compendium](#/radiopharmaceutical-compendium)**; for the decay math, the **[decay calculator](#/tool-decay)**.

## Radionuclides at a glance

Half-life sets the logistics (generator, cyclotron, or reactor, and how far a dose can travel) and, with biological clearance, the dose delivered. Emission type sets the role: **positrons** annihilate to 511 keV pairs for PET; a single **γ** in the ~100–360 keV window images on a gamma camera; **β⁻** and **α** deposit energy locally to treat.

| Radionuclide | Decay / main emission | Half-life | Production | Role |
|---|---|---|---|---|
| **F-18** | β⁺ · 511 keV | 110 min | Cyclotron | PET workhorse (FDG, NaF, PSMA, FES) |
| **Ga-68** | β⁺ · 511 keV | 68 min | **Ge-68/Ga-68 generator** | PET (DOTATATE, PSMA) |
| **C-11** | β⁺ · 511 keV | 20 min | Cyclotron (on-site) | PET (choline, methionine) |
| **N-13** | β⁺ · 511 keV | 10 min | Cyclotron (on-site) | PET (ammonia, myocardial perfusion) |
| **O-15** | β⁺ · 511 keV | 2 min | Cyclotron (on-site) | PET (water perfusion; research) |
| **Rb-82** | β⁺ · 511 keV | **75 s** | **Sr-82/Rb-82 generator** | PET myocardial perfusion |
| **Cu-64** | β⁺ / β⁻ / EC · 511 keV | 12.7 h | Cyclotron | PET (investigational; theranostic-capable) |
| **Zr-89** | β⁺ · 511 keV | 78 h (3.3 d) | Cyclotron | Immuno-PET (antibody labelling) |
| **Tc-99m** | IT · γ **140 keV** | 6.0 h | **Mo-99/Tc-99m generator** | SPECT workhorse (~most SPECT studies) |
| **I-123** | EC · γ 159 keV | 13.2 h | Cyclotron | SPECT (thyroid, MIBG, DaTscan) |
| **In-111** | EC · γ 171 / 245 keV | 2.8 d | Cyclotron | SPECT (octreotide, labelled WBC) |
| **Ga-67** | EC · γ 93 / 185 / 300 keV | 3.3 d (78 h) | Cyclotron | SPECT (infection / inflammation) |
| **Tl-201** | EC · Hg X-rays ~69–80 keV | 73 h | Cyclotron | SPECT (perfusion / viability; legacy) |
| **I-131** | β⁻ (606 keV) · γ **364 keV** | 8.0 d | Reactor | Therapy **and** imaging (thyroid, MIBG) |
| **Lu-177** | β⁻ (~500 keV) · γ 113 / 208 keV | 6.65 d | Reactor | Therapy; imageable (DOTATATE, PSMA) |
| **Y-90** | β⁻ (2.28 MeV) · **pure β** | 64 h (2.67 d) | Reactor / generator | Therapy (radioembolization, ibritumomab); no imaging γ |
| **Ra-223** | **α** | 11.4 d | Decay of Ac-227 | Therapy (bone-dominant prostate) |
| **Ac-225** | **α** (decay chain) | 10 d | Th-229 / accelerator | Therapy (PSMA; investigational) |
| **Sm-153** | β⁻ · γ 103 keV | 46 h | Reactor | Bone-pain palliation (imageable) |
| **Sr-89** | β⁻ · pure β | 50.5 d | Reactor | Bone-pain palliation |
| **P-32** | β⁻ · pure β | 14.3 d | Reactor | Polycythemia vera, effusions (historical) |

## Radiopharmaceuticals at a glance

Colour dots follow the atlas's consistent per-tracer colours. The matched therapy column names the therapeutic partner where the target is a theranostic pair.

| Tracer | Isotope | Half-life | Target / mechanism | Modality | Primary use | Matched therapy |
|---|---|---|---|---|---|---|
| <span class="tdot" style="--tc:#C99700"></span>**FDG** | F-18 | 110 min | Glucose metabolism (GLUT / hexokinase) | PET | Oncology staging & response, infection, viability, brain | — |
| <span class="tdot" style="--tc:#7B4BC4"></span>**PSMA** (Ga-68 / F-18) | Ga-68 / F-18 | 68 / 110 min | PSMA (prostate) | PET | Prostate staging & recurrence; RLT selection | ¹⁷⁷Lu- / ²²⁵Ac-PSMA |
| <span class="tdot" style="--tc:#0E8C6A"></span>**DOTATATE** | Ga-68 | 68 min | Somatostatin receptor 2 | PET | NET staging; PRRT selection | ¹⁷⁷Lu-DOTATATE |
| <span class="tdot" style="--tc:#2E7D32"></span>**FDOPA** | F-18 | 110 min | AADC / catecholamine pathway | PET | Parkinsonism, NET, glioma | — |
| <span class="tdot" style="--tc:#B03A78"></span>**FES** | F-18 | 110 min | Estrogen receptor | PET | ER-positive breast cancer | (guides endocrine therapy) |
| <span class="tdot" style="--tc:#3B6EA5"></span>**Fluciclovine** | F-18 | 110 min | Amino-acid transport | PET | Prostate biochemical recurrence | — |
| <span class="tdot" style="--tc:#3B6EA5"></span>**Choline** | C-11 / F-18 | 20 / 110 min | Cell-membrane synthesis | PET | Prostate recurrence; parathyroid | — |
| <span class="tdot" style="--tc:#A83232"></span>**Rubidium-82** | Rb-82 | 75 s | K⁺ analog (perfusion) | PET | Myocardial perfusion | — |
| <span class="tdot" style="--tc:#0E7490"></span>**N-13 ammonia** | N-13 | 10 min | Perfusion | PET | Myocardial perfusion | — |
| <span class="tdot" style="--tc:#B03030"></span>**Sestamibi** | Tc-99m | 6 h | Mitochondrial / perfusion | SPECT | MPI; parathyroid | — |
| <span class="tdot" style="--tc:#5B6470"></span>**MDP / HDP** | Tc-99m | 6 h | Hydroxyapatite | SPECT | Bone scan | — |
| <span class="tdot" style="--tc:#5B6470"></span>**NaF** | F-18 | 110 min | Hydroxyapatite | PET | Bone (higher resolution) | — |
| <span class="tdot" style="--tc:#2563A6"></span>**MAG3** | Tc-99m | 6 h | Tubular secretion (ERPF) | SPECT | Renal function & drainage | — |
| <span class="tdot" style="--tc:#3F72AF"></span>**DTPA** | Tc-99m | 6 h | Glomerular filtration | SPECT | GFR, renography, aerosol ventilation | — |
| <span class="tdot" style="--tc:#1E7A8C"></span>**DMSA** | Tc-99m | 6 h | Cortical tubular binding | SPECT | Renal cortex / scarring | — |
| <span class="tdot" style="--tc:#0E7490"></span>**MAA** | Tc-99m | 6 h | Capillary micro-embolization | SPECT | Lung perfusion; Y-90 lung-shunt | — |
| <span class="tdot" style="--tc:#6B7280"></span>**Sulfur colloid** | Tc-99m | 6 h | Phagocytosis (reticuloendothelial) | SPECT | Liver/spleen, lymphoscintigraphy, GI bleed, marrow | — |
| <span class="tdot" style="--tc:#B0740A"></span>**HIDA** | Tc-99m | 6 h | Hepatocyte uptake & excretion | SPECT | Hepatobiliary (acute cholecystitis, leak) | — |
| <span class="tdot" style="--tc:#C24B6E"></span>**PYP** | Tc-99m | 6 h | ATTR amyloid binding | Planar / SPECT | Cardiac ATTR amyloidosis | — |
| <span class="tdot" style="--tc:#4A6FA5"></span>**Pertechnetate** | Tc-99m | 6 h | NIS trapping (not organified) | SPECT | Thyroid, Meckel, salivary | — |
| <span class="tdot" style="--tc:#B03030"></span>**Radioiodine** | I-123 / I-131 | 13 h / 8 d | NIS (trap & organify) | SPECT / planar | Thyroid uptake & scan; I-131 therapy | ¹³¹I |
| <span class="tdot" style="--tc:#C2410C"></span>**MIBG** | I-123 / I-131 | 13 h / 8 d | Norepinephrine transporter | SPECT | Pheo/paraganglioma, neuroblastoma | ¹³¹I-MIBG |
| <span class="tdot" style="--tc:#7A5C1E"></span>**Ioflupane** (DaTscan) | I-123 | 13 h | Dopamine transporter (DAT) | SPECT | Parkinsonian syndromes vs essential tremor / DLB | — |
| <span class="tdot" style="--tc:#556B2F"></span>**Gallium-67** | Ga-67 | 78 h | Transferrin / lactoferrin | SPECT | Infection / inflammation (niche) | — |
| <span class="tdot" style="--tc:#8A6D3B"></span>**Thallium-201** | Tl-201 | 73 h | K⁺ analog | SPECT | Perfusion / viability (legacy) | — |
| <span class="tdot" style="--tc:#8A5A2B"></span>**FAPI** | Ga-68 / F-18 | 68 / 110 min | Fibroblast activation protein | PET | Pan-cancer stroma (investigational) | (FAP-targeted, investigational) |

## How to read these

{K} Emission determines role: **positron emitters** (F-18, Ga-68, Rb-82) are for PET; **single-γ emitters** in the ~100–360 keV window (Tc-99m, I-123, In-111) are for SPECT; **β⁻ and α emitters** (Lu-177, Y-90, I-131, Ra-223, Ac-225) deposit energy locally to treat. **Half-life** determines whether a nuclide is made on-site (C-11, N-13, O-15, Rb-82), shipped from a regional cyclotron (F-18), eluted from a **generator** at the point of care (Tc-99m, Ga-68, Rb-82), or reactor-produced for therapy (I-131, Lu-177, Y-90). The **theranostic pairs** share a target across the two tables: image with the diagnostic isotope, treat with the therapeutic one on the same targeting molecule.

## Self-Check

<details><summary><strong>Q1.</strong> Which three radionuclides here are supplied by a generator at the point of care, and why does that matter?</summary>
<p><strong>Answer:</strong> <strong>Tc-99m</strong> (Mo-99/Tc-99m), <strong>Ga-68</strong> (Ge-68/Ga-68), and <strong>Rb-82</strong> (Sr-82/Rb-82). A generator lets a site produce a short-lived daughter on demand <strong>without an on-site cyclotron or same-day delivery</strong> — which is why Tc-99m dominates SPECT and Rb-82 enables PET perfusion without a cyclotron.</p>
</details>

<details><summary><strong>Q2.</strong> Why can Y-90 not be imaged the way Lu-177 and I-131 can?</summary>
<p><strong>Answer:</strong> Y-90 is essentially a <strong>pure β⁻ emitter with no imaging γ</strong>, whereas Lu-177 and I-131 emit imageable γ photons (permitting post-therapy SPECT). Y-90 distribution is inferred indirectly from <strong>bremsstrahlung SPECT or the small internal-pair-production PET signal</strong>.</p>
</details>

<details><summary><strong>Q3.</strong> Name the imaging isotope, therapy isotope, and shared target for the two flagship theranostic pairs.</summary>
<p><strong>Answer:</strong> <strong>Prostate/PSMA</strong> — image with Ga-68/F-18-PSMA, treat with ¹⁷⁷Lu-PSMA-617, target PSMA. <strong>NET/SSTR</strong> — image with ⁶⁸Ga-DOTATATE, treat with ¹⁷⁷Lu-DOTATATE, target somatostatin receptor 2.</p>
</details>

## Related Pages

- **[Radiopharmaceutical Compendium](#/radiopharmaceutical-compendium)** — the interactive, filterable version organized by mechanism class.
- **[Physics & Radiobiology](#/physics-nuclear-medicine)** — decay, emissions, and half-life in depth.
- **[Decay calculator](#/tool-decay)** — activity remaining after a given time.
