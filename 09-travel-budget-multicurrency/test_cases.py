"""
Test cases for Case Study 09 : Multi-Currency Travel Budget Analysis
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


print("Running test cases for Case Study 09 - Multi-Currency Travel Budget Analysis")
print("-" * 74)

# TC-01 known exchange rate
check("TC-01 1 USD = 83.40", close(sol.rate_of("USD"), 83.40))

# TC-02 the rate of the rupee itself
check("TC-02 1 INR = 1.00", close(sol.rate_of("INR"), 1.00))

# TC-03 unknown currency
check("TC-03 unknown currency returns -1", sol.rate_of("JPY") < 0)

# TC-04 card payment conversion
value, fee, total = sol.convert_to_inr(100.0, "SGD", "card")
check("TC-04 100 SGD on card = 6180.00", close(value, 6180.00))
check("TC-05 card markup of 2% = 123.60", close(fee, 123.60))
check("TC-06 total on card = 6303.60", close(total, 6303.60))

# TC-07 cash withdrawal conversion
value, fee, total = sol.convert_to_inr(100.0, "SGD", "cash")
check("TC-07 cash conversion value is the same 6180.00", close(value, 6180.00))
check("TC-08 cash withdrawal fee is the flat 250", close(fee, 250.0))
check("TC-09 total for cash = 6430.00", close(total, 6430.00))

# TC-10 the money changer mode uses 1.5%
value, fee, total = sol.convert_to_inr(100.0, "SGD", "dealer")
check("TC-10 dealer fee of 1.5% = 92.70", close(fee, 92.70))
check("TC-11 total for the dealer mode = 6272.70", close(total, 6272.70))

# TC-12 an unknown currency gives a negative value
value, fee, total = sol.convert_to_inr(100.0, "JPY", "card")
check("TC-12 an unknown currency cannot be converted", value < 0)

# TC-13 Thai baht conversion
value, fee, total = sol.convert_to_inr(2850.0, "THB", "card")
check("TC-13 2850 THB = 6612.00", close(value, 6612.00))

# TC-14 Malaysian ringgit conversion
value, fee, total = sol.convert_to_inr(420.0, "MYR", "card")
check("TC-14 420 MYR = 7455.00", close(value, 7455.00))

# TC-15 euro conversion
value, fee, total = sol.convert_to_inr(38.0, "EUR", "card")
check("TC-15 38 EUR = 3425.70", close(value, 3425.70))

# TC-16 zero amount
value, fee, total = sol.convert_to_inr(0.0, "USD", "card")
check("TC-16 a zero expense costs nothing", close(value, 0.0) and close(fee, 0.0))

# TC-17 the whole trip total
grand = 0.0
fees = 0.0
for expense in sol.EXPENSES:
    v, f, t = sol.convert_to_inr(expense[2], expense[3], expense[4])
    grand = grand + t
    fees = fees + f
check("TC-17 total trip cost is 91936.72", close(grand, 91936.72))
check("TC-18 total fees are 3719.17", close(fees, 3719.17))

# TC-19 the trip is inside the budget
check("TC-19 the trip stays inside the 250000 budget",
      grand < sol.PLANNED_BUDGET_INR)
check("TC-20 money left is 158063.28",
      close(sol.PLANNED_BUDGET_INR - grand, 158063.28))

# TC-21 category totals
cats = {}
for expense in sol.EXPENSES:
    v, f, t = sol.convert_to_inr(expense[2], expense[3], expense[4])
    if expense[1] in cats:
        cats[expense[1]] = cats[expense[1]] + t
    else:
        cats[expense[1]] = t
check("TC-21 hotel total is 26325.18", close(cats["Hotel"], 26325.18))
check("TC-22 food total is 7354.90", close(cats["Food"], 7354.90))

# TC-23 largest category
largest = ""
amount = -1.0
for c in cats:
    if cats[c] > amount:
        amount = cats[c]
        largest = c
check("TC-23 the largest category is Hotel at 26325.18",
      largest == "Hotel" and close(amount, 26325.18))

# TC-24 the largest category is below the 40% warning share
check("TC-24 no category crosses the 40% warning share",
      amount / grand * 100.0 < sol.WARNING_SHARE_PERCENT)

# TC-25 cash withdrawals are costlier than the card markup
card = 0.0
cash = 0.0
for expense in sol.EXPENSES:
    v, f, t = sol.convert_to_inr(expense[2], expense[3], expense[4])
    if expense[4] == "card":
        card = card + f
    else:
        cash = cash + f
check("TC-25 cash fees 2250.00 are more than card markup 1469.17",
      close(cash, 2250.00) and close(card, 1469.17) and cash > card)

# TC-26 number of expense lines
check("TC-26 there are 18 expense lines", len(sol.EXPENSES) == 18)

# TC-27 every currency used in the trip has a rate
missing = 0
for expense in sol.EXPENSES:
    if sol.rate_of(expense[3]) < 0:
        missing = missing + 1
check("TC-27 no expense line is missing an exchange rate", missing == 0)

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
