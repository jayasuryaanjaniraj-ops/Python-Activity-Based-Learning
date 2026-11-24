"""
Test cases for Case Study 01 : University Scholarship Allocation
Run : python3 test_cases.py
"""

import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location(
    "sol", os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py"))
sol = importlib.util.module_from_spec(spec)

# solution.py calls main() at the bottom, so stdout is silenced while loading it
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


print("Running test cases for Case Study 01 - University Scholarship Allocation")
print("-" * 74)

# TC-01 a strong applicant is eligible
ok, agg, reasons = sol.evaluate_applicant(sol.APPLICANTS[0])
check("TC-01 Meghana is eligible with aggregate 80.80 and no reason",
      ok is True and abs(agg - 80.8) < 0.01 and len(reasons) == 0)

# TC-02 low aggregate plus low subject mark
ok, agg, reasons = sol.evaluate_applicant(sol.APPLICANTS[1])
check("TC-02 Karthik rejected because aggregate 58.60 < 60",
      ok is False and abs(agg - 58.6) < 0.01)
check("TC-03 Karthik reason list contains the Physics failure",
      len(reasons) == 2 and "Physics" in reasons[1])

# TC-04 income limit
ok, agg, reasons = sol.evaluate_applicant(sol.APPLICANTS[2])
check("TC-04 Vaishnavi rejected only because of family income",
      ok is False and len(reasons) == 1 and "income" in reasons[0])

# TC-05 three conditions fail together
ok, agg, reasons = sol.evaluate_applicant(sol.APPLICANTS[5])
check("TC-05 Ganesh reports all three failures", ok is False and len(reasons) == 3)

# TC-06 attendance limit
ok, agg, reasons = sol.evaluate_applicant(sol.APPLICANTS[9])
check("TC-06 Nandini rejected for attendance 69% < 75%",
      ok is False and "attendance" in reasons[0])

# TC-07 exactly on the boundary should pass
boundary = ("26000999", "Test Student", [60, 60, 60, 60, 60], 75.0, 500000)
ok, agg, reasons = sol.evaluate_applicant(boundary)
check("TC-07 boundary applicant (60%, 75%, Rs.500000) is eligible",
      ok is True and abs(agg - 60.0) < 0.01)

# TC-08 one mark just below the subject limit is caught
almost = ("26000998", "Test Student 2", [80, 80, 49, 80, 80], 90.0, 200000)
ok, agg, reasons = sol.evaluate_applicant(almost)
check("TC-08 single subject mark 49 is rejected",
      ok is False and "Chemistry" in reasons[0])

# TC-09 ranking key puts higher aggregate first
record_a = ("26000001", "A", 71.0, 80.0, 300000)
record_b = ("26000002", "B", 75.0, 70.0, 300000)
check("TC-09 higher aggregate ranks above lower aggregate",
      sol.ranking_key(record_a) > sol.ranking_key(record_b))

# TC-10 tie on aggregate : attendance decides
record_c = ("26000003", "C", 71.0, 60.0, 300000)
check("TC-10 on equal aggregate the higher attendance ranks first",
      sol.ranking_key(record_a) < sol.ranking_key(record_c))

# TC-11 tie on aggregate and attendance : lower income decides
record_d = ("26000004", "D", 71.0, 80.0, 200000)
check("TC-11 on equal aggregate and attendance the lower income ranks first",
      sol.ranking_key(record_d) < sol.ranking_key(record_a))

# TC-12 total eligible and rejected count
eligible = 0
for applicant in sol.APPLICANTS:
    ok, agg, reasons = sol.evaluate_applicant(applicant)
    if ok:
        eligible = eligible + 1
check("TC-12 exactly 5 of the 10 applicants are eligible", eligible == 5)

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
