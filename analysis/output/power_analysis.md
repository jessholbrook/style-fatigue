# Power Analysis — Study 1 primary contrast

Contrast: exit-survey clear-change detection rate, variant arm vs control arm.
Two-sided alpha = 0.05; completer Ns inflated by 40% expected attrition for enrollment targets.

Arms are enrolled 1:1:1 (control : variant_a : variant_b). 'N/arm' is
completers per arm; 'Enroll total' covers all three arms with attrition.


## Power = 80%

| Control rate p0 | Variant rate p1 | N/arm (completers) | Enroll total (3 arms) |
|---|---|---|---|
| 0.10 | 0.30 | 62 | 310 |
| 0.10 | 0.40 | 32 | 160 |
| 0.10 | 0.50 | 20 | 100 |
| 0.10 | 0.60 | 14 | 70 |
| 0.15 | 0.30 | 121 | 605 |
| 0.15 | 0.40 | 49 | 245 |
| 0.15 | 0.50 | 27 | 135 |
| 0.15 | 0.60 | 17 | 85 |
| 0.20 | 0.30 | 294 | 1470 |
| 0.20 | 0.40 | 82 | 410 |
| 0.20 | 0.50 | 39 | 195 |
| 0.20 | 0.60 | 23 | 115 |

## Power = 90%

| Control rate p0 | Variant rate p1 | N/arm (completers) | Enroll total (3 arms) |
|---|---|---|---|
| 0.10 | 0.30 | 82 | 410 |
| 0.10 | 0.40 | 42 | 210 |
| 0.10 | 0.50 | 26 | 130 |
| 0.10 | 0.60 | 17 | 85 |
| 0.15 | 0.30 | 161 | 805 |
| 0.15 | 0.40 | 65 | 325 |
| 0.15 | 0.50 | 36 | 180 |
| 0.15 | 0.60 | 23 | 115 |
| 0.20 | 0.30 | 392 | 1960 |
| 0.20 | 0.40 | 109 | 545 |
| 0.20 | 0.50 | 52 | 260 |
| 0.20 | 0.60 | 30 | 150 |

## Notes

- If the two variant arms are pooled for the primary contrast (variant vs
  control), the variant group has 2n completers and power is higher than
  tabled; the table is conservative.
- Habituation-trajectory analyses (noticeability slopes, mixed models over
  sessions) generally need fewer participants than the detection contrast
  because each participant contributes 4-6 observations.
- Study 1 is exploratory: these numbers size the design, they are not a
  pre-registered commitment.
- Rates below p0=0.10 or shifts smaller than +0.15 are likely unrealistic
  to power in a first study; treat those cells as Study 2 territory.
