
cost = 0
for t in range(200):
    cost += t

print("Cost:", cost)
print("PASS" if cost > 5000 else "FAIL")
