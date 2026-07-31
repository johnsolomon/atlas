---
type: physics
title: Radiation Interactions with Matter
chapter: physics
order: 20
subtitle: Photoelectric effect, Compton scatter, pair production, and attenuation
aliases: [photoelectric effect, Compton scatter, pair production, coherent scatter, Rayleigh, attenuation, linear attenuation coefficient, half-value layer, HVL, mass attenuation, photon interactions, scatter, shielding physics]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "10 min"
tags: [physics, basic-principles]
related_tracers: []
related_diseases: []
related_therapies: []
---

## Quick Answer

Photons interact with matter mainly by the **photoelectric effect** and **Compton scatter** (with **pair production** only above 1.022 MeV). The **photoelectric effect** — full absorption, probability ∝ **Z³/E³** — **dominates at low energy and in high-Z materials** (bone, iodine contrast, lead shielding) and is the basis of **attenuation contrast and gamma shielding**. **Compton scatter** — partial energy transfer to an outer electron — **dominates in soft tissue at the diagnostic/PET energies** (~140–511 keV) and is the source of **scattered photons that degrade images** (mitigated by energy windowing and scatter correction). Overall photon attenuation is **exponential** (μ, half-value layer), the physics behind **attenuation correction**.

## The Interactions

### Photoelectric Effect
An incident photon is **completely absorbed** by an inner-shell electron, which is ejected (photoelectron), followed by **characteristic X-rays / Auger electrons**. Probability rises steeply with **atomic number (∝ Z³)** and falls with **energy (∝ 1/E³)** — so it **dominates at low photon energies and in high-Z materials**. Consequences: **bone/contrast/lead attenuate strongly** (imaging contrast and **shielding**), and there is **no scattered photon** to degrade the image.

### Compton Scatter
The photon interacts with a loosely bound **outer-shell electron**, transferring **part** of its energy and **scattering** in a new direction (the recoil electron carries the rest). It is nearly **independent of Z** and depends on **electron density**, so it **dominates in soft tissue across ~30 keV–~20 MeV** — i.e., at **all common NM energies (140 and 511 keV)**. Consequences: **scattered photons are the main source of image degradation** (loss of contrast, mispositioned counts) — countered by **energy-window (photopeak) discrimination** and **scatter correction**.

### Pair Production
Above the **1.022 MeV** threshold, a photon near a nucleus converts to an **electron–positron pair**; the positron later annihilates into two 511-keV photons. It is **not relevant at diagnostic/PET imaging energies** but matters for **high-energy (therapy/linac)** contexts.

### Coherent (Rayleigh) Scatter
Elastic scatter with **no energy loss** and small-angle deflection — a **minor** contributor at NM energies.

## Attenuation

A photon beam is attenuated **exponentially**: **I = I₀ · e^(−μx)**, where **μ** is the **linear attenuation coefficient** (sum of the interaction probabilities). Useful quantities:

- **Half-Value Layer (HVL):** thickness reducing intensity by half; **HVL = 0.693/μ**.
- **Mass attenuation coefficient (μ/ρ):** normalizes for density, tabulated by material/energy.
- Attenuation is **energy- and material-dependent** — the basis of **CT-based attenuation maps** used to correct SPECT/PET.

## Why It Matters in Nuclear Medicine

- **Photopeak windowing** accepts primary photons and **rejects Compton-scattered** (lower-energy) photons.
- **Scatter correction** models and subtracts the Compton-scatter background (SPECT and PET).
- **Attenuation correction** uses the material-dependent μ map (CT) — patient tissue attenuates 140/511-keV photons, and uncorrected attenuation causes artifacts (e.g., inferior-wall cardiac defects).
- **Shielding** exploits the **photoelectric effect in high-Z lead** for gamma emitters (recall **beta** emitters need **low-Z first, then lead** to limit bremsstrahlung).
- **Collimation and detector stopping power** (high-Z NaI/BGO/LSO) likewise rely on photoelectric absorption of the photopeak.

## Common Pitfalls

- Assuming **photoelectric** dominates in tissue at NM energies — **Compton** does (140/511 keV in soft tissue).
- Forgetting **pair production** requires **>1.022 MeV** (irrelevant to diagnostic imaging).
- Ignoring **uncorrected attenuation** as an artifact source (e.g., cardiac inferior wall).
- Shielding **beta** sources with lead alone (bremsstrahlung) — a photoelectric-shielding rule that does not transfer to particles.

## Board Pearls

{K} Photons interact chiefly by the **photoelectric effect** (full absorption; probability **∝ Z³/E³**; dominates at **low energy / high-Z** — bone, contrast, **lead shielding**; no scatter) and **Compton scatter** (partial energy transfer to an outer electron; **∝ electron density, Z-independent**; **dominates in soft tissue at 140/511 keV**; the source of image-degrading scatter). **Pair production** needs **>1.022 MeV** and is irrelevant to diagnostic imaging.

{H} Overall attenuation is **exponential (I = I₀e^(−μx))**; **HVL = 0.693/μ**. Compton scatter is countered by **photopeak energy windowing** and **scatter correction**; tissue attenuation is corrected by the **CT-based μ map** (uncorrected attenuation → artifacts such as the inferior-wall cardiac defect).

{D} **Photoelectric absorption in high-Z materials** underlies **gamma shielding (lead)**, **collimator septa**, and **detector stopping power** (NaI/BGO/LSO). It is **energy-dependent** — the same lead is far more effective against low-energy photons. For **beta** emitters, shield **low-Z first then lead** (bremsstrahlung) — the photoelectric shielding logic applies to photons, not particles.

## Related Pages

- Physics: **Physics of nuclear medicine**, **radiation biology & protection**; instrumentation: **radiation detection & instrumentation**, **PET/SPECT performance & reconstruction** (scatter/attenuation correction).

## Figure / Diagram Suggestions

- An **interaction-vs-energy** dominance chart (photoelectric / Compton / pair production by energy and Z).
- A **photoelectric vs Compton** event cartoon (full absorption vs scatter).
- An **exponential attenuation / HVL** curve.

## Self-Check

<details><summary><strong>Q1.</strong> Which interaction dominates in soft tissue at 140 and 511 keV, and why does it matter?</summary>
<p><strong>Answer:</strong> <strong>Compton scatter</strong> — it produces the <strong>scattered photons that degrade images</strong>, countered by photopeak energy windowing and scatter correction.</p>
</details>

<details><summary><strong>Q2.</strong> How does the photoelectric effect depend on atomic number and energy, and where does it dominate?</summary>
<p><strong>Answer:</strong> Probability <strong>∝ Z³/E³</strong> — it dominates at <strong>low energy and in high-Z materials</strong> (bone, iodine contrast, lead shielding).</p>
</details>

<details><summary><strong>Q3.</strong> What is the energy threshold for pair production, and is it relevant to diagnostic NM?</summary>
<p><strong>Answer:</strong> <strong>1.022 MeV</strong> — <strong>not relevant</strong> at diagnostic/PET imaging energies (matters only for high-energy contexts).</p>
</details>

<details><summary><strong>Q4.</strong> Write the attenuation equation and the half-value-layer relationship.</summary>
<p><strong>Answer:</strong> <strong>I = I₀·e^(−μx)</strong>; <strong>HVL = 0.693/μ</strong> (thickness halving intensity).</p>
</details>
