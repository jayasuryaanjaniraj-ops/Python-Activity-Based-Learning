"""
Case Study 02 : Progressive Electricity Billing
-----------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, lists, tuples, tuple unpacking.
"""

# ------------------------------- tariff card ---------------------------------
# (slab_lower, slab_upper, rate per unit)
SLABS = [
    (1, 100, 1.90),
    (101, 200, 3.00),
    (201, 500, 4.50),
    (501, 1000000, 6.00),
]

FIXED_CHARGE = 110.0        # rupees per month (single phase domestic)
ELECTRICITY_DUTY = 6.0      # percent of the energy charge
HIGH_USAGE_SURCHARGE = 2.0  # percent, only when units cross 500
LOW_USAGE_REBATE = 30.0     # percent of energy charge, only when units <= 100
UNUSUAL_RISE = 25.0         # percent rise that we treat as unusual

# ------------------------------- consumer data -------------------------------
# (consumer_no, name, list of monthly units from April to March)
CONSUMERS = [
    ("AP-4471205", "Ravuri Jaya Surya", [96, 118, 172, 205, 260, 241,
                                         198, 176, 164, 189, 236, 288]),
    ("AP-4471288", "K. Srinivasa Rao", [148, 152, 161, 178, 430, 512,
                                        398, 341, 300, 288, 322, 410]),
]

MONTHS = ["April", "May", "June", "July", "August", "September",
          "October", "November", "December", "January", "February", "March"]


def energy_charge(units):
    """Progressive (slab wise) charge for the given number of units."""
    charge = 0.0
    left = units
    for lower, upper, rate in SLABS:                # tuple unpacking
        if left <= 0:
            break
        width = upper - lower + 1                   # units available in this slab
        if left > width:
            used = width
        else:
            used = left
        charge = charge + used * rate
        left = left - used
    return charge


def slab_breakup(units):
    """Return a readable string such as '100x1.90 + 100x3.00 + 12x4.50'."""
    parts = []
    left = units
    for lower, upper, rate in SLABS:
        if left <= 0:
            break
        width = upper - lower + 1
        if left > width:
            parts.append("%d x %.2f" % (width, rate))
            left = left - width
        else:
            parts.append("%d x %.2f" % (left, rate))
            left = 0
    text = ""
    for i in range(len(parts)):
        if i > 0:
            text = text + " + "
        text = text + parts[i]
    return text


def calculate_bill(units):
    """Return (energy, fixed, duty, surcharge, rebate, total, remarks)."""
    energy = energy_charge(units)
    fixed = FIXED_CHARGE
    duty = energy * ELECTRICITY_DUTY / 100.0

    surcharge = 0.0
    rebate = 0.0
    remarks = "normal"

    if units > 500:
        surcharge = energy * HIGH_USAGE_SURCHARGE / 100.0
        remarks = "high usage surcharge applied"
    if units <= 100:
        rebate = energy * LOW_USAGE_REBATE / 100.0
        remarks = "low usage rebate applied"

    total = energy + fixed + duty + surcharge - rebate
    return energy, fixed, duty, surcharge, rebate, total, remarks


def separator(char="=", width=92):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def print_consumer_report(consumer_no, name, units_list):
    print("")
    separator()
    print("CONSUMER : %s  (%s)" % (name, consumer_no))
    separator()
    print("%-10s %7s %10s %8s %8s %10s %9s  %s" %
          ("Month", "Units", "Energy", "Fixed", "Duty", "Surcharge", "Bill", "Remarks"))
    separator("-")

    bills = []
    previous_bill = -1.0
    previous_units = 0
    total_units = 0
    total_bill = 0.0
    rises = 0

    for i in range(len(units_list)):
        units = units_list[i]
        energy, fixed, duty, surcharge, rebate, total, remarks = calculate_bill(units)

        if previous_bill >= 0:
            change = (total - previous_bill) / previous_bill * 100.0
            if change > UNUSUAL_RISE:
                remarks = "UNUSUAL RISE of %.1f%%" % change
                rises = rises + 1
            elif change < 0:
                remarks = "fell by %.1f%%" % (0 - change)
            else:
                remarks = "rise of %.1f%%" % change
        if rebate > 0:
            remarks = remarks + " (rebate Rs.%.2f)" % rebate

        print("%-10s %7d %10.2f %8.2f %8.2f %9.2f %9.2f  %s" %
              (MONTHS[i], units, energy, fixed, duty, surcharge, total, remarks))

        bills.append(total)
        previous_bill = total
        previous_units = units
        total_units = total_units + units
        total_bill = total_bill + total

    separator("-")

    average_units = total_units / len(units_list)
    average_bill = total_bill / len(units_list)

    highest = bills[0]
    highest_month = MONTHS[0]
    lowest = bills[0]
    lowest_month = MONTHS[0]
    for i in range(len(bills)):
        if bills[i] > highest:
            highest = bills[i]
            highest_month = MONTHS[i]
        if bills[i] < lowest:
            lowest = bills[i]
            lowest_month = MONTHS[i]

    print("Total units for the year : %d" % total_units)
    print("Total amount payable     : Rs.%.2f" % total_bill)
    print("Average units per month  : %.2f" % average_units)
    print("Average bill per month   : Rs.%.2f" % average_bill)
    print("Highest bill             : Rs.%.2f in %s" % (highest, highest_month))
    print("Lowest bill              : Rs.%.2f in %s" % (lowest, lowest_month))
    print("Unusual increases found  : %d" % rises)
    return total_units, total_bill


def main():
    separator()
    print("             PROGRESSIVE ELECTRICITY BILLING - ANNUAL STATEMENT")
    print("             Name : Jaya Surya Ravuri        Roll No : 26000542")
    separator()
    print("Tariff  : slab 1-100 @ Rs.1.90 | 101-200 @ Rs.3.00")
    print("          201-500 @ Rs.4.50 | above 500 @ Rs.6.00 per unit")
    print("Fixed charge Rs.%.0f + duty %.0f%% + surcharge %.0f%% above 500 units"
          % (FIXED_CHARGE, ELECTRICITY_DUTY, HIGH_USAGE_SURCHARGE))
    print("Rebate    : %.0f%% of energy charge when usage is 100 units or less"
          % LOW_USAGE_REBATE)
    print("A rise of more than %.0f%% over the previous month is reported as unusual."
          % UNUSUAL_RISE)

    summary = []
    for consumer in CONSUMERS:
        consumer_no, name, units_list = consumer        # tuple unpacking
        total_units, total_bill = print_consumer_report(consumer_no, name, units_list)
        summary.append((name, consumer_no, total_units, total_bill))

    print("")
    separator()
    print("COMPARISON BETWEEN THE TWO CONSUMERS")
    separator("-")
    print("%-22s %-14s %10s %14s %12s" %
          ("Consumer", "Consumer No", "Units", "Amount", "Avg Rs/unit"))
    separator("-")
    for name, consumer_no, total_units, total_bill in summary:
        print("%-22s %-14s %10d %14.2f %12.2f" %
              (name, consumer_no, total_units, total_bill, total_bill / total_units))
    separator()
    print("Both bills were generated from the same tariff card,")
    print("so the difference is only because of the number of units consumed.")
    separator()


main()
