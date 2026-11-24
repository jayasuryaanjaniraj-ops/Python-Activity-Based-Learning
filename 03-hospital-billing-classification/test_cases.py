"""
Test cases for Case Study 03 : Hospital Billing and Patient Classification
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


def close(a, b, tol=0.01):
    return abs(a - b) < tol


print("Running test cases for Case Study 03 - Hospital Billing and Patient Classification")
print("-" * 74)

# TC-01 a clean record produces no problem
check("TC-01 first record is valid", len(sol.validate(sol.PATIENTS[0])) == 0)

# TC-02 negative diagnostic charge is caught
problems = sol.validate(sol.PATIENTS[6])
check("TC-02 negative diagnostic charge is rejected",
      len(problems) == 1 and "negative" in problems[0])

# TC-03 a stay longer than 60 days is rejected
long_stay = ("P-2001", "Test", 40, "general", 450, 0, 0, 75, "self")
check("TC-03 stay of 75 days is rejected",
      any("exceeds" in p for p in sol.validate(long_stay)))

# TC-04 wrong consultation fee for the consultant type
wrong_fee = ("P-2002", "Test", 40, "specialist", 450, 0, 0, 2, "self")
check("TC-04 specialist charged at the general rate is rejected",
      any("specialist rate" in p for p in sol.validate(wrong_fee)))

# TC-05 unknown consultant type
bad_type = ("P-2003", "Test", 40, "surgeon", 450, 0, 0, 2, "self")
check("TC-05 unknown consultant type is rejected",
      any("consultant type" in p for p in sol.validate(bad_type)))

# TC-06 plain bill without concession and without insurance
subtotal, ward, cp, conc, ins, pay, note = sol.bill_of(sol.PATIENTS[0])
check("TC-06 4 day general ward bill is 13450.00", close(subtotal, 13450.00))
check("TC-07 no concession and no insurance for that patient",
      close(conc, 0.0) and close(ins, 0.0) and close(pay, 13450.00))

# TC-08 long stay plus senior citizen concession
subtotal, ward, cp, conc, ins, pay, note = sol.bill_of(sol.PATIENTS[1])
check("TC-08 long stay and senior concession add up to 13%", close(cp, 13.0))
check("TC-09 concession amount is 13% of 34400.00", close(conc, 4472.00))
check("TC-10 insurer bears 20% of the balance", close(ins, 5985.60))
check("TC-11 payable amount after insurance is 23942.40", close(pay, 23942.40))

# TC-12 exactly 7 days does not get the long stay concession
seven = ("P-2004", "Test", 30, "general", 450, 1000, 1000, 7, "self")
check("TC-12 exactly 7 days gets no long stay concession",
      close(sol.bill_of(seven)[2], 0.0))

# TC-13 eight days gets the long stay concession
eight = ("P-2005", "Test", 30, "general", 450, 1000, 1000, 8, "self")
check("TC-13 8 days gets the 8% long stay concession",
      close(sol.bill_of(eight)[2], 8.0))

# TC-14 age exactly 60 is treated as a senior citizen
sixty = ("P-2006", "Test", 60, "general", 450, 1000, 1000, 2, "self")
check("TC-14 age 60 gets the 5% senior concession",
      close(sol.bill_of(sixty)[2], 5.0))

# TC-15 classification boundaries
check("TC-15 amount 4999 is category A", sol.category_of(4999) == "A - minor")
check("TC-16 amount 5000 is category B", sol.category_of(5000) == "B - moderate")
check("TC-17 amount 15000 is category C", sol.category_of(15000) == "C - major")
check("TC-18 amount 30000 is category D", sol.category_of(30000) == "D - critical")

# TC-19 payment plan threshold
check("TC-19 a bill of 25000 is full settlement",
      "FULL" in sol.payment_plan(25000))
check("TC-20 a bill of 25001 needs an instalment plan",
      "INSTALMENT" in sol.payment_plan(25001))

# TC-21 exactly one record in the given data is rejected
rejected = 0
for patient in sol.PATIENTS:
    if len(sol.validate(patient)) > 0:
        rejected = rejected + 1
check("TC-21 exactly 1 of the 8 records is rejected", rejected == 1)

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
