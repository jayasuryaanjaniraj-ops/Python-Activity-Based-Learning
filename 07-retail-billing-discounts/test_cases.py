"""
Test cases for Case Study 07 : Retail Billing with Multiple Discount Rules
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


print("Running test cases for Case Study 07 - Retail Billing with Multiple Discount Rules")
print("-" * 74)

# TC-01 a valid product code is found
product = sol.find_product("R101")
check("TC-01 R101 is found in the master list",
      product is not None and product[1] == "Rice 25 kg bag")

# TC-02 an unknown code returns None
check("TC-02 X999 is not found", sol.find_product("X999") is None)

# TC-03 unit price of a product
check("TC-03 price of R101 is 1450.00", close(product[3], 1450.00))

# TC-04 tax percent of a product
check("TC-04 detergent carries 18% tax", close(sol.find_product("D201")[4], 18.0))

# TC-05 grocery discount is given above the limit
check("TC-05 grocery line of 3630 gets 5%",
      close(sol.category_discount_percent("grocery", 3630.00), 5.0))

# TC-06 grocery discount is not given below the limit
check("TC-06 grocery line of 1999 gets no discount",
      close(sol.category_discount_percent("grocery", 1999.00), 0.0))

# TC-07 exactly on the limit the discount is given
check("TC-07 grocery line of exactly 2000 gets 5%",
      close(sol.category_discount_percent("grocery", 2000.00), 5.0))

# TC-08 household discount
check("TC-08 household line of 420 gets 8%",
      close(sol.category_discount_percent("household", 420.00), 8.0))

# TC-09 confectionery discount
check("TC-09 confectionery line of 2910 gets 10%",
      close(sol.category_discount_percent("confectionery", 2910.00), 10.0))

# TC-10 electrical discount below the limit
check("TC-10 electrical line of 390 gets nothing",
      close(sol.category_discount_percent("electrical", 390.00), 0.0))

# TC-11 an unknown category gets nothing
check("TC-11 unknown category gets no discount",
      close(sol.category_discount_percent("furniture", 99999.00), 0.0))

# TC-12 valid lines of the basket
valid = 0
for code, qty in sol.BASKET:
    if sol.find_product(code) is not None and qty > 0:
        valid = valid + 1
check("TC-12 exactly 8 of the 10 basket lines are valid", valid == 8)

# TC-13 two lines are rejected
check("TC-13 exactly 2 basket lines are rejected", len(sol.BASKET) - valid == 2)

# TC-14 category totals of the basket
totals = {}
for code, qty in sol.BASKET:
    product = sol.find_product(code)
    if product is None or qty <= 0:
        continue
    if product[2] in totals:
        totals[product[2]] = totals[product[2]] + product[3] * qty
    else:
        totals[product[2]] = product[3] * qty
check("TC-14 grocery total is 3630.00", close(totals["grocery"], 3630.00))
check("TC-15 confectionery total is 2910.00", close(totals["confectionery"], 2910.00))
check("TC-16 electrical total is 1510.00", close(totals["electrical"], 1510.00))

# TC-17 gross value of the bill
gross = 0.0
tax = 0.0
for code, qty in sol.BASKET:
    product = sol.find_product(code)
    if product is None or qty <= 0:
        continue
    gross = gross + product[3] * qty
    tax = tax + product[3] * qty * product[4] / 100.0
check("TC-17 gross value of the bill is 8470.00", close(gross, 8470.00))
check("TC-18 total tax is 962.10", close(tax, 962.10))

# TC-19 category discounts of the bill
disc = 0.0
for category in totals:
    disc = disc + totals[category] * sol.category_discount_percent(
        category, totals[category]) / 100.0
check("TC-19 category discount total is 596.70", close(disc, 596.70))

# TC-20 bill level discount is 5% above 5000
bill_discount = gross * sol.BILL_DISCOUNT_PERCENT / 100.0
check("TC-20 bill discount is 423.50", close(bill_discount, 423.50))

# TC-21 the discount cap is applied
total_discount = disc + bill_discount
if total_discount > sol.MAX_DISCOUNT_AMOUNT:
    total_discount = sol.MAX_DISCOUNT_AMOUNT
check("TC-21 total discount is capped at 900.00", close(total_discount, 900.00))

# TC-22 final payable amount
payable = round(gross - total_discount + tax)
check("TC-22 net amount payable is 8532", payable == 8532)

# TC-23 free delivery above 3000
check("TC-23 a bill of 7570 after discount gets free delivery",
      (gross - total_discount) >= sol.FREE_DELIVERY_ABOVE)

# TC-24 delivery is charged on a small bill
check("TC-24 a bill of 1000 pays the delivery charge of 60",
      1000 < sol.FREE_DELIVERY_ABOVE and close(sol.HOME_DELIVERY_CHARGE, 60.0))

# TC-25 the costliest line is the chocolate gift pack
costliest = 0.0
name = ""
for code, qty in sol.BASKET:
    product = sol.find_product(code)
    if product is None or qty <= 0:
        continue
    value = product[3] * qty
    if value > costliest:
        costliest = value
        name = product[1]
check("TC-25 costliest line is the chocolate gift pack at 1950.00",
      name == "Chocolate gift pack" and close(costliest, 1950.00))

print("-" * 74)
print("Passed : %d        Failed : %d" % (passed, failed))
if failed == 0:
    print("All test cases passed.")
else:
    print("Some test cases failed.")
