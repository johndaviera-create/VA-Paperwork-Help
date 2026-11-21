#!/usr/bin/env python3
"""Illustrative 38 CFR 4.25 VA combined-rating arithmetic (NON-BILATERAL only).

Never input predicted/unawarded percentages as if awarded. This helper intentionally
refuses bilateral cases: 38 CFR 4.26 including subsection (d) needs review.
Reconfirm current rule and table before use. This is not a VA determination.
"""

from argparse import ArgumentParser
from decimal import Decimal, ROUND_HALF_UP


def half_up(number: Decimal) -> int:
    return int(number.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def combine_non_bilateral(ratings: list[int]) -> dict:
    if not ratings:
        raise ValueError("Provide at least one awarded individual evaluation.")
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 or x > 100 or x % 10 != 0 for x in ratings):
        raise ValueError("Only integer percentages from 0 to 100 in tens are supported.")
    ordered = sorted(ratings, reverse=True)
    running = ordered[0]
    steps = []
    for rating in ordered[1:]:
        merged = half_up(Decimal(running) + (Decimal(100 - running) * Decimal(rating) / Decimal(100)))
        steps.append({"left": running, "right": rating, "combined": merged})
        running = merged
    final = min(100, (running + 5) // 10 * 10)
    return {"ordered": ordered, "steps": steps, "pre_rounding": running, "final": final,
            "note": "Illustrative only; §4.26 bilateral factor and other legal rules NOT included."}


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("ratings", type=int, nargs="+", help="already-awarded individual ratings, e.g. 60 40 20")
    parser.add_argument("--bilateral", action="store_true", help="flag possibility of bilateral-factor applicability; refuses to estimate")
    args = parser.parse_args()
    if args.bilateral:
        parser.error("Bilateral case: do not use this calculator. Review current 38 CFR 4.26, including (d), and VA table manually.")
    result = combine_non_bilateral(args.ratings)
    for s in result["steps"]:
        print(f'{s["left"]}% + {s["right"]}% -> {s["combined"]}% (table step)')
    print(f'Unrounded combined value: {result["pre_rounding"]}%')
    print(f'Combined evaluation after final rounding: {result["final"]}%')
    print(result["note"])


if __name__ == "__main__":
    main()
