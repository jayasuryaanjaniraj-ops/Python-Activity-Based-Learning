"""
Case Study 08 : Manufacturing Cost and Profitability Analysis
------------------------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, strings, lists, tuples, tuple unpacking.
"""

# ------------------------------- workshop rates ------------------------------
LABOUR_RATE_PER_HOUR = 220.0      # rupees
MACHINE_HOUR_RATE = 480.0         # rupees
OVERHEAD_PERCENT = 12.0           # factory overhead on the prime cost
MAX_WASTAGE_PERCENT = 12.0        # a batch wasting more than this is rejected
TARGET_MARGIN_PERCENT = 18.0      # profit target on the selling price

# ------------------------------ product master ------------------------------
# (code, product name, selling price per unit)
PRODUCTS = [
    ("FG-101", "Steel hinge 4 inch",   78.00),
    ("FG-102", "Aluminium bracket",   158.00),
    ("FG-103", "MS clamp",             36.00),
    ("FG-104", "Powder coated hook",  300.00),
    ("FG-105", "Stainless spacer",     70.00),
]

# ------------------------------- batch records ------------------------------
# (batch_no, product_code, units_produced, material_kg,
#  material_rate_per_kg, labour_hours, machine_hours, wastage_percent)
BATCHES = [
    ("B-2601", "FG-101", 1200, 480.0, 62.0, 96, 34, 6.0),
    ("B-2602", "FG-102",  600, 300.0, 148.0, 74, 42, 4.5),
    ("B-2603", "FG-103", 2500, 620.0, 44.0, 110, 28, 9.0),
    ("B-2604", "FG-104",  400, 260.0, 210.0, 88, 56, 15.0),
    ("B-2605", "FG-105",  900, 190.0, 175.0, 62, 30, 3.0),
    ("B-2606", "FG-101", 1500, 570.0, 62.0, 118, 40, 7.5),
]


def product_of(code):
    """Return (name, price) of the product or (None, 0)."""
    for p_code, name, price in PRODUCTS:                # tuple unpacking
        if p_code == code:
            return name, price
    return None, 0.0


def batch_cost(batch):
    """Return the complete cost sheet of one batch."""
    (batch_no, code, units, material_kg, material_rate,
     labour_hours, machine_hours, wastage_percent) = batch   # tuple unpacking

    name, price = product_of(code)

    wastage_kg = material_kg * wastage_percent / 100.0
    usable_kg = material_kg - wastage_kg
    material_cost = usable_kg * material_rate

    labour_cost = labour_hours * LABOUR_RATE_PER_HOUR
    machine_cost = machine_hours * MACHINE_HOUR_RATE

    prime_cost = material_cost + labour_cost + machine_cost
    overhead = prime_cost * OVERHEAD_PERCENT / 100.0
    total_cost = prime_cost + overhead

    cost_per_unit = total_cost / units
    revenue = units * price
    profit = revenue - total_cost

    if revenue > 0:
        margin_percent = profit / revenue * 100.0
    else:
        margin_percent = 0.0

    status = "OK"
    if wastage_percent > MAX_WASTAGE_PERCENT:
        status = "REJECTED - wastage above %.0f%%" % MAX_WASTAGE_PERCENT
    elif profit <= 0:
        status = "LOSS MAKING"
    elif margin_percent < TARGET_MARGIN_PERCENT:
        status = "BELOW TARGET"
    else:
        status = "MEETS TARGET"

    return [batch_no, code, name, units, price, wastage_kg, material_cost,
            labour_cost, machine_cost, prime_cost, overhead, total_cost,
            cost_per_unit, revenue, profit, margin_percent, status]


def separator(char="-", width=104):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    print("=" * 104)
    print("               MANUFACTURING COST AND PROFITABILITY ANALYSIS - MARCH 2026")
    print("               Name : Jaya Surya Ravuri        Roll No : 26000542")
    print("=" * 104)
    print("Rates      : labour Rs.%.2f per hour, machine Rs.%.2f per hour"
          % (LABOUR_RATE_PER_HOUR, MACHINE_HOUR_RATE))
    print("Overhead   : %.0f%% of the prime cost" % OVERHEAD_PERCENT)
    print("Quality    : a batch wasting more than %.0f%% of the material is rejected"
          % MAX_WASTAGE_PERCENT)
    print("Target     : profit margin of at least %.0f%% of the selling value"
          % TARGET_MARGIN_PERCENT)

    results = []
    for batch in BATCHES:
        results.append(batch_cost(batch))

    print("")
    separator("=", 104)
    print("COST SHEET OF EVERY BATCH")
    separator("-", 104)
    print("%-8s %-8s %-20s %6s %9s %11s %10s %10s %12s %12s" %
          ("Batch", "Code", "Product", "Units", "Wastage", "Material",
           "Labour", "Machine", "Overhead", "Total cost"))
    separator("-", 104)

    for r in results:
        print("%-8s %-8s %-20s %6d %8.1fkg %11.2f %10.2f %10.2f %12.2f %12.2f" %
              (r[0], r[1], r[2], r[3], r[5], r[6], r[7], r[8], r[10], r[11]))

    separator("-", 104)
    total_cost_all = 0.0
    total_revenue_all = 0.0
    for r in results:
        total_cost_all = total_cost_all + r[11]
        total_revenue_all = total_revenue_all + r[13]
    print("%-68s %12s %12.2f" % ("TOTAL COST OF ALL BATCHES", "", total_cost_all))
    print("%-68s %12s %12.2f" % ("TOTAL SALES VALUE OF ALL BATCHES", "", total_revenue_all))

    print("")
    separator("=", 104)
    print("UNIT COST, SELLING PRICE AND PROFITABILITY")
    separator("-", 104)
    print("%-8s %-20s %11s %11s %12s %12s %7s  %s" %
          ("Batch", "Product", "Cost/unit", "Price/unit", "Revenue",
           "Profit", "Margin", "Status"))
    separator("-", 104)

    for r in results:
        print("%-8s %-20s %11.2f %11.2f %12.2f %12.2f %6.1f%%  %s" %
              (r[0], r[2], r[12], r[4], r[13], r[14], r[15], r[16]))

    # ---------------------------- classification ----------------------------
    meets = 0
    below = 0
    loss = 0
    rejected = 0
    for r in results:
        if r[16] == "MEETS TARGET":
            meets = meets + 1
        elif r[16] == "BELOW TARGET":
            below = below + 1
        elif r[16] == "LOSS MAKING":
            loss = loss + 1
        else:
            rejected = rejected + 1

    separator("-", 104)
    print("Batches meeting the profit target : %d" % meets)
    print("Batches below the profit target   : %d" % below)
    print("Loss making batches               : %d" % loss)
    print("Batches rejected for wastage      : %d" % rejected)

    # ------------------------- best and worst batch -------------------------
    best = results[0]
    worst = results[0]
    for r in results:
        if r[15] > best[15]:
            best = r
        if r[15] < worst[15]:
            worst = r

    print("")
    separator("=", 104)
    print("OBSERVATIONS")
    separator("-", 104)
    print("Best batch  : %s (%s) with a margin of %.1f%%"
          % (best[0], best[2], best[15]))
    print("Worst batch : %s (%s) with a margin of %.1f%%"
          % (worst[0], worst[2], worst[15]))

    # which cost head dominates in every batch
    for r in results:
        highest = r[6]
        head = "material"
        if r[7] > highest:
            highest = r[7]
            head = "labour"
        if r[8] > highest:
            highest = r[8]
            head = "machine"
        print("%-8s largest cost head is %-9s (Rs.%.2f of Rs.%.2f)"
              % (r[0], head, highest, r[11]))

    # ------------------------- what if suggestions --------------------------
    print("")
    separator("-", 104)
    print("SUGGESTIONS TO REACH THE TARGET")
    separator("-", 104)
    suggestion_found = False
    for r in results:
        if r[15] < TARGET_MARGIN_PERCENT:
            suggestion_found = True
            required_profit = r[13] * TARGET_MARGIN_PERCENT / 100.0
            gap = required_profit - r[14]
            extra_per_unit = gap / r[3]
            allowed_cost = r[13] - required_profit
            reduction_percent = (r[11] - allowed_cost) / r[11] * 100.0
            print("%-8s short of the target by Rs.%.2f (Rs.%.2f per unit)"
                  % (r[0], gap, extra_per_unit))
            print("         option 1 : raise the selling price to Rs.%.2f per unit"
                  % (r[4] + extra_per_unit))
            if reduction_percent > 0:
                print("         option 2 : reduce the total cost by %.1f%% (to Rs.%.2f)"
                      % (reduction_percent, allowed_cost))
            else:
                print("         option 2 : the cost is already within the limit,"
                      " only the price or the batch size has to change")
    if suggestion_found is False:
        print("Every batch is already meeting the profit target.")

    print("")
    separator("=", 104)
    print("Overall factory profit : Rs.%.2f" % (total_revenue_all - total_cost_all))
    print("Overall margin         : %.2f%%" %
          ((total_revenue_all - total_cost_all) / total_revenue_all * 100.0))
    separator("=", 104)
    print("End of the manufacturing cost report")


main()
