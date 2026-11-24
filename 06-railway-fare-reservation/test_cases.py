"""
Test cases for Case Study 06 : Railway Fare and Reservation Calculator
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


print("Running test cases for Case Study 06 - Railway Fare and Reservation Calculator")
print("-" * 74)

# TC-01 distance slab fare up to 200 km
check("TC-01 200 km = 200 x 0.85 = 170.00", close(sol.slab_fare(200), 170.00))

# TC-02 distance slab fare up to 500 km
check("TC-02 500 km = 170 + 300 x 0.72 = 386.00", close(sol.slab_fare(500), 386.00))

# TC-03 distance slab fare up to 1000 km
check("TC-03 1000 km = 386 + 500 x 0.61 = 691.00", close(sol.slab_fare(1000), 691.00))

# TC-04 the fare for the actual journey
check("TC-04 1548 km = 691 + 548 x 0.55 = 992.40", close(sol.slab_fare(1548), 992.40))

# TC-05 the last slab with no upper limit
check("TC-05 2500 km extends into the open ended slab",
      sol.slab_fare(2500) > sol.slab_fare(2000))

# TC-06 zero distance
check("TC-06 0 km costs nothing", close(sol.slab_fare(0), 0.0))

# TC-07 class multipliers
check("TC-07 sleeper multiplier is 1.00", close(sol.class_multiplier("SL"), 1.00))
check("TC-08 2S multiplier is 0.55", close(sol.class_multiplier("2S"), 0.55))
check("TC-09 1A multiplier is 5.60", close(sol.class_multiplier("1A"), 5.60))
check("TC-10 unknown class falls back to 1.00",
      close(sol.class_multiplier("XX"), 1.00))

# TC-11 an adult male gets no concession
percent, note = sol.concession_percent(20, "M")
check("TC-11 adult male gets no concession", close(percent, 0.0))

# TC-12 a child below 5 travels free
percent, note = sol.concession_percent(3, "M")
check("TC-12 child of 3 years pays nothing", close(percent, 100.0))

# TC-13 a child below 12 gets 50%
percent, note = sol.concession_percent(10, "F")
check("TC-13 child of 10 years gets 50%", close(percent, 50.0))

# TC-14 a senior male gets 30%
percent, note = sol.concession_percent(65, "M")
check("TC-14 senior male gets 30%", close(percent, 30.0))

# TC-15 a senior lady gets 30 + 30
percent, note = sol.concession_percent(67, "F")
check("TC-15 senior lady gets 60%", close(percent, 60.0))

# TC-16 a young lady gets 30%
percent, note = sol.concession_percent(24, "F")
check("TC-16 lady passenger of 24 gets 30%", close(percent, 30.0))

# TC-17 boundary : age exactly 12 is not a child
percent, note = sol.concession_percent(12, "M")
check("TC-17 age 12 is treated as an adult male", close(percent, 0.0))

# TC-18 boundary : age exactly 60 is a senior citizen
percent, note = sol.concession_percent(60, "M")
check("TC-18 age 60 gets the senior concession", close(percent, 30.0))

# TC-19 cancellation slabs
check("TC-19 cancellation 60 hours before departure = 10%",
      sol.cancellation_penalty(60)[0] == 10)
check("TC-20 cancellation 30 hours before departure = 25%",
      sol.cancellation_penalty(30)[0] == 25)
check("TC-21 cancellation 18 hours before departure = 50%",
      sol.cancellation_penalty(18)[0] == 50)
check("TC-22 cancellation 6 hours before departure = 75%",
      sol.cancellation_penalty(6)[0] == 75)
check("TC-23 cancellation 1 hour before departure = 90%",
      sol.cancellation_penalty(1)[0] == 90)

# TC-24 fare of an ordinary adult in sleeper
d = sol.calculate_passenger(sol.PASSENGERS[0])
check("TC-24 adult sleeper fare is 1084.55", close(d[14], 1084.55))

# TC-25 no autofill for a confirmed ticket
check("TC-25 confirmed ticket has no autofill", close(d[12], 0.0))

# TC-26 autofill for a waiting list ticket
d2 = sol.calculate_passenger(sol.PASSENGERS[4])
check("TC-26 waiting list ticket pays the autofill of 30", close(d2[12], 30.0))

# TC-27 infant pays only insurance and tax
d3 = sol.calculate_passenger(sol.PASSENGERS[3])
check("TC-27 infant fare is 0.53", close(d3[14], 0.53))

# TC-28 cancelled passenger has zero payable amount
d4 = sol.calculate_passenger(sol.PASSENGERS[5])
check("TC-28 cancelled ticket has nothing to pay", close(d4[14], 0.0))

# TC-29 refund is total minus penalty
check("TC-29 refund of the cancelled ticket is 2689.04", close(d4[15], 2689.04))
check("TC-30 penalty of the cancelled ticket is 896.35", close(d4[16], 896.35))

# TC-31 the highest fare belongs to the 1A passenger
fares = []
for p in sol.PASSENGERS:
    res = sol.calculate_passenger(p)
    if res[19] == "no":
        fares.append(res[14])
highest = fares[0]
for f in fares:
    if f > highest:
        highest = f
check("TC-31 highest fare is 2376.65", close(highest, 2376.65))

# TC-32 exactly one passenger cancelled
cancelled = 0
for p in sol.PASSENGERS:
    if sol.calculate_passenger(p)[19] == "yes":
        cancelled = cancelled + 1
check("TC-32 exactly one passenger cancelled", cancelled == 1)

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
