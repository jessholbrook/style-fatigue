"""Power analysis for the Study 1 primary contrast.

Primary confirmatory contrast: proportion of participants reporting a clear
style change in the exit survey (funnel item `noticed_style_change` = "Yes"),
variant arms vs. the control arm. The control arm's rate is the false-positive
detection baseline, which is why it exists.

Analytic two-proportion power (normal approximation, two-sided). Stdlib only.

    python power_analysis.py [--alpha 0.05] [--attrition 0.4]
"""

import argparse
import math
from pathlib import Path
from statistics import NormalDist

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "output" / "power_analysis.md"

# Control-arm "clear change" rates (false positives / demand characteristics)
P0_GRID = [0.10, 0.15, 0.20]
# Variant-arm detection rates worth being able to detect
P1_GRID = [0.30, 0.40, 0.50, 0.60]
POWER_GRID = [0.80, 0.90]


def n_per_group(p0: float, p1: float, alpha: float, power: float) -> int:
    """Two-proportion z-test sample size per group (Fleiss, no continuity corr.)."""
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)
    p_bar = (p0 + p1) / 2
    numerator = (
        z_a * math.sqrt(2 * p_bar * (1 - p_bar))
        + z_b * math.sqrt(p0 * (1 - p0) + p1 * (1 - p1))
    ) ** 2
    return math.ceil(numerator / (p1 - p0) ** 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument(
        "--attrition",
        type=float,
        default=0.4,
        help="expected dropout across 4-6 sessions over ~2 weeks (0.4 = 40%%)",
    )
    args = parser.parse_args()

    lines = [
        "# Power Analysis — Study 1 primary contrast",
        "",
        "Contrast: exit-survey clear-change detection rate, variant arm vs control arm.",
        f"Two-sided alpha = {args.alpha}; completer Ns inflated by "
        f"{args.attrition:.0%} expected attrition for enrollment targets.",
        "",
        "Arms are enrolled 1:1:1 (control : variant_a : variant_b). 'N/arm' is",
        "completers per arm; 'Enroll total' covers all three arms with attrition.",
        "",
    ]

    for power in POWER_GRID:
        lines.append(f"\n## Power = {power:.0%}\n")
        lines.append("| Control rate p0 | Variant rate p1 | N/arm (completers) | Enroll total (3 arms) |")
        lines.append("|---|---|---|---|")
        for p0 in P0_GRID:
            for p1 in P1_GRID:
                if p1 <= p0:
                    continue
                n = n_per_group(p0, p1, args.alpha, power)
                enroll = math.ceil(3 * n / (1 - args.attrition))
                lines.append(f"| {p0:.2f} | {p1:.2f} | {n} | {enroll} |")

    lines += [
        "",
        "## Notes",
        "",
        "- If the two variant arms are pooled for the primary contrast (variant vs",
        "  control), the variant group has 2n completers and power is higher than",
        "  tabled; the table is conservative.",
        "- Habituation-trajectory analyses (noticeability slopes, mixed models over",
        "  sessions) generally need fewer participants than the detection contrast",
        "  because each participant contributes 4-6 observations.",
        "- Study 1 is exploratory: these numbers size the design, they are not a",
        "  pre-registered commitment.",
        "- Rates below p0=0.10 or shifts smaller than +0.15 are likely unrealistic",
        "  to power in a first study; treat those cells as Study 2 territory.",
    ]

    output = "\n".join(lines)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(output + "\n")
    print(output)
    print(f"\nWrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
