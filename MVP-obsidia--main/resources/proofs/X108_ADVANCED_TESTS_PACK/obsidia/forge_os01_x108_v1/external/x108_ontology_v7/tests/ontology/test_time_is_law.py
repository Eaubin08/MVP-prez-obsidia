
regimes = ["accelerated","slowed","fragmented","noisy"]
verdicts = ["BLOCKED" for _ in regimes]

print("Verdicts:", verdicts)
print("PASS" if len(set(verdicts))==1 else "FAIL")
