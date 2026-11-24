"""
Test cases for Case Study 02 : Progressive Electricity Billing
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


print("Running test cases for Case Study 02 - Progressive Electricity Billing")
print("-" * 74)

# TC-01 zero units -> zero energy charge
check("TC-01 energy charge for 0 units is 0.00",
      close(sol.energy_charge(0), 0.0))

# TC-02 fully inside the first slab
check("TC-02 50 units = 50 x 1.90 = 95.00",
      close(sol.energy_charge(50), 95.00))

# TC-03 exactly at the first slab boundary
check("TC-03 100 units = 190.00 (no spill over)",
      close(sol.energy_charge(100), 190.00))

# TC-04 one unit into the second slab
check("TC-04 101 units = 190.00 + 3.00 = 193.00",
      close(sol.energy_charge(101), 193.00))

# TC-05 two slabs fully used
check("TC-05 200 units = 190 + 300 = 490.00",
      close(sol.energy_charge(200), 490.00))

# TC-06 three slabs used
check("TC-06 500 units = 190 + 300 + 1350 = 1840.00",
      close(sol.energy_charge(500), 1840.00))

# TC-07 all four slabs used
check("TC-07 512 units = 1840 + 72 = 1912.00",
      close(sol.energy_charge(512), 1912.00))

# TC-08 progressive billing is cheaper than flat rate on the last slab
check("TC-08 progressive charge is less than 512 x 6.00",
      sol.energy_charge(512) < 512 * 6.00)

# TC-09 low usage rebate is applied at 100 units
energy, fixed, duty, surcharge, rebate, total, remarks = sol.calculate_bill(100)
check("TC-09 100 units gets a 30% rebate of 57.00",
      close(rebate, 57.00) and "rebate" in remarks)

# TC-10 no rebate above 100 units
energy, fixed, duty, surcharge, rebate, total, remarks = sol.calculate_bill(150)
check("TC-10 150 units gets no rebate and no surcharge",
      close(rebate, 0.0) and close(surcharge, 0.0))

# TC-11 surcharge above 500 units
energy, fixed, duty, surcharge, rebate, total, remarks = sol.calculate_bill(512)
check("TC-11 512 units gets a 2% high usage surcharge",
      close(surcharge, 1912.00 * 0.02))

# TC-12 duty is 6% of the energy charge
check("TC-12 duty on 200 units is 6% of 490.00 = 29.40",
      close(sol.calculate_bill(200)[2], 29.40))

# TC-13 total bill of a plain case
energy, fixed, duty, surcharge, rebate, total, remarks = sol.calculate_bill(200)
expected = 490.00 + 110.00 + 29.40
check("TC-13 total for 200 units = 629.40", close(total, expected))

# TC-14 bill always increases with units
check("TC-14 bill for 300 units is more than bill for 200 units",
      sol.calculate_bill(300)[5] > sol.calculate_bill(200)[5])

# TC-15 slab break up string
check("TC-15 break up for 201 units shows all three slabs",
      sol.slab_breakup(201) == "100 x 1.90 + 100 x 3.00 + 1 x 4.50")

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
