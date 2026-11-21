"""Public synthetic examples only; verify against current § 4.25 table."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from combined_rating import combine_non_bilateral


def test_official_examples():
    # Official § 4.25 examples: 60+30=72 -> 70; 50+30=65 -> 70;
    # 40+20=52 -> 50; 60+40+20=76 ->81 -> 80
    for numbers, pre, final in [
        ([60, 30], 72, 70),
        ([50, 30], 65, 70),
        ([40, 20], 52, 50),
        ([60, 40, 20], 81, 80),
        ([10, 10], 19, 20),
        ([0, 0], 0, 0),
        ([100, 10], 100, 100),
        ([10, 20, 30], 50, 50),
    ]:
        result = combine_non_bilateral(numbers)
        assert (result["pre_rounding"], result["final"]) == (pre, final), (numbers, result)


def test_reject_invalid():
    for invalid in [[], [5], [-10], [110], [True], ["30"]]:
        try:
            combine_non_bilateral(invalid)
            raise AssertionError(f"Accepted invalid {invalid!r}")
        except ValueError:
            pass


if __name__ == "__main__":
    test_official_examples()
    test_reject_invalid()
    print("PASS: 8 official/synthetic arithmetic cases and invalid-input checks")
