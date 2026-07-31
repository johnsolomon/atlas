---
type: reference
title: Radiopharmaceutical Targets & Uptake Mechanisms
chapter: radiopharmacy
order: 30
subtitle: Mechanism → target → clinical and theranostic consequence
aliases: [uptake mechanisms, radiopharmaceutical targets, tracer mechanisms, NIS, SSTR, PSMA, NET transporter, hydroxyapatite, GLUT, extraction fraction, target expression]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "15 min"
tags: [reference, synthesis, molecular-imaging, radiopharmaceuticals]
related_tracers: [fdg, psma-11, dotatate]
related_diseases: []
related_therapies: []
related_calculators: []
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

A radiopharmaceutical's behavior — where it goes, what it means, and whether it can be paired with a therapeutic isotope — follows from its **uptake mechanism and molecular target**. Grouping tracers by mechanism (metabolic trapping, active transport, receptor binding, physical microembolization, chemisorption, blood-pool retention) makes their **normal biodistribution, characteristic artifacts, and theranostic potential** predictable rather than memorized. This page organizes the atlas's tracers by mechanism and draws the clinical consequence of each.

## Why Mechanism Predicts Everything Downstream

The same property that produces the signal produces the **physiologic biodistribution** (hence the normal-variant "mimics"), the **labeling-failure pattern**, and the **eligibility logic** for therapy. A tracer taken up by the sodium-iodide symporter images the thyroid *and* free pertechnetate lands in stomach/salivary tissue *and* the therapeutic isotope of the same handling (I-131) treats iodine-avid disease — one mechanism, three consequences.

## Metabolic Trapping

| Tracer | Mechanism / target | Clinical consequence |
|---|---|---|
| **FDG** | GLUT transport + hexokinase phosphorylation (trapped as FDG-6-P) | Broad oncology/inflammation/viability; hyperglycemia competes; well-differentiated HCC clears it (G6Pase) |
| **N-13-ammonia** | Diffusion + metabolic trapping (glutamine synthetase) | Cardiac PET perfusion; high, flow-stable extraction |
| **NaF** | Fluoride–hydroxyl exchange in hydroxyapatite | Bone PET; images bone *reaction*, not tumor |

## Active Transport

| Tracer | Mechanism / target | Clinical consequence |
|---|---|---|
| **Radioiodine (I-123/131)** | NIS **trapping + organification** | Thyroid imaging/therapy; the original theranostic; MTC (no NIS) fails |
| **Pertechnetate** | NIS **trapping only** (no organification); gastric/salivary uptake | Thyroid trapping, Meckel, salivary; its map = the free-pertechnetate artifact |
| **MIBG** | Norepinephrine transporter (uptake-1), vesicular storage | Pheo/para, neuroblastoma; drug interference; theranostic with I-131-MIBG |
| **Sestamibi / tetrofosmin** | Potential-driven diffusion → mitochondrial retention | MPI (flow) and parathyroid (mitochondria-rich adenoma); P-gp efflux |
| **Thallium-201 / Rb-82** | K⁺ analog via Na⁺/K⁺-ATPase | Viability (Tl redistribution); cardiac PET (Rb); extraction falls at high flow |
| **MAG3** | Tubular secretion (OAT) — high extraction | Dynamic renography; images well in poor function |
| **DTPA** | Glomerular filtration (no secretion/reabsorption) | True GFR marker; poor images in CKD |
| **DMSA** | Proximal-tubular cortical binding/retention | Cortical map (scars, split function) |
| **FDOPA** | LAT amino-acid transport + AADC decarboxylation | Pheo/para, NET, glioma, striatum |
| **Fluciclovine** | Amino-acid transport (ASCT2/LAT1) | Prostate recurrence (low urinary excretion) |

## Receptor / Antigen Binding

| Tracer | Target | Clinical / theranostic consequence |
|---|---|---|
| **DOTATATE** | SSTR2 | NET imaging → **¹⁷⁷Lu-DOTATATE**; physiologic spleen/adrenal/pituitary/uncinate |
| **PSMA ligands** | GCPII/FOLH1 (tumor cells; **neovascular** in RCC) | Prostate imaging → **¹⁷⁷Lu-PSMA**; salivary/renal/ganglion uptake |
| **FES** | Estrogen receptor | Whole-body ER phenotyping; ER-blocker false-negatives |
| **FAPI** | Fibroblast activation protein (stroma) | FDG-low/desmoplastic tumors; low liver/brain background |
| **Ioflupane** | Presynaptic dopamine transporter (DAT) | Deficit (not disease); normal excludes degenerative parkinsonism |
| **Amyloid ligands** | β-pleated-sheet plaque | Negative excludes AD amyloid; positive rises with age |
| **Tau ligands** | Paired-helical-filament tau | Tracks stage/topography better than amyloid |
| **Girentuximab** | CAIX (ccRCC) | ⁸⁹Zr characterization (ZIRCON) → ¹⁷⁷Lu (investigational) |
| **Anti-CD20 (ibritumomab)** | CD20 (B cells) | Radioimmunotherapy; crossfire kills antigen-negative neighbors |

## Physical / Compartmental Mechanisms

| Tracer | Mechanism | Clinical consequence |
|---|---|---|
| **MAA** | Capillary **microembolization** (particle > capillary) | Lung perfusion; Y-90 simulation/lung-shunt gate; R-to-L shunt → systemic activity |
| **Sulfur colloid** | RES phagocytosis (**size-dependent**) | Liver/spleen (large), marrow/lymphatic (small/filtered); colloid shift |
| **Labeled RBC** | Intravascular blood-pool retention | MUGA, hemangioma fill-in, GI bleed (appears-and-moves) |
| **Labeled WBC** | Neutrophil chemotaxis to infection | Infection (± marrow scan for the incongruence rule) |
| **HMPAO / ECD** | Lipophilic BBB crossing → intracellular fixation | Perfusion "snapshot" at injection (ictal SPECT, brain death) |
| **MDP / HDP** | Chemisorption to hydroxyapatite | Osteoblastic bone reaction (sensitive, not specific) |
| **PYP** | Binds amyloid-associated microcalcification | ATTR cardiac amyloid (monoclonal screen + SPECT) |
| **Ga-67** | Transferrin/lactoferrin at inflammation/tumor | Legacy infection/sarcoid/lymphoma |

## The Theranostic Corollary

{K} A mechanism is a **theranostic pair** when the same targeting handling can carry a diagnostic *and* a therapeutic isotope: **NIS** (I-123 → I-131), **SSTR2** (Ga-68-DOTATATE → ¹⁷⁷Lu-DOTATATE), **PSMA** (Ga-68/¹⁸F → ¹⁷⁷Lu/²²⁵Ac), **NET/uptake-1** (I-123-MIBG → I-131-MIBG), **CD20** (antibody + ⁹⁰Y), and — emerging — **CAIX** (⁸⁹Zr → ¹⁷⁷Lu-girentuximab) and **FAP**. The **DOTA chelator** is what makes the metal-based pairs interchangeable at near-identical biodistribution.

## The Artifact Corollary

{H} A tracer's **normal biodistribution is its artifact list**. Free-pertechnetate labeling failures reproduce the **NIS/gastric/salivary** map; DOTATATE's physiologic **uncinate/spleen/adrenal/pituitary** uptake mimics tumor; PSMA's **celiac ganglion/salivary/renal** uptake mimics nodes; MAA's clumping or a **right-to-left shunt** sends activity systemically. Knowing the mechanism is knowing the false positive.

## The Extraction & Kinetics Corollary

{D} Mechanism sets **quantitative behavior**: high-extraction tubular **MAG3** images poor kidneys where filtered **DTPA** fails; **Rb-82/Tl** extraction *falls at high flow* (a kinetic-modeling correction in MFR); **sestamibi/HMPAO** show minimal redistribution (flexible timing / injection-snapshot), unlike **thallium** (redistribution = viability). These are not trivia — they determine which agent answers a given question.

## Related Pages

- Foundational: **Molecular imaging & the theranostic pair**, **radiopharmaceuticals & production**, **physics of nuclear medicine**.
- Applied: the individual tracer pages linked from each row.

## Figure / Diagram Suggestions

- A **mechanism → biodistribution → artifact → theranostic** four-column synthesis.
- A **theranostic-pair** ladder (target → diagnostic isotope → therapeutic isotope).

## Self-Check

<details><summary><strong>Q1.</strong> Why does the free-pertechnetate artifact appear in the thyroid, stomach, and salivary glands?</summary>
<p><strong>Answer:</strong> Pertechnetate is handled by the <strong>sodium-iodide symporter (trapping)</strong> and concentrated by gastric/salivary tissue — so unbound Tc-99m reproduces that physiologic map on any poorly-labeled study.</p>
</details>

<details><summary><strong>Q2.</strong> A tumor is DOTATATE-negative but FDG-avid. What does the mechanism mismatch imply for therapy?</summary>
<p><strong>Answer:</strong> Loss of the <strong>SSTR2</strong> target with a shift to glucose metabolism indicates <strong>dedifferentiation</strong> — poorer PRRT benefit; consider chemotherapy/biopsy.</p>
</details>

<details><summary><strong>Q3.</strong> Why is MAG3 preferred over DTPA in a poorly functioning kidney?</summary>
<p><strong>Answer:</strong> MAG3 is <strong>actively secreted (high extraction)</strong>, giving usable images at low function, whereas filtered DTPA yields poor target-to-background in CKD.</p>
</details>

<details><summary><strong>Q4.</strong> What single chemical feature makes metal-based theranostic pairs (e.g. Ga-68/Lu-177) interchangeable at near-identical biodistribution?</summary>
<p><strong>Answer:</strong> A shared <strong>bifunctional chelator (DOTA)</strong> that binds either a diagnostic or a therapeutic radiometal on the same targeting ligand.</p>
</details>
