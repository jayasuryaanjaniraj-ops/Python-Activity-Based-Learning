"""
Test cases for Case Study 08 : Manufacturing Cost and Profitability Analysis
Run : python3 test_cases.py
"""

import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location(
    "sol", os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py"))
sol = importlib.util.module_from_spec(spec)

real_stdout = sys.stdout
sys.stdout = open(os.devnull, "w")
spec.loader.exec_module(sol)
sys.stdout.close()
sys.stdout = real_stdout

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        passed = passed + 1
        print("  PASS : " + name)
    else:
        failed = failed + 1
        print("  FAIL : " + name)


def close(a, b, tol=0.02):
    return abs(a - b) < tol


def batch_of(batch_no):
    for batch in sol.BATCHES:
        if batch[0] == batch_no:
            return batch
    return None


print("Running test cases for Case Study 08 - Manufacturing Cost and Profitability")
print("-" * 74)

# result layout :
# 0 batch_no, 1 code, 2 name, 3 units, 4 price, 5 wastage_kg,
# 6 material, 7 labour, 8 machine, 9 prime, 10 overhead, 11 total,
# 12 cost/unit, 13 revenue, 14 profit, 15 margin, 16 status

# TC-01 product lookup
name, price = sol.product_of("FG-103")
check("TC-01 FG-103 is the MS clamp costing 36.00",
      name == "MS clamp" and close(price, 36.00))

# TC-02 unknown product code
name, price = sol.product_of("FG-999")
check("TC-02 unknown product returns None and 0", name is None and close(price, 0.0))

r = sol.batch_cost(batch_of("B-2601"))

# TC-03 wastage in kilograms
check("TC-03 wastage of 6% on 480 kg is 28.8 kg", close(r[5], 28.80))

# TC-04 material cost uses the usable material only
check("TC-04 material cost = (480 - 28.8) x 62 = 27974.40", close(r[6], 27974.40))

# TC-05 labour cost
check("TC-05 labour cost = 96 x 220 = 21120.00", close(r[7], 21120.00))

# TC-06 machine cost
check("TC-06 machine cost = 34 x 480 = 16320.00", close(r[8], 16320.00))

# TC-07 prime cost
check("TC-07 prime cost = 27974.40 + 21120 + 16320 = 65414.40", close(r[9], 65414.40))

# TC-08 overhead at 12%
check("TC-08 overhead = 12% of 65414.40 = 7849.73", close(r[10], 7849.73))

# TC-09 total cost
check("TC-09 total cost = 73264.13", close(r[11], 73264.13))

# TC-10 cost per unit
check("TC-10 cost per unit = 73264.13 / 1200 = 61.05", close(r[12], 61.05))

# TC-11 revenue
check("TC-11 revenue = 1200 x 78 = 93600.00", close(r[13], 93600.00))

# TC-12 profit
check("TC-12 profit = 93600 - 73264.13 = 20335.87", close(r[14], 20335.87))

# TC-13 margin
check("TC-13 margin is 21.7%", close(r[15], 21.72, 0.05))

# TC-14 status of a good batch
check("TC-14 B-2601 meets the target", r[16] == "MEETS TARGET")

# TC-15 a batch with too much wastage is rejected
r2 = sol.batch_cost(batch_of("B-2604"))
check("TC-15 B-2604 is rejected for 15% wastage",
      r2[16].startswith("REJECTED"))

# TC-16 a loss making batch is reported
r3 = sol.batch_cost(batch_of("B-2605"))
check("TC-16 B-2605 is loss making", r3[16] == "LOSS MAKING" and r3[14] < 0)

# TC-17 a batch below the margin target
r4 = sol.batch_cost(batch_of("B-2602"))
check("TC-17 B-2602 is below the target with a 6.9% margin",
      r4[16] == "BELOW TARGET" and close(r4[15], 6.85, 0.05))

# TC-18 cost per unit for a small batch
check("TC-18 cost per unit of B-2604 is 259.42", close(r2[12], 259.42))

# TC-19 material is the largest cost head in every batch
material_is_largest = True
for batch in sol.BATCHES:
    res = sol.batch_cost(batch)
    if not (res[6] > res[7] and res[6] > res[8]):
        material_is_largest = False
check("TC-19 material is the largest cost in all 6 batches", material_is_largest)

# TC-20 total cost is prime cost plus overhead for every batch
ok = True
for batch in sol.BATCHES:
    res = sol.batch_cost(batch)
    if not close(res[11], res[9] + res[10]):
        ok = False
check("TC-20 total cost = prime cost + overhead everywhere", ok)

# TC-21 profit = revenue - total cost for every batch
ok = True
for batch in sol.BATCHES:
    res = sol.batch_cost(batch)
    if not close(res[14], res[13] - res[11]):
        ok = False
check("TC-21 profit = revenue - total cost everywhere", ok)

# TC-22 how many batches meet the target
meets = 0
for batch in sol.BATCHES:
    if sol.batch_cost(batch)[16] == "MEETS TARGET":
        meets = meets + 1
check("TC-22 exactly 3 batches meet the target", meets == 3)

# TC-23 factory level totals
total_cost = 0.0
total_revenue = 0.0
for batch in sol.BATCHES:
    res = sol.batch_cost(batch)
    total_cost = total_cost + res[11]
    total_revenue = total_revenue + res[13]
check("TC-23 total cost of all batches is 490014.78", close(total_cost, 490014.78))
check("TC-24 total sales value is 578400.00", close(total_revenue, 578400.00))
check("TC-25 overall factory profit is 88385.22", close(total_revenue - total_cost, 88385.22))

# TC-26 the second steel hinge batch has the best margin
best = sol.batch_cost(sol.BATCHES[0])
for batch in sol.BATCHES:
    res = sol.batch_cost(batch)
    if res[15] > best[15]:
        best = res
check("TC-26 best batch is B-2606 with a 25.5% margin",
      best[0] == "B-2606" and close(best[15], 25.48, 0.05))

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
