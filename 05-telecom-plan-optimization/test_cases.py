"""
Test cases for Case Study 05 : Multi-Plan Telecommunications Cost Optimization
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


def plan_by_name(name):
    for plan in sol.PLANS:
        if plan[0] == name:
            return plan
    return None


print("Running test cases for Case Study 05 - Telecom Plan Cost Optimization")
print("-" * 74)

# result layout :
# [name, price, days, excess_data, excess_calls, excess_sms,
#  excess_amount, total, eligible, within_budget, reason]

# TC-01 a plan with short validity is not eligible
r = sol.evaluate_plan(plan_by_name("Smart Saver 149"))
check("TC-01 Smart Saver 149 is rejected for a 28 day validity",
      r[8] is False and "validity" in r[10])

# TC-02 excess data is computed correctly
check("TC-02 1.4 GB excess data on the 1 GB plan", close(r[3], 1.4))

# TC-03 excess calls are computed correctly
check("TC-03 320 excess minutes on the 300 minute plan", r[4] == 320)

# TC-04 excess sms are computed correctly
check("TC-04 80 excess sms on the 100 sms plan", r[5] == 80)

# TC-05 excess amount adds up all three components
expected = 1.4 * sol.EXCESS_DATA_RATE + 320 * sol.EXCESS_CALL_RATE + 80 * sol.EXCESS_SMS_RATE
check("TC-05 excess amount is 281.20", close(r[6], expected) and close(r[6], 281.20))

# TC-06 total = price + excess
check("TC-06 total of Smart Saver 149 is 430.20",
      close(r[7], 149 + 281.20))

# TC-07 a plan that fully covers the usage has zero excess
r = sol.evaluate_plan(plan_by_name("Super 699"))
check("TC-07 Super 699 has no excess charges at all",
      close(r[6], 0.0) and r[3] == 0.0 and r[4] == 0 and r[5] == 0)

# TC-08 total equals the price when there is no excess
check("TC-08 total of Super 699 equals its price 699.00", close(r[7], 699.00))

# TC-09 feasible plan flag
check("TC-09 Super 699 is eligible", r[8] is True)

# TC-10 a plan whose total crosses the budget is rejected
r = sol.evaluate_plan(plan_by_name("Ultra 999"))
check("TC-10 Ultra 999 is rejected because of the budget",
      r[8] is False and "budget" in r[10])

# TC-11 equal validity exactly at the requirement is accepted
r = sol.evaluate_plan(plan_by_name("Quarterly 549"))
check("TC-11 exactly 84 days of validity is accepted", r[8] is True)

# TC-12 partial excess data on the quarterly plan
check("TC-12 0.4 GB excess on the quarterly plan = 7.20", close(r[6], 7.20))
check("TC-13 total of the quarterly plan is 556.20", close(r[7], 556.20))

# TC-14 the cheapest plan has more excess but a smaller total
combo = sol.evaluate_plan(plan_by_name("Combo 449"))
quarterly = sol.evaluate_plan(plan_by_name("Quarterly 549"))
check("TC-14 Combo 449 is cheaper than Quarterly 549 even with more excess",
      combo[6] > quarterly[6] and combo[7] < quarterly[7])

# TC-15 cheapest feasible plan of the whole table
feasible = []
for plan in sol.PLANS:
    res = sol.evaluate_plan(plan)
    if res[8]:
        feasible.append(res)
cheapest = feasible[0]
for res in feasible:
    if res[7] < cheapest[7]:
        cheapest = res
check("TC-15 cheapest feasible plan is Combo 449 at 541.20",
      cheapest[0] == "Combo 449" and close(cheapest[7], 541.20))

# TC-16 number of feasible plans
check("TC-16 exactly 3 of the 7 plans are feasible", len(feasible) == 3)

# TC-17 exactly 4 plans are rejected
rejected = 0
for plan in sol.PLANS:
    if sol.evaluate_plan(plan)[8] is False:
        rejected = rejected + 1
check("TC-17 exactly 4 of the 7 plans are rejected", rejected == 4)

# TC-18 a plan that covers everything but is outside the budget
check("TC-18 Ultra 999 covers all the usage but is over budget",
      close(sol.evaluate_plan(plan_by_name("Ultra 999"))[6], 0.0))

# TC-19 excess never becomes negative
negative = False
for plan in sol.PLANS:
    res = sol.evaluate_plan(plan)
    if res[3] < 0 or res[4] < 0 or res[5] < 0:
        negative = True
check("TC-19 no plan reports a negative excess", negative is False)

# TC-20 the cheapest feasible plan stays inside the budget
check("TC-20 the recommended plan leaves Rs.258.80 in the budget",
      close(sol.BUDGET - cheapest[7], 258.80))

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
