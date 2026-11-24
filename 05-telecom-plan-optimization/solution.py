"""
Case Study 05 : Multi-Plan Telecommunications Cost Optimization
--------------------------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, lists, tuples, tuple unpacking.
"""

# --------------------------- usage of the customer ---------------------------
CUSTOMER_NAME = "Ravuri Jaya Surya"
ROLL_NO = "26000542"
VALIDITY_NEEDED = 84          # days of validity the customer wants
BUDGET = 800                  # maximum amount the customer is willing to pay

# monthly usage of the customer
DATA_USED_GB = 2.4
CALLS_USED_MIN = 620
SMS_USED = 180

# charges applied when the usage crosses the plan limit
EXCESS_DATA_RATE = 18.0       # rupees per extra GB
EXCESS_CALL_RATE = 0.60       # rupees per extra minute
EXCESS_SMS_RATE = 0.80        # rupees per extra sms

# ------------------------------ plans available ------------------------------
# (plan_name, price, data_gb, calls_min, sms_count, validity_days)
PLANS = [
    ("Smart Saver 149",    149, 1.0,  300,  100,  28),
    ("Value 299",          299, 1.5,  500,  100,  56),
    ("Daily 399",          399, 2.5,  600,  150,  56),
    ("Quarterly 549",      549, 2.0,  750,  300,  84),
    ("Super 699",          699, 3.0, 1000,  300,  84),
    ("Ultra 999",          999, 3.5, 1500,  500,  84),
    ("Combo 449",          449, 1.5,  600,  100,  84),
]


def evaluate_plan(plan):
    """Return the details of one plan for this customer."""
    name, price, data_gb, calls, sms, days = plan           # tuple unpacking

    eligible = True
    reason = "eligible"

    if days < VALIDITY_NEEDED:
        eligible = False
        reason = "validity only %d days, %d required" % (days, VALIDITY_NEEDED)

    excess_data = 0.0
    excess_calls = 0
    excess_sms = 0

    if DATA_USED_GB > data_gb:
        excess_data = DATA_USED_GB - data_gb
    if CALLS_USED_MIN > calls:
        excess_calls = CALLS_USED_MIN - calls
    if SMS_USED > sms:
        excess_sms = SMS_USED - sms

    excess_amount = (excess_data * EXCESS_DATA_RATE +
                     excess_calls * EXCESS_CALL_RATE +
                     excess_sms * EXCESS_SMS_RATE)

    total = price + excess_amount

    within_budget = total <= BUDGET
    if eligible and not within_budget:
        eligible = False
        reason = "total Rs.%.2f crosses the budget of Rs.%d" % (total, BUDGET)

    return [name, price, days, excess_data, excess_calls, excess_sms,
            excess_amount, total, eligible, within_budget, reason]


def make_separator(char="-", width=100):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    make_separator("=", 100)
    print("        MULTI-PLAN TELECOMMUNICATIONS COST OPTIMIZATION - PLAN ADVISOR")
    print("        Customer : %s        Roll No : %s" % (CUSTOMER_NAME, ROLL_NO))
    make_separator("=", 100)
    print("Monthly usage   : %.1f GB data, %d minutes of calls, %d SMS"
          % (DATA_USED_GB, CALLS_USED_MIN, SMS_USED))
    print("Requirements    : validity of at least %d days and total cost within Rs.%d"
          % (VALIDITY_NEEDED, BUDGET))
    print("Excess charges  : Rs.%.2f per extra GB, Rs.%.2f per extra minute, Rs.%.2f per extra SMS"
          % (EXCESS_DATA_RATE, EXCESS_CALL_RATE, EXCESS_SMS_RATE))

    results = []
    for plan in PLANS:
        results.append(evaluate_plan(plan))

    print("")
    make_separator("=", 100)
    print("PLAN WISE EVALUATION")
    make_separator("-", 100)
    print("%-16s %7s %6s %9s %9s %7s %11s %11s %s" %
          ("Plan", "Price", "Days", "ExData", "ExCalls", "ExSMS",
           "Excess Rs", "Total Rs", "Status"))
    make_separator("-", 100)

    for r in results:
        name, price, days, exd, exc, exs, examt, total, eligible, in_budget, reason = r
        status = "OK"
        if not eligible:
            status = "NOT ELIGIBLE"
        elif not in_budget:
            status = "OVER BUDGET"
        print("%-16s %7d %6d %8.1fGB %8d %6d %11.2f %11.2f %s" %
              (name, price, days, exd, exc, exs, examt, total, status))

    # keep only the plans that can really be used
    feasible = []
    for r in results:
        if r[8]:
            feasible.append(r)

    print("")
    make_separator("=", 100)
    if len(feasible) == 0:
        print("No plan satisfies both the validity requirement and the budget.")
        print("Suggestion : either increase the budget or reduce the usage.")
        make_separator("=", 100)
        return

    # sort the feasible plans by total cost, and for equal cost by more validity
    for i in range(len(feasible) - 1):
        for j in range(i + 1, len(feasible)):
            if feasible[j][7] < feasible[i][7]:
                temp = feasible[i]
                feasible[i] = feasible[j]
                feasible[j] = temp
            elif feasible[j][7] == feasible[i][7] and feasible[j][2] > feasible[i][2]:
                temp = feasible[i]
                feasible[i] = feasible[j]
                feasible[j] = temp

    print("FEASIBLE PLANS ARRANGED FROM THE CHEAPEST")
    make_separator("-", 100)
    position = 0
    for r in feasible:
        position = position + 1
        print("%d. %-16s price %4d + excess %7.2f = Rs.%8.2f for %d days"
              % (position, r[0], r[1], r[6], r[7], r[2]))

    best = feasible[0]
    print("")
    make_separator("=", 100)
    print("RECOMMENDED PLAN : %s" % best[0])
    make_separator("-", 100)
    print("Plan price        : Rs.%d" % best[1])
    print("Validity          : %d days (requirement is %d days)" % (best[2], VALIDITY_NEEDED))
    print("Excess data       : %.1f GB x Rs.%.2f = Rs.%.2f"
          % (best[3], EXCESS_DATA_RATE, best[3] * EXCESS_DATA_RATE))
    print("Excess calls      : %d min x Rs.%.2f = Rs.%.2f"
          % (best[4], EXCESS_CALL_RATE, best[4] * EXCESS_CALL_RATE))
    print("Excess SMS        : %d x Rs.%.2f = Rs.%.2f"
          % (best[5], EXCESS_SMS_RATE, best[5] * EXCESS_SMS_RATE))
    print("Total monthly cost: Rs.%.2f" % best[7])
    print("Money left in the budget : Rs.%.2f" % (BUDGET - best[7]))

    if len(feasible) > 1:
        second = feasible[1]
        saving = second[7] - best[7]
        print("Saving compared with the next best plan (%s) : Rs.%.2f"
              % (second[0], saving))

    # why the rejected plans were rejected
    print("")
    make_separator("-", 100)
    print("PLANS THAT WERE NOT CONSIDERED")
    make_separator("-", 100)
    rejected = 0
    for r in results:
        if not r[8]:
            rejected = rejected + 1
            print("%-16s -> %s" % (r[0], r[10]))
    if rejected == 0:
        print("Every plan was usable.")
    else:
        print("Total plans rejected : %d out of %d" % (rejected, len(results)))
    make_separator("=", 100)
    print("End of plan comparison")


main()
