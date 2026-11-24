"""
Test cases for Case Study 04 : Employee Payroll and Deduction Analysis
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


print("Running test cases for Case Study 04 - Employee Payroll and Deduction Analysis")
print("-" * 74)

# TC-01 tax is nil inside the first slab
check("TC-01 no tax up to Rs.25000", close(sol.tax_on(25000), 0.0))

# TC-02 tax on a small amount in the second slab
check("TC-02 tax on Rs.30000 = 5000 x 5% = 250.00", close(sol.tax_on(30000), 250.0))

# TC-03 full second slab
check("TC-03 tax on Rs.50000 = 1250.00", close(sol.tax_on(50000), 1250.0))

# TC-04 two slabs used
check("TC-04 tax on Rs.60000 = 1250 + 1000 = 2250.00", close(sol.tax_on(60000), 2250.0))

# TC-05 three slabs used
check("TC-05 tax on Rs.120000 = 1250 + 5000 + 4000 = 10250.00",
      close(sol.tax_on(120000), 10250.0))

# TC-06 zero income
check("TC-06 tax on 0 is 0", close(sol.tax_on(0), 0.0))

# TC-07 HRA is 20% of basic
values = sol.calculate_salary(sol.EMPLOYEES[0])
check("TC-07 HRA of Ravuri (basic 24000) is 4800.00", close(values[1], 4800.0))

# TC-08 overtime amount
check("TC-08 overtime for 12 hours is 3000.00", close(values[3], 3000.0))

# TC-09 incentive amount
check("TC-09 incentive at 4% of 24000 is 960.00", close(values[4], 960.0))

# TC-10 gross salary
check("TC-10 gross salary is 34360.00", close(values[5], 34360.0))

# TC-11 provident fund
check("TC-11 PF at 12% of 24000 is 2880.00", close(values[6], 2880.0))

# TC-12 income tax on the gross
check("TC-12 income tax on 34360 is 468.00", close(values[7], 468.00))

# TC-13 total deductions
check("TC-13 total deductions are 3548.00", close(values[9], 3548.00))

# TC-14 net salary
check("TC-14 net salary is 30812.00", close(values[10], 30812.00))

# TC-15 net salary = gross - deductions for every employee
ok = True
for employee in sol.EMPLOYEES:
    v = sol.calculate_salary(employee)
    if not close(v[10], v[5] - v[9]):
        ok = False
check("TC-15 net = gross - deductions for all 6 employees", ok)

# TC-16 gross = sum of the earning components
v = sol.calculate_salary(sol.EMPLOYEES[4])
check("TC-16 gross of the manager is the sum of his earnings",
      close(v[5], v[0] + v[1] + v[2] + v[3] + v[4]))

# TC-17 an employee with zero overtime
v = sol.calculate_salary(sol.EMPLOYEES[3])
check("TC-17 zero overtime gives zero overtime pay", close(v[3], 0.0))

# TC-18 the lowest paid employee still has a positive net salary
v = sol.calculate_salary(sol.EMPLOYEES[5])
check("TC-18 support executive gets a positive net salary", v[10] > 0)

# TC-19 the manager has the highest net salary of the team
nets = []
for employee in sol.EMPLOYEES:
    nets.append(sol.calculate_salary(employee)[10])
highest = nets[0]
for n in nets:
    if n > highest:
        highest = n
check("TC-19 highest net salary is the manager's 127950.00",
      close(highest, 127950.00))

# TC-20 slab breakup text
check("TC-20 break up for 60000 shows both taxable slabs",
      sol.tax_breakup(60000) == "25000 x 5.0% + 10000 x 10.0%")

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
