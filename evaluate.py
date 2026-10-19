"""Run every sample letter and print an accuracy report:  python evaluate.py

Precision = of the dates we reported, how many were right (few false alarms).
Recall    = of the dates we should have found, how many we found (few misses).
"""
from datetime import date

from extractor import analyze
from samples import CASES

TODAY = date(2026, 10, 9)   # fixed, so results never change from day to day


def found_dates(case):
    findings = analyze(case["text"], case["notice"], case["received"], today=TODAY)
    return {f.deadline for f in findings if f.deadline is not None}


def main():
    true_pos = false_pos = false_neg = 0
    graded = 0
    gaps = []

    for case in CASES:
        found = found_dates(case)
        expected = case["expected"]

        if case["known_gap"]:
            gaps.append((case["name"], found == expected))
            continue                          # known gaps are not counted in the scores

        graded += 1
        true_pos += len(found & expected)
        false_pos += len(found - expected)
        false_neg += len(expected - found)
        if found == expected:
            print(f"ok    {case['name']}")
        else:
            print(f"FAIL  {case['name']}")
            print(f"        expected {sorted(expected)}")
            print(f"        got      {sorted(found)}")

    reported = true_pos + false_pos
    wanted = true_pos + false_neg
    precision = true_pos / reported if reported else 1.0
    recall = true_pos / wanted if wanted else 1.0
    print(f"\n{graded} letters | precision {precision:.0%} | recall {recall:.0%}")

    print("\nKnown gaps:")
    for name, passes in gaps:
        print(f"  {'now passing' if passes else 'still failing'}  {name}")


if __name__ == "__main__":
    main()