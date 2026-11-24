"""
Test cases for Case Study 10 : Campus Event Financial Planning
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


print("Running test cases for Case Study 10 - Campus Event Financial Planning")
print("-" * 74)

fixed, variable = sol.totals()

# TC-01 total of the fixed cost heads
check("TC-01 fixed cost total is 45200.00", close(fixed, 45200.00))

# TC-02 total of the variable cost heads
check("TC-02 variable cost per participant is 210.00", close(variable, 210.00))

# TC-03 total cost for 150 participants
check("TC-03 total cost for 150 participants is 76700.00",
      close(sol.total_cost(150), 76700.00))

# TC-04 total cost for zero participants is only the fixed cost
check("TC-04 total cost for 0 participants is 45200.00",
      close(sol.total_cost(0), 45200.00))

# TC-05 total cost grows by the variable cost per head
check("TC-05 one more participant adds 210.00",
      close(sol.total_cost(151) - sol.total_cost(150), 210.00))

# TC-06 fee for 150 participants
check("TC-06 fee for 150 participants is 244.67",
      close(sol.participation_fee(150), 244.67))

# TC-07 fee for 100 participants
check("TC-07 fee for 100 participants is 262.00",
      close(sol.participation_fee(100), 262.00))

# TC-08 fee for 200 participants
check("TC-08 fee for 200 participants is 236.00",
      close(sol.participation_fee(200), 236.00))

# TC-09 fee falls as the count rises
check("TC-09 fee for 300 is less than the fee for 200",
      sol.participation_fee(300) < sol.participation_fee(200))

# TC-10 break even count
break_even = 0
for count in range(1, sol.MAX_PARTICIPANTS + 1):
    if sol.participation_fee(count) <= sol.MAX_PARTICIPATION_FEE:
        break_even = count
        break
check("TC-10 break even count is 104", break_even == 104)

# TC-11 the fee at the break even count is exactly the limit
check("TC-11 fee at 104 participants is 260.00",
      close(sol.participation_fee(104), 260.00, 0.01))

# TC-12 one participant less than break even is not acceptable
check("TC-12 fee at 103 participants is above 260",
      sol.participation_fee(103) > sol.MAX_PARTICIPATION_FEE)

# TC-13 at break even the collection equals the cost
collected = sol.participation_fee(104) * 104 + sol.SPONSORSHIP
check("TC-13 collection at break even equals the total cost",
      close(collected, sol.total_cost(104), 0.5))

# TC-14 a fully sponsored case gives a zero fee
saved = sol.SPONSORSHIP
sol.SPONSORSHIP = 100000.0
check("TC-14 a big sponsorship makes the fee zero",
      close(sol.participation_fee(50), 0.0))
sol.SPONSORSHIP = saved

# TC-15 zero participants is handled without dividing by zero
check("TC-15 zero participants gives a zero fee",
      close(sol.participation_fee(0), 0.0))

# TC-16 the expected 150 registrations are feasible
check("TC-16 the expected count is inside the acceptable fee",
      sol.participation_fee(sol.EXPECTED_PARTICIPANTS) <= sol.MAX_PARTICIPATION_FEE)

# TC-17 scenario at 40 participants is not feasible
check("TC-17 40 participants would need a fee of 340.00",
      close(sol.participation_fee(40), 340.00))

# TC-18 the venue limit is respected
check("TC-18 the maximum participants is 400", sol.MAX_PARTICIPANTS == 400)

# TC-19 total income equals the total cost at the expected count
income = (sol.participation_fee(sol.EXPECTED_PARTICIPANTS) *
          sol.EXPECTED_PARTICIPANTS + sol.SPONSORSHIP)
check("TC-19 income equals cost at 150 participants",
      close(income, sol.total_cost(sol.EXPECTED_PARTICIPANTS), 0.05))

# TC-20 the risk check : a 20% lower sponsorship needs a higher fee
reduced = sol.SPONSORSHIP * 0.80
reduced_fee = (sol.total_cost(150) - reduced) / 150
check("TC-20 a 20% lower sponsorship raises the fee to 298.00",
      close(reduced_fee, 298.00))
check("TC-21 that fee is above the acceptable limit",
      reduced_fee > sol.MAX_PARTICIPATION_FEE)

# TC-22 the per head costs are all positive
positive = True
for head, amount in sol.VARIABLE_COSTS:
    if amount <= 0:
        positive = False
check("TC-22 every per head cost is positive", positive)

# TC-23 the fixed cost heads add up to the value used everywhere
sum_fixed = 0.0
for head, amount in sol.FIXED_COSTS:
    sum_fixed = sum_fixed + amount
check("TC-23 the fixed cost heads add up correctly", close(sum_fixed, fixed))

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
