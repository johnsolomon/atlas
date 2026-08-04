---
type: physics
title: Physics of Nuclear Medicine
chapter: physics
order: 10
subtitle: Decay modes, particle emissions, LET, and half-life, the basis of imaging and therapy
aliases: [physics, radioactive decay, alpha, beta, positron, gamma, LET, linear energy transfer, half-life, decay modes, electron capture, effective half-life, secular equilibrium, positron range]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "13 min"
tags: [physics, basic-principles, dosimetry]
related_tracers: []
related_protocols: []
related_diseases: []
related_calculators: [decay, effective-dose]
related_pitfalls: []
---

## Quick Answer

Radionuclides decay by emitting particles or photons whose properties determine whether an isotope is suited to **imaging** or **therapy**. Gamma and positron emitters (Tc-99m, F-18, Ga-68) are for **imaging** because their photons escape the body to a detector. Particle emitters — **beta (β⁻)** (Lu-177, Y-90, I-131) and **alpha (α)** (Ra-223, Ac-225) — deposit energy locally over millimeters or micrometers, which makes them **therapeutic**. **Linear energy transfer (LET)** and **half-life** are the two properties that most shape efficacy and radiation protection.

## Why Physics Matters Clinically

A therapy-capable nuclear-medicine physician explains *why* a given isotope is chosen and *how* its dose is delivered. **Decay mode** sets the imaging/therapy role; **LET** sets biological potency; **half-life** sets logistics, retained activity, and patient-release rules. These physical properties are the foundation of every theranostic decision.

## Radiation Quantities (Orientation)

- **Activity** — becquerel (Bq) / curie (Ci): decays per unit time.
- **Absorbed dose** — gray (Gy): energy per unit mass.
- **Equivalent dose** — sievert (Sv): absorbed dose weighted for radiation type (α weighted heavily).
- **Effective dose** — Sv: equivalent dose weighted by tissue radiosensitivity (compares whole-body stochastic risk).

## Decay Modes

| Mode | Emission | Role | Examples |
|---|---|---|---|
| Isomeric transition | γ photon | Imaging (SPECT) | Tc-99m (140 keV) |
| Positron (β⁺) | positron → 511 keV annihilation photons | Imaging (PET) | F-18, Ga-68, Rb-82 |
| Electron capture | characteristic X-rays / γ | Imaging (SPECT) | I-123, Tl-201, In-111 |
| Beta minus (β⁻) | electron | Therapy (± imageable γ) | Lu-177, Y-90, I-131 |
| Alpha (α) | helium nucleus | Therapy | Ra-223, Ac-225, Pb-212 |

## Particle Range & LET

- **Beta particles** travel **millimeters** (low-to-moderate LET), giving a useful **crossfire** effect across cell clusters — good for bulkier/heterogeneous disease. Lu-177 conveniently also emits an imageable γ (post-therapy SPECT/dosimetry).
- **Alpha particles** travel only a **few cell diameters (micrometers)** but carry very **high LET**, producing dense, clustered DNA double-strand breaks that are largely irreparable and relatively **independent of oxygenation and dose rate**. This makes alphas potent against micrometastatic/radioresistant disease, at the cost of harder dosimetry and **daughter-nuclide** concerns (e.g. Ac-225's recoiling progeny).

## Half-Life & Decay

Physical half-life governs how quickly activity decays: **A = A₀·e^(−0.693·t/t½)**. It sets pre-calibration/decay corrections and achievable protocols (Rb-82's 76-second half-life forces on-generator, pharmacologic-stress-only workflows). With biological clearance it yields the **effective half-life** that drives radiation dose and patient-release timing.

## Effective Half-Life — the Number That Governs Dose

Radiation dose and patient-release timing depend on the **effective** half-life, not the physical one alone:

**1/t½(eff) = 1/t½(physical) + 1/t½(biological)**

A tracer that is physically long-lived but rapidly excreted delivers **less** dose than its physical half-life suggests, and vice versa.

## Generator Equilibria (Preview)

Generators exploit parent→daughter decay: **transient equilibrium** (Mo-99 → Tc-99m; parent half-life somewhat longer than daughter) and **secular equilibrium** (very long-lived parent, e.g. Sr-82 → Rb-82 / Ge-68 → Ga-68). See the radiopharmaceuticals page for the practical elution logic.

## Positron Range & PET Resolution

A positron travels a short distance before annihilation — **positron range** blurs the reconstructed location, **larger for higher-energy emitters (Rb-82, Ga-68)** than for F-18 (one reason F-18 agents look sharper). The two 511-keV photons are also **not emitted at exactly 180°** (a small angular deviation), adding a further, scanner-diameter-dependent resolution limit.

## Choosing an Isotope — the Summary Logic

Imaging needs **escaping photons** (γ for SPECT, e.g. 140 keV for Tc-99m; positrons → 511 keV for PET); therapy needs **locally deposited particle energy** (β for mm-range crossfire, α for µm-range high-LET kill). Half-life sets logistics (generator vs cyclotron vs distribution) and, with biological clearance, dose to the patient and others. A single element can serve both ends of a **theranostic pair** when chemistry allows (Ga-68 image / Lu-177 treat on the same DOTA-conjugated ligand).

## Board Pearls

{K} Imaging isotopes must emit **escaping photons**; therapy isotopes must **deposit particle energy locally** — the same element can do both across a theranostic pair (e.g. Ga-68/Lu-177 on the same ligand). Radiation dose and patient-release timing depend on **effective half-life**, not physical half-life alone.

{H} **Alpha vs beta** is the crux of the modern therapy conversation: **alphas** are high-LET, micrometer-range, oxygen/dose-rate-independent (potent against micrometastases, harder dosimetry, daughter-nuclide concerns); **betas** are mm-range with crossfire for bulkier disease.

{D} **Positron range** blurs PET localization — larger for high-energy emitters (Rb-82, Ga-68) than F-18 — and the small non-180° annihilation-photon deviation adds a scanner-size-dependent limit. These physics set the resolution ceiling before any reconstruction choice. Effective half-life combines physical decay with biological clearance to determine actual dose.

## Related Pages

- Calculators: **decay** and **effective dose** tools.
- Related: **Radiopharmaceuticals & production**, **radiation detection & instrumentation**, **radiation biology & protection**.

## Figure / Diagram Suggestions

- A **decay-mode chart** mapping emission → imaging/therapy role.
- An **α vs β range/LET** comparison (µm high-LET vs mm crossfire).
- An **effective half-life** schematic (physical ⊕ biological clearance).

## Self-Check (Board-Style)

<details><summary><strong>Q1.</strong> Why are alpha emitters (e.g. Ac-225) attractive for micrometastatic disease despite harder dosimetry?</summary>
<p><strong>Answer:</strong> Their <strong>very high LET</strong> over a <strong>few-cell-diameter range</strong> produces dense, largely irreparable DNA double-strand breaks that are relatively <strong>independent of oxygenation and dose rate</strong> — potent against small, radioresistant deposits.</p>
</details>

<details><summary><strong>Q2.</strong> A radionuclide has a long physical half-life but is rapidly renally excreted. How does this affect patient dose?</summary>
<p><strong>Answer:</strong> Dose depends on the <strong>effective half-life</strong> (physical ⊕ biological clearance); rapid excretion shortens it, so the delivered dose is <strong>less</strong> than the physical half-life alone implies.</p>
</details>

<details><summary><strong>Q3.</strong> Why do F-18 PET images tend to look sharper than Ga-68 or Rb-82?</summary>
<p><strong>Answer:</strong> F-18's lower positron energy gives a <strong>shorter positron range</strong> (less blurring of the annihilation location) than higher-energy Ga-68/Rb-82.</p>
</details>

<details><summary><strong>Q4.</strong> What makes Lu-177 convenient for theranostics beyond its therapeutic beta?</summary>
<p><strong>Answer:</strong> It also emits an <strong>imageable gamma</strong>, enabling <strong>post-therapy SPECT and dosimetry</strong> on the same administration.</p>
</details>
