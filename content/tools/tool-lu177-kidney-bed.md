---
type: tool
title: Lu-177 PRRT Kidney BED Tracker
chapter: tools
order: 16
subtitle: Cumulative renal biologically-effective dose across PRRT cycles, with the tolerance thresholds and remaining headroom
aliases: [kidney BED, PRRT kidney dosimetry, biologically effective dose kidney, Lu-177 renal dose, cumulative kidney dose PRRT, 40 Gy 28 Gy kidney, renal tolerance PRRT, DOTATATE kidney BED]
tags: [tool, therapy, theranostics, dosimetry, safety]
---

Kidney **biologically effective dose (BED)** is the accepted way to track cumulative renal risk across PRRT cycles, because it accounts for **dose rate and sublethal-damage repair** rather than absorbed dose alone. For each administration, **BED = D · [1 + (D / (α/β)) · λ/(μ+λ)]**, with kidney **α/β ≈ 2.6 Gy**, repair half-time **≈ 2.8 h**, and λ from the **kidney effective half-life**; cycle BEDs are additive. Widely used tolerance thresholds are **~40 Gy BED** without renal risk factors and **~28 Gy** with them (hypertension, diabetes), against the classic **23 Gy** absorbed-dose TD₅/₅. Enter each cycle's kidney absorbed dose to track cumulative BED and remaining headroom.
