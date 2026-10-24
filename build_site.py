#!/usr/bin/env python3
"""Nuclear Medicine Atlas — single-file build, organized on an original
Six-Domain framework (Foundations · Probes & Targets · Clinical Systems ·
Therapy & Theranostics · Interpretation & Reasoning · Dosimetry, Safety &
Evidence) that follows the causal arc of a nuclear medicine study.
Design and evidence-grading (A/B/C/INFERENCE) adopted from the I-131 planner."""
import os, re, json, glob, math
import urllib.parse as _url0
import yaml
import markdown

# Paths are relative to this script so the repo builds anywhere (local + CI/GitHub Actions).
_HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(_HERE, "content")
OUT = os.path.join(_HERE, "nuclear-medicine-atlas.html")

import datetime as _dt
VERSION = "1.76"                                   # bump on substantive releases
BUILD_DATE = _dt.date.today().isoformat()          # stamped at build time (provenance)
_ROOT = os.path.dirname(BASE)

# ---- Deployment config (edit these before publishing) --------------------------
# SITE_URL: the canonical https origin the atlas will be hosted at (no trailing slash).
# CONTACT_EMAIL: where "Report an issue" corrections are sent.
# REPO_URL: optional public source/issues URL (e.g. a GitHub repo); blank to omit.
SITE_URL = "https://nuc.med"
CONTACT_EMAIL = "mail@jhs.md"
REPO_URL = ""
CSS = open(os.path.join(_ROOT, 'assets', 'atlas.css'), encoding='utf-8').read()
JS = open(os.path.join(_ROOT, 'assets', 'atlas.js'), encoding='utf-8').read()

# ── The Six Domains: an original framework organized by the causal arc of a
#    nuclear medicine study — how the signal is made, what carries it, what it
#    reveals, how it treats, how we read it, and how we quantify & verify it.
#    Each domain has a single inclusion rule so the atlas scales without reorg.
CHAPTERS = [
 # F · The Field & Future — orientation, careers, and where nuclear medicine is going
 ("field-future", "Why Nuclear Medicine & Careers", "F"),
 ("learning-paths", "Learning Paths", "F"),
 # I · Foundations — how the signal is made
 ("physics", "Physics & Radiobiology", "I"),
 ("instrumentation", "Instrumentation & Image Formation", "I"),
 # II · Probes & Targets — what carries the signal
 ("radiopharmacy", "Radiochemistry, Radiopharmacy & Targets", "II"),
 # III · Clinical Systems — what the signal reveals
 ("endocrine", "Endocrine & Neuroendocrine", "III"),
 ("cardiac", "Cardiovascular", "III"),
 ("neuro", "Neurology", "III"),
 ("musculoskeletal", "Musculoskeletal", "III"),
 ("genitourinary", "Genitourinary", "III"),
 ("pulmonary", "Pulmonary", "III"),
 ("gastrointestinal", "Gastrointestinal & Hepatobiliary", "III"),
 ("infection", "Infection & Inflammation", "III"),
 ("oncology", "Oncology", "III"),
 # IV · Therapy & Theranostics — how the signal treats
 ("theranostics", "Theranostics & Radionuclide Therapy", "IV"),
 # V · Interpretation & Reasoning — how we read it
 ("correlative-ct", "Correlative CT", "V"),
 ("pearls", "Patterns, Pitfalls & Variants", "V"),
 ("test-selection", "Test Selection & Comparison", "V"),
 ("reporting", "Reporting & Response Criteria", "V"),
 # VI · Dosimetry, Safety & Evidence — how we quantify, protect & verify
 ("dosimetry-safety", "Dosimetry, Safety & Regulatory", "VI"),
 ("landmark-trials", "Landmark Trials", "VI"),
 ("boards", "Quantitation, Evidence & Boards", "VI"),
 # J · Scholarship & Community — contributed articles and the people behind them
 ("articles", "Contributed Articles", "J"),
 ("contributors", "Contributors", "J"),
 # Utilities
 ("tools", "Interactive Tools", "T"),
]
PART_LABEL = {
 "F": "The Field & Future",
 "I": "Part I · Foundations",
 "II": "Part II · Probes & Targets",
 "III": "Part III · Clinical Systems",
 "IV": "Part IV · Therapy & Theranostics",
 "V": "Part V · Interpretation & Reasoning",
 "VI": "Part VI · Dosimetry, Safety & Evidence",
 "J": "Scholarship & Community",
 "T": "Utilities",
}
CH_LABEL = {k: lbl for k, lbl, _ in CHAPTERS}
CH_PART = {k: pt for k, _, pt in CHAPTERS}
CH_ORDER_LIST = [k for k, _, _ in CHAPTERS]

# PAGE_CHAPTER and CH_ORDER are DERIVED from each page's frontmatter
# (chapter:, order:) after parsing — see derivation below. SINGLE SOURCE OF
# TRUTH: to add or move a page, edit only that page's own frontmatter.

# ============================ GRADED EVIDENCE ============================
# A = RCT/meta-analysis · B = large cohort (>~400) or society guideline · C = smaller/
# confounded cohort or physiologic reasoning · I = INFERENCE (reasoning, not a citation).
EVIDENCE = {
 # ---- Basic principles ----
 "physics-nuclear-medicine": [
  ["B","<b>Standard nuclear-medicine physics references</b> (e.g. Cherry, Sorenson & Phelps, <i>Physics in Nuclear Medicine</i>) — decay modes, particle emissions, LET, half-life."],
  ["B","<b>MIRD / ICRP framework</b> — LET and effective half-life as determinants of absorbed dose and radiation protection."]],
 "radiopharmaceuticals-overview": [
  ["B","<b>USP &lt;823&gt; / SNMMI / EANM radiopharmacy standards</b> — generator systems, cold-kit preparation, and radiochemical quality control."],
  ["C","<b>Mo-99/Tc-99m generator chemistry and supply</b> — reviews of transient equilibrium, Mo-99 breakthrough, and aluminum limits."]],
 "molecular-imaging": [
  ["B","<b>Bodei L, Herrmann K, Schöder H, et al.</b> Radiotheranostics in oncology: current challenges and emerging opportunities. <i>Nat Rev Clin Oncol</i> 2022;19:534–550."],
  ["B","<b>Bodei L, Chiti A, Modlin IM, Scott B, Schöder H.</b> The Path to the Future: Education of Nuclear Medicine Therapeutic Specialists as Responsible Physicians. <i>J Nucl Med</i> 2019;60(12):1663–1664."],
  ["I","<b>Emerging targets (FAP, DLL3)</b> — the diagnostic–therapeutic pairing logic generalizes to newer targets; clinical validation is ongoing."]],
 "instrumentation-detection": [
  ["B","<b>Standard instrumentation references and SNMMI/IAEA QC guidance</b> — gamma-camera and PET detector principles, collimation, and quality-control programs."]],
 "counting-statistics-roc": [
  ["B","<b>Cherry, Sorenson & Phelps, <i>Physics in Nuclear Medicine</i></b> — Poisson counting statistics, error propagation, chi-square, and dead time."],
  ["B","<b>Metz CE</b> and standard references on <b>ROC analysis</b> — threshold-independent evaluation of diagnostic performance."]],
 "mird-dosimetry-worked": [
  ["B","<b>MIRD Committee pamphlets (SNMMI)</b> — the D = Ã × S schema, S-values, and residence-time formalism."],
  ["B","<b>OLINDA/EXM</b> and EANM dosimetry guidance — reference-phantom and patient-specific organ dosimetry; kidney BED for PRRT."],
  ["A","<b>DOSISPHERE-01</b> — personalized dosimetry improved outcomes (Y-90), illustrating patient-specific dosimetry value."]],
 "qc-procedures": [
  ["B","<b>SNMMI / IAEA / ACR QC programs</b> — gamma-camera uniformity/COR/bar-phantom, PET normalization, dose-calibrator constancy/linearity/accuracy/geometry."],
  ["B","<b>US NRC / USP</b> — Mo-99 breakthrough (0.15) and aluminum (10 µg/mL) limits; radiochemical-purity testing."]],
 "pet-spect-performance-reconstruction": [
  ["B","<b>NEMA NU-2 / NU-1</b> performance standards — resolution, sensitivity, scatter fraction, NECR."],
  ["B","<b>Standard reconstruction references</b> — OSEM, PSF/resolution recovery, TOF; attenuation/scatter/partial-volume corrections and their effect on SUV."]],
 "spect-pet-hybrid": [
  ["B","<b>EANM/SNMMI acquisition guidelines</b> — iterative reconstruction, attenuation/scatter correction, time-of-flight, and hybrid SPECT/CT, PET/CT, PET/MR."],
  ["C","<b>Quantitation dependencies</b> — technical studies on reconstruction, uptake time, and partial-volume effects on SUV."]],
 "dosimetry-theranostics": [
  ["B","<b>MIRD Committee pamphlets (SNMMI)</b> — absorbed-dose framework (time-integrated activity × S-values)."],
  ["B","<b>EANM dosimetry committee guidance</b> for ¹⁷⁷Lu radioligand therapy (multi-time-point SPECT/CT; organs at risk)."],
  ["C","<b>Lesional dosimetry</b> — I-124 PET dose–response supports a ~85 Gy lesion threshold; empiric activities often fall short in bone."]],
 # ---- Endocrine ----
 "radioiodine-thyroid": [
  ["B","<b>ATA guidelines</b> for hyperthyroidism and for differentiated thyroid cancer (radioiodine indications, preparation)."],
  ["B","<b>SNMMI/EANM guidelines</b> for thyroid uptake, scanning, and I-131 therapy."],
  ["I","<b>Therapeutic activities are indication- and protocol-specific</b> — see a dedicated dosing tool for evidence-graded activity selection."]],
 "neuroendocrine-tumors": [
  ["A","<b>NETTER-1 / NETTER-2</b> — Strosberg J, <i>N Engl J Med</i> 2017; Singh S, <i>Lancet</i> 2024: ¹⁷⁷Lu-DOTATATE improves PFS in progressive midgut and first-line grade 2–3 GEP-NETs."],
  ["B","<b>WHO classification of NETs</b> (5th ed., IARC 2022) — Ki-67 / mitotic grading (G1–G3)."],
  ["C","<b>Dual SSTR + FDG imaging</b> — cohort data: FDG-positive/SSTR-negative phenotype predicts poorer PRRT response."]],
 "dotatate": [
  ["B","<b>SNMMI/EANM practice guideline</b> for somatostatin-receptor PET imaging."],
  ["C","<b>Krenning score</b> — uptake grading relative to liver/spleen; 3–4 predicts PRRT benefit."]],
 "mibg-i123": [
  ["B","<b>SNMMI/EANM guideline</b> for MIBG scintigraphy in neuroendocrine tumors and neuroblastoma."]],
 # ---- Skeletal / HPB ----
 "mdp": [
  ["B","<b>SNMMI procedure standard / EANM guideline</b> for bone scintigraphy — technique and interpretation."]],
 "hida": [
  ["B","<b>SNMMI procedure standard</b> for hepatobiliary scintigraphy (acute cholecystitis, CCK ejection fraction, morphine augmentation)."]],
 # ---- Genitourinary ----
 "renal-scintigraphy": [
  ["B","<b>SNMMI/EANM practice guideline for renal scintigraphy in adults</b> — diuretic renography, split function, and cortical (DMSA) imaging."],
  ["C","<b>Diuretic-renography protocols</b> (F+20 / F−15 / F0) and hydration/bladder dependence — technical/consensus literature."]],
 "mag3": [
  ["B","<b>SNMMI/EANM guidelines</b> for diuretic renography and split renal function."]],
 "psma-11": [
  ["A","<b>proPSMA</b> — Hofman MS, et al. <i>Lancet</i> 2020: PSMA-PET/CT superior to conventional imaging for staging high-risk prostate cancer."],
  ["B","<b>PROMISE / PSMA-RADS and SNMMI/EANM guideline</b> — standardized PSMA-ligand PET interpretation."]],
 "psma-biochemical-recurrence": [
  ["A","<b>Fendler WP, et al.</b> <i>JAMA Oncol</i> 2019 — prospective validation of ⁶⁸Ga-PSMA-11 PET localizing recurrent prostate cancer; detection rises with PSA."],
  ["B","<b>Prospective multicenter cohort (n≈2,005)</b> — PSMA-11 PET detection efficiency in biochemical recurrence stratified by PSA."],
  ["I","<b>PSMA-PET phenotype + genomics</b> — large biochemical-recurrence cohorts profiled with next-generation sequencing; emerging, not yet standard of care."]],
 "prostate-cancer": [
  ["A","<b>proPSMA</b> — Hofman MS, et al. <i>Lancet</i> 2020: PSMA-PET/CT superior for staging high-risk prostate cancer (randomized)."],
  ["A","<b>VISION</b> — Sartor O, <i>N Engl J Med</i> 2021; <b>ALSYMPCA</b> — Parker C, <i>N Engl J Med</i> 2013: survival benefit of ¹⁷⁷Lu-PSMA and ²²³Ra in mCRPC."],
  ["B","<b>PROMISE / PSMA-RADS and SNMMI/EANM guidance</b> — standardized PSMA-PET interpretation."]],
 # ---- Pulmonary ----
 "vq-scan-pe": [
  ["A","<b>PIOPED</b> — The PIOPED Investigators. <i>JAMA</i> 1990;263:2753–2759: prospective probability-based V/Q criteria for pulmonary embolism.", "https://doi.org/10.1001/jama.1990.03440200057023"],
  ["B","<b>EANM guideline for V/Q SPECT</b> — Bajc M, et al. <i>Eur J Nucl Med Mol Imaging</i> 2019;46:2429–2451: mismatch-based interpretation for PE and beyond.", "https://doi.org/10.1007/s00259-019-04450-0"]],
 "maa": [
  ["B","<b>SNMMI/EANM guidelines</b> for lung scintigraphy (V/Q) and pre-⁹⁰Y radioembolization mapping (lung-shunt fraction)."]],
 # ---- Oncology: PET ----
 "fdg-oncology": [
  ["A","<b>PERCIST</b> — Wahl RL, et al. <i>J Nucl Med</i> 2009: quantitative metabolic response criteria."],
  ["B","<b>EANM tumour-imaging guideline v2.0</b> (Boellaard) and SNMMI procedure standard — acquisition and SUV standardization."],
  ["C","<b>SUV dependencies</b> — technical literature on uptake time, glucose, reconstruction, and partial-volume effects."]],
 "fdg": [
  ["B","<b>EANM tumour-imaging guideline v2.0</b> — Boellaard R, et al. <i>Eur J Nucl Med Mol Imaging</i>."],
  ["B","<b>SNMMI procedure standard</b> for ¹⁸F-FDG PET/CT in oncology."],
  ["A","<b>PERCIST</b> — Wahl RL, et al. <i>J Nucl Med</i> 2009."]],
 "lymphoma": [
  ["B","<b>Lugano classification</b> — Cheson BD, et al. <i>J Clin Oncol</i> 2014: FDG-PET/CT staging and response."],
  ["B","<b>Deauville 5-point scale</b> — Barrington SF, et al. <i>J Clin Oncol</i> 2014."],
  ["A","<b>Response-adapted therapy</b> — RATHL (Johnson P, <i>N Engl J Med</i> 2016): interim-PET-guided de-escalation in Hodgkin lymphoma."]],
 "head-neck-cancer": [
  ["A","<b>PET-NECK</b> — Mehanna H, et al. <i>N Engl J Med</i> 2016: PET-CT surveillance non-inferior to planned neck dissection after chemoradiation, and cost-saving."],
  ["B","<b>NI-RADS</b> — ACR Neck Imaging Reporting and Data System — structured post-treatment interpretation and management."]],
 # ---- Oncology: therapy ----
 "theranostics-overview": [
  ["A","<b>VISION</b> — Sartor O, et al. <i>N Engl J Med</i> 2021; <b>NETTER-1</b> — Strosberg J, et al. <i>N Engl J Med</i> 2017."],
  ["B","<b>Bodei L, Herrmann K, Schöder H, et al.</b> Radiotheranostics in oncology. <i>Nat Rev Clin Oncol</i> 2022;19:534–550."],
  ["B","<b>SNMMI/EANM practice guidelines</b> for ¹⁷⁷Lu-PSMA and ¹⁷⁷Lu-DOTATATE radioligand therapy."]],
 "lu177-psma-617": [
  ["A","<b>VISION</b> — Sartor O, et al. <i>N Engl J Med</i> 2021;385:1091–1103: improved OS and rPFS in PSMA-positive mCRPC after ARPI and taxane."],
  ["A","<b>PSMAfore</b> — Morris MJ, et al.: benefit in taxane-naïve mCRPC after ARPI progression, supporting the 2025 pre-chemotherapy label expansion."],
  ["B","<b>SNMMI/EANM procedure guideline</b> for ¹⁷⁷Lu-PSMA therapy."],
  ["B","<b>FDA prescribing information</b> (lutetium Lu-177 vipivotide tetraxetan) — 7.4 GBq q6 weeks × up to 6 cycles."]],
 "lu177-dotatate": [
  ["A","<b>NETTER-1</b> — Strosberg J, et al. <i>N Engl J Med</i> 2017;376:125–135: improved PFS in progressive midgut NETs."],
  ["A","<b>NETTER-2</b> — Singh S, et al. <i>Lancet</i> 2024: first-line ¹⁷⁷Lu-DOTATATE in grade 2–3 GEP-NETs."],
  ["B","<b>FDA approval</b> — pediatric (≥12 y) SSTR-positive GEP-NET indication (2024)."],
  ["B","<b>SNMMI/EANM PRRT guideline</b> — dosing (7.4 GBq × 4, q8 weeks) and amino-acid renal protection."]],
 "ra223-dichloride": [
  ["A","<b>ALSYMPCA</b> — Parker C, et al. <i>N Engl J Med</i> 2013;369:213–223: improved OS in symptomatic bone-metastatic mCRPC without visceral disease."],
  ["A","<b>ERA-223</b> — Smith M, et al. <i>Lancet Oncol</i> 2019: Ra-223 + abiraterone/prednisone increased fractures and deaths."],
  ["B","<b>Xofigo prescribing information</b> — 55 kBq/kg IV q4 weeks × 6."]],
 "i131-mibg": [
  ["B","<b>High-specific-activity I-131-iobenguane</b> — Pryma DA, et al. <i>J Nucl Med</i> 2019: phase 2 in iobenguane-avid pheochromocytoma/paraganglioma."],
  ["B","<b>SNMMI/EANM guidance</b> on I-131-MIBG therapy (thyroid blockade, isolation, interfering drugs)."],
  ["C","<b>Neuroblastoma series</b> — retrospective experience in relapsed/refractory high-risk disease."]],
 "y90-radioembolization": [
  ["A","<b>HCC RCTs</b> — SARAH (Vilgrain V, <i>Lancet Oncol</i> 2017) and SIRveNIB (Chow PKH, <i>J Clin Oncol</i> 2018)."],
  ["A","<b>Colorectal liver metastases</b> — SIRFLOX/FOXFIRE (van Hazel G, <i>J Clin Oncol</i> 2016; Wasan HS, <i>Lancet Oncol</i> 2017)."],
  ["B","<b>SNMMI/EANM procedure guidance</b> and joint IR standards — ⁹⁹ᵐTc-MAA mapping, lung-shunt assessment, dosimetry."]],
 "men-syndromes": [
  ["B","<b>Wells SA, et al.</b> Revised ATA guidelines for the management of medullary thyroid carcinoma — RET testing, MEN2 phenotypes, and prophylactic thyroidectomy timing."],
  ["B","<b>Thakker RV, et al.</b> Clinical practice guidelines for MEN type 1 (menin; the '3 Ps'). <i>J Clin Endocrinol Metab</i> 2012."],
  ["B","<b>SNMMI/EANM</b> — genotype-informed functional imaging (DOTATATE, MIBG, FDOPA) in hereditary neuroendocrine/pheochromocytoma syndromes."]],
 "carcinoid-syndrome-functioning-net": [
  ["B","<b>NANETS / ENETS consensus guidelines</b> — carcinoid syndrome, carcinoid heart disease, and functioning pancreatic NET management."],
  ["A","<b>TELESTAR</b> — Kulke MH, et al.: telotristat ethyl reduced bowel-movement frequency in carcinoid-syndrome diarrhea inadequately controlled by somatostatin analogs."],
  ["B","<b>Carcinoid crisis / peri-procedural octreotide</b> — SNMMI/anesthesia guidance on somatostatin-analog cover for surgery, embolization, and PRRT."]],
 "ata-thyroid-risk": [
  ["B","<b>2015 ATA Management Guidelines for Differentiated Thyroid Cancer</b> — Haugen BR, et al. <i>Thyroid</i> 2016;26:1–133 — initial risk stratification (low/intermediate/high) and response-to-therapy (dynamic) restratification.", "https://doi.org/10.1089/thy.2015.0020"],
  ["B","<b>Tuttle RM, et al.</b> Dynamic risk stratification: updating recurrence risk by response to initial therapy. <i>Thyroid</i> / <i>Cancer</i> series."],
  ["B","<b>AJCC/TNM 8th edition</b> — age-dependent thyroid-cancer staging (mortality), threshold at 55 years."]],
 "seventeen-segment-model": [
  ["B","<b>Cerqueira MD, et al.</b> Standardized myocardial segmentation and nomenclature — the <b>17-segment model</b>. AHA Writing Group, <i>Circulation</i> 2002."],
  ["B","<b>ASNC imaging guidelines</b> — segment scoring and coronary-territory assignment for MPI."]],
 "fdg-preparation-physiologic-uptake": [
  ["B","<b>Boellaard R, et al.</b> FDG PET/CT: EANM procedure guidelines for tumour imaging (patient preparation, glucose, uptake time). <i>Eur J Nucl Med Mol Imaging</i> 2015."],
  ["B","<b>SNMMI procedure standard</b> for tumour FDG-PET/CT imaging — fasting, glucose thresholds, and physiologic-uptake reduction (brown fat, muscle)."],
  ["C","<b>Metformin and bowel FDG uptake</b> — cohort/technical reports supporting holding metformin ~24–48 h for abdominal reads."]],
 "acquisition-parameters-spect": [
  ["B","<b>SNMMI/EANM procedure standards</b> — representative adult activities, collimator/energy-window selection, and acquisition/timing for planar and SPECT studies (verify locally)."],
  ["B","<b>EANM Dosage Card / North American consensus</b> — weight-based pediatric administered activities."]],
 "acquisition-parameters-pet": [
  ["B","<b>SNMMI/EANM procedure standards</b> — PET tracer activities, uptake times, and acquisition (FDG, PSMA, DOTATATE, cardiac, amyloid/tau, NaF)."],
  ["B","<b>EARL / harmonization guidance</b> — reconstruction and uptake-time matching for quantitative/serial SUV."]],
 "therapy-administration-protocols": [
  ["B","<b>SNMMI/EANM therapy guidelines & prescribing information</b> — representative activities/schedules, premedication, monitoring, and release for radionuclide therapies."],
  ["B","<b>US NRC 10 CFR 35</b> — written directive and patient-release requirements (35.75)."]],
 "thresholds-decision-cutoffs": [
  ["B","<b>Society procedure standards & appropriate-use criteria</b> (SNMMI/EANM/ASNC/ACR) — the source of the quantitative cutoffs, with the explicit caveat that most are protocol/software/population-dependent."],
  ["B","<b>US NRC 10 CFR Part 20 &amp; 35</b> — occupational/public dose limits, patient release (35.75), written directive, medical-event definitions, and generator breakthrough limits."],
  ["I","<b>ICRP vs NRC</b> — recommendation frameworks differ (e.g. occupational effective dose); jurisdiction determines the operative number."]],
 "radiopharmaceutical-targets-mechanisms": [
  ["B","<b>Standard radiopharmacy/molecular-imaging references</b> — uptake mechanisms, targets, and biodistribution underpinning imaging and theranostics."],
  ["B","<b>Bodei L, Herrmann K, Schöder H, et al.</b> Radiotheranostics in oncology. <i>Nat Rev Clin Oncol</i> 2022 — mechanism-to-therapy pairing logic."]],
 "patient-preparation-confounders": [
  ["B","<b>SNMMI/EANM procedure guidelines</b> — patient preparation for FDG-PET, cardiac FDG (suppression vs promotion), vasodilator stress, radioiodine, PRRT, and GI/renal studies."],
  ["C","<b>Interfering-drug and physiologic-uptake literature</b> — MIBG/DAT/FES blockade, brown fat, metformin bowel uptake, mucosal washout."]],
 "landmark-evidence": [
  ["A","<b>VISION / TheraP / PSMAfore</b> (Lu-177-PSMA); <b>NETTER-1 / NETTER-2</b> (PRRT); <b>ALSYMPCA / ERA-223</b> (Ra-223) — pivotal theranostic and radionuclide-therapy trials."],
  ["A","<b>ISCHEMIA</b>, <b>STICH</b> viability substudy, <b>ATTR-ACT</b> (cardiac); <b>RATHL</b> (lymphoma); <b>DOSISPHERE-01 / LEGACY</b> (Y-90); <b>ZIRCON</b> (CAIX RCC)."],
  ["A","<b>HiLo / ESTIMABL / IoN</b> and <b>DECISION / SELECT</b> (thyroid); <b>proPSMA</b>, <b>PET-NECK</b>, <b>SEMPET</b>, <b>MSLT-I/II</b> — staging/de-escalation evidence."]],
 "oncology-response-criteria-percist": [
  ["B","<b>Eisenhauer EA, et al.</b> New response evaluation criteria in solid tumours: <b>RECIST 1.1</b>. <i>Eur J Cancer</i> 2009;45:228–247.", "https://doi.org/10.1016/j.ejca.2008.10.026"],
  ["B","<b>Wahl RL, et al.</b> From RECIST to <b>PERCIST</b>: evolving considerations for PET response criteria in solid tumors. <i>J Nucl Med</i> 2009;50(Suppl 1):122S–150S.", "https://doi.org/10.2967/jnumed.108.057307"],
  ["B","<b>Choi H, et al.</b> (GIST, density + size) and <b>Seymour L, et al.</b> <b>iRECIST</b> for immunotherapy (<i>Lancet Oncol</i> 2017)."]],
 "melanoma-staging-ajcc": [
  ["B","<b>AJCC Cancer Staging Manual, 8th edition (Melanoma)</b> — Gershenwald JE, et al. <i>CA Cancer J Clin</i> 2017;67:472–492: Breslow thickness/ulceration (T), nodal + in-transit (N), and site + LDH (M1a–M1d).", "https://doi.org/10.3322/caac.21409"],
  ["A","<b>MSLT-I/II</b> — Morton DL / Faries MB, <i>N Engl J Med</i>: sentinel-node biopsy for staging and the (limited) role of completion dissection."],
  ["B","<b>NCCN / SNMMI</b> — FDG-PET/CT for stage III–IV staging and response; sentinel-node mapping for early disease; brain MRI for CNS."]],
 "lymphoma-staging-lugano-deauville": [
  ["B","<b>Cheson BD, et al.</b> Recommendations for initial evaluation, staging, and response assessment of Hodgkin and non-Hodgkin lymphoma: the <b>Lugano classification</b>. <i>J Clin Oncol</i> 2014;32:3059–3068.", "https://doi.org/10.1200/JCO.2013.54.8800"],
  ["B","<b>Barrington SF, et al.</b> Role of imaging in staging and response assessment of lymphoma (Deauville 5-point scale). <i>J Clin Oncol</i> 2014;32:3048–3058.", "https://doi.org/10.1200/JCO.2013.53.5229"],
  ["A","<b>RATHL</b> — Johnson P, et al. <i>N Engl J Med</i> 2016;374:2419–2429: interim-PET-adapted therapy (bleomycin omission) in Hodgkin lymphoma.", "https://doi.org/10.1056/NEJMoa1510093"]],
 "psma-reporting-promise-rads": [
  ["B","<b>Eiber M, et al.</b> PROMISE: molecular-imaging TNM (miTNM) and standardized PSMA-PET reporting. <i>J Nucl Med</i> 2018."],
  ["B","<b>Rowe SP, et al.</b> Proposal for a structured reporting system for PSMA-targeted PET: <b>PSMA-RADS version 1.0</b>. <i>J Nucl Med</i> 2018;59:479–485.", "https://doi.org/10.2967/jnumed.117.195255"],
  ["B","<b>EANM E-PSMA</b> standardized reporting guidelines and <b>PROMISE V2</b> — refinements of reference-organ scoring and miTNM."],
  ["B","<b>RECIP 1.0</b> — Gafita A, et al. <i>Radiology</i> 2023: PROMISE-based response criteria for ¹⁷⁷Lu-PSMA."]],
 "targeted-alpha-therapy": [
  ["C","<b>Ac-225-PSMA-617</b> — Kratochwil C, et al. <i>J Nucl Med</i> (2016 onward): small series, responses incl. Lu-177-refractory disease; xerostomia dose-limiting."],
  ["C","<b>Reviews of targeted alpha therapy</b> — daughter-nuclide redistribution, supply, and dosimetry challenges."]],
 "radioimmunotherapy": [
  ["A","<b>Witzig TE, et al.</b> <i>J Clin Oncol</i> 2002 — randomized ⁹⁰Y-ibritumomab tiuxetan vs rituximab in relapsed/refractory low-grade/follicular/transformed B-cell NHL: higher overall and complete response rates."],
  ["A","<b>Morschhauser F, et al.</b> (FIT trial) <i>J Clin Oncol</i> 2008 — ⁹⁰Y-ibritumomab tiuxetan consolidation after first-line induction prolonged progression-free survival in advanced follicular lymphoma."],
  ["B","<b>SNMMI/EANM and product labeling</b> — weight- and platelet-based fixed activity, marrow-reserve and &lt;25% marrow-involvement eligibility, delayed myelosuppression."],
  ["I","<b>Positioning</b> — use has narrowed with immunochemotherapy, bispecifics, and CAR-T; the crossfire mechanism remains advantageous in bulky/antigen-heterogeneous disease."]],
 "theranostics-response-criteria": [
  ["B","<b>RECIP 1.0</b> — Gafita A, et al. <i>Radiology</i> 2023: PSMA-PET response by tumor-volume change plus new lesions."],
  ["B","<b>PROMISE / PSMA-RADS</b> — Eiber M, et al.: standardized PSMA-PET reporting."],
  ["C","<b>Krenning score</b> — SSTR uptake grading (0–4); 3–4 predicts PRRT benefit."]],
 "radiation-safety-release": [
  ["B","<b>U.S. NRC criteria</b> for release of patients administered radioactive material (dose-to-others basis) and Agreement-State equivalents."],
  ["B","<b>SNMMI/EANM radiation-protection guidance</b> for radionuclide therapy."]],
 # ---- CNS ----
 "ioflupane": [
  ["B","<b>SNMMI/EANM guideline</b> for dopamine-transporter (DAT) SPECT imaging."],
  ["B","<b>DaTscan pivotal studies</b> — differentiation of degenerative parkinsonism from essential tremor and drug-induced/psychogenic causes."]],
 # ---- Cardiac ----
 "nuclear-cardiology-overview": [
  ["B","<b>ASNC/SNMMI imaging guidelines</b> for SPECT and PET myocardial perfusion imaging."],
  ["B","<b>ASNC/AHA appropriate-use criteria</b> for cardiac radionuclide imaging."]],
 "mpi-spect": [
  ["A","<b>Prognostic value of a normal SPECT MPI</b> — meta-analyses report a low hard-event rate ('warranty period') rising with defect burden."],
  ["B","<b>ASNC imaging guideline for SPECT MPI</b> — protocols, attenuation correction, gated analysis."],
  ["B","<b>SNMMI procedure standard</b> for myocardial perfusion imaging."]],
 "stress-testing": [
  ["A","<b>Regadenoson non-inferiority</b> — Iskandrian AE, et al. ADVANCE-MPI, <i>J Nucl Cardiol</i> 2007."],
  ["B","<b>ASNC/SNMMI stress protocol guidelines</b> — exercise vs. vasodilator vs. dobutamine."],
  ["B","<b>Prescribing information</b> for regadenoson, adenosine, dipyridamole, dobutamine."]],
 "cardiac-pet-perfusion": [
  ["B","<b>Myocardial flow reserve and prognosis</b> — Murthy VL, et al. <i>Circulation</i> 2011, n>2700: reduced global MFR independently associated with cardiac mortality."],
  ["B","<b>ASNC/SNMMI cardiac PET guideline</b> — Rb-82 and N-13-ammonia acquisition and flow quantification."],
  ["C","<b>TID normal values (PET)</b> — Rischpler C, et al. <i>J Nucl Med</i> 2012: protocol/software-specific."]],
 "mpi-interpretation-grading": [
  ["B","<b>Quantitative perfusion scoring</b> — Berman/Cedars-Sinai summed-score methodology and normal ranges (17-segment, 0–4)."],
  ["B","<b>ASNC guideline on quantification and interpretation</b> — SSS/SRS/SDS, % myocardium, TID, gated function."],
  ["C","<b>TID thresholds vary</b> — normal limits differ by SPECT vs. PET, tracer, and software."]],
 "myocardial-viability": [
  ["A","<b>STICH viability substudy</b> — Bonow RO, et al. <i>N Engl J Med</i> 2011: viability identified higher-survival patients but did not independently predict CABG benefit."],
  ["B","<b>Viability meta-analysis</b> — Allman KC, et al. <i>J Am Coll Cardiol</i> 2002: observational link between viability and post-revascularization survival."],
  ["B","<b>ASNC/SNMMI guidance</b> on FDG PET viability (perfusion–metabolism mismatch)."]],
 "cardiac-amyloidosis": [
  ["B","<b>Nonbiopsy diagnosis of ATTR</b> — Gillmore JD, et al. <i>Circulation</i> 2016;133:2404–2412, n=1217: grade 2–3 uptake with negative monoclonal screen >99% specificity/PPV.", "https://doi.org/10.1161/CIRCULATIONAHA.116.021612"],
  ["B","<b>Multisociety practice points</b> (ASNC/AHA/ASE/EANM/SNMMI/SCMR) for Tc-99m-PYP/DPD/HMDP imaging."],
  ["C","<b>Perugini visual grade</b> — Perugini E, et al. <i>J Am Coll Cardiol</i> 2005;46:1076–1084: original 0–3 scale.", "https://doi.org/10.1016/j.jacc.2005.05.073"]],
 "cardiac-sarcoidosis": [
  ["B","<b>ASNC/SNMMI expert consensus</b> on FDG PET for cardiac sarcoidosis (dietary preparation, interpretation)."],
  ["B","<b>HRS expert consensus statement</b> on cardiac sarcoidosis — Birnie DH, et al. <i>Heart Rhythm</i> 2014;11:1304–1323 (imaging role in diagnosis/management).", "https://doi.org/10.1016/j.hrthm.2014.03.043"],
  ["C","<b>Suppression protocols</b> — technical studies on high-fat/low-carbohydrate prep ± heparin."]],
 "muga": [
  ["B","<b>SNMMI procedure standard</b> for equilibrium radionuclide angiography (count-based LVEF)."],
  ["B","<b>Cardio-oncology guidelines</b> referencing MUGA LVEF thresholds."]],
 "cardiac-reporting": [
  ["B","<b>ASNC imaging guidelines and reporting standards</b> for nuclear cardiology."]],
 "sestamibi": [
  ["B","<b>ASNC/SNMMI procedure standards</b> for myocardial perfusion imaging (sestamibi/tetrofosmin)."],
  ["B","<b>SNMMI/EANM guidance</b> for parathyroid scintigraphy."]],
 "pyp": [
  ["B","<b>Multisociety practice points</b> for Tc-99m-PYP/DPD/HMDP cardiac amyloid imaging (SPECT mandatory; exclude monoclonal protein)."],
  ["B","<b>Gillmore JD, et al.</b> <i>Circulation</i> 2016 — diagnostic performance of bone-tracer imaging for ATTR."]],
 # ---- new clinical pages ----
 "thyroid-cancer": [
  ["A","<b>ESTIMABL1 / HiLo</b> — Schlumberger M, <i>N Engl J Med</i> 2012; Mallick U, <i>N Engl J Med</i> 2012: 1.1 GBq non-inferior to 3.7 GBq for remnant ablation in low/intermediate risk."],
  ["A","<b>ESTIMABL2 / IoN</b> — Leboulleux S, <i>N Engl J Med</i> 2022; Mallick U, <i>Lancet</i> 2025: omission of radioiodine non-inferior in selected low-risk disease."],
  ["B","<b>ATA guideline for differentiated thyroid cancer</b> — risk stratification, radioiodine indications/intents, preparation, and RAI-refractory definition."]],
 "hyperthyroidism": [
  ["A","<b>Fixed vs calculated activity in Graves</b> — randomized trial (n=122): fewer treatment failures with fixed activity."],
  ["B","<b>ATA/AACE hyperthyroidism guidelines</b> — uptake-pattern diagnosis and radioiodine therapy (goal of hypothyroidism)."],
  ["B","<b>SNMMI/EANM guidance</b> for thyroid uptake and scanning."]],
 "parathyroid": [
  ["B","<b>SNMMI/EANM parathyroid scintigraphy guidance</b> — dual-phase sestamibi and SPECT/CT localization."],
  ["B","<b>¹⁸F-fluorocholine PET/CT</b> — cohort/meta-analytic data show higher sensitivity than sestamibi, especially for small/negative adenomas."]],
 "bone-scintigraphy": [
  ["B","<b>SNMMI procedure standard / EANM guideline</b> for bone scintigraphy — three-phase technique, SPECT/CT, and interpretation."]],
 "gastric-emptying": [
  ["B","<b>Consensus recommendations for gastric-emptying scintigraphy</b> — Abell TL, et al. (ANMS/SNMMI). <i>Am J Gastroenterol</i> 2008;103:753–763: standardized solid meal, 4-hour protocol, and normal values (>60% at 2 h, >10% at 4 h = delayed).", "https://doi.org/10.1111/j.1572-0241.2007.01636.x"]],
 "gi-bleeding-meckel": [
  ["B","<b>SNMMI procedure standards</b> for Tc-99m-RBC GI bleeding scintigraphy and Tc-99m-pertechnetate Meckel imaging (cimetidine augmentation)."]],
 "infection-inflammation": [
  ["B","<b>SNMMI/EANM guidelines</b> for labeled-leukocyte imaging, combined WBC/marrow interpretation, and FDG-PET/CT in infection/inflammation."],
  ["B","<b>EANM/SNMMI recommendations</b> for FDG-PET/CT in fever of unknown origin and large-vessel vasculitis."]],
 "brain-fdg-dementia": [
  ["B","<b>SNMMI/EANM procedure guideline</b> for brain FDG-PET in neurodegenerative disease."],
  ["B","<b>Appropriate-use criteria for amyloid PET</b> (SNMMI/Alzheimer's Association) — a negative scan argues against Alzheimer pathology."],
  ["C","<b>Cingulate island sign</b> — cohort data supporting its value in distinguishing dementia with Lewy bodies from Alzheimer disease."]],
 "lung-cancer": [
  ["A","<b>FDG-PET in NSCLC staging</b> — randomized/prospective evidence (e.g. PLUS, Fischer <i>N Engl J Med</i> 2009) that PET-based staging reduces futile thoracotomy."],
  ["B","<b>Guideline use of FDG-PET/CT</b> — solitary pulmonary nodule characterization and mediastinal staging (with pathologic confirmation of PET-positive nodes)."]],
 "hepatocellular-carcinoma": [
  ["A","<b>Y-90 radioembolization RCTs</b> — SARAH (Vilgrain, <i>Lancet Oncol</i> 2017); SIRveNIB (Chow, <i>J Clin Oncol</i> 2018)."],
  ["B","<b>SNMMI/EANM and interventional standards</b> — ⁹⁹ᵐTc-MAA mapping, lung-shunt assessment, radiation segmentectomy."],
  ["C","<b>FDG avidity in HCC</b> — cohort data: well-differentiated HCC is often FDG-low; FDG-avidity carries adverse prognosis."]],
 "pearls-pitfalls": [
  ["B","<b>Society atlases of normal variants and pitfalls</b> (SNMMI/EANM) — brown fat, physiologic uptake, attenuation and labeling artifacts."],
  ["C","<b>Named mimics</b> — celiac ganglion (PSMA), uncinate process (DOTATATE), superscan and flare (bone) described across the imaging literature."]],
 "novartis": [
  ["B","<b>FDA/EMA approvals and prescribing information</b> — Pluvicto (¹⁷⁷Lu-PSMA-617) and Lutathera (¹⁷⁷Lu-DOTATATE)."],
  ["I","<b>Pipeline status is time-sensitive</b> — verify current programs against primary regulatory/company sources at time of use."]],
 # ---- batch: further clinical coverage ----
 "adrenal-pheochromocytoma": [
  ["B","<b>SNMMI/EANM guidance</b> on functional imaging of pheochromocytoma/paraganglioma — I-123-MIBG, Ga-68-DOTATATE, F-18-FDOPA, FDG."],
  ["B","<b>Genotype-driven imaging</b> — cohort data: Ga-68-DOTATATE highest sensitivity for metastatic/head-and-neck paraganglioma and SDHx-related disease; FDG favored in SDHB."]],
 "medullary-thyroid-cancer": [
  ["B","<b>ATA medullary thyroid carcinoma guidelines</b> — calcitonin/CEA kinetics, RET testing, and imaging (no radioiodine role)."],
  ["A","<b>Selective RET inhibitors</b> — LIBRETTO-001 (selpercatinib) and ARROW (pralsetinib): high response rates in RET-altered MTC."],
  ["C","<b>F-18-FDOPA / Ga-68-DOTATATE localization</b> — cohort data for recurrent MTC by calcitonin level."]],
 "thyroiditis": [
  ["B","<b>ATA/AACE guidance</b> — low radioiodine uptake distinguishes thyroiditis (and exogenous/iodine causes) from Graves disease in thyrotoxicosis."]],
 "naf-bone-pet": [
  ["B","<b>SNMMI/EANM guideline for ¹⁸F-NaF PET/CT</b> — technique and interpretation; higher sensitivity than planar/SPECT bone scintigraphy."]],
 "liver-spleen-imaging": [
  ["B","<b>SNMMI procedure standards</b> — Tc-99m-sulfur colloid liver–spleen imaging and Tc-99m-RBC hepatic hemangioma study (perfusion–blood-pool mismatch with fill-in)."],
  ["C","<b>FNH colloid uptake</b> — Kupffer-cell content produces normal/increased colloid uptake, helping distinguish FNH from adenoma/malignancy."]],
 "dmsa-cortical": [
  ["B","<b>SNMMI/EANM guideline for DMSA cortical scintigraphy</b> — pyelonephritis, scarring, differential function, and pediatric use."]],
 "captopril-renography": [
  ["B","<b>SNMMI/EANM consensus on ACE-inhibitor renography</b> — detecting functionally significant renovascular hypertension; best in preserved renal function."]],
 "systemic-sarcoidosis": [
  ["B","<b>FDG-PET/CT in sarcoidosis</b> — society/consensus support for assessing disease activity, occult sites, biopsy targeting, and treatment response."],
  ["B","<b>Cardiac sarcoidosis expert consensus</b> (ASNC/SNMMI/HRS) — suppression-prepared FDG with rest perfusion."],
  ["C","<b>Ga-67 panda/lambda signs</b> — classic legacy patterns, largely superseded by FDG."]],
 "paget-disease": [
  ["B","<b>Endocrine Society / bone-society guidance</b> — diagnosis (ALP, radiographs, bone scan for extent) and bisphosphonate (zoledronic acid) therapy of Paget disease."],
  ["C","<b>Bone scan in Paget</b> — intense 'whole-bone' uptake; best modality for mapping polyostotic extent."],
  ["I","<b>Sarcomatous transformation</b> — rare; new FDG avidity / aggressive lysis / soft-tissue mass are warning features."]],
 "osteomyelitis-diabetic-foot": [
  ["B","<b>SNMMI/EANM/IDSA</b> — labeled-WBC + sulfur-colloid marrow imaging for complex osteomyelitis/diabetic foot; FDG-PET for spondylodiscitis."],
  ["B","<b>WBC–marrow incongruence</b> — the specific criterion separating infection from marrow/Charcot in violated bone."],
  ["C","<b>Charcot vs osteomyelitis</b> — distribution (midfoot vs ulcer-contiguous) and MRI correlation."]],
 "large-vessel-vasculitis": [
  ["B","<b>EANM/SNMMI/EULAR</b> recommendations — FDG-PET/CT for large-vessel vasculitis; image before/early in steroids; grade wall uptake vs liver."],
  ["A","<b>Tocilizumab (GiACTA)</b> — Stone JH, et al. <i>N Engl J Med</i> 2017;377:317–328: IL-6 blockade as steroid-sparing therapy in GCA.", "https://doi.org/10.1056/NEJMoa1613849"],
  ["B","<b>Temporal-artery ultrasound halo sign</b> and the smooth-circumferential vs patchy-calcified (atherosclerosis) distinction."]],
 "melanoma": [
  ["A","<b>MSLT-I / MSLT-II</b> — Morton DL, <i>N Engl J Med</i> 2014; Faries MB, <i>N Engl J Med</i> 2017: sentinel-node status prognostic; completion dissection of limited benefit."],
  ["B","<b>FDG-PET/CT in stage III–IV melanoma</b> — guideline-endorsed staging/restaging; low yield for microscopic nodal disease in early disease."]],
 "renal-cell-carcinoma": [
  ["A","<b>ZIRCON</b> — Shuch B, et al. <i>Lancet Oncol</i> 2024: ⁸⁹Zr-girentuximab (CAIX) PET/CT accurately characterized indeterminate renal masses as clear-cell RCC."],
  ["B","<b>PSMA-PET in ccRCC</b> — cohort data: neovascular PSMA expression enables detection of metastatic clear-cell RCC (often &gt; FDG/CT)."],
  ["C","<b>FDG-PET in RCC</b> — limited for the primary (variable avidity, urinary excretion); useful for metastatic staging/restaging and prognosis."],
  ["I","<b>¹⁷⁷Lu-girentuximab</b> — CAIX radioligand therapy is investigational, mirroring PSMA/SSTR theranostic logic."]],
 "germ-cell-testicular": [
  ["A","<b>SEMPET</b> — De Santis M, et al. <i>J Clin Oncol</i> 2004: FDG-PET of post-chemotherapy residual seminoma (&gt; 3 cm, ≥ 6 weeks) predicts viable tumor."],
  ["B","<b>NSGCT residual masses</b> — teratoma is FDG-negative yet requires resection; FDG unreliable (guideline/consensus)."],
  ["B","<b>IGCCCG</b> risk classification and tumor-marker (AFP/β-hCG/LDH) staging."]],
 "merkel-cell-carcinoma": [
  ["B","<b>NCCN / consensus</b> — FDG-PET/CT recommended for MCC staging/restaging (frequently upstages); sentinel-node mapping for cN0 disease."],
  ["A","<b>Immune-checkpoint therapy</b> — avelumab (JAVELIN Merkel 200) and pembrolizumab: durable responses in advanced MCC."],
  ["C","<b>SSTR imaging/PRRT</b> in MCC — variable DOTATATE uptake; investigational ¹⁷⁷Lu-DOTATATE for select SSTR-avid disease."]],
 "bladder-urothelial-cancer": [
  ["B","<b>FDG-PET/CT in MIBC</b> — value for distant/nodal staging and response; limited for primary/pelvic nodes due to urinary excretion (hydration/diuretic/delayed technique)."],
  ["A","<b>Enfortumab vedotin (nectin-4)</b> and <b>erdafitinib (FGFR)</b> — practice-changing targeted agents in advanced urothelial carcinoma."],
  ["B","<b>VI-RADS</b> — multiparametric MRI for muscle-invasion assessment (complementary to nuclear imaging)."]],
 "breast-cancer": [
  ["A","<b>NSABP B-32</b> — Krag DN, <i>Lancet Oncol</i> 2010: sentinel-node biopsy accurate and, when negative, avoids axillary dissection."],
  ["B","<b>FDG-PET/CT in locally advanced/metastatic breast cancer</b> — guideline use for staging, restaging, and response."],
  ["B","<b>F-18-FES PET</b> — FDA-approved ER imaging agent; whole-body ER phenotyping to inform endocrine therapy."]],
 "colorectal-cancer": [
  ["B","<b>FDG-PET/CT for colorectal restaging</b> — rising CEA with negative conventional imaging and pre-metastasectomy work-up (guideline-endorsed)."],
  ["C","<b>Mucinous/signet-ring tumors</b> — frequently FDG-low; esophagogastric early T/N staging better served by EUS/CT."]],
 "lymphoscintigraphy-sentinel-node": [
  ["A","<b>Sentinel-node trials</b> — MSLT (melanoma) and NSABP B-32 (breast): sentinel-node mapping accurately stages and spares nodal dissection."],
  ["B","<b>SNMMI/EANM lymphoscintigraphy guideline</b> — radiocolloid choice (sulfur colloid, tilmanocept), SPECT/CT, and intraoperative probe technique."]],
 "gallium-67": [
  ["B","<b>SNMMI/EANM guidance</b> — Ga-67 citrate imaging; largely superseded by FDG-PET and labeled-WBC, with niche roles (spinal infection, sarcoidosis activity)."]],
 "epilepsy-brain": [
  ["B","<b>SNMMI/EANM procedure guidelines</b> — interictal FDG-PET and ictal perfusion SPECT for pre-surgical epilepsy localization; SISCOM methodology."],
  ["C","<b>Localization performance</b> — cohort data: interictal FDG hypometabolism and ictal SPECT hyperperfusion concordant with EEG/MRI improve surgical outcomes."]],
 "brain-death-perfusion": [
  ["B","<b>SNMMI/EANM guidance</b> — cerebral scintigraphy as an ancillary test for brain death (absent intracranial perfusion; hollow-skull and hot-nose signs)."]],
 "csf-cisternography": [
  ["B","<b>SNMMI/EANM guidance</b> — radionuclide cisternography for CSF leak localization, shunt-patency assessment, and the NPH ventricular-reflux pattern."]],
 # ---- batch: tracers & further protocols ----
 "thallium-201": [
  ["B","<b>ASNC guidance</b> on thallium-201 myocardial perfusion and viability (stress–redistribution–reinjection)."],
  ["B","<b>Viability meta-analysis</b> — Allman KC, et al. <i>J Am Coll Cardiol</i> 2002."]],
 "rubidium-82": [
  ["B","<b>ASNC/SNMMI cardiac PET guideline</b> — Rb-82 generator-based perfusion and MBF/MFR."],
  ["B","<b>MFR prognosis</b> — Murthy VL, et al. <i>Circulation</i> 2011."]],
 "n13-ammonia": [
  ["B","<b>ASNC/SNMMI cardiac PET guideline</b> — N-13-ammonia perfusion and absolute flow quantification."]],
 "fes": [
  ["B","<b>F-18-FES (fluoroestradiol)</b> — FDA-approved ER imaging agent; SNMMI appropriate-use guidance."],
  ["C","<b>FES–IHC correlation</b> — cohort data linking uptake to ER expression and endocrine-therapy response."]],
 "fluciclovine": [
  ["B","<b>F-18-fluciclovine</b> — FDA-approved for suspected prostate cancer recurrence (LOCATE); largely superseded by PSMA-PET."]],
 "fapi": [
  ["C","<b>FAPI PET</b> — Kratochwil/Giesel et al. (2019 onward): high tumor-to-background across carcinomas; advantage in FDG-low and peritoneal disease; largely investigational."]],
 "amyloid-tau-pet": [
  ["B","<b>Amyloid PET appropriate-use criteria</b> (SNMMI/Alzheimer's Association) — a negative scan argues against Alzheimer pathology."],
  ["B","<b>Flortaucipir (Tauvid)</b> — FDA-approved tau PET; topography tracks clinical stage."]],
 "in111-octreotide": [
  ["B","<b>OctreoScan (In-111-pentetreotide)</b> — origin of the Krenning score; superseded by DOTATATE PET."]],
 "ventilation-agents": [
  ["B","<b>EANM/SNMMI V/Q guidelines</b> — Technegas, aerosol, and xenon ventilation agents; SPECT V/Q."]],
 "esophageal-gerd-salivary": [
  ["B","<b>SNMMI procedure standards</b> — esophageal transit, gastroesophageal reflux (milk) scintigraphy, and salivary gland scintigraphy."]],
 "renal-transplant": [
  ["B","<b>SNMMI/EANM renal scintigraphy guidance</b> — transplant patterns of ATN, rejection, obstruction, and urine leak."]],
 "pediatric-nuclear-medicine": [
  ["B","<b>EANM Dosage Card</b> and <b>North American consensus pediatric dosing guidelines</b> (Image Gently) — harmonized weight-based activities."]],
 "radiation-biology-protection": [
  ["B","<b>ICRP recommendations</b> (Publication 103) — stochastic/deterministic effects, effective dose, dose limits."],
  ["B","<b>NRC / national regulatory dose limits</b> and ALARA."]],
 # ---- tools ----
 "tool-deauville": [
  ["B","<b>Deauville 5-point scale</b> — Barrington SF, et al. <i>J Clin Oncol</i> 2014; Lugano classification (Cheson 2014)."]],
 "tool-gastric-retention": [
  ["B","<b>Consensus gastric-emptying protocol</b> — Abell TL, et al. (ANMS/SNMMI): 4-hour normal values and severity grading."]],
 "radionuclides-tracers-comparison": [
  ["B","<b>Half-lives, emissions, and decay data</b> follow the ICRP/DDEP reference values and standard nuclear-medicine physics texts (e.g. Cherry, Sorenson &amp; Phelps, <i>Physics in Nuclear Medicine</i>); production routes reflect standard cyclotron/reactor/generator sources."],
  ["B","<b>Clinical roles and matched theranostic pairs</b> reflect current SNMMI/EANM practice — e.g. the ¹⁷⁷Lu / ⁶⁸Ga PSMA and DOTATATE pairs, and ²²³Ra for bone-dominant mCRPC."],
  ["I","<b>This is an orientation table, not a dosing reference</b> — activities, protocols, and eligibility live on each agent's own page and in the written directive for the individual patient."]],
 "tool-i131-thyroid": [
  ["B","<b>SNMMI procedure standard / EANM guideline — therapy of benign thyroid disease</b>: the calculated (dosimetric) and fixed-activity ¹³¹I methods, and target absorbed dose per gram of thyroid tissue."],
  ["B","<b>Calculated vs fixed activity</b> — comparable cure rates in benign hyperthyroidism; the target dose per gram and choice of method are institution- and physician-specific."],
  ["I","<b>Gland mass and target µCi/g are estimates</b> — the definitive prescribed activity is the physician's written directive for the individual patient."]],
 "tool-mfr": [
  ["A","<b>Prognostic value of coronary flow reserve</b> — Murthy VL, et al. <i>Circulation</i> 2011;124:2215–2224: impaired global CFR independently predicted cardiac mortality (lowest tertile, CFR &lt;1.5, ~5.6&#215; higher cardiac death) across the spectrum of relative perfusion.", "https://doi.org/10.1161/CIRCULATIONAHA.111.050427"],
  ["B","<b>ASNC/SNMMI quantitative PET MPI</b> — absolute MBF and MFR methodology; global MFR &lt;2.0 flags impaired flow and &lt;1.5 high risk (tracer- and lab-dependent)."],
  ["I","<b>Rest MBF is workload-dependent</b> — RPP normalization uses a lab-convention reference value, and thresholds vary by lab and tracer; interpret with relative perfusion and clinical context."]],
 "tool-renogram": [
  ["B","<b>SNMMI/EANM diuretic renal scintigraphy guideline</b> — Taylor AT, et al. 2018: MAG3/DTPA technique, diuretic protocols, split function, and drainage assessment.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC6020824/"],
  ["C","<b>O'Reilly diuresis-renography classification</b> — O'Reilly PH, et al. <i>Br J Urol</i> 1978: Types 1 (normal), 2 (obstructed), 3a (dilated non-obstructed) and 3b (equivocal).", "https://pubmed.ncbi.nlm.nih.gov/423326/"],
  ["B","<b>NORA (normalized residual activity)</b> — Piepsz A, et al. <i>J Nucl Med</i> 2002;43:33: a quantitative drainage index less confounded than the raw washout T½.", "https://jnm.snmjournals.org/content/jnumed/43/1/33.full.pdf"],
  ["B","<b>ACE-inhibitor renography consensus</b> — Taylor A, Nally JV, et al. <i>J Nucl Med</i> 1996: a positive study is the post-ACEI deterioration (grade change ≥ 2 / new retention), not the baseline.", "https://jnm.snmjournals.org/content/jnumed/37/11/1876.full.pdf"],
  ["C","<b>Homsy sign (post-diuretic double peak)</b> — Homsy YL, et al. <i>J Urol</i> 1988: flow-dependent intermittent PUJ obstruction — an addition to, not one of, O'Reilly's types.", "https://pubmed.ncbi.nlm.nih.gov/3054162/"],
  ["I","<b>Curves are idealized teaching models</b> — indices are modeled to move correctly, not to reproduce a specific patient; always read real studies with counts, images, split function, hydration, and clinical context."]],
 # ---- batch: further oncology & neuro-oncology ----
 "multiple-myeloma": [
  ["B","<b>IMWG imaging recommendations</b> — FDG-PET/CT for bone disease detection, prognosis, and response in multiple myeloma."],
  ["B","<b>IMPeTUs criteria</b> — Nanni C, et al.: standardized (Deauville-like) FDG-PET reporting in myeloma."],
  ["B","<b>Prognostic value</b> — Zamagni E, et al.: number of focal lesions and extramedullary disease predict outcome; FDG normalization is prognostic."]],
 "gynecologic-cancer": [
  ["B","<b>FDG-PET/CT in cervical cancer</b> — guideline-endorsed nodal/distant staging and radiotherapy planning; para-aortic nodal status alters fields."],
  ["B","<b>Ovarian recurrence</b> — FDG-PET/CT for recurrence with rising CA-125 (NCCN/ESGO-referenced use)."]],
 "pancreatic-biliary-cancer": [
  ["B","<b>FDG-PET/CT selective use</b> — detection of occult metastases before pancreatic resection and staging of biliary cancers (guideline-referenced)."],
  ["C","<b>FAPI PET</b> — cohort data showing higher tumor-to-background than FDG in desmoplastic pancreatic/biliary tumors (investigational)."]],
 "brain-tumor-pet": [
  ["B","<b>PET-RANO / EANM-EANO-SNMMI guidelines</b> — amino-acid PET (FET, FDOPA, MET) for glioma delineation, grading, and recurrence vs radiation necrosis."],
  ["B","<b>Amino-acid vs FDG</b> — literature establishing superior tumor-to-background of amino-acid tracers over FDG for gliomas."]],
 # ---- batch: radiopharmaceutical agents, further oncology, GFR, reporting ----
 "tc99m-sulfur-colloid": [
  ["B","<b>SNMMI procedure standards</b> — Tc-99m-sulfur colloid liver–spleen, bone-marrow, lymphoscintigraphy, and GI applications (particle-size-dependent biodistribution)."]],
 "tc99m-rbc": [
  ["B","<b>SNMMI procedure standards</b> — Tc-99m-RBC labeling and blood-pool imaging (MUGA, hepatic hemangioma, GI bleeding); in-vitro labeling maximizes efficiency."]],
 "tc99m-dtpa": [
  ["B","<b>SNMMI/EANM guidance</b> — Tc-99m-DTPA for GFR (Gates/plasma clearance), dynamic renography, and aerosol ventilation."]],
 "tc99m-pertechnetate": [
  ["B","<b>SNMMI procedure standards</b> — pertechnetate thyroid, Meckel, and salivary imaging (trapped, not organified); free-pertechnetate biodistribution."]],
 "brain-perfusion-agents": [
  ["B","<b>SNMMI/EANM brain SPECT guidelines</b> — Tc-99m-HMPAO/ECD perfusion imaging (ictal SPECT, brain death) and HMPAO leukocyte labeling."]],
 "pet-radiochemistry": [
  ["B","<b>Radiopharmacy references and USP standards</b> — cyclotron/generator production, F-18/C-11/Ga-68/Cu-64 labeling, DOTA chelation, and PET QC."]],
 "sarcoma": [
  ["B","<b>FDG grading in sarcoma</b> — SUV correlates with histologic grade; guideline use for biopsy targeting, staging, and response."],
  ["A","<b>GIST early response</b> — imatinib produces rapid FDG metabolic response predicting benefit (foundational GIST PET studies)."]],
 "carcinoma-unknown-primary": [
  ["B","<b>FDG-PET/CT in CUP</b> — meta-analyses/guidelines: primary detected in ~25–40% after negative conventional work-up; highest yield in cervical-node CUP."]],
 "gfr-measurement": [
  ["B","<b>SNMMI/EANM / BNMS GFR guidelines</b> — Gates camera method and plasma-clearance measurement of GFR (Tc-99m-DTPA / Cr-51-EDTA)."]],
 "structured-reporting": [
  ["B","<b>Standardized frameworks</b> — Deauville/Lugano, PERCIST, PROMISE/PSMA-RADS, RECIP 1.0, Krenning, Perugini, IMPeTUs, NI-RADS: society-endorsed reporting systems."]],
 "neuroblastoma": [
  ["B","<b>I-123-MIBG in neuroblastoma</b> — SNMMI/EANM guidance; Curie and SIOPEN semiquantitative scoring are prognostic and used for response."],
  ["B","<b>MIBG-non-avid disease</b> — FDG-PET and Ga-68-DOTATATE localize tumor when MIBG is negative (cohort/consensus data)."]],
 "thyroid-nodule": [
  ["B","<b>ATA thyroid nodule guidelines</b> — a scintigraphically autonomous ('hot') nodule with suppressed TSH is very rarely malignant; evaluate non-functioning nodules by ultrasound risk stratification and FNA."],
  ["B","<b>Bethesda System for Reporting Thyroid Cytopathology (2017)</b> — Cibas ES, Ali SZ. <i>Thyroid</i> 2017;27:1341–1346: the six FNA categories and their malignancy risks.", "https://doi.org/10.1089/thy.2017.0500"]],
 "lymphedema-lymphoscintigraphy": [
  ["B","<b>SNMMI/EANM lymphoscintigraphy guidance</b> — lymphatic transport assessment; dermal backflow and delayed/absent transport indicate lymphatic insufficiency."]],
 "cardiac-shunt-firstpass": [
  ["B","<b>First-pass radionuclide angiography</b> — gamma-variate Qp:Qs quantification of left-to-right shunts; Tc-99m-MAA systemic activity quantifies right-to-left shunts (SNMMI methodology)."]],
 "radionuclide-cystography": [
  ["B","<b>SNMMI/EANM pediatric guidance</b> — direct and indirect radionuclide cystography for vesicoureteral reflux with markedly lower gonadal dose than VCUG and continuous monitoring."]],
 "incidental-findings-pet": [
  ["B","<b>Focal thyroid incidentaloma on FDG-PET</b> — meta-analyses report a substantial malignancy rate for focal (not diffuse) uptake; recommend ultrasound/FNA."],
  ["B","<b>Focal colonic FDG uptake</b> — cohort data: a meaningful proportion are premalignant adenomas or carcinoma; recommend colonoscopy."]],
 "suv-harmonization-earl": [
  ["B","<b>EARL (EANM Research Ltd) accreditation</b> — phantom-based standards harmonizing SUV across scanners; EANM tumour-imaging guideline v2.0."],
  ["A","<b>PERCIST</b> — Wahl RL, et al. <i>J Nucl Med</i> 2009: response assessment requires consistent, harmonized quantitation."]],
 "pregnancy-lactation": [
  ["B","<b>SNMMI/EANM and ICRP guidance</b> — fetal-dose considerations, radioiodine contraindication in pregnancy, and breastfeeding-interruption intervals."],
  ["B","<b>NRC / regulatory guidance</b> — patient-release and close-contact precautions after therapy in lactating/childbearing patients."]],
 "scrotal-scintigraphy": [
  ["B","<b>SNMMI guidance on scrotal scintigraphy</b> — perfusion patterns of torsion (decreased), missed torsion (rim sign), and epididymitis (increased); Doppler ultrasound is first-line."]],
 # ---- tools ----
 "tool-effective-dose": [
  ["B","<b>ICRP Publication 128</b> — radiation dose coefficients (effective dose per unit administered activity) for radiopharmaceuticals."]],
 "tool-pediatric-dose": [
  ["B","<b>EANM Dosage Card</b> and <b>North American consensus pediatric guidelines</b> — weight-based administered activity with minimum-activity floors."],
  ["I","<b>Linear weight scaling is a conservative convention</b> — class-based schemes (EANM card) are non-linear; use local protocol for the definitive activity."]],
 "tool-psma-rlt": [
  ["A","<b>VISION</b> — Sartor O, et al. <i>N Engl J Med</i> 2021: OS benefit in PSMA-positive mCRPC after ARPI and taxane (the original indication)."],
  ["A","<b>PSMAfore</b> — Morris MJ, et al.: benefit in taxane-naïve mCRPC after ARPI, supporting the 2025 pre-chemotherapy label expansion."],
  ["A","<b>TheraP</b> — Hofman MS, et al. <i>Lancet</i> 2021: ¹⁷⁷Lu-PSMA-617 vs cabazitaxel — informs the Lu-PSMA-vs-taxane choice in taxane-eligible patients."],
  ["B","<b>FDG/PSMA discordance</b> — Buteau JP, et al. <i>Lancet Oncol</i> 2022 (TheraP substudy): high FDG / low PSMA disease predicts poorer benefit."],
  ["B","<b>FDA prescribing information</b> — lutetium Lu-177 vipivotide tetraxetan: PSMA positivity, mCRPC status, and organ-function requirements."]],
 "tool-dotatate-prrt": [
  ["A","<b>NETTER-1</b> — Strosberg J, et al. <i>N Engl J Med</i> 2017: ¹⁷⁷Lu-DOTATATE improved PFS in progressive, SSTR-positive midgut NETs after SSA."],
  ["A","<b>NETTER-2</b> — Singh S, et al. <i>Lancet</i> 2024: first-line ¹⁷⁷Lu-DOTATATE in grade 2–3 GEP-NET."],
  ["C","<b>Krenning score 3–4</b> gates PRRT; <b>FDG/SSTR discordance</b> predicts poorer benefit."],
  ["B","<b>SNMMI/EANM PRRT guideline & label</b> — 7.4 GBq × 4 (q8 weeks) with amino-acid renal protection; organ-function prerequisites."]],
 "cardiac-innervation-mibg": [
  ["A","<b>ADMIRE-HF</b> — Jacobson AF, et al. <i>J Am Coll Cardiol</i> 2010: low H/M ratio independently predicted cardiac events/mortality in heart failure."],
  ["B","<b>SNMMI/EANM guidance</b> on cardiac ¹²³I-MIBG (H/M ratio, washout; collimator dependence)."],
  ["C","<b>Parkinsonian syndromes</b> — reduced cardiac MIBG distinguishes Parkinson disease/DLB from MSA."]],
 "tool-vq-probability": [
  ["A","<b>PIOPED</b> — The PIOPED Investigators. <i>JAMA</i> 1990;263:2753–2759: prospective probability categories for V/Q interpretation of pulmonary embolism.", "https://doi.org/10.1001/jama.1990.03440200057023"],
  ["B","<b>Modified PIOPED II & EANM V/Q SPECT guideline</b> — mismatch-based interpretation; triple-match indeterminacy."]],
 "tool-amyloid-pathway": [
  ["B","<b>Gillmore JD, et al.</b> <i>Circulation</i> 2016;133:2404–2412 (n=1217): grade 2–3 uptake + negative monoclonal screen &gt;99% specific/PPV for ATTR."],
  ["B","<b>Multisociety practice points</b> (ASNC/AHA/ASE/EANM/SNMMI/SCMR) — SPECT mandatory, monoclonal screen required, H/CL thresholds."],
  ["A","<b>ATTR-ACT</b> — Maurer MS, et al. <i>N Engl J Med</i> 2018: tafamidis improved outcomes in ATTR cardiomyopathy (accurate diagnosis is actionable)."],
  ["C","<b>Perugini E, et al.</b> <i>J Am Coll Cardiol</i> 2005;46:1076–1084 — 0–3 visual grading scale.", "https://doi.org/10.1016/j.jacc.2005.05.073"],
  ["B","<b>ESC 2023 cardiomyopathy guidance</b> — diagnostic algorithm integrating monoclonal screen and bone scintigraphy."]],
 "tool-suv": [
  ["B","<b>EANM tumour-imaging guideline v2.0</b> (Boellaard) — SUV definition and standardization."]],
 "tool-decay": [
  ["B","<b>Radioactive decay law</b> — standard physics (A = A₀·e^(−0.693·t/t½)); isotope half-lives from reference data."]],
 "tool-renal-split": [
  ["B","<b>SNMMI/EANM renal scintigraphy guideline</b> — differential function from background-subtracted, geometric-mean-corrected counts."]],
 "tool-summed-scores": [
  ["B","<b>Berman/ASNC quantitative perfusion scoring</b> — 17-segment SSS/SRS/SDS, % myocardium, and severity ranges."],
  ["C","<b>Thresholds are software/lab-specific</b> — confirm against your normal database."]],
 "tool-pyp-amyloid": [
  ["B","<b>Multisociety PYP practice points</b> — H/CL ratio thresholds (≥1.5 at 1 h) and Perugini grading; monoclonal-protein exclusion required."],
  ["B","<b>Gillmore JD, et al.</b> <i>Circulation</i> 2016 — grade 2–3 with negative monoclonal screen is highly specific for ATTR."]],
 "tool-lung-shunt": [
  ["B","<b>SNMMI/EANM ⁹⁰Y radioembolization guidance</b> — MAA-derived lung-shunt fraction and lung-dose limits."],
  ["I","<b>Lung dose depends on the dosimetry model</b> — apply your microsphere-specific method; LSF thresholds here are conventional planning guides."]],
}

# ============================ INTERACTIVE TOOLS ============================
# Raw HTML widgets injected verbatim (not markdown-processed). Each is an IIFE
# with a unique id prefix so multiple tools coexist on the single-page app.
# TOOLS (interactive calculators) are loaded from assets/tools/*.html — one file
# per tool, edited in native HTML/JS (no Python-string escaping hazards).
TOOLS = {}
for _tf in sorted(glob.glob(os.path.join(BASE.replace('/content',''), 'assets', 'tools', '*.html'))):
    TOOLS[os.path.basename(_tf)[:-5]] = open(_tf, encoding='utf-8').read()

# ============================ LANDMARK-STUDY ENRICHMENT ============================
# Additional major-trial citations appended to existing pages, referenced where applicable.
EXTRA_EVIDENCE = {
 "vision-trial": [
  ["A","<b>VISION</b> — Sartor O, et al. <i>N Engl J Med</i> 2021;385:1091–1103: ¹⁷⁷Lu-PSMA-617 improved OS and rPFS in PSMA-positive mCRPC.", "https://doi.org/10.1056/NEJMoa2107322"]],
 "netter-1-trial": [
  ["A","<b>NETTER-1</b> — Strosberg J, et al. <i>N Engl J Med</i> 2017;376:125–135: ¹⁷⁷Lu-DOTATATE improved PFS in progressive midgut NETs.", "https://doi.org/10.1056/NEJMoa1607427"]],
 "alsympca-trial": [
  ["A","<b>ALSYMPCA</b> — Parker C, et al. <i>N Engl J Med</i> 2013;369:213–223: ²²³Ra improved OS in symptomatic bone-metastatic mCRPC.", "https://doi.org/10.1056/NEJMoa1213755"]],
 "therap-trial": [
  ["A","<b>TheraP</b> — Hofman MS, et al. <i>Lancet</i> 2021;397:797–804: ¹⁷⁷Lu-PSMA-617 vs cabazitaxel — higher PSA response, fewer severe toxicities.", "https://doi.org/10.1016/S0140-6736(21)00237-3"]],
 "propsma-trial": [
  ["A","<b>proPSMA</b> — Hofman MS, et al. <i>Lancet</i> 2020;395:1208–1216: PSMA PET/CT more accurate than conventional imaging for high-risk staging.", "https://doi.org/10.1016/S0140-6736(20)30314-7"]],
 "netter-2-trial": [
  ["A","<b>NETTER-2</b> — Singh S, et al. <i>Lancet</i> 2024;403:2807–2817: first-line ¹⁷⁷Lu-DOTATATE more than doubled PFS in grade 2–3 SSTR-positive GEP-NETs.", "https://doi.org/10.1016/S0140-6736(24)00701-3"]],
 "psmafore-trial": [
  ["A","<b>PSMAfore</b> — Morris MJ, et al. <i>Lancet</i> 2024;404:1227–1239: ¹⁷⁷Lu-PSMA-617 improved rPFS vs ARPI change in taxane-naïve mCRPC (OS confounded by crossover).", "https://doi.org/10.1016/S0140-6736(24)01653-2"]],
 "enza-p-trial": [
  ["A","<b>ENZA-p</b> — Emmett L, et al. <i>Lancet Oncol</i> 2024;25:563–571: enzalutamide + ¹⁷⁷Lu-PSMA-617 improved PSA-PFS with PSMA-PET-adaptive dosing in first-line mCRPC.", "https://doi.org/10.1016/S1470-2045(24)00135-9"]],
 "era-223-trial": [
  ["A","<b>ERA-223</b> — Smith M, et al. <i>Lancet Oncol</i> 2019;20:408–419: adding ²²³Ra to abiraterone+prednisone did not improve outcomes and increased fractures; use a bone-health agent, avoid the combination.", "https://doi.org/10.1016/S1470-2045(18)30860-X"]],
 "fit-trial": [
  ["A","<b>FIT (First-line Indolent Trial)</b> — Morschhauser F, et al. <i>J Clin Oncol</i> 2008;26:5156–5164: ⁹⁰Y-ibritumomab tiuxetan consolidation prolonged PFS after first remission in follicular lymphoma.", "https://doi.org/10.1200/JCO.2008.17.2015"]],
 "parr-2-trial": [
  ["A","<b>PARR-2</b> — Beanlands RSB, et al. <i>J Am Coll Cardiol</i> 2007;50:2002–2012: FDG-PET viability-guided management was neutral overall but beneficial when recommendations were followed (Ottawa-FIVE).", "https://doi.org/10.1016/j.jacc.2007.09.006"]],
 "pioped-trial": [
  ["A","<b>PIOPED</b> — The PIOPED Investigators. <i>JAMA</i> 1990;263:2753–2759: defined V/Q probability categories; scan must be combined with clinical pretest probability.", "https://jamanetwork.com/journals/jama/fullarticle/381954"],
  ["A","<b>PIOPED II</b> — Stein PD, et al. <i>N Engl J Med</i> 2006;354:2317–2327: characterized multidetector CT pulmonary angiography for acute PE.", "https://doi.org/10.1056/NEJMoa052367"]],
 "quantitative-lung-perfusion": [
  ["B","<b>ACCP / ERS–ESTS physiologic-evaluation guidelines</b> — predicted postoperative FEV₁/DLCO from split perfusion; the ~40%-predicted high-risk threshold and staged exercise testing."],
  ["B","<b>SNMMI/EANM lung-scintigraphy guidance</b> — geometric-mean planar and SPECT quantification of regional perfusion for split-function estimation."]],
 "cteph-vq": [
  ["B","<b>ESC/ERS pulmonary hypertension guidelines</b> — V/Q scintigraphy as the recommended screening test for CTEPH; a normal scan effectively excludes it."],
  ["B","<b>Tunariu N, et al.</b> <i>J Nucl Med</i> 2007 — V/Q scintigraphy is more sensitive than CTPA for chronic thromboembolic pulmonary disease."],
  ["I","<b>Curability rationale</b> — CTEPH is the potentially operable (PEA) / BPA-amenable PH group, so a sensitive screen changes management."]],
 "pe-imaging-pregnancy": [
  ["B","<b>ATS/STR clinical practice guideline</b> — evaluation of suspected pulmonary embolism in pregnancy (CXR-guided pathway; perfusion-only option; leg ultrasound first when DVT is suspected)."],
  ["C","<b>Dosimetry reviews</b> — fetal doses from V/Q and CTPA are well below the ~100 mGy threshold; CTPA delivers the higher maternal breast dose."]],
 "why-nuclear-medicine": [
  ["B","<b>White paper on radiopharmaceutical therapy</b> (<i>J Nucl Med</i> 2025) — RPT market growth (~$750M 2022 → ~$5.5B 2028), 80+ agents in development, and the workforce shortage."],
  ["B","<b>Lancet Oncology Commission</b> — projected global PSMA radioligand-therapy demand (&gt;500,000 doses/year) requiring hundreds of new centers and more trained experts."]],
 "becoming-a-nuclear-medicine-physician": [
  ["B","<b>American Board of Nuclear Medicine (ABNM)</b> — initial-certification training requirements and pathways (dedicated NM residency; NM within/through diagnostic radiology; other-specialty routes)."],
  ["B","<b>American Board of Radiology (ABR)</b> — nuclear radiology subspecialty pathways, including the 16-month pathway; NRC 10 CFR Part 35 authorized-user framework."]],
 "careers-in-nuclear-medicine": [
  ["B","<b>SNMMI Career Center</b> — the primary continuously-updated nuclear-medicine / molecular-imaging job board (academic, hospital, industry; filterable by location)."],
  ["B","<b>Radiopharmaceutical-therapy workforce analyses</b> (<i>J Nucl Med</i> 2025; <i>Lancet Oncol</i> 2024) — the demand/capacity gap driving hiring and academic-out-of-residency recruitment."]],
 "the-therapy-transformation": [
  ["B","<b>Radiopharmaceutical-therapy workforce/growth analyses</b> (<i>J Nucl Med</i> 2025; <i>Lancet Oncol</i> 2024) — market and demand projections, targets pipeline, and the training imperative."],
  ["A","<b>Pivotal RPT trials</b> — VISION, NETTER-1/2, TheraP, ALSYMPCA, PSMAfore: the evidence base for the therapeutic transformation (see Landmark Trials)."]],
 "correlative-ct-overview": [
  ["B","<b>SNMMI/EANM PET/CT and SPECT/CT practice guidance</b> — low-dose CT for attenuation correction and localization; when a diagnostic contrast CT is separately indicated."],
  ["B","<b>ACR–SNMMI guidance</b> — the interpreting physician's responsibility for findings visible on the CT component of hybrid imaging."]],
 "nm-radiologist-ct-line": [
  ["B","<b>ACR–SNMMI guidance</b> — interpreting-physician responsibility for CT findings on hybrid studies; scope of the low-dose non-contrast component."],
  ["B","<b>ACR practice parameters</b> — communication of imaging findings and appropriate scope of interpretation."]],
 "urgent-actionable-ct-findings": [
  ["B","<b>ACR practice parameter for communication of diagnostic imaging findings</b> — critical/actionable results and closed-loop communication, including incidental findings."],
  ["B","<b>ACR Incidental Findings Committee white papers</b> — management of incidental adrenal, renal, hepatic, thyroid, and pulmonary findings."],
  ["B","<b>Fleischner Society guidelines</b> — incidental pulmonary nodule follow-up."]],
 "reading-low-dose-noncontrast-ct": [
  ["B","<b>Fleischner Society guidelines</b> — management of incidental pulmonary nodules detected on CT."],
  ["C","<b>Non-contrast density characterization</b> — HU thresholds for adrenal adenoma (≤10 HU), simple cysts, fat-containing and calcified lesions; low-dose noise caveats."]],
 "normal-cross-sectional-ct-anatomy": [
  ["B","<b>Cross-sectional anatomy and CT measurement references</b> — mediastinal nodal-station maps and normal organ/vessel dimensions used as 'enlarged' thresholds."],
  ["C","<b>Size-threshold literature</b> — short-axis lymph-node (&lt;1 cm), aortic (&lt;3 cm abdominal), and biliary (age-adjusted) cutoffs; imperfect specificity of size alone."]],
 "ct-tracer-correlation": [
  ["B","<b>Integrated PET/CT–SPECT/CT interpretation guidance</b> — uptake correlated with CT substrate improves specificity over either dataset alone."],
  ["C","<b>Benign-uptake reviews</b> — calcified/granulomatous, fatty, degenerative, brown-fat, and physiologic substrates that reclassify focal uptake as benign."]],
 "cns-lymphoma-toxoplasmosis": [
  ["B","<b>Thallium-201 SPECT and FDG-PET</b> differentiating primary CNS lymphoma (avid) from toxoplasmosis (non-avid) in immunocompromised patients."],
  ["C","<b>Ring-enhancing-lesion differential</b> — reviews on empiric anti-toxoplasma therapy with follow-up imaging and biopsy when uptake favours lymphoma."]],
 "peritoneal-carcinomatosis": [
  ["B","<b>FDG-PET/CT for peritoneal carcinomatosis</b> — sensitivity for macroscopic disease; limits in small-volume miliary and low-grade mucinous disease."],
  ["C","<b>Cytoreductive surgery/HIPEC selection</b> — peritoneal cancer index and the reference role of laparoscopy for true peritoneal burden."]],
 "solitary-pulmonary-nodule": [
  ["B","<b>MacMahon H, et al.</b> Guidelines for management of incidental pulmonary nodules detected on CT: <b>Fleischner Society 2017</b>. <i>Radiology</i> 2017;284:228–243.", "https://doi.org/10.1148/radiol.2017161659"],
  ["B","<b>Diagnostic accuracy reviews</b> — FDG false positives (granulomatous/infectious disease) and false negatives (carcinoid, lepidic adenocarcinoma, ground-glass and sub-cm nodules); SUV 2.5 as a heuristic."]],
 "mesothelioma": [
  ["B","<b>Reviews of FDG-PET/CT in malignant pleural mesothelioma</b> — malignant-vs-benign pleural disease, staging, prognosis, and response."],
  ["C","<b>Talc pleurodesis</b> as a durable, intensely FDG-avid granulomatous pitfall in the reviewed literature."]],
 "anal-squamous-carcinoma": [
  ["B","<b>Society guidance/cohorts</b> on FDG-PET/CT for staging, radiotherapy field definition (inguinal/pelvic nodes), and post-chemoradiation response in anal SCC."]],
 "bladder-urothelial-cancer": [
  ["B","<b>SNMMI/EANM guidance</b> on FDG-PET/CT in urothelial carcinoma — diuretic/delayed pelvic technique to overcome urinary excretion; nodal/distant staging role."],
  ["B","<b>Staging cohorts</b> — FDG-PET/CT superior to CT for nodal and distant disease in muscle-invasive bladder cancer; response-assessment caveats."]],
 "pediatric-oncology-pet": [
  ["B","<b>EANM pediatric dosage card</b> and North American consensus pediatric dosing; Image Gently/ALARA principles for weight-based activity."],
  ["A","<b>PET-adapted pediatric lymphoma trials</b> (Deauville response) and MIBG Curie/SIOPEN scoring with ¹³¹I-MIBG therapy selection in neuroblastoma."]],
 "thymic-epithelial-tumors": [
  ["B","<b>FDG-PET/CT in thymic epithelial tumours</b> — SUV correlation with WHO grade and thymic carcinoma vs thymoma; staging of pleural/nodal spread."],
  ["C","<b>Anterior mediastinal mass differential</b> and thymic hyperplasia/rebound as an FDG pitfall in the reviewed literature."]],
 "immunotherapy-response-fdg": [
  ["A","<b>iRECIST</b> (Seymour L, et al. <i>Lancet Oncol</i> 2017) — immune-adapted response criteria requiring confirmation of progression, addressing pseudoprogression."],
  ["B","<b>PET-specific immune response frameworks</b> (PERCIMT, imPERCIST/iPERCIST) and reviews of immune-related adverse events and the sarcoid-like reaction on FDG-PET/CT."]],
 "fdg-radiotherapy-planning": [
  ["A","<b>Stage-changing impact</b> — trials/cohorts in locally advanced NSCLC showing FDG-PET alters radiotherapy candidacy and target volumes; treatment-position PET/CT guidance."],
  ["B","<b>Post-chemoradiation surveillance</b> — negative ~12-week FDG-PET supports watch-and-wait of the neck in head-and-neck cancer (high negative predictive value)."]],
 "thyroid-cancer-fdg-flip-flop": [
  ["B","<b>ATA differentiated thyroid cancer guidelines</b> — radioiodine-refractory definitions and FDG-PET for thyroglobulin-positive, iodine-negative (TENIS) disease."],
  ["B","<b>Prognosis & redifferentiation</b> — FDG avidity as an adverse prognostic marker; MEK/BRAF-inhibitor restoration of radioiodine avidity in RAI-refractory DTC."]],
 "radiopharmaceutical-compendium": [
  ["B","<b>SNMMI/EANM procedure guidelines</b> for the individual agents tabulated — isotope, mechanism, target, and indication per current society standards."],
  ["C","<b>Mechanism-based organization</b> — grouping tracers by target class (perfusion, metabolism, receptor, antigen, transporter, etc.) follows standard radiopharmacology and this atlas's Domain II framework."]],
 "cardiac-viability-imaging-selection": [
  ["B","<b>ASNC/SNMMI guidance</b> on FDG PET myocardial viability and metabolic preparation — perfusion–metabolism mismatch as the marker of hibernating myocardium."],
  ["B","<b>Comparative literature</b> — FDG-PET mismatch, thallium redistribution, and LGE-MRI scar transmurality for predicting recovery of function after revascularization."]],
 "pulmonary-embolism-imaging-selection": [
  ["B","<b>EANM V/Q scintigraphy and V/Q SPECT guidelines</b>; PIOPED II — modality selection for suspected acute PE by contrast/radiation considerations and pretest probability."],
  ["B","<b>CTEPH screening</b> — society guidance establishing V/Q as more sensitive than CTPA for chronic thromboembolic disease; a normal V/Q effectively excludes it."]],
 "bone-metastasis-imaging-selection": [
  ["B","<b>SNMMI/EANM bone scintigraphy and ¹⁸F-NaF PET guidelines</b>; guidance on FDG-PET and PSMA PET for skeletal staging — osteoblastic vs metabolic vs target-specific imaging."],
  ["B","<b>Tumor-specific data</b> — PSMA PET for prostate bone mets, FDG/whole-body MRI for lytic and myeloma disease; bone scan insensitivity to purely lytic metastases."]],
 "parathyroid-imaging-selection": [
  ["A","<b>Comparative meta-analyses</b> — ¹⁸F-fluorocholine PET/CT shows higher pooled sensitivity than sestamibi and ⁴ᴰ-CT for parathyroid localization in primary hyperparathyroidism."],
  ["B","<b>SNMMI/EANM parathyroid imaging guidelines</b> — roles of ultrasound, dual-phase/dual-tracer sestamibi SPECT/CT, ⁴ᴰ-CT, and choline PET; imaging is for localization, not diagnosis."]],
 "neuroendocrine-imaging-selection": [
  ["A","<b>SSTR PET superiority</b> — ⁶⁸Ga-DOTATATE PET/CT outperforms ¹¹¹In-pentetreotide and CT for well-differentiated NET; basis for staging and PRRT selection."],
  ["B","<b>Dual SSTR/FDG imaging</b> — cohorts (e.g. NETPET grade) linking the SSTR/FDG flip-flop to grade, prognosis, and therapy response; genotype-driven PPGL imaging."]],
 "infection-imaging-selection": [
  ["B","<b>SNMMI/EANM joint guidelines</b> on labeled-leukocyte scintigraphy and ¹⁸F-FDG imaging of infection/inflammation — site-specific modality selection."],
  ["B","<b>WBC + marrow subtraction</b> — society guidance establishing spatial incongruence with sulfur-colloid marrow as the criterion for skeletal/prosthetic-joint infection."]],
 "dementia-imaging-selection": [
  ["B","<b>Johnson KA, et al.</b> <b>Appropriate-use criteria for amyloid PET</b> (Amyloid Imaging Task Force / SNMMI / Alzheimer's Association). <i>J Nucl Med</i> 2013;54:476–490.", "https://doi.org/10.2967/jnumed.113.120618"],
  ["B","<b>EANM/SNMMI ¹²³I-ioflupane (DAT-SPECT) guidelines</b> and FDG brain PET guidance — dopaminergic integrity vs metabolic pattern for the cognitive/parkinsonian differential."]],
 "prostate-cancer-imaging-selection": [
  ["A","<b>proPSMA</b> — Hofman MS, et al. <i>Lancet</i> 2020: PSMA PET/CT more accurate than conventional CT + bone scan for high-risk staging, changing management."],
  ["B","<b>Recurrence detection by PSA</b> — cohorts showing PSMA PET's detection advantage at low PSA over choline/fluciclovine; dual PSMA/FDG for therapy selection."]],
 "superscan": [
  ["B","<b>SNMMI/EANM bone scintigraphy guidelines</b> and normal-variant atlases — recognition of diffuse skeletal uptake with the absent-kidney sign."],
  ["C","<b>Metastatic vs metabolic superscan</b> — distribution-based differentiation (axial-predominant irregular uptake vs uniform metabolic pattern with calvarial/costochondral/metaphyseal features) described across the imaging literature."]],
 "photopenic-cold-lesions": [
  ["B","<b>Organ-specific procedure guidelines</b> (bone, thyroid, hepatic, cardiac) — photopenic-lesion differential and the higher malignancy risk of cold thyroid nodules and lytic/destructive bone lesions."],
  ["C","<b>Artifact-first discipline</b> — attenuation and technical causes of cold defects resolved with CT correlation / non-attenuation-corrected review."]],
 "physiologic-fdg-mimics": [
  ["B","<b>SNMMI/EANM FDG-PET/CT oncology guidelines</b> — patient preparation and suppression of physiologic uptake (fasting/glucose control, warming for brown fat, avoiding insulin/exercise, G-CSF timing)."],
  ["C","<b>Normal-variant atlases</b> — brown fat, muscle, bowel/metformin, thymic rebound, G-CSF marrow, and inflammatory false positives on FDG."]],
 "attenuation-artifacts": [
  ["B","<b>SNMMI/EANM PET-CT and SPECT-CT guidance</b> — attenuation correction, respiratory misregistration, dense-material over-correction, halo and truncation artifacts."],
  ["B","<b>Nuclear cardiology literature</b> — soft-tissue (breast/diaphragm) attenuation, gated wall-motion analysis, and attenuation-correction/prone imaging to separate artifact from scar."]],
 "flare-phenomenon": [
  ["B","<b>Bone-scintigraphy flare</b> — reviews of transient osteoblastic healing uptake within ~3 months of effective systemic therapy for prostate/breast cancer, resolving on interval follow-up."],
  ["B","<b>PERCIST and immunotherapy response criteria</b> — treatment-related inflammation and pseudoprogression on FDG-PET addressed via timing and confirmatory imaging."]],
 "discordant-psma-fdg": [
  ["B","<b>Dual PSMA/FDG PET</b> — analyses using paired imaging to identify PSMA-negative/FDG-positive disease and select/prognosticate patients before ¹⁷⁷Lu-PSMA therapy."],
  ["C","<b>Neuroendocrine SSTR/FDG flip-flop</b> — target-negative, FDG-avid dedifferentiated disease as a determinant of theranostic eligibility."]],
 "lu177-psma-617": [
  ["A","<b>TheraP</b> — Hofman MS, et al. <i>Lancet</i> 2021: ¹⁷⁷Lu-PSMA-617 vs cabazitaxel in mCRPC — higher PSA response with fewer grade 3–4 events."],
  ["A","<b>ENZA-p</b> — Emmett L, et al. <i>Lancet Oncol</i> 2024 (ANZUP): adding ¹⁷⁷Lu-PSMA to enzalutamide improved PSA-progression-free survival."]],
 "theranostics-overview": [
  ["A","<b>TheraP</b> — Hofman MS, et al. <i>Lancet</i> 2021: randomized ¹⁷⁷Lu-PSMA-617 vs cabazitaxel."],
  ["A","<b>DOSISPHERE-01</b> — Garin E, et al. <i>Lancet Gastroenterol Hepatol</i> 2021: personalized dosimetry improved response in ⁹⁰Y for HCC."]],
 "prostate-cancer": [
  ["A","<b>TheraP</b> — Hofman MS, et al. <i>Lancet</i> 2021 (¹⁷⁷Lu-PSMA-617 vs cabazitaxel)."]],
 "psma-11": [
  ["B","<b>OSPREY / CONDOR</b> — Pienta KJ, <i>J Urol</i> 2021; Morris MJ, <i>Clin Cancer Res</i> 2021: ¹⁸F-DCFPyL (piflufolastat) staging and biochemical-recurrence localization."]],
 "psma-biochemical-recurrence": [
  ["B","<b>CONDOR</b> — Morris MJ, et al. <i>Clin Cancer Res</i> 2021;27:3674–3682: ¹⁸F-DCFPyL correct localization rate in biochemical recurrence with negative/equivocal imaging.", "https://doi.org/10.1158/1078-0432.CCR-20-4573"]],
 "y90-radioembolization": [
  ["A","<b>DOSISPHERE-01</b> — Garin E, et al. <i>Lancet Gastroenterol Hepatol</i> 2021: personalized vs standard dosimetry improved response in ⁹⁰Y for HCC."]],
 "hepatocellular-carcinoma": [
  ["A","<b>DOSISPHERE-01</b> — Garin E, et al. <i>Lancet Gastroenterol Hepatol</i> 2021: personalized dosimetry in ⁹⁰Y radioembolization for HCC."],
  ["A","<b>LEGACY</b> — Salem R, et al. <i>Hepatology</i> 2021;74:2342–2352: radiation segmentectomy achieved high response and durable control in early HCC.", "https://doi.org/10.1002/hep.31819"]],
 "lu177-dotatate": [
  ["A","<b>COMPETE / COMPOSIT context</b> and long-term NETTER-1 (Strosberg, <i>Lancet Oncol</i> 2021): sustained PFS benefit and quality-of-life advantage of PRRT."]],
 "nuclear-cardiology-overview": [
  ["A","<b>ISCHEMIA</b> — Maron DJ, et al. <i>N Engl J Med</i> 2020;382:1395–1407: in stable CAD with moderate–severe ischemia, a routine invasive strategy did not reduce events vs medical therapy.", "https://doi.org/10.1056/NEJMoa1915922"]],
 "mpi-spect": [
  ["A","<b>Warranty period</b> — Metz LD, et al. <i>J Am Coll Cardiol</i> 2007: meta-analysis of low event rates after a normal stress MPI."],
  ["A","<b>ISCHEMIA</b> — Maron DJ, et al. <i>N Engl J Med</i> 2020;382:1395–1407: reframes how ischemia burden should guide revascularization decisions.", "https://doi.org/10.1056/NEJMoa1915922"]],
 "mpi-interpretation-grading": [
  ["A","<b>ISCHEMIA</b> — Maron DJ, et al. <i>N Engl J Med</i> 2020;382:1395–1407: ischemia severity alone did not identify a revascularization survival benefit — interpret extent/severity in this context.", "https://doi.org/10.1056/NEJMoa1915922"]],
 "myocardial-viability": [
  ["A","<b>PARR-2</b> — Beanlands RS, et al. <i>J Am Coll Cardiol</i> 2007: FDG-PET-assisted management in ischemic cardiomyopathy."],
  ["A","<b>STICH viability substudy</b> — Bonow RO, et al. <i>N Engl J Med</i> 2011 (see also main sources)."]],
 "cardiac-amyloidosis": [
  ["A","<b>ATTR-ACT</b> — Maurer MS, et al. <i>N Engl J Med</i> 2018: tafamidis improved survival in ATTR cardiomyopathy — raising the stakes of accurate PYP diagnosis."]],
 "pyp": [
  ["A","<b>ATTR-ACT</b> — Maurer MS, et al. <i>N Engl J Med</i> 2018: disease-modifying therapy for ATTR makes accurate diagnosis actionable."]],
 "fdg-oncology": [
  ["B","<b>National Oncologic PET Registry (NOPR)</b> — Hillner BE, et al. <i>J Clin Oncol</i> 2008: FDG-PET changed intended management in roughly a third of cases across cancers."]],
 "fdg": [
  ["B","<b>NOPR</b> — Hillner BE, et al. <i>J Clin Oncol</i> 2008: real-world impact of FDG-PET on oncologic management."]],
 "lymphoma": [
  ["A","<b>Interim-PET-adapted trials</b> — H10 (André, <i>J Clin Oncol</i> 2017) and PETAL (Dührsen, <i>J Clin Oncol</i> 2018): interim-PET response guides therapy in Hodgkin and aggressive NHL."]],
 "lung-cancer": [
  ["A","<b>PET in NSCLC staging</b> — van Tinteren H (PLUS), <i>Lancet</i> 2002; Fischer B, <i>N Engl J Med</i> 2009: PET-based staging reduces futile thoracotomy."]],
 "thyroid-cancer": [
  ["A","<b>DECISION / SELECT</b> — Brose MS, <i>Lancet</i> 2014 (sorafenib); Schlumberger M, <i>N Engl J Med</i> 2015 (lenvatinib): multikinase inhibitors improve PFS in RAI-refractory DTC."],
  ["B","<b>Redifferentiation</b> — Ho AL, et al. <i>N Engl J Med</i> 2013: selumetinib restored radioiodine uptake in a subset of RAI-refractory patients."]],
 "amyloid-tau-pet": [
  ["B","<b>IDEAS study</b> — Rabinovici GD, et al. <i>JAMA</i> 2019;321:1286–1294: amyloid PET changed management in ~60% of patients with uncertain-cause cognitive impairment.", "https://doi.org/10.1001/jama.2019.2000"]],
 "brain-fdg-dementia": [
  ["B","<b>IDEAS study</b> — Rabinovici GD, et al. <i>JAMA</i> 2019;321:1286–1294: real-world impact of amyloid PET on diagnosis and management.", "https://doi.org/10.1001/jama.2019.2000"]],
 "ioflupane": [
  ["B","<b>DaTscan validation</b> — Benamer HTS, et al. <i>Mov Disord</i> 2000; Catafau AM, et al. 2004: reproducible differentiation of degenerative parkinsonism from essential tremor."]],
 "ra223-dichloride": [
  ["A","<b>ALSYMPCA</b> — Parker C, et al. <i>N Engl J Med</i> 2013 (survival and symptomatic-skeletal-event benefit; see also main sources)."]],
 "bone-pain-palliation": [
  ["B","Sartor O, et al. Samarium-153-EDTMP for painful bone metastases — randomized pain-response data."],
  ["B","Strontium-89 (Metastron) trials — pain palliation in metastatic prostate/breast disease; myelosuppression profile."],
  ["INFERENCE","Requirement for osteoblastic (positive bone-scan) uptake follows directly from the diphosphonate/calcium-analog mechanism."]],
 "radiosynovectomy": [
  ["B","EANM procedure guidelines for radiosynovectomy (isotope selection by joint size; technique and leakage mitigation)."],
  ["INFERENCE","Isotope-to-joint-size matching follows from published soft-tissue beta ranges (Y-90 > Re-186 > Er-169)."]],
 "phosphorus-32-therapies": [
  ["B","Polycythemia Vera Study Group and subsequent analyses — P-32 efficacy and increased leukemic transformation vs phlebotomy."],
  ["INFERENCE","Second-line positioning reflects the transformation-risk data relative to phlebotomy/hydroxyurea."]],
 "radionuclide-therapy-toxicity-monitoring": [
  ["A","<b>NETTER-1</b> — Strosberg J, et al. <i>N Engl J Med</i> 2017 (¹⁷⁷Lu-DOTATATE; amino-acid renal protection, toxicity profile)."],
  ["A","<b>VISION</b> — Sartor O, et al. <i>N Engl J Med</i> 2021 (¹⁷⁷Lu-PSMA-617; marrow/salivary toxicity)."],
  ["B","EANM/SNMMI guidance on organ-at-risk monitoring and eligibility for radioligand therapy."]],
 "usp-compounding-standards": [
  ["B","USP General Chapters ⟨795⟩, ⟨797⟩, and ⟨825⟩ (radiopharmaceutical preparation, compounding, dispensing, repackaging)."],
  ["INFERENCE","The rationale for a radiopharmaceutical-specific chapter (short half-life, ALARA vs asepsis) is inferred from the chapters' stated scope."]],
 "radiation-accident-contamination-management": [
  ["B","US NRC regulations on medical events and reporting; SNMMI/health-physics spill-response and decontamination guidance."],
  ["INFERENCE","Spill-response priority (protect → contain → decontaminate → survey) synthesizes standard radiation-safety practice."]],
 "cardiac-device-endocarditis-fdg": [
  ["B","ESC guidelines on infective endocarditis — FDG-PET/CT abnormal peri-valvular uptake as a major diagnostic criterion for prosthetic-valve endocarditis."],
  ["B","SNMMI/EANM/ASNC guidance on FDG-PET/CT for cardiac device (CIED) and vascular-graft infection, including myocardial-suppression preparation."],
  ["INFERENCE","The >3-month post-op caveat follows from post-surgical inflammation overlapping infective uptake."]],
 "thyroid-cancer-i131-therapy": [
  ["A","<b>ESTIMABL</b> (Schlumberger) and <b>HiLo</b> (Mallick) — 30 mCi + rhTSH non-inferior to 100 mCi + withdrawal for low-risk remnant ablation. <i>N Engl J Med</i> 2012."],
  ["B","ATA management guidelines for differentiated thyroid cancer — risk-adapted RAI, preparation, and post-therapy scanning."],
  ["B","Benua/Leeper dosimetry limits (blood/whole-body/lung) for high-activity and metastatic I-131 therapy."]],
 "quantitative-bone-spect": [
  ["B","SNMMI/EANM and vendor literature on quantitative SPECT/CT (xSPECT Quant and equivalents) — calibration, SUV recovery, and reproducibility in bone imaging."],
  ["INFERENCE","Dependence on standardized reconstruction/calibration follows directly from the same physics governing PET SUV harmonization."]],
 "radioactive-materials-licensing-waste": [
  ["B","NRC 10 CFR Parts 20 & 35 (and Agreement-State equivalents) — medical use, Authorized User/RSO, surveys, waste, and reporting."],
  ["B","DOT hazardous-materials transport regulations for radioactive packages (labels, transport index)."],
  ["INFERENCE","The ≥10-half-life decay-in-storage rule follows from reducing activity to ~0.1% (below background)."]],
 "acetazolamide-brain-perfusion": [
  ["B","SNMMI/EANM guidance on brain perfusion SPECT with acetazolamide challenge for cerebrovascular reserve."],
  ["B","Studies of cerebrovascular reserve and stroke risk in carotid occlusion/moyamoya guiding revascularization (e.g., EC-IC bypass selection)."],
  ["INFERENCE","The augment-vs-fail pattern follows from exhausted autoregulatory arteriolar dilation."]],
 "radiopharmaceutical-extravasation": [
  ["B","SNMMI/EANM commentary on injection quality and extravasation — effects on SUV quantification and dosimetry."],
  ["C","Reports of therapeutic-radiopharmaceutical extravasation causing local tissue dose; evolving US reporting policy."],
  ["INFERENCE","Falsely low SUV follows directly from injection-site activity being excluded from tissue distribution."]],
 "total-body-pet": [
  ["B","Reviews of long-axial-FOV/total-body PET (uEXPLORER, Biograph Vision Quadra) — sensitivity gains and total-body dynamic/parametric imaging."],
  ["INFERENCE","The dose/speed/delayed-imaging trade space follows directly from the order-of-magnitude sensitivity increase."]],
 "esophagogastric-cancer": [
  ["B","Guidelines and cohorts on FDG-PET/CT staging of esophageal/EGJ cancer — detection of occult M1 disease altering surgical candidacy."],
  ["A","<b>MUNICON</b> — Lordick F, et al. PET-guided neoadjuvant therapy in EGJ adenocarcinoma (early metabolic response). <i>Lancet Oncol</i> 2007."],
  ["INFERENCE","FDG-low signet-ring/mucinous/diffuse histology follows from their low glycolytic/glucose-transporter phenotype."]],
 "emerging-research-pet-tracers": [
  ["B","Reviews of hypoxia (FMISO/FAZA/Cu-ATSM), proliferation (FLT), CXCR4 (pentixafor), GRPR, and amino-acid (MET/FET) PET tracers."],
  ["INFERENCE","Each tracer's niche follows from targeting a biology (hypoxia/proliferation/receptor/amino-acid transport) distinct from glucose metabolism."]],
 "abbreviations-glossary": [
  ["INFERENCE","Reference glossary compiled from the atlas's own usage; terms are defined per standard nuclear-medicine nomenclature."]],
 "effective-dose-reference": [
  ["B","ICRP radiopharmaceutical dose coefficients and SNMMI/EANM dose references for common nuclear-medicine procedures."],
  ["INFERENCE","Per-study figures are representative and scale with administered activity and any CT component."]],
 "radiation-interactions-matter": [
  ["B","Standard nuclear-medicine physics references (Cherry/Sorenson & Phelps) — photoelectric, Compton, pair production, and attenuation."],
  ["INFERENCE","Z³/E³ photoelectric and Z-independent Compton dependences are standard interaction-cross-section results."]],
 "colonic-whole-gut-transit": [
  ["B","SNMMI/consensus guidance on colonic and whole-gut transit scintigraphy (geometric-center method) for chronic constipation/dysmotility."],
  ["INFERENCE","The 72-hour imaging requirement follows from the slow physiologic timescale of colonic transit."]],
 "nuclear-hematology-studies": [
  ["B","ICSH/classic references on Cr-51 red-cell survival, splenic sequestration surface counting, and blood-volume measurement."],
  ["INFERENCE","The apparent-vs-true survival discrepancy follows directly from Cr-51 elution from red cells."]],
 "meningioma": [
  ["B","Studies of Ga-68-DOTATATE PET in meningioma — SSTR2 expression, radiotherapy target-volume delineation, and recurrence assessment."],
  ["C","Investigational ¹⁷⁷Lu-DOTATATE PRRT for refractory/progressive meningioma."],
  ["INFERENCE","Low-background advantage over FDG follows from meningioma SSTR2 expression vs high physiologic cortical FDG uptake."]],
 "pediatric-dosimetry": [
  ["B","North American Consensus Guidelines for pediatric administered activity; EANM pediatric dosage card."],
  ["B","Image Gently / SNMMI pediatric ALARA recommendations."],
  ["INFERENCE","The minimum-activity principle follows from the repeat-study dose penalty of a non-diagnostic scan."]],
 "labeled-leukocyte-scintigraphy": [
  ["B","SNMMI/EANM procedure guidelines for ¹¹¹In-oxine and ⁹⁹ᵐTc-HMPAO leukocyte imaging."],
  ["B","Combined leukocyte/marrow (sulfur-colloid) imaging for complicating osteomyelitis — dual-tracer incongruence."],
  ["INFERENCE","Preference for In-111 in the abdomen follows from HMPAO's physiologic bowel/renal excretion."]],
 "fdopa": [
  ["B","SNMMI/EANM guidance on ¹⁸F-FDOPA PET in neuroendocrine tumors, congenital hyperinsulinism, and movement disorders."],
  ["B","FDOPA for focal vs diffuse congenital hyperinsulinism; sensitivity in MIBG-negative/SDHx paraganglioma and MTC recurrence."],
  ["INFERENCE","Carbidopa's tumor-uptake benefit follows from blockade of peripheral AADC decarboxylation."]],
 "cholescintigraphy-hida": [
  ["B","SNMMI procedure standard for hepatobiliary scintigraphy (acute cholecystitis, morphine augmentation, GBEF)."],
  ["B","CCK-cholescintigraphy consensus recommendations for gallbladder ejection fraction (standardized infusion)."],
  ["INFERENCE","Both short- and long-fasting false positives follow from gallbladder contraction vs distension physiology."]],
 "adrenal-cortical-scintigraphy": [
  ["B","NP-59 (I-131-iodocholesterol) adrenocortical scintigraphy — lateralization in primary aldosteronism/Cushing; dexamethasone-suppression protocol."],
  ["B","Adrenal venous sampling as reference standard for aldosteronism lateralization (context for NP-59's role)."],
  ["INFERENCE","Non-uptake of adrenocortical carcinoma follows from its loss of differentiated steroidogenic cholesterol handling."]],
 "choline-pet": [
  ["B","SNMMI/EANM experience with C-11-choline and F-18-fluorocholine PET in biochemically recurrent prostate cancer."],
  ["B","F-18-fluorocholine PET/CT for parathyroid adenoma localization — superior to sestamibi in small/negative/multiglandular disease."],
  ["INFERENCE","PSMA's superiority at low PSA (vs choline) follows from the prospective PSMA detection-rate data."]],
 "bone-metastases-imaging": [
  ["B","<b>SNMMI/EANM bone scintigraphy and ¹⁸F-NaF PET/CT practice guidelines</b> — osteoblastic-reaction imaging, patterns, and NaF's improved sensitivity/specificity."],
  ["B","<b>Comparative skeletal-staging reviews</b> — bone scan vs NaF/FDG/PSMA PET, CT, and MRI by lesion type (blastic vs lytic vs marrow), including the photopenic-lytic false-negative and the healing-flare pitfall."]],
 "stress-insufficiency-fractures": [
  ["B","<b>SNMMI bone scintigraphy guideline</b> and three-phase-technique reviews — early positivity before radiographs; focal three-phase pattern vs longitudinal delayed-only shin-splint uptake."],
  ["B","<b>SPECT/CT literature</b> — localizing and dating spondylolysis (active vs old pars defect) and the sacral-insufficiency 'Honda/H sign' distinguished from metastasis."]],
 "avascular-necrosis": [
  ["B","<b>Scintigraphy and MRI in osteonecrosis staging</b> — the cold-then-hot-rim ('doughnut') evolution and SPECT's added femoral-head sensitivity."],
  ["A","<b>MRI as reference standard</b> — earliest marrow changes and the double-line sign; bone scan/SPECT reserved for MRI-contraindicated cases or whole-body survey of multifocal infarcts."]],
 "complex-regional-pain-syndrome": [
  ["B","<b>Three-phase bone scintigraphy reviews in CRPS</b> — diffuse periarticular delayed-phase uptake as the supportive pattern; variable, often modest sensitivity (lower in children and chronic disease)."],
  ["B","<b>Budapest diagnostic criteria for CRPS</b> — CRPS as a clinical diagnosis with imaging adjunctive, not required."]],
 "prosthetic-joint-hardware": [
  ["B","<b>SNMMI/EANM labeled-leukocyte and combined WBC + sulfur-colloid marrow guidelines</b> — spatial incongruence (WBC without matching marrow) as the criterion for periprosthetic joint infection."],
  ["B","<b>Painful-arthroplasty imaging reviews</b> — bone-scan nonspecificity for ~12 months post-op, loosening patterns (stem-tip/lesser-trochanter uptake), and the limited specificity of FDG-PET."]],
 "dual-time-point-fdg": [
  ["B","<b>Dual-time-point FDG-PET methodology reviews</b> — the retention index and continued malignant trapping vs benign washout for characterizing equivocal foci."],
  ["C","<b>Limitation literature</b> — granulomatous/infectious false positives and the lack of a universally validated retention-index threshold; delayed/diuretic pelvic imaging for background clearance."]],
 "post-treatment-fdg-pitfalls": [
  ["B","<b>SNMMI/EANM FDG-PET/CT oncology guidelines</b> — recommended intervals after chemotherapy, radiotherapy, surgery, and G-CSF to avoid stunning and treatment-inflammation errors."],
  ["C","<b>Treatment-mimic reviews</b> — radiation pneumonitis/mucositis, surgical-bed granulation, G-CSF marrow/splenic uptake, and thymic rebound patterns on FDG-PET."]],
 "pet-mri-oncology": [
  ["B","<b>Clinical PET/MRI application reviews and society guidance</b> — soft-tissue-contrast and dose-reduction advantages by tumour site (pelvis, liver, head/neck, brain, marrow, pediatrics)."],
  ["C","<b>MR-based attenuation-correction literature</b> — tissue-segmentation MRAC, bone/metal artefacts, and non-interchangeability of SUV across PET/CT and PET/MRI platforms."]],
 "tumor-induced-osteomalacia": [
  ["B","<b>⁶⁸Ga-DOTATATE (and FAPI) PET/CT localization studies in TIO</b> — SSTR-based detection of occult phosphaturic mesenchymal tumors superior to ¹¹¹In-octreotide."],
  ["C","<b>Endocrine reviews of FGF23 physiology and TIO</b> — hypophosphatemia/renal phosphate wasting, selective venous sampling, and surgical cure."]],
 "paraneoplastic-tumor-search": [
  ["B","<b>EFNS/EAN guidelines on tumor screening in paraneoplastic neurologic syndromes</b> — whole-body FDG-PET after negative conventional imaging and interval re-screening."],
  ["C","<b>Onconeural-antibody reviews</b> — antibody-to-tumor associations (anti-Hu/LEMS→SCLC, anti-Yo/Ri→breast/gyn, anti-Ma2→testis) directing the targeted search."]],
 "theranostics-clinic-operations": [
  ["B","<b>NRC 10 CFR Part 35</b> — medical-use licensing, authorized-user training/experience, and the written-directive requirement for radionuclide therapy."],
  ["C","<b>SNMMI/EANM practice-operations guidance</b> — establishing a radioligand-therapy service (facility, hot lab, staffing, workflow) and buy-and-bill reimbursement overviews."]],
 "theranostics-sequencing-retreatment": [
  ["A","<b>Pivotal sequencing evidence</b> — VISION (post-taxane), PSMAfore (pre-taxane) and the 2025 label expansion; NETTER-1 (2nd-line) and NETTER-2 (first-line grade 2–3 GEP-NET); ENZA-p (combination)."],
  ["C","<b>Retreatment/rechallenge literature</b> — observational Lu-PSMA rechallenge and salvage/retreatment PRRT cohorts; ²²⁵Ac-PSMA in β-refractory disease."]],
 "emerging-therapeutic-targets": [
  ["C","<b>Emerging-target reviews</b> — FAP (e.g. FAP-2286), GRPR (RM2), CXCR4 (pentixafor/pentixather), and SSTR-antagonist radioligand therapy in early-phase development."],
  ["C","<b>Alpha-emitter and isotope-supply literature</b> — ²²⁵Ac, ²¹²Pb, ²²⁷Th therapy rationale, daughter-recoil dosimetry, and production/supply constraints."]],
 "on-call-nuclear-medicine": [
  ["B","<b>SNMMI procedure standards</b> — GI-bleeding, Meckel, testicular, hepatobiliary (HIDA), lung V/Q, and cerebral-perfusion (brain-death) scintigraphy."],
  ["B","<b>ACR practice parameter</b> — communication of critical/actionable imaging findings (closed-loop)."]],
 "protocoling-appropriate-use": [
  ["B","<b>ACR Appropriateness Criteria and SNMMI appropriate-use criteria</b>; US clinical-decision-support policy for advanced imaging."],
  ["B","<b>ICRP principles of justification and optimization (ALARA)</b> applied to diagnostic nuclear medicine ordering and protocoling."]],
 "ai-machine-learning-nuclear-medicine": [
  ["B","<b>Reviews of deep-learning reconstruction, denoising, segmentation, and automated dosimetry</b> in PET/SPECT and their dose/throughput benefits."],
  ["C","<b>Medical-imaging AI limitations literature</b> — generalization/domain shift, bias, explainability, and clinical-AI regulatory frameworks."]],
 "fever-unknown-origin": [
  ["B","<b>SNMMI/EANM guidelines on FDG-PET/CT for fever and inflammation of unknown origin</b> — whole-body search after an unrevealing initial workup."],
  ["B","<b>Diagnostic-yield and prognosis data</b> — FDG-PET/CT change-in-management rates in FUO/IUO and the value of a negative scan."]],
 "spondylodiscitis": [
  ["B","<b>SNMMI/EANM guidance on FDG-PET/CT for osteomyelitis (peripheral and spinal)</b>; reviews of the photopenic labeled-WBC spine as a false-negative."],
  ["B","<b>Comparative imaging literature</b> — MRI, FDG-PET/CT, and combined bone/gallium imaging in vertebral osteomyelitis/discitis."]],
 "movement-disorder-metabolic-patterns": [
  ["B","<b>EANM/SNMMI guidelines on ¹²³I-FP-CIT (DaTscan) and brain FDG-PET</b> in movement disorders — transporter vs metabolic roles."],
  ["C","<b>Spatial-covariance-pattern literature</b> (PDRP and disease-related patterns) for differentiating IPD, MSA, PSP, CBD, and DLB (cingulate island sign)."]],
 "personalized-dosimetry-rpt": [
  ["A","<b>DOSISPHERE-01</b> — Garin E, et al. <i>Lancet Gastroenterol Hepatol</i> 2021: personalized vs standard dosimetry improved response in ⁹⁰Y radioembolization for HCC.", "https://doi.org/10.1016/S2468-1253(20)30290-9"],
  ["B","<b>MIRD/EANM dosimetry guidance and PRRT dose–effect analyses</b> — tumor-dose/outcome and kidney-dose/toxicity relationships; the fixed-activity vs personalized-dosing debate."],
  ["C","<b>Single-time-point dosimetry and AI-automated segmentation validation</b> — simplifying multi-time-point SPECT/CT workflows toward routine personalized dosing."]],
}

def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    fm = yaml.safe_load(m.group(1))
    body = m.group(2)
    body = re.split(r"\n##\s+References\s*\n", body)[0].rstrip() + "\n"
    # Pull out $$...$$ display-equation blocks before markdown so it can't mangle the
    # LaTeX; they are rendered to MathML and reinserted as centered equation graphics.
    body, _eqs = _extract_equations(body)
    html = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    # Wrap every content table in a horizontal-scroll container so wide tables scroll
    # within themselves on narrow screens (iPhone) instead of overflowing the page.
    html = re.sub(r"<table>", '<div class="tbl-wrap"><table>', html)
    html = html.replace("</table>", "</table></div>")
    html = apply_yield(html)
    html = style_sections(html)
    html = _restore_equations(html, _eqs)
    return fm, html

# ---- Standardized educational-section identity -------------------------------
# Every content page draws from one shared vocabulary of teaching sections
# (review items 7-13). Rather than rewrite 250+ files, the renderer recognises
# each canonical section by its heading — folding label variants
# ("Common Pitfalls" == "Common Pitfalls / Cautions", "Self-Check" ==
# "Self-Check (Board-Style)") into one family — and gives it a consistent,
# colour-coded icon so the scaffolding reads the same on every page.
_SEC_ICONS = {
    # key: 24x24 stroke path(s) (feather-style, fill:none, currentColor)
    "quick":   ["M13 2 4 14h6l-1 8 9-12h-6z"],                                              # bolt
    "why":     ["M12 3 2 8.5 12 14l10-5.5z", "M6 11v4.2c0 1.3 2.7 2.3 6 2.3s6-1 6-2.3V11"],# grad cap
    "pearls":  ["M12 3l2.6 5.6 6 .7-4.5 4.2 1.2 6L12 16.9 6.7 19.5l1.2-6L3.4 9.3l6-.7z"],   # star
    "pitfall": ["M12 3 2 20h20z", "M12 9v5", "M12 17.2v.05"],                               # warning
    "ddx":     ["M9 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10z", "M15 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10z"], # venn
    "report":  ["M9 4h6v3H9z", "M7 5.5H5V20h14V5.5h-2", "M8.5 11h7", "M8.5 15h5"],          # clipboard
    "check":   ["M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z", "M9.5 9.3a2.6 2.6 0 0 1 4.6 1.6c0 1.7-2.1 2.1-2.1 3.6", "M12 17.2v.05"], # ? in circle
    "refs":    ["M4 4h8a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4z", "M20 4h-4a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h4z"], # book
    "related": ["M9 12a3 3 0 0 0 3 3l2 2a4 4 0 0 0 6-6l-2-2a4 4 0 0 0-5 0", "M15 12a3 3 0 0 0-3-3l-2-2a4 4 0 0 0-6 6l2 2a4 4 0 0 0 5 0"], # link
}
# Ordered matchers: (predicate on normalised heading) -> family key.
def _sec_key(norm):
    def has(*subs): return any(s in norm for s in subs)
    if has("quick answer"):                                   return "quick"
    if has("why it matters", "why this matters", "clinical importance", "why nuclear"): return "why"
    if has("board pearl", "high-yield pearl", "high yield pearl", "board fact", "key takeaway"): return "pearls"
    if has("pitfall", "common mistake", "caution"):           return "pitfall"
    if has("differential"):                                   return "ddx"
    if norm.startswith("reporting"):                          return "report"
    if has("self-check", "self check"):                       return "check"
    if norm.endswith("reference") or norm.endswith("references") or "evidence" in norm: return "refs"
    if has("related page", "related topic", "see also"):      return "related"
    return None

def _sec_norm(text):
    t = re.sub(r"<[^>]+>", "", text)                 # strip any inline tags
    t = t.replace("&amp;", "&").lower().strip()
    t = re.sub(r"\s*\([^)]*\)\s*$", "", t)           # drop trailing "(Board-Style)" etc.
    return t.strip(" .:")

def style_sections(html):
    def repl(m):
        raw = m.group(1)
        key = _sec_key(_sec_norm(raw))
        if not key:
            return m.group(0)
        paths = "".join(f'<path d="{d}"/>' for d in _SEC_ICONS[key])
        ic = (f'<svg class="sec-ic" viewBox="0 0 24 24" fill="none" '
              f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
              f'stroke-linejoin="round" aria-hidden="true">{paths}</svg>')
        return f'<h2 class="sec sec-{key}">{ic}<span>{raw}</span></h2>'
    return re.sub(r"<h2>(.*?)</h2>", repl, html, flags=re.S)

# ---- Display equations: $$ LaTeX $$ → centered MathML block (typeset, offline, no runtime dep) ----
def _extract_equations(body):
    eqs = []
    def repl(m):
        eqs.append(m.group(1).strip())
        return f"\n\nEQNBLOCK{len(eqs)-1}ENDEQN\n\n"
    body = re.sub(r"\$\$(.+?)\$\$", repl, body, flags=re.S)
    return body, eqs

def _render_equation(latex):
    try:
        from latex2mathml.converter import convert
        ml = convert(latex).replace('display="inline"', 'display="block"')
    except Exception:
        # Fallback: show the LaTeX source in a mono span rather than break the build.
        ml = '<code>' + latex.replace('<', '&lt;').replace('>', '&gt;') + '</code>'
    return f'<div class="equation" role="math">{ml}</div>'

def _restore_equations(html, eqs):
    for i, latex in enumerate(eqs):
        blk = _render_equation(latex)
        tok = f"EQNBLOCK{i}ENDEQN"
        html = html.replace(f"<p>{tok}</p>", blk).replace(tok, blk)
    return html

def apply_yield(html):
    """4-level emphasis hierarchy.
    Inline tokens at the start of a paragraph/bullet: {K}=key point, {H}=high-yield,
    {D}=deep/low-yield detail. Plus automatic styling of Quick Answer (lead) and
    every High-Yield Pearls bullet (bold)."""
    for tok, cls in (("K", "y1"), ("H", "y2"), ("D", "y4")):
        for tag in ("p", "li"):
            html = html.replace(f"<{tag}>{{{tok}}} ", f'<{tag} class="{cls}">')
            html = html.replace(f"<{tag}>{{{tok}}}", f'<{tag} class="{cls}">')
    # Quick Answer paragraph -> prominent lead
    html = re.sub(r"(<h2>Quick Answer</h2>\s*)<p>", r'\1<p class="lead">', html)
    # High-Yield Pearls bullets -> bold (auto high-yield)
    html = re.sub(r"(<h2>High-Yield Pearls</h2>.*?)(?=<h2>|\Z)",
                  lambda mm: mm.group(1).replace("<li>", '<li class="y2">'), html, flags=re.S)
    return html

# discover all pages, assign to chapters
raw_pages = {}
for path in glob.glob(os.path.join(BASE, "**", "*.md"), recursive=True):
    pid = os.path.basename(path)[:-3]
    fm, html = parse(path)
    aliases = " ".join(fm.get("aliases", []) or [])
    raw_pages[pid] = {"id": pid, "title": fm.get("title", pid), "iso": fm.get("isotope_label", ""),
                      "subtitle": fm.get("subtitle", ""), "tags": fm.get("tags", []) or [],
                      "aliases": aliases, "html": html,
                      "_chapter": fm.get("chapter"), "_order": fm.get("order"),
                      "_updated": fm.get("last_updated"), "_review": fm.get("review_status"),
                      "_rel": {_g: (fm.get(_g) or []) for _g in
                               ("related_tracers", "related_diseases", "related_protocols",
                                "related_calculators", "related_pitfalls")},
                      "_figures": fm.get("figures") or [],
                      # ---- authorship / provenance layer ----
                      "_type": fm.get("type"),
                      "_authors": fm.get("authors") or [],       # article -> author ids
                      "_informs": fm.get("informs") or [],       # article -> atlas page ids
                      "_ameta": {_k: fm.get(_k) for _k in        # article publication meta
                                 ("journal", "pub_date", "article_doi", "article_url")},
                      "_umeta": {_k: fm.get(_k) for _k in        # author profile meta
                                 ("credentials", "affiliation", "orcid", "role", "homepage")}}

# ---- single source of truth: derive chapter & order from frontmatter ----
PAGE_CHAPTER = {pid: rp.get('_chapter') for pid, rp in raw_pages.items() if rp.get('_chapter')}
_missing_ch = [pid for pid, rp in raw_pages.items() if not rp.get('_chapter')]
if _missing_ch:
    print('WARNING pages missing frontmatter chapter:', _missing_ch)
CH_ORDER = {}
for _pid, _ch in PAGE_CHAPTER.items():
    CH_ORDER.setdefault(_ch, []).append(_pid)
for _ch in CH_ORDER:
    CH_ORDER[_ch].sort(key=lambda p: (raw_pages[p].get('_order') if raw_pages[p].get('_order') is not None else 9999, p))

unassigned = [p for p in raw_pages if p not in PAGE_CHAPTER]
if unassigned:
    print("WARNING unassigned pages:", unassigned)

pages = []
for ch in CH_ORDER_LIST:
    ids = [i for i in CH_ORDER.get(ch, []) if i in raw_pages]
    ids += sorted([i for i, c in PAGE_CHAPTER.items() if c == ch and i in raw_pages and i not in ids])
    for pid in ids:
        p = raw_pages[pid]; p["chapter"] = ch
        pages.append(p)

# ============================ AUTO CROSS-LINKS ("Related pages") ============================
_REL_STOP = set("""pet spect ct mri imaging therapy therapies cancer cancers tumor tumour tumors scan scans
uptake disease diseases syndrome syndromes agent agents study studies reporting overview protocol protocols
dose doses perfusion tracer tracers nuclear medicine bone brain cardiac renal thyroid lung liver spleen
gastric general the and for with amyloid amyloidosis reference standards systems variants normal principles
production dosimetry safety physics evaluation grading model score criteria mapping""".split())

def _rel_clean_title(t):
    t = re.sub(r'\(.*?\)', '', t)                 # drop parentheticals
    t = re.split(r'[—·/&]', t)[0]                  # first segment
    t = t.strip().lower()
    t = re.sub(r'[^a-z0-9\- ]', '', t).strip()
    return t

def _rel_terms(p):
    terms = set()
    ct = _rel_clean_title(p["title"])
    if len(ct) >= 5 and ct not in _REL_STOP:
        terms.add(ct)
    # add distinctive short aliases (isotope/eponym/entity tokens)
    for a in (p["aliases"] or "").split(","):
        a = re.sub(r'[^a-z0-9\- ]', '', a.strip().lower()).strip()
        if 4 <= len(a) <= 22 and a not in _REL_STOP and " " not in a and not a.isdigit():
            terms.add(a)
    return terms

# term -> id ; drop terms that are ambiguous (map to >1 page) or generic
_termmap = {}
_ambig = set()
for _p in pages:
    if _p["id"].startswith("tool-"):
        continue
    for _t in _rel_terms(_p):
        if _t in _ambig:
            continue
        if _t in _termmap and _termmap[_t] != _p["id"]:
            _ambig.add(_t); _termmap.pop(_t, None)
        else:
            _termmap[_t] = _p["id"]

_title_by_id = {p["id"]: p["title"] for p in pages}
_plain = {}
for _p in pages:
    _plain[_p["id"]] = re.sub(r'<[^>]+>', ' ', _p["html"]).lower()

REL_LINKS = {}
REL_HITS = {}
# Compile each term's word-boundary pattern ONCE, not once per (page × term).
_term_pats = [(re.compile(r'(?<![a-z0-9])' + re.escape(_t) + r'(?![a-z0-9])'), _tid)
              for _t, _tid in _termmap.items()]
for _p in pages:
    if _p["id"].startswith("tool-"):
        continue
    body = _plain[_p["id"]]
    _pid = _p["id"]
    hits = [_tid for _pat, _tid in _term_pats if _tid != _pid and _pat.search(body)]
    hits = sorted(set(hits), key=lambda i: _title_by_id[i].lower())[:14]
    REL_HITS[_p["id"]] = hits          # the links actually shown as "See also"
    if not hits:
        continue
    chips = "".join(
        f'<span class="rel-chip" onclick="go(\'{i}\')">{_title_by_id[i]}</span>' for i in hits
    )
    REL_LINKS[_p["id"]] = f'<div class="related"><div class="related-h">See also</div>{chips}</div>'

# ---- Backlinks ("Referenced by"): invert the See-also graph ----
_backrefs = {}
for _src, _targets in REL_HITS.items():
    for _t in _targets:
        _backrefs.setdefault(_t, set()).add(_src)
BACKLINK_HTML = {}
for _tid, _srcs in _backrefs.items():
    _s = sorted(_srcs, key=lambda i: _title_by_id.get(i, "").lower())[:18]
    chips = "".join(
        f'<span class="rel-chip" onclick="go(\'{i}\')">{_title_by_id[i]}</span>' for i in _s)
    BACKLINK_HTML[_tid] = f'<div class="related backrefs"><div class="related-h">Referenced by</div>{chips}</div>'

# ---- Curated cross-references from authored front-matter (typed chips) ----
_REL_LABELS = [("related_tracers", "Tracers"), ("related_diseases", "Diseases & topics"),
               ("related_protocols", "Protocols"), ("related_calculators", "Tools"),
               ("related_pitfalls", "Pitfalls")]
def _resolve_rel(rid, self_id):
    for cand in (rid, "tool-" + str(rid)):
        if cand in raw_pages and cand != self_id:
            return cand
    return None
CURATED_HTML = {}
for _p in pages:
    _rel = _p.get("_rel") or {}
    _rows = []
    for _field, _lbl in _REL_LABELS:
        _ids = []
        for _rid in (_rel.get(_field) or []):
            _r = _resolve_rel(_rid, _p["id"])
            if _r and _r not in _ids:
                _ids.append(_r)
        if _ids:
            _chips = "".join(
                f'<span class="rel-chip" onclick="go(\'{i}\')">{_title_by_id[i]}</span>' for i in _ids)
            _rows.append(f'<div class="cur-row"><span class="cur-lbl">{_lbl}</span>'
                         f'<span class="cur-chips">{_chips}</span></div>')
    if _rows:
        CURATED_HTML[_p["id"]] = f'<div class="related curated"><div class="related-h">Related</div>{"".join(_rows)}</div>'

# ============================ AUTHORSHIP & PROVENANCE LAYER ============================
# A contributed `article` declares the atlas pages its research `informs:` and its
# `authors:`. We render the forward links on the article, INVERT them into a
# provenance banner on each informed clinical page, and aggregate each author's
# contributions on their profile — a bidirectional, citable graph (pillars 3 & 4).
def _valid_ids(id_list, self_id=None):
    out = []
    for rid in (id_list or []):
        rid = str(rid)
        if rid in raw_pages and rid != self_id and rid not in out:
            out.append(rid)
    return out

def _chips(ids):
    return "".join(
        f'<span class="rel-chip" onclick="go(\'{i}\')">{_title_by_id[i]}</span>' for i in ids)

ARTICLES = [p for p in pages if p.get("_type") == "article"]
AUTHORS  = [p for p in pages if p.get("_type") == "author"]

# invert informs -> PROVENANCE[page_id] = [article_id, ...]
PROVENANCE = {}
for _a in ARTICLES:
    for _pid in _valid_ids(_a.get("_informs"), _a["id"]):
        PROVENANCE.setdefault(_pid, [])
        if _a["id"] not in PROVENANCE[_pid]:
            PROVENANCE[_pid].append(_a["id"])

AUTHOR_ARTICLES = {}                                   # author_id -> [article_id, ...]
for _a in ARTICLES:
    for _uid in _valid_ids(_a.get("_authors"), _a["id"]):
        AUTHOR_ARTICLES.setdefault(_uid, []).append(_a["id"])

def _doi_link(meta):
    doi, url = meta.get("article_doi"), meta.get("article_url")
    href = url or (f"https://doi.org/{doi}" if doi else None)
    if not href:
        return ""
    label = f"doi:{doi}" if doi else "View source"
    return (f'<a class="cite-link" href="{href}" target="_blank" rel="noopener" '
            f'title="View published source">{label} ↗</a>')

# provenance banner shown on each clinical page an article informs
PROVBAR_HTML = {}
for _pid, _aids in PROVENANCE.items():
    PROVBAR_HTML[_pid] = (
        '<div class="provbar"><span class="provbar-i" aria-hidden="true">◆</span>'
        '<span class="provbar-t">Informed by contributed research</span>'
        f'<span class="provbar-chips">{_chips(_aids)}</span></div>')

# article header (authors + publication) and footer (sections informed)
ARTICLE_HEAD_HTML, ARTICLE_FOOT_HTML = {}, {}
for _a in ARTICLES:
    _auth = _valid_ids(_a.get("_authors"), _a["id"])
    _rows = ""
    if _auth:
        _rows += (f'<div class="artmeta-row"><span class="artmeta-k">Author'
                  f'{"s" if len(_auth) > 1 else ""}</span>'
                  f'<span class="artmeta-v">{_chips(_auth)}</span></div>')
    _m = _a.get("_ameta") or {}
    _pubbits = [b for b in (_m.get("journal"),
                            (str(_m.get("pub_date")) if _m.get("pub_date") else None),
                            _doi_link(_m)) if b]
    if _pubbits:
        _rows += ('<div class="artmeta-row"><span class="artmeta-k">Published</span>'
                  f'<span class="artmeta-v">{" · ".join(_pubbits)}</span></div>')
    if _rows:
        ARTICLE_HEAD_HTML[_a["id"]] = f'<div class="artmeta">{_rows}</div>'
    _informed = _valid_ids(_a.get("_informs"), _a["id"])
    if _informed:
        ARTICLE_FOOT_HTML[_a["id"]] = (
            '<div class="related informs"><div class="related-h">Informs these atlas sections</div>'
            f'{_chips(_informed)}</div>')

# author profile header + contributions footer (pillar 4)
AUTHOR_HEAD_HTML, AUTHOR_FOOT_HTML = {}, {}
for _u in AUTHORS:
    _m = _u.get("_umeta") or {}
    _bits = ""
    _line = " · ".join(b for b in (_m.get("credentials"), _m.get("role")) if b)
    if _line:
        _bits += f'<div class="authhead-cred">{_line}</div>'
    if _m.get("affiliation"):
        _bits += f'<div class="authhead-aff">{_m["affiliation"]}</div>'
    _links = []
    if _m.get("orcid"):
        _oc = str(_m["orcid"])
        _links.append(f'<a class="cite-link" href="https://orcid.org/{_oc}" target="_blank" '
                      f'rel="noopener">ORCID {_oc} ↗</a>')
    if _m.get("homepage"):
        _links.append(f'<a class="cite-link" href="{_m["homepage"]}" target="_blank" '
                      f'rel="noopener">Homepage ↗</a>')
    if _links:
        _bits += f'<div class="authhead-links">{" · ".join(_links)}</div>'
    if _bits:
        AUTHOR_HEAD_HTML[_u["id"]] = f'<div class="authhead">{_bits}</div>'
    _arts = AUTHOR_ARTICLES.get(_u["id"], [])
    _foot = ""
    if _arts:
        _foot += ('<div class="related contribs"><div class="related-h">Contributed articles</div>'
                  f'{_chips(_arts)}</div>')
        _sec = []
        for _aid in _arts:
            for _s in _valid_ids(raw_pages[_aid].get("_informs"), _aid):
                if _s not in _sec:
                    _sec.append(_s)
        if _sec:
            _foot += ('<div class="related"><div class="related-h">Atlas sections informed</div>'
                      f'{_chips(_sec)}</div>')
    if _foot:
        AUTHOR_FOOT_HTML[_u["id"]] = _foot

def evidence_for(pid):
    return EVIDENCE.get(pid, []) + EXTRA_EVIDENCE.get(pid, [])

def grade_summary(pid):
    ev = evidence_for(pid)
    seen = [g for g in ["A", "B", "C", "I"] if any(e[0] == g for e in ev)]
    if not seen:
        return ""
    chips = "".join(f'<span class="gr g{g}">{"INF" if g=="I" else g}</span>' for g in seen)
    return f'<span class="evsum">Evidence {chips}</span>'

# Verified landmark-trial DOIs — recognized trial names are auto-linked in evidence text.
# Only trials whose identifier has been verified are listed here (extended as verified).
TRIAL_LINKS = {
    "VISION": "https://doi.org/10.1056/NEJMoa2107322",     # Sartor, NEJM 2021 (177Lu-PSMA-617)
    "NETTER-1": "https://doi.org/10.1056/NEJMoa1607427",   # Strosberg, NEJM 2017 (177Lu-DOTATATE)
    "ALSYMPCA": "https://doi.org/10.1056/NEJMoa1213755",   # Parker, NEJM 2013 (radium-223)
    "TheraP": "https://doi.org/10.1016/S0140-6736(21)00237-3",   # Hofman, Lancet 2021
    "proPSMA": "https://doi.org/10.1016/S0140-6736(20)30314-7",  # Hofman, Lancet 2020
    "NETTER-2": "https://doi.org/10.1016/S0140-6736(24)00701-3", # Singh, Lancet 2024 (first-line PRRT)
    "PSMAfore": "https://doi.org/10.1016/S0140-6736(24)01653-2", # Morris, Lancet 2024 (pre-taxane)
    "ENZA-p": "https://doi.org/10.1016/S1470-2045(24)00135-9",   # Emmett, Lancet Oncol 2024
    "ERA-223": "https://doi.org/10.1016/S1470-2045(18)30860-X",  # Smith, Lancet Oncol 2019 (safety)
    "PARR-2": "https://doi.org/10.1016/j.jacc.2007.09.006",      # Beanlands, JACC 2007 (viability)
    "PIOPED": "https://jamanetwork.com/journals/jama/fullarticle/381954",  # JAMA 1990 (V/Q)
    # "FIT" deliberately omitted from auto-link: bare bold token collides with common word.
}

def _linkify_trials(txt):
    for trial, url in TRIAL_LINKS.items():
        txt = txt.replace(
            f"<b>{trial}</b>",
            f'<b><a class="cite-link" href="{url}" target="_blank" rel="noopener" '
            f'title="View source (DOI)">{trial}</a></b>')
    return txt

def cites_html(pid):
    ev = evidence_for(pid)
    if not ev:
        return ""
    def row(item):
        g, txt = item[0], _linkify_trials(item[1])
        url = item[2] if len(item) > 2 else None
        link = (f' <a class="cite-link" href="{url}" target="_blank" rel="noopener" '
                f'title="View source">↗</a>') if url else ""
        return (f'<div class="ct"><span class="gr g{g}">{"INF" if g == "I" else g}</span>'
                f'<span>{txt}{link}</span></div>')
    rows = "".join(row(item) for item in ev)
    return f'<h2>Evidence &amp; sources</h2><div class="cites">{rows}</div>'

# ============================ ORIGINAL VECTOR DIAGRAMS (SVG) ============================
# All figures are original, drawn in the atlas palette — copyright-clean, vector, tiny.
PAL = dict(ink="#14171B", soft="#565E68", faint="#8D949C", line="#E2E5E9", bg="#F6F7F9",
           ac="#4A3A82", lad="#4A3A82", lcx="#0B6B52", rca="#1A5480",
           ladt="#E7E0F3", lcxt="#DCEFE8", rcat="#DEEAF4", A="#0B6B52", red="#9E3417",
           amber="#8A6009", green="#0B6B52")
FONT = "font-family='Inter,system-ui,sans-serif'"

def _sector(cx, cy, ri, ro, a0, a1):
    def pt(r, a):
        rad = math.radians(a); return (cx + r*math.cos(rad), cy + r*math.sin(rad))
    x1, y1 = pt(ro, a0); x2, y2 = pt(ro, a1); x3, y3 = pt(ri, a1); x4, y4 = pt(ri, a0)
    laf = 1 if (a1 - a0) % 360 > 180 else 0
    return (f"M{x1:.1f} {y1:.1f} A{ro} {ro} 0 {laf} 1 {x2:.1f} {y2:.1f} "
            f"L{x3:.1f} {y3:.1f} A{ri} {ri} 0 {laf} 0 {x4:.1f} {y4:.1f} Z")

def bullseye():
    cx, cy = 118, 112
    rings = [(78, 108), (48, 78), (18, 48)]  # basal, mid, apical (outer,inner reversed below)
    terr6 = ["lad", "lad", "rca", "rca", "lcx", "lcx"]
    s = [f'<svg viewBox="0 0 236 250" {FONT} xmlns="http://www.w3.org/2000/svg">']
    def lbl(n, r, a):
        rad = math.radians(a); x = cx + r*math.cos(rad); y = cy + r*math.sin(rad)
        return f'<text x="{x:.1f}" y="{y+3:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{PAL["ink"]}">{n}</text>'
    seg = 1
    # basal + mid (6 sectors each), start at top (-90) clockwise
    for (ro, ri) in [(108, 78), (78, 48)]:
        for k in range(6):
            a0 = -90 + k*60; a1 = a0 + 60
            s.append(f'<path d="{_sector(cx,cy,ri,ro,a0,a1)}" fill="{PAL[terr6[k]+"t"]}" stroke="#fff" stroke-width="2"/>')
            s.append(lbl(seg, (ro+ri)/2, a0+30)); seg += 1
    # apical 4 sectors
    api = ["lad", "rca", "lcx", "lad"]  # top, right? we go from -135
    aname = [(-135, "lad"), (-45, "rca"), (45, "lcx"), (135, "lad")]
    for i, (a0, t) in enumerate([(-135, "lad"), (-45, "lad"), (45, "rca"), (135, "lcx")]):
        s.append(f'<path d="{_sector(cx,cy,18,48,a0,a0+90)}" fill="{PAL[t+"t"]}" stroke="#fff" stroke-width="2"/>')
        s.append(lbl(13+i, 33, a0+45))
    # apex
    s.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="{PAL["ladt"]}" stroke="#fff" stroke-width="2"/>')
    s.append(lbl(17, 0, -90) if False else f'<text x="{cx}" y="{cy+3}" text-anchor="middle" font-size="10" font-weight="700" fill="{PAL["ink"]}">17</text>')
    # ring labels
    s.append(f'<text x="{cx}" y="14" text-anchor="middle" font-size="9" fill="{PAL["faint"]}">anterior</text>')
    s.append(f'<text x="{cx}" y="228" text-anchor="middle" font-size="9" fill="{PAL["faint"]}">inferior</text>')
    # legend
    leg = [("LAD", PAL["ladt"], PAL["lad"]), ("LCx", PAL["lcxt"], PAL["lcx"]), ("RCA", PAL["rcat"], PAL["rca"])]
    lx = 20
    for name, fill, stroke in leg:
        s.append(f'<rect x="{lx}" y="238" width="12" height="12" rx="2" fill="{fill}" stroke="{stroke}"/>')
        s.append(f'<text x="{lx+17}" y="248" font-size="10" fill="{PAL["soft"]}">{name}</text>')
        lx += 72
    s.append("</svg>")
    return "".join(s)

def vq_fig():
    def lung(cx, s):  # smooth lung silhouette; s=+1/-1 mirrors medial (concave) border to face centre
        return (f'M {cx} 44 C {cx-s*32} 60, {cx-s*36} 112, {cx-s*24} 150 '
                f'C {cx-s*15} 166, {cx+s*8} 166, {cx+s*15} 150 '
                f'C {cx+s*24} 116, {cx+s*20} 66, {cx+s*8} 48 '
                f'C {cx+s*4} 42, {cx-s*3} 42, {cx} 44 Z')
    o = [f'<svg viewBox="0 0 460 214" {FONT} xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<text x="115" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Ventilation (V)</text>')
    o.append(f'<text x="345" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Perfusion (Q)</text>')
    for cx, s in [(88, 1), (142, -1)]:
        o.append(f'<path d="{lung(cx,s)}" fill="{PAL["ladt"]}" stroke="{PAL["ac"]}" stroke-width="1.5"/>')
    o.append(f'<text x="115" y="188" text-anchor="middle" font-size="9" fill="{PAL["soft"]}">uniform ventilation</text>')
    for cx, s in [(318, 1), (372, -1)]:
        o.append(f'<path d="{lung(cx,s)}" fill="{PAL["ladt"]}" stroke="{PAL["ac"]}" stroke-width="1.5"/>')
    # wedge (pleural-based, segmental) perfusion defects — the PE pattern
    o.append(f'<path d="M290 72 L302 84 L290 100 Z" fill="#fff" stroke="{PAL["red"]}" stroke-width="1.4"/>')
    o.append(f'<path d="M400 118 L388 130 L400 146 Z" fill="#fff" stroke="{PAL["red"]}" stroke-width="1.4"/>')
    o.append(f'<text x="345" y="188" text-anchor="middle" font-size="9" fill="{PAL["red"]}">segmental perfusion defects</text>')
    o.append(f'<text x="230" y="207" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["red"]}">V normal + Q defect = MISMATCH → high probability for PE</text>')
    o.append("</svg>")
    return "".join(o)

def perugini_fig():
    panels = [(0, .15, 1.0, "Grade 0", "no cardiac uptake"), (1, .5, 1.0, "Grade 1", "heart < bone"),
              (2, .85, .85, "Grade 2", "heart = bone"), (3, 1.0, .3, "Grade 3", "heart > bone")]
    o = [f'<svg viewBox="0 0 460 214" {FONT} xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<text x="230" y="14" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Perugini visual grade &amp; H/CL ratio</text>')
    for i, (g, hop, bop, t, d) in enumerate(panels):
        x = 15 + i*112
        o.append(f'<rect x="{x}" y="22" width="98" height="82" rx="8" fill="{PAL["bg"]}" stroke="{PAL["line"]}"/>')
        o.append(f'<path d="M{x+14} 40 q35 -13 70 0" fill="none" stroke="{PAL["rca"]}" stroke-width="4" opacity="{bop}"/>')
        o.append(f'<path d="M{x+14} 92 q35 13 70 0" fill="none" stroke="{PAL["rca"]}" stroke-width="4" opacity="{bop}"/>')
        o.append(f'<path d="M{x+49} 78 c-15 -15 -28 -6 -28 8 c0 13 17 20 28 28 c11 -8 28 -15 28 -28 c0 -14 -13 -23 -28 -8 z" fill="{PAL["ac"]}" opacity="{hop}"/>')
        o.append(f'<text x="{x+49}" y="118" text-anchor="middle" font-size="10" font-weight="700" fill="{PAL["ink"]}">{t}</text>')
        o.append(f'<text x="{x+49}" y="131" text-anchor="middle" font-size="8" fill="{PAL["soft"]}">{d}</text>')
    o.append(f'<text x="26" y="162" font-size="9" font-weight="700" fill="{PAL["ink"]}">H/CL ratio:</text>')
    o.append(f'<ellipse cx="150" cy="176" rx="28" ry="20" fill="{PAL["ac"]}" opacity="0.85"/>')
    o.append(f'<circle cx="150" cy="176" r="15" fill="none" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 2"/>')
    o.append(f'<text x="150" y="204" text-anchor="middle" font-size="8" fill="{PAL["soft"]}">heart (H)</text>')
    o.append(f'<circle cx="250" cy="176" r="15" fill="none" stroke="{PAL["rca"]}" stroke-width="1.5" stroke-dasharray="3 2"/>')
    o.append(f'<text x="250" y="204" text-anchor="middle" font-size="8" fill="{PAL["soft"]}">contralateral (CL)</text>')
    o.append(f'<text x="300" y="172" font-size="10" font-weight="700" fill="{PAL["red"]}">H/CL ≥ 1.5 (1 h)</text>')
    o.append(f'<text x="300" y="186" font-size="8.5" fill="{PAL["soft"]}">+ negative light chains</text>')
    o.append(f'<text x="300" y="198" font-size="8.5" fill="{PAL["A"]}">→ ATTR (grade 2–3)</text>')
    o.append("</svg>")
    return "".join(o)

def particles_fig():
    rows = [("α", PAL["red"], 60, "µm — stopped by skin/paper · very high LET", "therapy"),
            ("β⁻", PAL["ac"], 150, "mm in tissue — stopped by plastic · moderate LET", "therapy (Lu-177, Y-90, I-131)"),
            ("γ / 511 keV", PAL["rca"], 300, "penetrating — needs lead · imaging", "SPECT / PET")]
    out = [f'<svg viewBox="0 0 460 190" {FONT} xmlns="http://www.w3.org/2000/svg">']
    for i, (name, col, ln, desc, use) in enumerate(rows):
        y = 34 + i*52
        out.append(f'<circle cx="46" cy="{y}" r="7" fill="{col}"/>')
        out.append(f'<text x="46" y="{y-12}" text-anchor="middle" font-size="11" font-weight="700" fill="{col}">{name}</text>')
        out.append(f'<line x1="56" y1="{y}" x2="{56+ln}" y2="{y}" stroke="{col}" stroke-width="3"/>')
        out.append(f'<path d="M{56+ln} {y-4} l7 4 l-7 4 z" fill="{col}"/>')
        out.append(f'<text x="70" y="{y+16}" font-size="9.5" fill="{PAL["soft"]}">{desc}</text>')
    # barriers
    for bx, lab in [(120, "paper/skin"), (215, "plastic"), (395, "lead")]:
        out.append(f'<line x1="{bx}" y1="18" x2="{bx}" y2="168" stroke="{PAL["faint"]}" stroke-width="1" stroke-dasharray="3 3"/>')
        out.append(f'<text x="{bx}" y="184" text-anchor="middle" font-size="8.5" fill="{PAL["faint"]}">{lab}</text>')
    out.append("</svg>")
    return "".join(out)

def theranostic_fig():
    return f'''<svg viewBox="0 0 460 210" {FONT} xmlns="http://www.w3.org/2000/svg">
<text x="230" y="18" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">One targeting molecule · two isotopes</text>
<circle cx="230" cy="120" r="46" fill="{PAL["ladt"]}" stroke="{PAL["ac"]}" stroke-width="1.5"/>
<text x="230" y="124" text-anchor="middle" font-size="10" fill="{PAL["ac"]}" font-weight="700">tumor cell</text>
{"".join(f'<rect x="{230+46*math.cos(math.radians(a))-5:.0f}" y="{120+46*math.sin(math.radians(a))-5:.0f}" width="10" height="10" rx="2" fill="{PAL["ac"]}"/>' for a in (210,240,270,300,330))}
<text x="230" y="196" text-anchor="middle" font-size="9" fill="{PAL["soft"]}">target (PSMA · SSTR · NIS …) + DOTA-linked ligand</text>
<g><rect x="20" y="46" width="150" height="52" rx="8" fill="{PAL["bg"]}" stroke="{PAL["A"]}"/>
<text x="95" y="66" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["A"]}">Diagnostic — SEE</text>
<text x="95" y="83" text-anchor="middle" font-size="9.5" fill="{PAL["soft"]}">Ga-68 / F-18 → PET</text></g>
<g><rect x="290" y="46" width="150" height="52" rx="8" fill="{PAL["bg"]}" stroke="{PAL["red"]}"/>
<text x="365" y="66" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["red"]}">Therapeutic — TREAT</text>
<text x="365" y="83" text-anchor="middle" font-size="9.5" fill="{PAL["soft"]}">Lu-177 / Ac-225 → dose</text></g>
<path d="M120 98 L200 112" stroke="{PAL["A"]}" stroke-width="2" fill="none" marker-end="url(#a1)"/>
<path d="M340 98 L262 112" stroke="{PAL["red"]}" stroke-width="2" fill="none" marker-end="url(#a2)"/>
<defs><marker id="a1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 l6 3 l-6 3 z" fill="{PAL["A"]}"/></marker>
<marker id="a2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 l6 3 l-6 3 z" fill="{PAL["red"]}"/></marker></defs>
</svg>'''

def ai_loop_fig():
    ac, bg, ink, soft = PAL["ac"], PAL["bg"], PAL["ink"], PAL["soft"]
    def node(x, y, n, title, sub):
        return (f'<rect x="{x}" y="{y}" width="130" height="46" rx="9" fill="{bg}" stroke="{ac}" stroke-width="1.3"/>'
                f'<text x="{x+65}" y="{y+20}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{ac}">{n} · {title}</text>'
                f'<text x="{x+65}" y="{y+35}" text-anchor="middle" font-size="8.5" fill="{soft}">{sub}</text>')
    def tag(x, y, t):
        return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="8" font-weight="700" fill="{ac}" opacity="0.85">{t}</text>'
    arrow = f'marker-end="url(#aiar)"'
    return f'''<svg viewBox="0 0 470 268" {FONT} xmlns="http://www.w3.org/2000/svg">
<defs><marker id="aiar" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0 0 l6 3 l-6 3 z" fill="{ac}"/></marker></defs>
<text x="235" y="15" text-anchor="middle" font-size="11" font-weight="700" fill="{ink}">AI at the hub of the theranostic loop</text>
<circle cx="235" cy="140" r="40" fill="{PAL["ladt"]}" stroke="{ac}" stroke-width="1.6"/>
<text x="235" y="136" text-anchor="middle" font-size="17" font-weight="800" fill="{ac}">AI</text>
<text x="235" y="152" text-anchor="middle" font-size="7.5" fill="{soft}">the quantitative engine</text>
{node(170, 30, "①", "SELECT", "image &amp; find the target")}
{node(335, 117, "②", "TREAT", "matched isotope")}
{node(170, 200, "③", "QUANTIFY", "delivered dose")}
{node(5, 117, "④", "REASSESS", "next cycle")}
<path d="M300 55 C 360 62 400 82 400 114" fill="none" stroke="{ac}" stroke-width="2" {arrow}/>
<path d="M400 163 C 400 200 345 224 302 216" fill="none" stroke="{ac}" stroke-width="2" {arrow}/>
<path d="M170 219 C 118 224 70 200 70 166" fill="none" stroke="{ac}" stroke-width="2" {arrow}/>
<path d="M70 114 C 70 82 118 62 170 55" fill="none" stroke="{ac}" stroke-width="2" {arrow}/>
{tag(360, 92, "denoise · segment")}
{tag(360, 192, "voxel dosimetry")}
{tag(110, 192, "predict response")}
{tag(112, 92, "detect · read")}
<text x="235" y="258" text-anchor="middle" font-size="8.5" fill="{soft}">Automating dosimetry turns fixed-activity therapy into personalized, dose-optimized treatment.</text>
</svg>'''

def deauville_fig():
    heights = [10, 30, 58, 82, 108]
    cols = [PAL["A"], PAL["A"], PAL["A"], PAL["red"], PAL["red"]]
    out = [f'<svg viewBox="0 0 520 200" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<line x1="40" y1="150" x2="430" y2="150" stroke="{PAL["line"]}"/>')
    # reference lines: mediastinum (score2 top) and liver (score3 top); labels sit in the right margin
    out.append(f'<line x1="40" y1="120" x2="430" y2="120" stroke="{PAL["faint"]}" stroke-width="1" stroke-dasharray="5 3"/><text x="436" y="123" font-size="9" fill="{PAL["faint"]}">mediastinum</text>')
    out.append(f'<line x1="40" y1="92" x2="430" y2="92" stroke="{PAL["amber"]}" stroke-width="1" stroke-dasharray="5 3"/><text x="436" y="95" font-size="9" fill="{PAL["amber"]}">liver</text>')
    for i, (h, c) in enumerate(zip(heights, cols)):
        x = 70 + i*74
        out.append(f'<rect x="{x}" y="{150-h}" width="44" height="{h}" rx="3" fill="{c}"/>')
        out.append(f'<text x="{x+22}" y="168" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">{i+1}</text>')
    out.append(f'<text x="240" y="190" text-anchor="middle" font-size="10" fill="{PAL["soft"]}">Deauville score — lesion uptake vs mediastinal blood pool &amp; liver</text>')
    out.append("</svg>")
    return "".join(out)

def renogram_fig():
    return f'''<svg viewBox="0 0 460 220" {FONT} xmlns="http://www.w3.org/2000/svg">
<line x1="46" y1="30" x2="46" y2="170" stroke="{PAL["line"]}"/><line x1="46" y1="170" x2="440" y2="170" stroke="{PAL["line"]}"/>
<text x="20" y="100" font-size="9" fill="{PAL["faint"]}" transform="rotate(-90 20 100)">counts</text>
<text x="240" y="192" text-anchor="middle" font-size="9" fill="{PAL["faint"]}">time (min)</text>
<path d="M46 168 C90 60 120 52 150 60 C210 78 320 150 430 165" fill="none" stroke="{PAL["A"]}" stroke-width="2.5"/>
<path d="M46 168 C90 70 130 46 170 40 C260 30 360 26 430 24" fill="none" stroke="{PAL["red"]}" stroke-width="2.5"/>
<path d="M46 168 C88 66 120 56 150 62 L250 108 C255 60 340 150 430 165" fill="none" stroke="{PAL["rca"]}" stroke-width="2.5" stroke-dasharray="6 3"/>
<line x1="250" y1="44" x2="250" y2="118" stroke="{PAL["faint"]}" stroke-width="1" stroke-dasharray="3 3"/><text x="250" y="14" text-anchor="middle" font-size="8.5" fill="{PAL["faint"]}">furosemide</text>
<g font-size="10"><rect x="300" y="44" width="12" height="4" fill="{PAL["A"]}"/><text x="318" y="49" fill="{PAL["soft"]}">normal</text>
<rect x="300" y="60" width="12" height="4" fill="{PAL["red"]}"/><text x="318" y="65" fill="{PAL["soft"]}">obstructed (no washout)</text>
<rect x="300" y="76" width="12" height="4" fill="{PAL["rca"]}"/><text x="318" y="81" fill="{PAL["soft"]}">dilated, non-obstructed</text></g>
</svg>'''

def hu_scale_fig():
    # Greyscale density swatches (air dark → bone/metal bright), with HU values.
    items = [("Air", "−1000", "#0b0b0b", "#ffffff"), ("Fat", "−90", "#3a3a3a", "#ffffff"),
             ("Water", "0", "#6a6a6a", "#ffffff"), ("Soft tissue", "+40", "#7c7c7c", "#ffffff"),
             ("Blood", "+60", "#8c8c8c", "#ffffff"), ("Calcium", "+300", "#cfcfcf", "#222222"),
             ("Bone", "+1000", "#efefef", "#222222"), ("Metal", ">1000", "#ffffff", "#222222")]
    n = len(items); w = 48.0; total = 470.0; x0 = 12.0
    gap = (total - 2 * x0 - n * w) / (n - 1)
    out = [f'<svg viewBox="0 0 470 142" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="235" y="16" text-anchor="middle" font-size="11" font-weight="700" '
               f'fill="{PAL["ink"]}">Hounsfield units — density on non-contrast CT</text>')
    x = x0
    for name, hu, fill, txt in items:
        out.append(f'<rect x="{x:.1f}" y="32" width="{w:.0f}" height="48" rx="5" fill="{fill}" '
                   f'stroke="{PAL["line"]}" stroke-width="1"/>')
        out.append(f'<text x="{x+w/2:.1f}" y="60" text-anchor="middle" font-size="10" '
                   f'font-weight="700" fill="{txt}">{hu}</text>')
        out.append(f'<text x="{x+w/2:.1f}" y="98" text-anchor="middle" font-size="9" '
                   f'fill="{PAL["soft"]}">{name}</text>')
        x += w + gap
    out.append(f'<line x1="12" y1="120" x2="450" y2="120" stroke="{PAL["faint"]}" stroke-width="1"/>')
    out.append(f'<path d="M450 116 l8 4 l-8 4 z" fill="{PAL["faint"]}"/>')
    out.append(f'<text x="12" y="136" font-size="9" fill="{PAL["faint"]}">less dense · darker</text>')
    out.append(f'<text x="450" y="136" text-anchor="end" font-size="9" '
               f'fill="{PAL["faint"]}">more dense · brighter</text>')
    out.append("</svg>")
    return "".join(out)

def pet_coincidence_fig():
    cx, cy, R = 230, 118, 90
    s = [f'<svg viewBox="0 0 460 250" {FONT} xmlns="http://www.w3.org/2000/svg">']
    s.append(f'<text x="230" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">PET coincidence detection</text>')
    n = 28
    for i in range(n):
        a = 2 * math.pi * i / n
        x = cx + R * math.cos(a); y = cy + R * math.sin(a)
        s.append(f'<rect x="{x-6:.1f}" y="{y-6:.1f}" width="12" height="12" rx="2" fill="{PAL["ladt"]}" '
                 f'stroke="{PAL["ac"]}" stroke-width="0.8" transform="rotate({math.degrees(a):.0f} {x:.1f} {y:.1f})"/>')
    ang = math.radians(-22); ca = math.cos(ang); sa = math.sin(ang)
    x1 = cx - R*ca; y1 = cy - R*sa; x2 = cx + R*ca; y2 = cy + R*sa
    s.append(f'<defs><marker id="pcp" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">'
             f'<path d="M0 0 l6 3 l-6 3 z" fill="{PAL["red"]}"/></marker></defs>')
    s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{PAL["red"]}" stroke-width="1.3" stroke-dasharray="5 4" opacity="0.5"/>')
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+0.6*R*ca:.1f}" y2="{cy+0.6*R*sa:.1f}" stroke="{PAL["red"]}" stroke-width="2" marker-end="url(#pcp)"/>')
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx-0.6*R*ca:.1f}" y2="{cy-0.6*R*sa:.1f}" stroke="{PAL["red"]}" stroke-width="2" marker-end="url(#pcp)"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{PAL["red"]}"/>')
    s.append(f'<text x="296" y="76" text-anchor="middle" font-size="9.5" font-weight="700" fill="{PAL["red"]}">511 keV</text>')
    s.append(f'<text x="168" y="162" text-anchor="middle" font-size="9.5" font-weight="700" fill="{PAL["red"]}">511 keV</text>')
    s.append(f'<text x="230" y="{cy+70}" text-anchor="middle" font-size="8.5" fill="{PAL["soft"]}">annihilation (e⁺e⁻)</text>')
    s.append(f'<text x="230" y="240" text-anchor="middle" font-size="9.5" fill="{PAL["soft"]}">two 511-keV photons ~180° apart → a line of response (coincidence)</text>')
    s.append("</svg>")
    return "".join(s)

def generator_fig():
    ox, oy, w, h = 46, 168, 392, 140
    s = [f'<svg viewBox="0 0 460 210" {FONT} xmlns="http://www.w3.org/2000/svg">']
    s.append(f'<text x="230" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">⁹⁹Mo → ⁹⁹ᵐTc generator — transient equilibrium</text>')
    s.append(f'<line x1="{ox}" y1="28" x2="{ox}" y2="{oy}" stroke="{PAL["line"]}"/><line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="{PAL["line"]}"/>')
    s.append(f'<text x="20" y="100" font-size="9" fill="{PAL["faint"]}" transform="rotate(-90 20 100)">activity</text>')
    s.append(f'<text x="240" y="204" text-anchor="middle" font-size="9" fill="{PAL["faint"]}">time (h)</text>')
    # parent Mo-99: slow decay from top
    s.append(f'<path d="M{ox} 44 C160 60 300 84 {ox+w} 104" fill="none" stroke="{PAL["ac"]}" stroke-width="2.5"/>')
    s.append(f'<text x="300" y="66" text-anchor="middle" font-size="9.5" font-weight="700" fill="{PAL["ac"]}">⁹⁹Mo (T½ 66 h)</text>')
    # daughter Tc-99m: ingrowth to ~24h then sawtooth elutions
    s.append(f'<path d="M{ox} {oy} C90 90 120 70 156 66 C200 62 210 70 {ox+w} 108" fill="none" stroke="{PAL["red"]}" stroke-width="2.5"/>')
    # elution 1 at 24h (x=156): drop to near baseline then regrow
    s.append(f'<line x1="156" y1="66" x2="156" y2="{oy}" stroke="{PAL["faint"]}" stroke-width="1" stroke-dasharray="3 3"/>')
    s.append(f'<text x="156" y="{oy+12}" text-anchor="middle" font-size="8.5" fill="{PAL["faint"]}">elute ~24 h</text>')
    s.append(f'<path d="M156 {oy-2} C180 120 210 92 246 86 C270 82 280 88 300 92" fill="none" stroke="{PAL["red"]}" stroke-width="2" stroke-dasharray="0" opacity="0.9"/>')
    s.append(f'<text x="196" y="52" font-size="9.5" font-weight="700" fill="{PAL["red"]}">⁹⁹ᵐTc (T½ 6 h)</text>')
    s.append("</svg>")
    return "".join(s)

def _ring(cx, cy, r, defect_a=None, defect_span=70):
    # short-axis myocardial ring; optional pale defect wedge
    p = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAL["lcxt"]}" stroke="{PAL["A"]}" stroke-width="2"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.45:.0f}" fill="#fff" stroke="{PAL["line"]}" stroke-width="1"/>']
    if defect_a is not None:
        a0 = math.radians(defect_a); a1 = math.radians(defect_a + defect_span)
        x0 = cx + r*math.cos(a0); y0 = cy + r*math.sin(a0)
        x1 = cx + r*math.cos(a1); y1 = cy + r*math.sin(a1)
        ri = r*0.45
        xi1 = cx + ri*math.cos(a1); yi1 = cy + ri*math.sin(a1)
        xi0 = cx + ri*math.cos(a0); yi0 = cy + ri*math.sin(a0)
        p.append(f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f} L{xi1:.1f} {yi1:.1f} '
                 f'A{ri:.0f} {ri:.0f} 0 0 0 {xi0:.1f} {yi0:.1f} Z" fill="#F3ECEA" stroke="{PAL["red"]}" stroke-width="1.5"/>')
    return "".join(p)

def mpi_defect_fig():
    s = [f'<svg viewBox="0 0 460 220" {FONT} xmlns="http://www.w3.org/2000/svg">']
    s.append(f'<text x="150" y="18" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["ink"]}">STRESS</text>')
    s.append(f'<text x="300" y="18" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["ink"]}">REST</text>')
    # row 1: reversible (ischemia) — defect at stress, normal at rest
    s.append(_ring(150, 66, 40, defect_a=55))
    s.append(_ring(300, 66, 40))
    s.append(f'<text x="352" y="62" font-size="10.5" font-weight="700" fill="{PAL["red"]}">reversible</text>')
    s.append(f'<text x="352" y="78" font-size="9.5" fill="{PAL["soft"]}">= ischemia</text>')
    # row 2: fixed (scar) — defect at both
    s.append(_ring(150, 160, 40, defect_a=55))
    s.append(_ring(300, 160, 40, defect_a=55))
    s.append(f'<text x="352" y="156" font-size="10.5" font-weight="700" fill="{PAL["ink"]}">fixed</text>')
    s.append(f'<text x="352" y="172" font-size="9.5" fill="{PAL["soft"]}">= scar</text>')
    s.append("</svg>")
    return "".join(s)

def gastric_emptying_fig():
    ox, oy, w = 46, 170, 360
    s = [f'<svg viewBox="0 0 460 210" {FONT} xmlns="http://www.w3.org/2000/svg">']
    s.append(f'<text x="230" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Solid gastric emptying — % meal retained</text>')
    s.append(f'<line x1="{ox}" y1="28" x2="{ox}" y2="{oy}" stroke="{PAL["line"]}"/><line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="{PAL["line"]}"/>')
    # x ticks 0-4h
    for i, lab in enumerate(["0", "1 h", "2 h", "3 h", "4 h"]):
        x = ox + i*w/4
        s.append(f'<text x="{x:.0f}" y="{oy+14}" text-anchor="middle" font-size="9" fill="{PAL["faint"]}">{lab}</text>')
    s.append(f'<text x="18" y="100" font-size="9" fill="{PAL["faint"]}" transform="rotate(-90 18 100)">% retained</text>')
    # normal emptying curve: 100 -> ~55(1h) -> ~35(2h) -> ~15(3h) -> ~5(4h)
    def pt(hr, pct): return (ox + hr*w/4, oy - (pct/100)*(oy-32))
    p0 = pt(0, 100); p1 = pt(1, 55); p2 = pt(2, 35); p3 = pt(3, 15); p4 = pt(4, 5)
    s.append(f'<path d="M{p0[0]:.0f} {p0[1]:.0f} C{p0[0]+40:.0f} {p1[1]-6:.0f} {p1[0]-20:.0f} {p1[1]:.0f} {p1[0]:.0f} {p1[1]:.0f} '
             f'S{p2[0]-20:.0f} {p2[1]:.0f} {p2[0]:.0f} {p2[1]:.0f} S{p3[0]-20:.0f} {p3[1]:.0f} {p3[0]:.0f} {p3[1]:.0f} '
             f'S{p4[0]-20:.0f} {p4[1]:.0f} {p4[0]:.0f} {p4[1]:.0f}" fill="none" stroke="{PAL["A"]}" stroke-width="2.5"/>')
    # threshold markers: >60% at 2h, >10% at 4h
    y60 = oy - 0.60*(oy-32); y10 = oy - 0.10*(oy-32)
    s.append(f'<line x1="{ox}" y1="{y60:.0f}" x2="{p2[0]:.0f}" y2="{y60:.0f}" stroke="{PAL["red"]}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{ox}" y1="{y10:.0f}" x2="{p4[0]:.0f}" y2="{y10:.0f}" stroke="{PAL["red"]}" stroke-width="1" stroke-dasharray="4 3"/>')
    s.append(f'<text x="230" y="202" text-anchor="middle" font-size="9" fill="{PAL["soft"]}">delayed (gastroparesis): &gt;60% at 2 h or &gt;10% at 4 h</text>')
    s.append("</svg>")
    return "".join(s)

def krenning_fig():
    panels = [(0, "0", "none"), (1, "1", "&lt; liver"), (2, "2", "= liver"),
              (3, "3", "&gt; liver"), (4, "4", "&gt; liver/spleen")]
    op = {0: 0.0, 1: 0.35, 2: 0.6, 3: 0.85, 4: 1.0}
    out = [f'<svg viewBox="0 0 460 150" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="230" y="14" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["ink"]}">Krenning score — SSTR uptake vs liver</text>')
    for i, (g, t, d) in enumerate(panels):
        x = 12 + i*89
        out.append(f'<rect x="{x}" y="24" width="78" height="78" rx="8" fill="{PAL["bg"]}" stroke="{PAL["line"]}"/>')
        # liver reference bar
        out.append(f'<rect x="{x+12}" y="80" width="22" height="14" rx="2" fill="{PAL["rca"]}" opacity="0.5"/>')
        out.append(f'<text x="{x+23}" y="112" text-anchor="middle" font-size="7.5" fill="{PAL["faint"]}">liver</text>')
        # tumor dot with increasing intensity
        out.append(f'<circle cx="{x+56}" cy="{62}" r="15" fill="{PAL["A"]}" opacity="{op[g]:.2f}" stroke="{PAL["A"]}" stroke-width="1"/>')
        out.append(f'<text x="{x+56}" y="112" text-anchor="middle" font-size="7.5" fill="{PAL["faint"]}">tumor</text>')
        out.append(f'<text x="{x+39}" y="128" text-anchor="middle" font-size="10" font-weight="700" fill="{PAL["ink"]}">{t}</text>')
        out.append(f'<text x="{x+39}" y="142" text-anchor="middle" font-size="8" fill="{PAL["soft"]}">{d}</text>')
    out.append("</svg>")
    return "".join(out)

def three_phase_bone_fig():
    def bone(cx, top, bot):
        f, s = "#EEE6DC", "#B79B78"
        return (f'<rect x="{cx-5}" y="{top+10}" width="10" height="{bot-top-20}" rx="3" fill="{f}" stroke="{s}" stroke-width="1.2"/>'
                f'<ellipse cx="{cx-4}" cy="{top+8}" rx="7" ry="6" fill="{f}" stroke="{s}" stroke-width="1.2"/>'
                f'<ellipse cx="{cx+4}" cy="{top+8}" rx="7" ry="6" fill="{f}" stroke="{s}" stroke-width="1.2"/>'
                f'<ellipse cx="{cx-4}" cy="{bot-8}" rx="7" ry="6" fill="{f}" stroke="{s}" stroke-width="1.2"/>'
                f'<ellipse cx="{cx+4}" cy="{bot-8}" rx="7" ry="6" fill="{f}" stroke="{s}" stroke-width="1.2"/>')
    titles = [("Phase 1 · Flow", "0–60 s"), ("Phase 2 · Blood pool", "~5–10 min"), ("Phase 3 · Delayed", "~2–4 h")]
    o = [f'<svg viewBox="0 0 460 196" {FONT} xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<text x="230" y="15" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Three-phase bone scan</text>')
    for i, (t, tm) in enumerate(titles):
        x = 14 + i*148; cx = x + 66
        o.append(f'<rect x="{x}" y="24" width="132" height="96" rx="9" fill="{PAL["bg"]}" stroke="{PAL["line"]}"/>')
        if i == 0:            # flow — arterial vessels reaching the bone
            o.append(bone(cx, 40, 104))
            for dy in (56, 74, 92):
                o.append(f'<path d="M{x+12} {dy} q22 -6 40 0" fill="none" stroke="{PAL["red"]}" stroke-width="1.6"/>')
                o.append(f'<path d="M{cx+18} {dy-3} l6 3 l-6 3 z" fill="{PAL["red"]}"/>')
        elif i == 1:          # blood pool — soft-tissue hyperemic blush
            o.append(f'<ellipse cx="{cx}" cy="72" rx="34" ry="40" fill="{PAL["amber"]}" opacity="0.22"/>')
            o.append(bone(cx, 40, 104))
        else:                 # delayed — focal osteoblastic bone uptake
            o.append(bone(cx, 40, 104))
            o.append(f'<ellipse cx="{cx}" cy="74" rx="11" ry="16" fill="{PAL["red"]}" opacity="0.85"/>')
        o.append(f'<text x="{cx}" y="134" text-anchor="middle" font-size="9.5" font-weight="700" fill="{PAL["ink"]}">{t}</text>')
        o.append(f'<text x="{cx}" y="148" text-anchor="middle" font-size="8.5" fill="{PAL["soft"]}">{tm}</text>')
    o.append(f'<line x1="14" y1="162" x2="440" y2="162" stroke="{PAL["faint"]}" stroke-width="1.1"/><path d="M440 158 l8 4 l-8 4 z" fill="{PAL["faint"]}"/>')
    o.append(f'<text x="228" y="186" text-anchor="middle" font-size="8.5" fill="{PAL["soft"]}">osteomyelitis: hot on all three phases · cellulitis: flow + pool only</text>')
    o.append("</svg>")
    return "".join(o)

def eff_half_life_fig():
    ox, oy, w = 46, 168, 392
    out = [f'<svg viewBox="0 0 460 208" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="230" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Effective half-life</text>')
    out.append(f'<line x1="{ox}" y1="28" x2="{ox}" y2="{oy}" stroke="{PAL["line"]}"/><line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="{PAL["line"]}"/>')
    out.append(f'<text x="18" y="100" font-size="9" fill="{PAL["faint"]}" transform="rotate(-90 18 100)">activity</text>')
    out.append(f'<text x="{ox+w-2}" y="{oy+13}" text-anchor="end" font-size="8.5" fill="{PAL["faint"]}">time</text>')
    out.append(f'<path d="M{ox} 34 C160 66 300 96 {ox+w} 116" fill="none" stroke="{PAL["ac"]}" stroke-width="2.3"/>')
    out.append(f'<path d="M{ox} 34 C140 88 260 126 {ox+w} 146" fill="none" stroke="{PAL["rca"]}" stroke-width="2.3"/>')
    out.append(f'<path d="M{ox} 34 C118 108 220 146 {ox+w} 158" fill="none" stroke="{PAL["red"]}" stroke-width="2.6"/>')
    out.append(f'<g font-size="9.5"><rect x="300" y="40" width="12" height="4" rx="1" fill="{PAL["ac"]}"/><text x="318" y="45" fill="{PAL["soft"]}">physical (Tₚ)</text>')
    out.append(f'<rect x="300" y="54" width="12" height="4" rx="1" fill="{PAL["rca"]}"/><text x="318" y="59" fill="{PAL["soft"]}">biological (T_b)</text>')
    out.append(f'<rect x="300" y="68" width="12" height="4" rx="1" fill="{PAL["red"]}"/><text x="318" y="73" fill="{PAL["soft"]}">effective (Tₑ)</text></g>')
    out.append(f'<text x="200" y="198" text-anchor="middle" font-size="10" font-weight="700" fill="{PAL["ink"]}">1/Tₑ = 1/Tₚ + 1/T_b  →  Tₑ is the shortest</text>')
    out.append("</svg>")
    return "".join(out)

def gamma_camera_fig():
    out = [f'<svg viewBox="0 0 460 176" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="200" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Gamma (Anger) camera</text>')
    out.append(f'<rect x="70" y="26" width="260" height="18" rx="4" fill="{PAL["bg"]}" stroke="{PAL["faint"]}"/>')
    out.append(f'<text x="200" y="39" text-anchor="middle" font-size="8.5" fill="{PAL["soft"]}">position logic → image</text>')
    out.append(f'<text x="342" y="39" font-size="9" fill="{PAL["faint"]}">electronics</text>')
    for i in range(9):
        out.append(f'<rect x="{72+i*29}" y="50" width="24" height="22" rx="3" fill="{PAL["ladt"]}" stroke="{PAL["ac"]}"/>')
    out.append(f'<text x="342" y="65" font-size="9" fill="{PAL["ac"]}">PMTs</text>')
    out.append(f'<rect x="70" y="78" width="260" height="15" rx="3" fill="{PAL["lcxt"]}" stroke="{PAL["A"]}"/>')
    out.append(f'<text x="342" y="90" font-size="9" fill="{PAL["A"]}">NaI(Tl)</text>')
    out.append(f'<rect x="70" y="99" width="260" height="17" rx="2" fill="{PAL["rcat"]}" stroke="{PAL["rca"]}"/>')
    for i in range(21):
        out.append(f'<line x1="{78+i*12}" y1="101" x2="{78+i*12}" y2="114" stroke="{PAL["rca"]}" stroke-width="1"/>')
    out.append(f'<text x="342" y="112" font-size="9" fill="{PAL["rca"]}">collimator</text>')
    for i in range(5):
        x = 128 + i*36
        out.append(f'<line x1="{x}" y1="140" x2="{x}" y2="120" stroke="{PAL["soft"]}" stroke-width="1.4"/>')
        out.append(f'<path d="M{x-3} 124 L{x} 118 L{x+3} 124 z" fill="{PAL["soft"]}"/>')
    out.append(f'<text x="200" y="156" text-anchor="middle" font-size="8.5" fill="{PAL["soft"]}">γ photons from the patient ↑</text>')
    out.append("</svg>")
    return "".join(out)

def decay_curve_fig():
    ox, oy, w = 48, 168, 388
    top = 34
    out = [f'<svg viewBox="0 0 460 206" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="230" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Radioactive decay &amp; half-life</text>')
    out.append(f'<line x1="{ox}" y1="28" x2="{ox}" y2="{oy}" stroke="{PAL["line"]}"/><line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="{PAL["line"]}"/>')
    out.append(f'<text x="20" y="100" font-size="9" fill="{PAL["faint"]}" transform="rotate(-90 20 100)">activity</text>')
    labels = ["100%", "50%", "25%", "12.5%"]
    pcts = [100, 50, 25, 12.5]
    def yy(p): return oy - (p/100)*(oy-top)
    xs = [ox + i*(w/4.2) for i in range(4)]
    pts = [(xs[i], yy(pcts[i])) for i in range(4)]
    d = f'M{pts[0][0]:.0f} {pts[0][1]:.0f} '
    for i in range(1, 4):
        mx = (pts[i-1][0]+pts[i][0])/2
        d += f'Q{mx:.0f} {pts[i][1]:.0f} {pts[i][0]:.0f} {pts[i][1]:.0f} '
    # extend tail
    d += f'T{ox+w} {yy(6):.0f}'
    out.append(f'<path d="{d}" fill="none" stroke="{PAL["ac"]}" stroke-width="2.6"/>')
    for i in range(1, 4):
        out.append(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[i][0]:.0f}" y2="{oy}" stroke="{PAL["faint"]}" stroke-dasharray="3 3" stroke-width="1"/>')
        out.append(f'<line x1="{ox}" y1="{pts[i][1]:.0f}" x2="{pts[i][0]:.0f}" y2="{pts[i][1]:.0f}" stroke="{PAL["faint"]}" stroke-dasharray="3 3" stroke-width="1"/>')
        out.append(f'<text x="{pts[i][0]:.0f}" y="{oy+13}" text-anchor="middle" font-size="8.5" fill="{PAL["faint"]}">{i}·T½</text>')
        out.append(f'<text x="{ox-4}" y="{pts[i][1]+3:.0f}" text-anchor="end" font-size="8.5" fill="{PAL["faint"]}">{labels[i]}</text>')
    out.append(f'<text x="{ox-4}" y="{top+3}" text-anchor="end" font-size="8.5" fill="{PAL["faint"]}">100%</text>')
    out.append(f'<text x="230" y="198" text-anchor="middle" font-size="9" fill="{PAL["soft"]}">each half-life halves the activity: 100 → 50 → 25 → 12.5 %</text>')
    out.append("</svg>")
    return "".join(out)

def hida_ef_fig():
    ox, oy, w = 48, 168, 388
    out = [f'<svg viewBox="0 0 460 206" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="230" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Gallbladder ejection fraction (HIDA + CCK)</text>')
    out.append(f'<line x1="{ox}" y1="28" x2="{ox}" y2="{oy}" stroke="{PAL["line"]}"/><line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="{PAL["line"]}"/>')
    out.append(f'<text x="20" y="100" font-size="9" fill="{PAL["faint"]}" transform="rotate(-90 20 100)">GB counts</text>')
    cckx = ox + w*0.52
    out.append(f'<path d="M{ox} 150 C90 74 140 52 180 50 L{cckx:.0f} 52 C{cckx+34:.0f} 62 {cckx+80:.0f} 118 {ox+w} 138" fill="none" stroke="{PAL["A"]}" stroke-width="2.6"/>')
    out.append(f'<line x1="{cckx:.0f}" y1="40" x2="{cckx:.0f}" y2="{oy}" stroke="{PAL["faint"]}" stroke-dasharray="3 3" stroke-width="1"/>')
    out.append(f'<text x="{cckx:.0f}" y="37" text-anchor="middle" font-size="8.5" fill="{PAL["faint"]}">CCK</text>')
    out.append(f'<text x="150" y="44" font-size="9" fill="{PAL["A"]}">max fill</text>')
    out.append(f'<text x="230" y="198" text-anchor="middle" font-size="9" fill="{PAL["soft"]}">GBEF = (max − min) ÷ max × 100 · normal ≥ ~35–38%</text>')
    out.append("</svg>")
    return "".join(out)

def raiu_fig():
    ox, oy, w = 48, 168, 388
    out = [f'<svg viewBox="0 0 460 206" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="230" y="16" text-anchor="middle" font-size="11" font-weight="700" fill="{PAL["ink"]}">Radioactive iodine uptake (RAIU)</text>')
    out.append(f'<line x1="{ox}" y1="28" x2="{ox}" y2="{oy}" stroke="{PAL["line"]}"/><line x1="{ox}" y1="{oy}" x2="{ox+w}" y2="{oy}" stroke="{PAL["line"]}"/>')
    out.append(f'<text x="20" y="100" font-size="9" fill="{PAL["faint"]}" transform="rotate(-90 20 100)">% uptake</text>')
    ylo = oy - 0.10*(oy-34); yhi = oy - 0.30*(oy-34)
    out.append(f'<rect x="{ox}" y="{yhi:.0f}" width="{w}" height="{ylo-yhi:.0f}" fill="{PAL["lcxt"]}" opacity="0.55"/>')
    out.append(f'<text x="{ox+6}" y="{yhi-4:.0f}" font-size="8.5" fill="{PAL["A"]}">normal band (24 h ≈ 10–30%)</text>')
    out.append(f'<path d="M{ox} {oy} C120 70 210 48 {ox+w} 42" fill="none" stroke="{PAL["red"]}" stroke-width="2.3"/>')
    out.append(f'<path d="M{ox} {oy} C120 120 210 {(ylo+yhi)/2-4:.0f} {ox+w} {(ylo+yhi)/2:.0f}" fill="none" stroke="{PAL["A"]}" stroke-width="2.3"/>')
    out.append(f'<path d="M{ox} {oy} C130 152 230 152 {ox+w} 156" fill="none" stroke="{PAL["rca"]}" stroke-width="2.3"/>')
    for lab, fr in [("4 h", 0.28), ("24 h", 0.94)]:
        out.append(f'<text x="{ox+fr*w:.0f}" y="{oy+13}" text-anchor="middle" font-size="8.5" fill="{PAL["faint"]}">{lab}</text>')
    out.append(f'<text x="{ox+w-4}" y="40" text-anchor="end" font-size="9" fill="{PAL["red"]}">high (Graves)</text>')
    out.append(f'<text x="{ox+w-4}" y="153" text-anchor="end" font-size="9" fill="{PAL["rca"]}">low (thyroiditis)</text>')
    out.append("</svg>")
    return "".join(out)

def dat_scan_fig():
    out = [f'<svg viewBox="0 0 460 184" {FONT} xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="115" y="15" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["ink"]}">Normal</text>')
    out.append(f'<text x="345" y="15" text-anchor="middle" font-size="10.5" font-weight="700" fill="{PAL["ink"]}">Parkinsonism</text>')
    for px in (12, 242):
        out.append(f'<ellipse cx="{px+103}" cy="86" rx="98" ry="60" fill="{PAL["bg"]}" stroke="{PAL["line"]}"/>')
    def stri(cx, cy, d, put):  # caudate head + putamen sweeping infero-laterally; put = opacity (0 = lost)
        head = f'<circle cx="{cx}" cy="{cy}" r="12.5" fill="{PAL["ac"]}"/>'
        if put <= 0:
            return head
        pth = (f'M {cx-d*2} {cy+9} C {cx+d*15} {cy+12}, {cx+d*19} {cy+30}, {cx+d*12} {cy+46} '
               f'C {cx+d*8} {cy+52}, {cx+d*1} {cy+50}, {cx-d*3} {cy+42} '
               f'C {cx-d*5} {cy+30}, {cx-d*5} {cy+18}, {cx-d*2} {cy+9} Z')
        return head + f'<path d="{pth}" fill="{PAL["ac"]}" opacity="{put}"/>'
    out.append(stri(92, 70, -1, 1.0)); out.append(stri(138, 70, 1, 1.0))
    out.append(f'<text x="115" y="52" text-anchor="middle" font-size="7.5" fill="{PAL["faint"]}">caudate</text>')
    out.append(f'<text x="56" y="124" font-size="7.5" fill="{PAL["faint"]}">putamen</text>')
    out.append(stri(322, 70, -1, 0.5)); out.append(stri(368, 70, 1, 0.0))
    out.append(f'<text x="345" y="126" text-anchor="middle" font-size="8" fill="{PAL["red"]}">asymmetric putaminal loss</text>')
    out.append(f'<text x="115" y="172" text-anchor="middle" font-size="8.5" fill="{PAL["soft"]}">symmetric "comma" (caudate + putamen)</text>')
    out.append(f'<text x="345" y="172" text-anchor="middle" font-size="8.5" fill="{PAL["soft"]}">putamen fades → caudate "period"</text>')
    out.append("</svg>")
    return "".join(out)

# ---- Figure registry: original, license-clean vector schematics wired to pages ----
# Every figure here is drawn in-house (public-domain by construction — no attribution
# or reuse restrictions). Photographic/CT images are added per-page via `figures:`
# front-matter from openly-licensed sources; slots stay blank until a good one exists.
def placeholder_fig(label="Illustration to come"):
    """A clearly-marked reserved slot for a diagram not yet drawn/sourced. Drawn on the
    light figure backing (atlas palette); swap for a real figure when one exists."""
    return (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 640 240'>"
    "<rect x='6' y='6' width='628' height='228' rx='16' fill='#F6F7F9' stroke='#C4BADF' stroke-width='2' stroke-dasharray='10 8'/>"
    "<g transform='translate(320,92)' fill='none' stroke='#4A3A82' stroke-width='3' stroke-linejoin='round' stroke-linecap='round'>"
    "<rect x='-36' y='-28' width='72' height='56' rx='7'/>"
    "<circle cx='-15' cy='-7' r='6.5' fill='#4A3A82' stroke='none'/>"
    "<path d='M-36 22 L-9 -3 L7 13 L19 3 L36 20'/></g>"
    "<text x='320' y='158' text-anchor='middle' font-family=\"'JetBrains Mono',ui-monospace,monospace\" font-size='12' letter-spacing='2.5' fill='#8D949C'>DIAGRAM PLACEHOLDER</text>"
    "<text x='320' y='182' text-anchor='middle' font-family=\"'Inter',system-ui,sans-serif\" font-size='13' fill='#565E68'>" + label + "</text>"
    "</svg>")

FIGURES = {
 "seventeen-segment-model": [(bullseye(),
   "The 17-segment model mapped to coronary territories (LAD · LCx · RCA); the apex is segment 17.")],
 "vq-scan-pe": [(vq_fig(),
   "V/Q mismatch — normal ventilation with a segmental perfusion defect: the pattern of pulmonary embolism.")],
 "cardiac-amyloidosis": [(perugini_fig(),
   "Perugini visual grade 0–3: myocardial bone-tracer uptake relative to rib/bone uptake.")],
 "radiation-interactions-matter": [(particles_fig(),
   "Particle range and shielding: α (µm, very high LET) · β⁻ (mm in tissue) · γ / 511 keV (penetrating).")],
 "theranostics-overview": [(theranostic_fig(),
   "The theranostic pair — one targeting molecule labelled to SEE (Ga-68 / F-18 PET) or TREAT (Lu-177 / Ac-225).")],
 "lymphoma-staging-lugano-deauville": [(deauville_fig(),
   "Deauville 5-point score: lesion uptake vs mediastinal blood pool and liver (scores 4–5 exceed liver).")],
 "mag3": [(renogram_fig(),
   "Renogram curves: normal, obstructed (no furosemide washout), and dilated but non-obstructed.")],
 "correlative-ct-overview": [(hu_scale_fig(),
   "Hounsfield-unit density on non-contrast CT — air, fat, water, soft tissue, calcium, bone, and metal.")],
 "pet-spect-performance-reconstruction": [(pet_coincidence_fig(),
   "PET coincidence detection: positron annihilation yields two 511-keV photons ~180° apart, defining a line of response when detected within the coincidence window.")],
 "radiopharmaceuticals-overview": [(generator_fig(),
   "The ⁹⁹Mo→⁹⁹ᵐTc generator: the daughter grows in to a peak (~24 h), tracks the parent in transient equilibrium, and is reset by each elution.")],
 "mpi-spect": [(mpi_defect_fig(),
   "Reversible vs fixed defect: a defect present at stress that resolves at rest is ischemia; a defect present at both stress and rest is scar.")],
 "gastric-emptying": [(gastric_emptying_fig(),
   "Solid gastric emptying: normal meal retention falls over 4 h; delayed emptying (gastroparesis) is >60% retained at 2 h or >10% at 4 h.")],
 "dotatate": [(krenning_fig(),
   "Krenning score (0–4): somatostatin-receptor uptake graded against liver and spleen; grade 3–4 (uptake ≥ liver) supports PRRT eligibility.")],
 "mdp": [(three_phase_bone_fig(),
   "Three-phase bone scan: flow (0–60 s), blood pool (~5–10 min), and delayed bone-uptake (~2–4 h) — osteomyelitis is positive on all three.")],
 "instrumentation-detection": [(gamma_camera_fig(),
   "The gamma (Anger) camera: collimator → NaI(Tl) crystal → PMT array → position logic; the collimator sets spatial resolution.")],
 "physics-nuclear-medicine": [(decay_curve_fig(),
   "Radioactive decay: activity halves each half-life (100 → 50 → 25 → 12.5%)."),
  (placeholder_fig("one DOTA ligand, two radiometals"),
   "Placeholder — theranostic pairing: a single DOTA-conjugated targeting ligand carrying <b>Ga-68 to image</b> or <b>Lu-177 to treat</b>, the chemical basis of one element serving both ends of the pair.")],
 "mird-dosimetry-worked": [(eff_half_life_fig(),
   "Effective half-life combines physical and biological clearance (1/Tₑ = 1/Tₚ + 1/T_b) and is always the shortest of the three.")],
 "cholescintigraphy-hida": [(hida_ef_fig(),
   "Gallbladder ejection fraction: after CCK the gallbladder empties; GBEF = (max − min)/max × 100 (normal ≥ ~35–38%).")],
 "radioiodine-thyroid": [(raiu_fig(),
   "Radioactive iodine uptake: high in Graves disease, within the normal band in euthyroidism, and low in thyroiditis (or iodine load).")],
 "ioflupane": [(dat_scan_fig(),
   "DAT-SPECT: a normal symmetric 'comma' (caudate + putamen) vs the putaminal loss ('period/full-stop') of Parkinsonian degeneration.")],
 "ai-machine-learning-nuclear-medicine": [(ai_loop_fig(),
   "AI enters every node of the see→treat→quantify→reassess loop — but its highest-leverage role is automating dosimetry, the step that turns one-size-fits-all radioligand therapy into personalized, dose-optimized treatment.")],
}

def fig_html(p):
    """Render figures for a page. Two sources, both numbered together:
       (1) inline SVG schematics via the FIGURES dict; (2) image figures declared
       in front-matter as  figures: [{src, caption, credit, alt}].  Click = lightbox."""
    pid = p["id"] if isinstance(p, dict) else p
    out, n = [], 0
    for svg, cap in FIGURES.get(pid, []):
        n += 1
        _alabel = re.sub(r"<[^>]+>", "", cap).replace("&nbsp;", " ").replace('"', "'")
        svg = svg.replace("<svg ", f'<svg role="img" aria-label="Figure {n}: {_alabel}" ', 1)
        out.append(f'<figure class="fig" onclick="lightbox(this)"><div class="fig-media">{svg}</div>'
                   f'<figcaption><b>Fig&nbsp;{n}.</b> {cap}</figcaption></figure>')
    figs = p.get("_figures", []) if isinstance(p, dict) else []
    for f in figs:
        if not isinstance(f, dict) or not f.get("src"):
            continue
        n += 1
        alt = f.get("alt") or f.get("caption") or (p["title"] if isinstance(p, dict) else "")
        credit = f' <span class="fig-credit">{f["credit"]}</span>' if f.get("credit") else ""
        out.append(
            '<figure class="fig" onclick="lightbox(this)"><div class="fig-media">'
            f'<img src="{f["src"]}" alt="{alt}" loading="lazy"></div>'
            f'<figcaption><b>Fig&nbsp;{n}.</b> {f.get("caption", "")}{credit}</figcaption></figure>')
    return "".join(out)

# Persistent, consistent colours for the major radiotracers/agents wherever they appear as a tag.
TRACER_COLORS = {
    "fdg": "#C99700", "psma": "#7B4BC4", "dotatate": "#0E8C6A", "pyp": "#C24B6E",
    "mibg": "#C2410C", "mag3": "#2563A6", "dmsa": "#1E7A8C", "dtpa": "#3F72AF",
    "mdp": "#5B6470", "naf": "#5B6470", "hida": "#B0740A", "sestamibi": "#B03030",
    "mibi": "#B03030", "maa": "#0E7490", "ioflupane": "#7A5C1E", "datscan": "#7A5C1E",
    "gallium": "#556B2F", "ga67": "#556B2F", "thallium": "#8A6D3B", "rubidium": "#A83232",
    "fdopa": "#2E7D32", "fes": "#B03A78", "fluciclovine": "#3B6EA5", "choline": "#3B6EA5",
    "fapi": "#8A5A2B", "pertechnetate": "#4A6FA5", "sulfurcolloid": "#6B7280",
    "octreotide": "#0E8C6A", "radioiodine": "#B03030", "i131": "#B03030", "i123": "#B03030",
    "lu177": "#0E8C6A", "y90": "#8A5A2B", "ra223": "#7B4BC4", "n13": "#0E7490",
}
def _tag_html(t):
    key = re.sub(r"[^a-z0-9]", "", t.lower())
    c = TRACER_COLORS.get(key)
    return (f'<span class="tag tracer" style="--tc:{c}">#{t}</span>' if c
            else f'<span class="tag">#{t}</span>')

def page_html(p):
    iso = f'<span class="iso">{p["iso"]}</span>' if p["iso"] else ""
    tags = "".join(_tag_html(t) for t in p["tags"])
    rev = (p.get("_review") or "").replace("-", " ").replace("ai ", "AI-").strip()
    rev_lbl = {"AI-drafted": "AI-drafted", "physician reviewed": "Physician-reviewed"}.get(rev, rev.capitalize())
    upd = p.get("_updated")
    prov = ""
    if upd or rev_lbl:
        bits = []
        if upd:
            bits.append(f'Updated {upd}')
        if rev_lbl:
            bits.append(f'<span class="rev rev-{"phys" if "hysician" in rev_lbl else "ai"}">{rev_lbl}</span>')
        prov = f'<span class="prov">{" · ".join(bits)}</span>'
    _subj = _url0.quote(f"NM Atlas correction: {p['title']} (#{p['id']}) v{VERSION}")
    _report = (f' <a class="cite-link cite-report" href="mailto:{CONTACT_EMAIL}?subject={_subj}" '
               f'title="Report an error or suggest an edit for this page">Report an issue</a>')
    cite = ("" if p['chapter'] == "tools" else
            f'<div class="cite"><b>Cite this page.</b> <span class="cite-txt">Nuclear Medicine Atlas. '
            f'&ldquo;{p["title"]}.&rdquo; v{VERSION}, {BUILD_DATE}. Permalink: '
            f'<code>#/{p["id"]}</code></span> <button class="cite-copy" onclick="copyCite(this)">Copy</button>{_report}</div>')
    # authorship / provenance blocks (empty string for ordinary pages)
    prebody = (PROVBAR_HTML.get(p['id'], '')
               + ARTICLE_HEAD_HTML.get(p['id'], '')
               + AUTHOR_HEAD_HTML.get(p['id'], ''))
    postbody = (ARTICLE_FOOT_HTML.get(p['id'], '')
                + AUTHOR_FOOT_HTML.get(p['id'], ''))
    return f'''<article class="page" id="page-{p['id']}" data-search="{(p['title']+' '+p['subtitle']+' '+p['aliases']).lower()}">
  <button class="bm" id="bm-{p['id']}" onclick="toggleBM('{p['id']}')" title="Bookmark this page">☆</button>
  <nav class="crumbs" aria-label="Breadcrumb"><a class="crumb-home" onclick="go('home')" role="link" tabindex="0">Home</a><span class="csep">›</span><span class="crumb-part">{PART_LABEL.get(CH_PART[p['chapter']], '')}</span><span class="csep">›</span><span class="crumb-ch">{CH_LABEL[p['chapter']]}</span></nav>
  <h1 class="ptitle">{p['title']}{iso}</h1>
  <p class="psub">{p['subtitle']}</p>
  <div class="meta">{grade_summary(p['id'])}{tags}{prov}</div>
  <div class="hy-note">High-yield mode — key points, high-yield facts, tables &amp; quizzes only. Toggle off for full text.</div>
  {prebody}
  <div class="body">{p['html']}{fig_html(p)}{TOOLS.get(p['id'], '')}</div>
  {postbody}
  {CURATED_HTML.get(p['id'], '')}
  {REL_LINKS.get(p['id'], '')}
  {BACKLINK_HTML.get(p['id'], '')}
  <div class="ev">{cites_html(p['id'])}</div>
  {cite}
</article>'''

CH_DESC = {
 "physics": "Decay, statistics, radiation biology",
 "instrumentation": "Detectors, QC, SPECT/PET, reconstruction",
 "radiopharmacy": "Agents, production, chelation, molecular targets & mechanism classes",
 "dosimetry-safety": "MIRD, dose, pregnancy, pediatric, release, accidents",
 "endocrine": "Thyroid, parathyroid, adrenal, NET",
 "cardiac": "Perfusion, viability, amyloid, flow, function",
 "neuro": "Dementia, tumors, epilepsy, DAT, brain death",
 "musculoskeletal": "Bone scan, NaF PET, patterns",
 "genitourinary": "Renal function, GFR, PSMA, prostate",
 "pulmonary": "V/Q, PE, ventilation agents",
 "gastrointestinal": "HIDA, liver-spleen, emptying, bleeding, reflux",
 "infection": "WBC, FDG, Ga-67, osteomyelitis, vasculitis",
 "oncology": "FDG & PET oncology, lymphatic mapping",
 "theranostics": "Radioligand therapy, dosimetry, response, pipeline",
 "reporting": "Structured scoring & response frameworks",
 "pearls": "Finding-driven patterns, variants, mimics, artifacts, incidentals",
 "test-selection": "Which test when — head-to-head modality & tracer selection",
 "landmark-trials": "The trials that changed nuclear medicine — design, result, impact, reference",
 "boards": "Quantitation, thresholds, confounders, evidence, protocols, boards",
 "field-future": "Why the field is transforming, the training pathways, and where it's going",
 "learning-paths": "Guided reading tracks — student, resident, boards & theranostics",
 "correlative-ct": "Reading the low-dose, non-contrast CT of PET/CT & SPECT/CT",
 "articles": "Peer contributions that flow into the atlas — each references its source",
 "contributors": "The physicians & scientists whose work shapes the atlas",
 "tools": "Calculators & decision aids",
}
# Browse axes reflect how nuclear-medicine physicians actually navigate — by organ system,
# therapy, probe/target, indication, reporting, pitfalls, modality — mapped to real chapters/parts.
THEMES = [
    ("Organ systems", "part:III"),
    ("Therapy", "ch:theranostics"),
    ("Probes & targets", "part:II"),
    ("Physics", "part:I"),
    ("Test selection", "ch:test-selection"),
    ("Reporting", "ch:reporting"),
    ("Pitfalls & variants", "ch:pearls"),
    ("Landmark trials", "ch:landmark-trials"),
    ("PET", "pet"),
    ("SPECT", "spect scintigraph"),
    ("Tools", "tool"),
]

# ---- accordion sidebar ----
nav_html = '<div class="nav-home" data-id="home" tabindex="0" role="link" onclick="go(\'home\')">✦ Home</div>'
last_part = None
for ch, lbl, part in CHAPTERS:
    items = [p for p in pages if p["chapter"] == ch]
    if not items:
        continue
    if part != last_part:
        nav_html += f'<div class="nav-part">{PART_LABEL[part]}</div>'
        last_part = part
    inner = "".join(
        f'<a class="nav-item" data-id="{p["id"]}" href="#page-{p["id"]}">{p["title"]}</a>'
        for p in items)
    nav_html += (f'<div class="nav-ch" data-ch="{ch}">'
                 f'<div class="nav-ch-h" tabindex="0" role="button" onclick="toggleCh(\'{ch}\')">'
                 f'<span class="chev">›</span><span class="nav-ch-t">{lbl}</span>'
                 f'<span class="nav-ch-n">{len(items)}</span></div>'
                 f'<div class="nav-ch-items">{inner}</div></div>')

# ---- home dashboard ----
def home_html():
    total = len(pages)
    ntools = sum(1 for p in pages if p["chapter"] == "tools")
    cards = ""
    last = None
    for ch, lbl, part in CHAPTERS:
        items = [p for p in pages if p["chapter"] == ch]
        if not items:
            continue
        if part != last:
            cards += f'</div>' if last is not None else ''
            cards += f'<div class="home-part">{PART_LABEL[part]}</div><div class="home-cards">'
            last = part
        first = items[0]["id"]
        cards += (f'<a class="hcard" href="#page-{first}">'
                  f'<div class="hcard-t">{lbl}</div>'
                  f'<div class="hcard-d">{CH_DESC.get(ch, "")}</div>'
                  f'<div class="hcard-n">{len(items)} page{"s" if len(items) != 1 else ""}</div></a>')
    cards += '</div>'
    chips = "".join(f'<div class="chip" onclick="themeBrowse(\'{lbl}\',\'{q}\')">{lbl}</div>' for lbl, q in THEMES)
    return (f'<article class="page" id="page-home" data-search="home">'
            f'<div class="hero"><div class="kick">Clinical Reference</div>'
            f'<h1 class="home-title">Nuclear Medicine Atlas</h1>'
            f'<p class="home-sub">A fast, searchable clinical reference for nuclear medicine: every tracer, disease, organ system, protocol, and therapy in one place, graded by evidence.</p>'
            f'<div class="home-search"><svg class="hs-mag" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m21 21-4.3-4.3"></path></svg>'
            f'<input id="hq" class="hs-input" type="search" autocomplete="off" aria-label="Search the atlas" placeholder="Search a disease, tracer, organ, abbreviation, or therapy&hellip;" oninput="homeSearch(this.value)" onkeydown="homeSearchKey(event)">'
            f'<div id="hsr" class="hsr" role="listbox"></div></div>'
            f'<div class="home-browse"><span class="browse-lbl">Browse by area</span><div class="chips">{chips}</div></div>'
            f'<div class="home-stats"><span><b>{total}</b> pages</span><span><b>{len(CH_LABEL)}</b> chapters</span>'
            f'<span><b>{ntools}</b> tools</span><span><b>graded</b> A · B · C evidence</span>'
            f'<span><b>v{VERSION}</b> · {BUILD_DATE}</span></div>'
            f'</div>'
            f'{cards}'
            f'<div class="home-guide">'
            f'<div class="hg-col"><div class="hg-h">How to read the atlas</div>'
            f'<div class="hg-item"><span class="lg-k">KEY POINT</span> &nbsp;the single must-know takeaway on each page</div>'
            f'<div class="hg-item"><b>Bold text</b> marks high-yield facts; <span class="lg-d">smaller grey text</span> is deeper detail</div>'
            f'<div class="hg-item">Every page ends with <b>self-check</b> board questions and clickable <b>See also</b> cross-links</div>'
            f'<div class="hg-item">Search (top-left) spans titles, aliases, and sections; <b>tools</b> are interactive calculators</div></div>'
            f'<div class="hg-col"><div class="hg-h">Evidence &amp; review</div>'
            f'<div class="hg-item"><span class="gr gA">A</span> RCT / meta-analysis &nbsp; <span class="gr gB">B</span> large cohort or society guideline</div>'
            f'<div class="hg-item"><span class="gr gC">C</span> smaller / physiologic reasoning &nbsp; <span class="gr gI">INF</span> inference (reasoning, not a citation)</div>'
            f'<div class="hg-item">Each page is labelled <b>physician-reviewed</b> or <b>ai-drafted</b> (pending review)</div>'
            f'<div class="hg-item">A four-level <b>yield hierarchy</b> keeps board-critical points visually dominant</div></div>'
            f'</div>'
            f'<div class="home-disclaimer"><b>Educational use only.</b> This atlas is a study and reference aid — '
            f'it is <b>not medical advice</b> and not a substitute for clinical judgement. Verify all activities, doses, '
            f'thresholds, timings, and protocols against current society guidelines, product labelling, and local/regulatory '
            f'policy before any clinical use. Values are representative and vary by scanner, protocol, patient, and jurisdiction; '
            f'regulatory figures follow US NRC conventions (ICRP/other frameworks differ). Content is compiled from public primary '
            f'literature and society guidelines in original prose; some pages are AI-drafted and pending physician review.</div><div class="home-credit" style="margin-top:12px;font-size:.85em;opacity:.8">Created by <a href="https://jhs.md">John H. Solomon, MD</a> · Published by <a href="https://johnsolomon.org">John Solomon LLC</a> · <a href="https://johnsolomon.org/legal/">Terms &amp; privacy</a></div>'
            f'</article>')

pages_html = home_html() + "".join(page_html(p) for p in pages)
def _plain_text(h):
    """Strip HTML/scripts/styles to searchable prose."""
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    h = re.sub(r"&[a-zA-Z#0-9]+;", " ", h)
    return re.sub(r"\s+", " ", h).strip().lower()

search_index = json.dumps([{"id": p["id"], "title": p["title"], "sub": p["subtitle"],
                            "group": CH_LABEL[p["chapter"]],
                            "chapter": p["chapter"], "part": CH_PART[p["chapter"]],
                            "s": (p["title"] + " " + p["subtitle"] + " " + p["aliases"] + " "
                                  + _plain_text(p["html"])).lower()} for p in pages])
page_order = json.dumps(["home"] + [p["id"] for p in pages])

# ---- Study Mode: aggregate every self-check quiz into a board-prep dataset ----
def _extract_quizzes(pg):
    out = []
    for m in re.finditer(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", pg["html"], re.S):
        q = re.sub(r"^\s*<strong>\s*Q\d+\.?\s*</strong>\s*", "", m.group(1)).strip()
        a = re.sub(r"^<p>\s*<strong>\s*Answer:?\s*</strong>\s*", "<p>", m.group(2).strip()).strip()
        if len(q) > 2 and len(a) > 2:
            out.append({"id": pg["id"], "t": pg["title"], "ch": CH_LABEL[pg["chapter"]], "q": q, "a": a})
    return out

_quiz = []
for _p in pages:
    _quiz.extend(_extract_quizzes(_p))
quiz_index = json.dumps(_quiz)

# ---- Radiopharmaceutical Compendium (interactive tracer-target matrix) ----
# cls = mechanism class (drives colour + filter); mod = PET / SPECT / Therapy.
_COMPENDIUM = [
 ["¹⁸F-FDG", "F-18", "PET", "Metabolism", "Glucose transport (GLUT) & hexokinase trapping", "Oncology staging, infection/inflammation, viability", "fdg"],
 ["¹⁸F-NaF", "F-18", "PET", "Bone", "Hydroxyapatite (osteoblastic)", "Skeletal metastasis detection", "naf-bone-pet"],
 ["⁸²Rb-chloride", "Rb-82", "PET", "Perfusion", "K⁺ analogue, myocardial uptake", "Myocardial perfusion (rest/stress)", "rubidium-82"],
 ["¹³N-ammonia", "N-13", "PET", "Perfusion", "Metabolic trapping (glutamine)", "Myocardial perfusion & flow", "n13-ammonia"],
 ["⁶⁸Ga/⁶⁴Cu-DOTATATE", "Ga-68", "PET", "Receptor", "Somatostatin receptor 2 (SSTR)", "NET staging; PRRT selection", "dotatate"],
 ["⁶⁸Ga/¹⁸F-PSMA", "Ga-68", "PET", "Antigen", "Prostate-specific membrane antigen", "Prostate staging/recurrence; RLT selection", "psma-11"],
 ["¹⁸F-fluciclovine", "F-18", "PET", "Transporter", "Amino-acid transport (ASCT2/LAT1)", "Prostate cancer recurrence", "fluciclovine"],
 ["¹¹C/¹⁸F-choline", "C-11", "PET", "Metabolism", "Choline kinase / membrane synthesis", "Prostate recurrence; parathyroid", "choline-pet"],
 ["¹⁸F-FDOPA", "F-18", "PET", "Transporter", "AADC / catecholamine pathway", "NET, PPGL, MTC, parkinsonism, hyperinsulinism", "fdopa"],
 ["¹⁸F-FES", "F-18", "PET", "Receptor", "Estrogen receptor", "ER-positive breast cancer", "fes"],
 ["⁶⁸Ga/¹⁸F-FAPI", "Ga-68", "PET", "Receptor", "Fibroblast activation protein", "Pan-tumour & fibrosis (emerging)", "fapi"],
 ["⁹⁹ᵐTc-sestamibi", "Tc-99m", "SPECT", "Perfusion", "Mitochondrial membrane potential", "Myocardial perfusion; parathyroid; breast", "sestamibi"],
 ["²⁰¹Tl-chloride", "Tl-201", "SPECT", "Perfusion", "K⁺ analogue (Na/K-ATPase)", "Perfusion & viability (redistribution)", "thallium-201"],
 ["⁹⁹ᵐTc-HMPAO / ECD", "Tc-99m", "SPECT", "Perfusion", "Lipophilic brain-perfusion trapping", "Brain perfusion; WBC labelling (HMPAO)", "brain-perfusion-agents"],
 ["⁹⁹ᵐTc-MDP / HDP", "Tc-99m", "SPECT", "Bone", "Hydroxyapatite (osteoblastic)", "Bone scintigraphy", "mdp"],
 ["⁹⁹ᵐTc-MAG3", "Tc-99m", "SPECT", "Renal", "Tubular secretion (OAT)", "Renal function & obstruction", "mag3"],
 ["⁹⁹ᵐTc-DTPA", "Tc-99m", "SPECT", "Renal", "Glomerular filtration", "GFR; renal; ventilation (aerosol)", "tc99m-dtpa"],
 ["⁹⁹ᵐTc-mebrofenin (HIDA)", "Tc-99m", "SPECT", "Hepatobiliary", "Hepatocyte uptake & biliary excretion", "Cholescintigraphy", "cholescintigraphy-hida"],
 ["⁹⁹ᵐTc-sulfur colloid", "Tc-99m", "SPECT", "Phagocytic", "Reticuloendothelial (Kupffer) uptake", "Liver–spleen, marrow, LN mapping, GI", "tc99m-sulfur-colloid"],
 ["⁹⁹ᵐTc-MAA", "Tc-99m", "SPECT", "Perfusion", "Capillary microembolisation", "Lung perfusion; Y-90 lung-shunt mapping", "maa"],
 ["⁹⁹ᵐTc-pertechnetate", "Tc-99m", "SPECT", "Transporter", "Na/I symporter (thyroid, salivary, gastric)", "Thyroid; Meckel; ectopic gastric mucosa", "tc99m-pertechnetate"],
 ["⁹⁹ᵐTc-PYP", "Tc-99m", "SPECT", "Amyloid", "Binds ATTR cardiac amyloid", "Cardiac transthyretin amyloidosis", "pyp"],
 ["⁹⁹ᵐTc-RBC", "Tc-99m", "SPECT", "Blood pool", "Labelled erythrocytes", "GI bleeding; hemangioma; MUGA", "tc99m-rbc"],
 ["¹²³I / ¹³¹I-iodide", "I-123", "SPECT", "Transporter", "Na/I symporter (NIS)", "Thyroid uptake/scan; thyroid cancer", "radioiodine-thyroid"],
 ["¹²³I-MIBG", "I-123", "SPECT", "Transporter", "Norepinephrine transporter", "PPGL, neuroblastoma, cardiac", "mibg-i123"],
 ["¹²³I-ioflupane", "I-123", "SPECT", "Transporter", "Presynaptic dopamine transporter", "Parkinsonism / DLB", "ioflupane"],
 ["¹¹¹In / ⁹⁹ᵐTc-WBC", "In-111", "SPECT", "Inflammation", "Leukocyte migration to infection", "Prosthesis / peripheral osteomyelitis", "labeled-leukocyte-scintigraphy"],
 ["¹³¹I-iodide (therapy)", "I-131", "Therapy", "Transporter", "Na/I symporter (NIS)", "Thyroid ablation/therapy; hyperthyroidism", "thyroid-cancer-i131-therapy"],
 ["¹⁷⁷Lu-DOTATATE", "Lu-177", "Therapy", "Receptor", "SSTR (β-PRRT)", "Neuroendocrine tumour therapy", "lu177-dotatate"],
 ["¹⁷⁷Lu-PSMA-617", "Lu-177", "Therapy", "Antigen", "PSMA (β-RLT)", "mCRPC radioligand therapy", "lu177-psma-617"],
 ["²²³Ra-dichloride", "Ra-223", "Therapy", "Bone", "Ca-mimetic bone-seeking α", "Bone-metastatic prostate cancer", "ra223-dichloride"],
 ["¹³¹I-MIBG (therapy)", "I-131", "Therapy", "Transporter", "Norepinephrine transporter", "PPGL / neuroblastoma therapy", "i131-mibg"],
 ["⁹⁰Y-microspheres", "Y-90", "Therapy", "Embolic", "Arterial microembolisation (β)", "Hepatic radioembolisation", "y90-radioembolization"],
 ["¹⁵³Sm / ⁸⁹Sr", "Sm-153", "Therapy", "Bone", "Osteoblastic bone uptake (β)", "Bone-pain palliation", "bone-pain-palliation"],
 ["³²P-phosphate", "P-32", "Therapy", "Metabolism", "Phosphate incorporation (β)", "Polycythemia vera / ET; cavity therapy", "phosphorus-32-therapies"],
 ["²²⁵Ac-PSMA (TAT)", "Ac-225", "Therapy", "Antigen", "PSMA (α-emitter)", "Advanced prostate (investigational)", "targeted-alpha-therapy"],
]
_C_KEYS = ["n", "iso", "mod", "cls", "tgt", "use", "id"]
_comp = []
for _row in _COMPENDIUM:
    _d = dict(zip(_C_KEYS, _row))
    if _d["id"] not in raw_pages:   # never emit a link that would break navigation
        _d["id"] = ""
    _comp.append(_d)
compendium_json = json.dumps(_comp)

# ---- Personal layer: per-domain page lists (for progress tracking) ----
_ch_part = {ch: pt for ch, lbl, pt in CHAPTERS}
_dom = {}
for _p in pages:
    _pt = _ch_part.get(_p["chapter"])
    if _pt == "T":   # exclude the Tools utilities from reading progress
        continue
    _dom.setdefault(_pt, []).append(_p["id"])
domains_json = json.dumps([{"label": PART_LABEL[pt], "ids": _dom.get(pt, [])}
                           for pt in ["I", "II", "III", "IV", "V", "VI"]])

# ---- Glossary: curated, unambiguous abbreviations for inline hover-definitions ----
# Matched case-sensitively as whole words in body prose (first occurrence per page).
GLOSSARY = {
 "SUV": "Standardized uptake value — a semiquantitative measure of tracer concentration normalized to injected activity and body mass.",
 "PRRT": "Peptide receptor radionuclide therapy — radiolabeled somatostatin analogue therapy (e.g. ¹⁷⁷Lu-DOTATATE).",
 "SSTR": "Somatostatin receptor — target of DOTATATE imaging and therapy.",
 "PSMA": "Prostate-specific membrane antigen — cell-surface target for prostate cancer imaging and radioligand therapy.",
 "NIS": "Sodium-iodide symporter — the membrane transporter that concentrates iodide (and pertechnetate) in thyroid tissue.",
 "MIBG": "Metaiodobenzylguanidine — norepinephrine-transporter agent for pheochromocytoma/paraganglioma and neuroblastoma.",
 "FDG": "Fluorodeoxyglucose — ¹⁸F-labeled glucose analogue imaging glucose metabolism.",
 "NaF": "Sodium fluoride — ¹⁸F bone-metabolism PET tracer.",
 "MDP": "Methylene diphosphonate — ⁹⁹ᵐTc bone-scintigraphy agent.",
 "MAA": "Macroaggregated albumin — ⁹⁹ᵐTc lung-perfusion agent (capillary microembolisation).",
 "MAG3": "Mercaptoacetyltriglycine — ⁹⁹ᵐTc renal tubular agent.",
 "DTPA": "Diethylenetriaminepentaacetic acid — ⁹⁹ᵐTc agent for GFR/renal and aerosol ventilation.",
 "HIDA": "Hepatobiliary iminodiacetic acid — cholescintigraphy agent (hepatocyte uptake, biliary excretion).",
 "HMPAO": "Hexamethylpropyleneamine oxime — ⁹⁹ᵐTc lipophilic brain-perfusion and leukocyte-labelling agent.",
 "DAT": "Dopamine transporter — presynaptic target of ¹²³I-ioflupane (DaTscan).",
 "PET": "Positron emission tomography.",
 "SPECT": "Single-photon emission computed tomography.",
 "MPI": "Myocardial perfusion imaging.",
 "LVEF": "Left ventricular ejection fraction.",
 "CTEPH": "Chronic thromboembolic pulmonary hypertension.",
 "NET": "Neuroendocrine tumour.",
 "PPGL": "Pheochromocytoma and paraganglioma.",
 "MTC": "Medullary thyroid carcinoma.",
 "mCRPC": "Metastatic castration-resistant prostate cancer.",
 "RLT": "Radioligand therapy.",
 "TAT": "Targeted alpha therapy.",
 "LET": "Linear energy transfer — ionisation density along a particle track (high for alpha, low for beta/gamma).",
 "MIRD": "Medical Internal Radiation Dose — the schema/formalism for internal dosimetry.",
 "LSF": "Lung shunt fraction — fraction of hepatic-artery flow reaching the lungs (Y-90 planning).",
 "ATTR": "Transthyretin amyloidosis — the cardiac amyloid subtype imaged with ⁹⁹ᵐTc-PYP.",
 "DLB": "Dementia with Lewy bodies.",
 "FTD": "Frontotemporal dementia.",
 "AADC": "Aromatic L-amino acid decarboxylase — enzyme of the catecholamine pathway (FDOPA).",
 "FES": "Fluoroestradiol — ¹⁸F estrogen-receptor PET tracer.",
 "FAPI": "Fibroblast activation protein inhibitor — pan-tumour/fibrosis PET tracer class.",
 "PERCIST": "PET Response Criteria in Solid Tumours.",
 "SNMMI": "Society of Nuclear Medicine and Molecular Imaging.",
 "EANM": "European Association of Nuclear Medicine.",
 "GFR": "Glomerular filtration rate.",
 # ---- quantitation & cardiac ----
 "SUL": "SUV normalized to lean body mass — the metric PERCIST uses for metabolic response.",
 "TID": "Transient ischemic dilation — an enlarged post-stress LV cavity suggesting severe or balanced CAD.",
 "SSS": "Summed stress score — total perfusion-defect burden at stress (ischemia + infarct).",
 "SRS": "Summed rest score — fixed (scar) perfusion-defect burden at rest.",
 "SDS": "Summed difference score (SSS − SRS) — the reversible, ischemic burden.",
 "MBF": "Myocardial blood flow — absolute perfusion (mL/g/min) quantified on cardiac PET.",
 "MFR": "Myocardial flow reserve — stress ÷ rest MBF; a low reserve flags balanced or microvascular disease.",
 "CFR": "Coronary flow reserve — the ratio of hyperemic to resting coronary flow.",
 "HFpEF": "Heart failure with preserved ejection fraction.",
 "CRT": "Cardiac resynchronization therapy — biventricular pacing for dyssynchronous heart failure.",
 "ECV": "Extracellular volume — a cardiac-MRI measure elevated in infiltrative disease (e.g. amyloid).",
 "LGE": "Late gadolinium enhancement — a cardiac-MRI marker of fibrosis or infiltration.",
 "CAC": "Coronary artery calcium — a cardiovascular-risk marker visible even on non-gated CT.",
 "CTRCD": "Cancer-therapy-related cardiac dysfunction — the target of cardio-oncology surveillance.",
 "GLS": "Global longitudinal strain — an echocardiographic marker of subclinical LV dysfunction.",
 "INOCA": "Ischemia with non-obstructive coronary arteries.",
 "ANOCA": "Angina with non-obstructive coronary arteries.",
 "H/M": "Heart-to-mediastinum ratio — the key cardiac ¹²³I-MIBG innervation metric.",
 # ---- physics & instrumentation ----
 "TOF": "Time-of-flight — using photon arrival-time differences to localize PET events, improving signal-to-noise.",
 "OSEM": "Ordered-subset expectation maximization — the standard iterative reconstruction algorithm.",
 "PSF": "Point-spread function — the system's blur; PSF modeling recovers spatial resolution.",
 "NECR": "Noise-equivalent count rate — a PET count-rate performance metric.",
 "PVE": "Partial-volume effect — activity underestimation in objects near or below the scanner's resolution.",
 "FWHM": "Full width at half maximum — a measure of spatial resolution.",
 "CZT": "Cadmium-zinc-telluride — a solid-state detector used in modern SPECT cameras.",
 "ROC": "Receiver operating characteristic — a threshold-independent measure of diagnostic performance.",
 "NPV": "Negative predictive value — the probability disease is absent given a negative test.",
 "PPV": "Positive predictive value — the probability disease is present given a positive test.",
 "HVL": "Half-value layer — the thickness of material that halves a beam's intensity.",
 "RBE": "Relative biological effectiveness — biological damage per unit dose relative to a reference radiation.",
 "EARL": "EANM Research Ltd — the European PET/CT harmonization and accreditation program.",
 "Gy": "Gray — the SI unit of absorbed radiation dose (joules per kilogram).",
 "Sv": "Sievert — the SI unit of equivalent and effective (biological) dose.",
 "Bq": "Becquerel — the SI unit of radioactivity (one decay per second).",
 "Ci": "Curie — the traditional unit of radioactivity (3.7 × 10¹⁰ Bq).",
 "keV": "Kiloelectron-volt — a unit of photon or particle energy.",
 # ---- dosimetry, safety & regulatory ----
 "BED": "Biologically effective dose — absorbed dose adjusted for fractionation and dose-rate effects.",
 "ALARA": "As Low As Reasonably Achievable — the guiding principle of radiation protection.",
 "NRC": "Nuclear Regulatory Commission — the US regulator of byproduct radioactive material.",
 "ICRP": "International Commission on Radiological Protection.",
 "AU": "Authorized user — a physician credentialed to administer radiopharmaceutical therapy.",
 "BUD": "Beyond-use date — the date/time after which a compounded preparation must not be used.",
 "USP": "United States Pharmacopeia — sets compounding standards (chapters ⟨795⟩ / ⟨797⟩ / ⟨825⟩).",
 "PEC": "Primary engineering control — the device (e.g. a hood) providing an aseptic work environment.",
 # ---- therapy & theranostics ----
 "ARPI": "Androgen-receptor pathway inhibitor (e.g. abiraterone, enzalutamide).",
 "mHSPC": "Metastatic hormone-sensitive prostate cancer.",
 "RIT": "Radioimmunotherapy — a radionuclide conjugated to a tumor-targeting antibody.",
 "SIRT": "Selective internal radiation therapy — hepatic ⁹⁰Y radioembolization.",
 "TARE": "Transarterial radioembolization — ⁹⁰Y-microsphere therapy of liver tumors.",
 "TACE": "Transarterial chemoembolization — a catheter-based, non-radionuclide liver therapy.",
 "MTD": "Maximum tolerated dose.",
 # ---- oncology & disease ----
 "GEP-NET": "Gastroenteropancreatic neuroendocrine tumor.",
 "TTR": "Transthyretin — the protein that misfolds in ATTR cardiac amyloidosis.",
 "HGSC": "High-grade serous carcinoma — the dominant ovarian, tubal, and peritoneal cancer.",
 "CTPA": "CT pulmonary angiography — the contrast-CT test for pulmonary embolism.",
 "VTE": "Venous thromboembolism (DVT plus PE).",
 "DVT": "Deep vein thrombosis.",
 "NSCLC": "Non-small-cell lung cancer.",
 "SCLC": "Small-cell lung cancer — a high-grade neuroendocrine carcinoma.",
 "PD-L1": "Programmed death-ligand 1 — expression helps guide immunotherapy.",
 "MSI": "Microsatellite instability — predicts immunotherapy benefit; linked to mismatch-repair deficiency.",
 "dMMR": "Deficient mismatch repair — the basis of MSI-high tumors.",
 "CEA": "Carcinoembryonic antigen — a serum marker; a rising CEA is a key FDG-PET indication in colorectal cancer.",
 "CA-125": "Cancer antigen 125 — an ovarian-cancer serum marker followed for recurrence.",
 "FIGO": "The gynecologic-cancer staging system (Fédération Internationale de Gynécologie et d'Obstétrique).",
 "TNM": "Tumor–Node–Metastasis cancer staging.",
 "EUS": "Endoscopic ultrasound — the tool for local T-staging of esophagogastric cancer.",
 "NI-RADS": "Neck Imaging Reporting and Data System — post-treatment head-and-neck surveillance categories.",
 "RECIST": "Response Evaluation Criteria in Solid Tumors — anatomic, size-based response.",
 "iRECIST": "Immune-adapted RECIST — accounts for pseudoprogression on immunotherapy.",
 "HCC": "Hepatocellular carcinoma.",
 "RCC": "Renal cell carcinoma.",
 "GIST": "Gastrointestinal stromal tumor.",
 "MEN": "Multiple endocrine neoplasia — hereditary syndromes with endocrine tumors.",
 "Ki-67": "A proliferation index used to grade neuroendocrine (and other) tumors.",
 # ---- clinical & tracers ----
 "CCK": "Cholecystokinin — stimulates gallbladder contraction during hepatobiliary imaging.",
 "GBEF": "Gallbladder ejection fraction — the fraction of bile expelled after CCK; normal ≥ ~35–38%.",
 "RAIU": "Radioactive iodine uptake — the fraction of administered iodine trapped by the thyroid.",
 "DMSA": "Dimercaptosuccinic acid — a ⁹⁹ᵐTc renal cortical agent for scarring and relative function.",
 "FDOPA": "6-[¹⁸F]fluoro-L-DOPA — a catecholamine-pathway PET tracer (NET, PPGL, parkinsonism).",
 "FLT": "¹⁸F-fluorothymidine — a cell-proliferation PET tracer.",
}
glossary_json = json.dumps(GLOSSARY)

TEMPLATE = '''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Nuclear Medicine Atlas</title>
<meta name="description" content="An evidence-graded, physician-reviewed nuclear medicine reference — every major tracer, protocol, disease, and therapy, organized by the causal arc of a study, with interactive decision tools and a study mode.">
<meta name="author" content="Nuclear Medicine Atlas">
<meta name="theme-color" content="#4A3A82">
__HEADEXTRA__
<meta property="og:type" content="website">
<meta property="og:title" content="Nuclear Medicine Atlas">
<meta property="og:description" content="The evidence-graded reference for nuclear medicine — tracers, protocols, diseases, therapies, patterns, and interactive tools.">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Nuclear Medicine Atlas">
<meta name="twitter:description" content="The evidence-graded reference for nuclear medicine.">
<link rel="canonical" href="https://nuc.med/"><script>if(/[.]nuc[.]med$/.test(location.hostname))location.replace('https://nuc.med/'+location.hash)</script>
<meta property="og:url" content="__SITEURL__">
<meta name="robots" content="index,follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Inter:wght@400;450;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
__CSS__</style></head><body>
<noscript><div style="max-width:660px;margin:20px auto 0;padding:14px 18px;border:1px solid #E2E5E9;border-radius:10px;background:#FFF;font-family:-apple-system,system-ui,sans-serif;line-height:1.55;color:#14171B;font-size:14px">
<b>You're reading without JavaScript</b> — likely an iPhone/iPad preview (Files, Mail, or an in-app viewer). You can still <b>browse every page</b>: tap a chapter or card below. For the interactive extras — search, calculators, study mode — open this file in <b>Safari</b> (save to Files, then open it from Safari), or visit it once it's hosted online.
</div></noscript>
<a href="#main" class="skip-link">Skip to content</a>
<div class="app">
 <nav class="rail" aria-label="Atlas navigation">
  <div class="brand" onclick="go(FIRST)" role="button" tabindex="0" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();go(FIRST);}"><svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="var(--ac)"/><ellipse cx="32" cy="32" rx="21" ry="10.5" fill="none" stroke="#fff" stroke-width="3.2" transform="rotate(-28 32 32)"/><circle cx="32" cy="32" r="6.5" fill="#fff"/><circle cx="50" cy="21.5" r="3.6" fill="var(--ac-l)"/></svg><div class="brand-txt"><div class="k">Clinical Reference</div><h1>Nuclear Medicine Atlas</h1></div></div>
  <div class="sb"><span class="mag" aria-hidden="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></span>
   <input id="q" placeholder="Search all text…  ( / )" autocomplete="off" oninput="search(this.value)" onfocus="search(this.value)">
   <div class="sr" id="sr"></div></div>
  <button class="navtoggle" onclick="toggleNav()" aria-expanded="false" aria-controls="nav">&#9776;&nbsp; Menu &amp; chapters</button>
  <div class="modebar"><button id="hybtn" class="hybtn" onclick="toggleHY()" title="Collapse every page to key points only">High-yield</button><button id="stbtn" class="hybtn" onclick="openStudy()" title="Quiz yourself on every self-check">Study</button><button class="hybtn" onclick="openMyAtlas()" title="Bookmarks, reading progress & recently viewed">My Atlas</button><button class="hybtn" onclick="openIndex()" title="Browse every entry alphabetically">A–Z Index</button><button id="themebtn" class="hybtn" onclick="toggleTheme()" title="Toggle light / dark theme">Dark</button></div>
  <div id="nav">__NAV__</div>
 </nav>
 <main class="main" id="main">
  __PAGES__
  <p class="legend" id="legend"><b>Evidence grades.</b> <span class="gr gA">A</span> randomized trial or meta-analysis of randomized trials. <span class="gr gB">B</span> large cohort (roughly &gt;400 patients) or a society guideline / procedure standard. <span class="gr gC">C</span> smaller or confounded cohort, or physiologic reasoning without outcome data. <span class="gr gI">INF</span> is not a grade — it marks a conclusion drawn by reasoning where no study addresses the question directly.<br><br>
  <b>Emphasis reflects yield.</b> <span style="color:var(--ac);font-weight:700">KEY POINT</span> callouts and <b>bold text</b> are the highest-yield must-knows; standard text is core detail; smaller grey text is deeper reference detail — so the essentials stay prominent as pages go deep.<br><br>
  <b>Structure.</b> The atlas is organized to follow the causal arc of a nuclear medicine study: <b>Foundations</b> (how the signal is made), <b>Probes &amp; Targets</b> (what carries it), <b>Clinical Systems</b> (what it reveals), <b>Therapy &amp; Theranostics</b> (how it treats), <b>Interpretation &amp; Reasoning</b> (how we read it), and <b>Dosimetry, Safety &amp; Evidence</b> (how we quantify, protect and verify), with the fastest-changing content grouped last so the stable core rarely moves. <b>Scope.</b> A reference compiled from public, primary literature and society guidelines in original prose; it supports but does not replace clinical judgement, local protocol, or a written directive.</p>
  <div class="appfoot"><span>Nuclear Medicine Atlas &middot; <b>v__VERSION__</b> &middot; built __BUILD_DATE__</span><span>Evidence-graded &middot; <a class="foot-link" onclick="toggleHelp()">&#9000; Shortcuts (?)</a></span></div>
 </main>
</div>
<script>
__JS__
</script>
<div class="pager"><button id="pgp" onclick="step(-1)" title="Previous (←)">‹ Prev</button><button id="pgn" onclick="step(1)" title="Next (→)">Next ›</button></div>
<div id="toc" class="toc"></div>
<div id="lightbox" class="lb-ov" onclick="closeLightbox()"><div class="lb-inner"><button class="study-x" onclick="closeLightbox()" title="Close (Esc)">×</button><div class="lb-media"></div><div class="lb-cap"></div></div></div>
<div id="study" class="study-ov" onclick="if(event.target===this)closeStudy()"><div class="study-box"><button class="study-x" onclick="closeStudy()" title="Close (Esc)">×</button><div id="study-body"></div></div></div>
<div id="myatlas" class="study-ov" onclick="if(event.target===this)closeMyAtlas()"><div class="study-box"><button class="study-x" onclick="closeMyAtlas()" title="Close (Esc)">×</button><div id="myatlas-body"></div></div></div>
<div id="index-ov" class="study-ov" onclick="if(event.target===this)closeIndex()"><div class="study-box idx-box"><button class="study-x" onclick="closeIndex()" title="Close (Esc)">×</button><h2 id="idx-h">A&ndash;Z Index</h2><input id="idx-q" class="cmp-search" placeholder="Filter the index&hellip;" oninput="renderIndex(this.value)" autocomplete="off"><div class="idx-jump" id="idx-jump"></div><div class="idx-count" id="idx-count"></div><div class="idx-list" id="idx-list"></div></div></div>
<div id="palette" class="pal-ov" onclick="if(event.target===this)closePalette()"><div class="pal-box"><input id="pal-q" class="pal-in" placeholder="Jump to a page or run a command&hellip;" oninput="renderPalette(this.value)" autocomplete="off" spellcheck="false"><div class="pal-list" id="pal-list"></div><div class="pal-foot"><span><kbd>&uarr;</kbd><kbd>&darr;</kbd> move</span><span><kbd>&crarr;</kbd> select</span><span><kbd>Esc</kbd> close</span></div></div></div>
<div id="help" class="help-ov" onclick="if(event.target===this)closeHelp()"><div class="help-box"><button class="study-x" onclick="closeHelp()" title="Close (Esc)">×</button><h2>Keyboard shortcuts</h2><table class="help-tbl"><tr><td><kbd>&#8984;K</kbd> <kbd>Ctrl-K</kbd></td><td>Command palette (jump / actions)</td></tr><tr><td><kbd>/</kbd></td><td>Focus search</td></tr><tr><td><kbd>&uarr;</kbd> <kbd>&darr;</kbd></td><td>Move through search results</td></tr><tr><td><kbd>Enter</kbd></td><td>Open selected result</td></tr><tr><td><kbd>&larr;</kbd> <kbd>&rarr;</kbd></td><td>Previous / next page</td></tr><tr><td><kbd>Space</kbd></td><td>Reveal answer (Study mode)</td></tr><tr><td><kbd>1</kbd> <kbd>2</kbd></td><td>Missed / Got it (Study mode)</td></tr><tr><td><kbd>?</kbd></td><td>This help</td></tr><tr><td><kbd>Esc</kbd></td><td>Close panels / clear</td></tr></table></div></div>
</body></html>'''

# ---- PWA: inline icon + data-URI manifest, app-capable meta, no-flash theme init ----
_url = _url0
_ICON_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
             "<rect width='64' height='64' rx='14' fill='#4A3A82'/>"
             "<ellipse cx='32' cy='32' rx='21' ry='10.5' fill='none' stroke='#fff' stroke-width='3.2' transform='rotate(-28 32 32)'/>"
             "<circle cx='32' cy='32' r='6.5' fill='#fff'/>"
             "<circle cx='50' cy='21.5' r='3.6' fill='#A896EC'/></svg>")
_ICON_URI = "data:image/svg+xml," + _url.quote(_ICON_SVG)
_MANIFEST = json.dumps({
    "name": "Nuclear Medicine Atlas", "short_name": "NM Atlas",
    "start_url": ".", "scope": ".", "display": "standalone",
    "background_color": "#F6F7F9", "theme_color": "#4A3A82",
    "description": "The evidence-graded reference for nuclear medicine.",
    "icons": [{"src": _ICON_URI, "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}],
}, separators=(",", ":"))
_MANIFEST_URI = "data:application/manifest+json," + _url.quote(_MANIFEST)
HEADEXTRA = (
    f'<link rel="icon" href="{_ICON_URI}">\n'
    f'<link rel="apple-touch-icon" href="{_ICON_URI}">\n'
    f'<link rel="manifest" href="{_MANIFEST_URI}">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
    '<meta name="apple-mobile-web-app-title" content="NM Atlas">\n'
    "<script>document.documentElement.className+=' js';(function(){try{var s=localStorage.getItem('nma-theme');"
    "var d=s?s==='dark':(window.matchMedia&&matchMedia('(prefers-color-scheme:dark)').matches);"
    "if(d)document.documentElement.setAttribute('data-theme','dark');}catch(e){}})();</script>"
)

out = (TEMPLATE.replace("__CSS__", CSS).replace("__JS__", JS)
       .replace("__HEADEXTRA__", HEADEXTRA)
       .replace("__NAV__", nav_html).replace("__PAGES__", pages_html)
       .replace("__INDEX__", search_index).replace("__ORDER__", page_order)
       .replace("__QUIZ__", quiz_index).replace("__COMPENDIUM__", compendium_json)
       .replace("__DOMAINS__", domains_json).replace("__GLOSSARY__", glossary_json)
       .replace("__VERSION__", VERSION).replace("__BUILD_DATE__", BUILD_DATE)
       .replace("__SITEURL__", SITE_URL).replace("__CONTACT__", CONTACT_EMAIL)
       .replace("__FIRST__", "home"))
open(OUT, "w", encoding="utf-8").write(out)

# ---- Deployment artifacts: robots.txt + sitemap.xml (SPA → single canonical URL) ----
# The atlas is a hash-routed single page: all content lives on one indexable URL, so the
# sitemap lists that origin. (Per-URL indexing would require server-rendered routes.)
open(os.path.join(_ROOT, "robots.txt"), "w", encoding="utf-8").write(
    f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
open(os.path.join(_ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f'  <url><loc>{SITE_URL}/</loc><lastmod>{BUILD_DATE}</lastmod>'
    '<changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
    '</urlset>\n')

covered = sum(1 for p in pages if p["id"] in EVIDENCE)
print(f"Wrote {OUT}: {len(pages)} pages across {len({p['chapter'] for p in pages})} chapters, "
      f"{covered} with graded evidence, {len(out)} bytes")
