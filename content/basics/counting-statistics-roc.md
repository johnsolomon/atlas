---
type: physics
title: Counting Statistics, Error Propagation & ROC
chapter: physics
order: 30
subtitle: Poisson statistics, error propagation, the chi-square test, and diagnostic-performance analysis
aliases: [counting statistics, Poisson, standard deviation, error propagation, net counts, chi square, ROC, AUC, sensitivity, specificity, Bayes, dead time, minimum detectable activity]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "16 min"
tags: [physics, statistics, quantitation, basic-principles]
related_tracers: []
related_diseases: []
related_therapies: []
related_calculators: []
related_pitfalls: []
---

## Quick Answer

Radioactive decay is a **Poisson process**, so the standard deviation of a count **N** is **√N** and the fractional (percent) error is **1/√N**. Achieving 1% precision requires **10,000 counts**; 5% requires **400**. Errors **propagate** — variances add for sums/differences, fractional variances add for products/quotients — which governs **net-count** (signal-minus-background) uncertainty. The **chi-square** test checks system reproducibility, and **ROC/AUC** analysis compares diagnostic performance independent of any single threshold.

## Poisson Statistics — the Foundation

For a Poisson-distributed count **N**:

- **Standard deviation:** σ = **√N**
- **Fractional (relative) error:** σ/N = **1/√N**; percent error = **100/√N**
- 95% confidence ≈ N ± 1.96√N

| Counts N | σ = √N | % error (1/√N) |
|---|---|---|
| 100 | 10 | 10% |
| 400 | 20 | 5% |
| 1,000 | ~32 | ~3.2% |
| 10,000 | 100 | 1% |
| 1,000,000 | 1,000 | 0.1% |

The practical corollary: **precision improves only as the square root of counts** — a 10× improvement in precision needs **100×** the counts (or time). This is why low-count studies (delayed images, small ROIs, short frames) are inherently noisier.

## Error Propagation

- **Sum or difference** (A ± B): **add variances** → σ = √(σ²_A + σ²_B) = √(A + B) for counts.
- **Product or quotient** (A×B or A/B): **add fractional variances** (relative errors in quadrature) → (σ/R)² = (σ_A/A)² + (σ_B/B)².
- **Multiply by a constant k:** σ scales by k; fractional error unchanged.

### Worked: Net Counts (Signal − Background)

Net = Gross − Background. Because both are counts, the **variance of the net = Gross + Background** (not Gross − Background):

- Gross = 1,000; Background = 200 → **Net = 800**
- σ_net = √(1000 + 200) = √1200 ≈ **34.6**
- Fractional error = 34.6/800 = **4.3%**

Note the net count (800) has *more* relative uncertainty than the gross count alone — background subtraction always **increases** relative error, the reason high background (or low target-to-background) degrades quantitation.

## The Chi-Square Test (Reproducibility)

Repeated measurements of a constant source should vary only by Poisson statistics. **χ² = Σ(Nᵢ − N̄)² / N̄** over *n* measurements; the value is compared to tabulated ranges for (n−1) degrees of freedom. An **out-of-range χ²** indicates the system is varying **more (instability) or less (something suppressing normal variation)** than Poisson statistics allow — a QC red flag for camera/counter reproducibility.

## Dead Time & Count-Rate Losses

At high count rates, detectors miss events during the processing ("dead") time:

- **Nonparalyzable** model: measured rate saturates toward a maximum.
- **Paralyzable** model: measured rate **rises, peaks, then falls** at very high rates (each event extends the dead period) — dangerous because a very high true rate can read as a low one.
- Relevant to **first-pass**, **Rb-82 cardiac**, and high-activity therapy imaging; corrected by system dead-time models.

## Minimum Detectable Activity

The smallest signal distinguishable from background depends on background counts and counting time (e.g. Currie's L_D). Practically: **lower background and longer counting** lower the detection limit — the basis for wipe-test and contamination-survey sensitivity.

## Diagnostic Performance — Beyond a Single Threshold

| Measure | Definition |
|---|---|
| **Sensitivity (TPF)** | TP / (TP + FN) |
| **Specificity** | TN / (TN + FP) |
| **PPV** | TP / (TP + FP) — **prevalence-dependent** |
| **NPV** | TN / (TN + FN) — **prevalence-dependent** |
| **Accuracy** | (TP + TN) / total |

**PPV/NPV depend on prevalence** (Bayes): the same test performs differently in a screening vs a high-prevalence population — a normal MPI's high NPV (the "warranty period") reflects low pretest risk as much as test performance.

## ROC / AUC — Threshold-Independent Comparison

A **receiver-operating-characteristic (ROC)** curve plots **sensitivity (TPF)** vs **1 − specificity (FPF)** across all thresholds. The **area under the curve (AUC)** summarizes discrimination:

- **AUC 1.0** = perfect; **0.5** = chance (diagonal).
- ROC **compares observers, systems, or tracers independent of any single cutoff** — the standard method for imaging-performance studies (and for justifying a chosen operating threshold).

## Board-Level Synthesis

{K} Decay is **Poisson**: σ = **√N**, percent error = **1/√N** — so **10,000 counts = 1%**, **400 = 5%**, and precision improves only as the **square root** of counts (10× precision needs 100× counts). **Net-count** variance = **Gross + Background**, so background subtraction always raises relative error.

{H} **Error propagation:** add **variances** for sums/differences, add **fractional variances** for products/quotients. The **chi-square** test flags a system varying more (or less) than Poisson statistics allow — a reproducibility QC check.

{D} **PPV/NPV are prevalence-dependent** (Bayes) — the same sensitivity/specificity gives different predictive values across populations. **ROC/AUC** compares diagnostic performance **independent of threshold** (AUC 1.0 perfect, 0.5 chance), the correct way to compare tracers/observers/systems. At high count rates, **paralyzable dead time** can make a very high true rate read falsely low.

## Related Pages

- Physics: **Physics of nuclear medicine**, **radiation detection & instrumentation** (dead time, QC).
- Reference: **Quality control procedures** (chi-square/constancy in practice).

## Figure / Diagram Suggestions

- A **√N precision** curve (counts vs % error) with the 400/10,000 landmarks.
- A **net-count error** worked schematic (gross, background, propagated σ).
- An **ROC curve** with AUC and the sensitivity/specificity trade-off.

## Self-Check

<details><summary><strong>Q1.</strong> How many counts are needed for a 1% statistical error, and for 5%?</summary>
<p><strong>Answer:</strong> <strong>10,000 counts</strong> for 1% (1/√10000 = 1%) and <strong>400 counts</strong> for 5% (1/√400 = 5%).</p>
</details>

<details><summary><strong>Q2.</strong> Gross counts 900, background 100. What is the net count and its standard deviation?</summary>
<p><strong>Answer:</strong> Net = <strong>800</strong>; σ_net = √(900 + 100) = <strong>√1000 ≈ 31.6</strong> (≈ 4.0% error) — variance adds, so it is Gross + Background, not Gross − Background.</p>
</details>

<details><summary><strong>Q3.</strong> Why do PPV and NPV change between a screening and a high-prevalence population if sensitivity and specificity are unchanged?</summary>
<p><strong>Answer:</strong> PPV/NPV are <strong>prevalence-dependent (Bayes)</strong>; sensitivity/specificity are intrinsic to the test, but predictive values shift with pretest probability.</p>
</details>

<details><summary><strong>Q4.</strong> What does the area under an ROC curve represent, and what AUC indicates chance performance?</summary>
<p><strong>Answer:</strong> AUC is <strong>threshold-independent discrimination</strong> (probability of ranking a true positive above a true negative); <strong>AUC 0.5 = chance</strong>, 1.0 = perfect.</p>
</details>
