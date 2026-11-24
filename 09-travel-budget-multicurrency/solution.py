"""
Case Study 09 : Multi-Currency Travel Budget Analysis
----------------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, strings, lists, tuples, tuple unpacking.
"""

# ------------------------------ traveller details ----------------------------
TRAVELLER = "Ravuri Jaya Surya"
ROLL_NO = "26000542"
TRIP_NAME = "South East Asia trip, May 2026"
PLANNED_BUDGET_INR = 250000.0

# ------------------------------ exchange rates -------------------------------
# value of one unit of the currency in Indian rupees
EXCHANGE_RATES = [
    ("INR", 1.00),
    ("USD", 83.40),
    ("SGD", 61.80),
    ("MYR", 17.75),
    ("THB", 2.32),
    ("EUR", 90.15),
]

CONVERSION_FEE_PERCENT = 1.5      # charged by the forex dealer on every conversion
ATM_FEE_PER_WITHDRAWAL = 250.0    # flat fee for a cash withdrawal abroad
CARD_MARKUP_PERCENT = 2.0         # bank markup on card payments
WARNING_SHARE_PERCENT = 40.0      # a category above this share is flagged

# -------------------------------- expenses ----------------------------------
# (day, category, amount, currency, payment_mode)
EXPENSES = [
    ("Day 1", "Flight ticket",      412.00, "SGD", "card"),
    ("Day 1", "Airport taxi",        28.50, "SGD", "cash"),
    ("Day 2", "Hotel",              190.00, "SGD", "card"),
    ("Day 2", "Food",                46.00, "SGD", "cash"),
    ("Day 3", "Local transport",     18.75, "SGD", "cash"),
    ("Day 3", "Sight seeing",        75.00, "SGD", "card"),
    ("Day 4", "Hotel",              420.00, "MYR", "card"),
    ("Day 4", "Food",               110.00, "MYR", "cash"),
    ("Day 5", "Shopping",           260.00, "MYR", "card"),
    ("Day 5", "Local transport",     34.00, "MYR", "cash"),
    ("Day 6", "Hotel",             2850.00, "THB", "card"),
    ("Day 6", "Food",               780.00, "THB", "cash"),
    ("Day 6", "Spa and massage",    1200.00, "THB", "cash"),
    ("Day 7", "Sight seeing",       1650.00, "THB", "card"),
    ("Day 7", "Local transport",     210.00, "THB", "cash"),
    ("Day 7", "Gifts",              2450.00, "THB", "card"),
    ("Day 8", "Airport transfer",     22.00, "SGD", "cash"),
    ("Day 8", "Snacks",               38.00, "EUR", "card"),
]


def rate_of(currency):
    """Return the rupee value of one unit of the currency, or -1 if unknown."""
    for code, rate in EXCHANGE_RATES:                    # tuple unpacking
        if code == currency:
            return rate
    return -1.0


def convert_to_inr(amount, currency, mode):
    """Return (amount_in_inr, fee_in_inr, total_in_inr) for one expense."""
    rate = rate_of(currency)
    if rate < 0:
        return -1.0, -1.0, -1.0

    fees = 0.0
    if mode == "cash":
        fees = ATM_FEE_PER_WITHDRAWAL
        converted = amount * rate
        fees_inr = fees
    elif mode == "card":
        fees_inr = amount * rate * CARD_MARKUP_PERCENT / 100.0
        converted = amount * rate
    else:
        # any other mode is treated as a normal conversion at the dealer
        fees_inr = amount * rate * CONVERSION_FEE_PERCENT / 100.0
        converted = amount * rate

    return converted, fees_inr, converted + fees_inr


def separator(char="-", width=92):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    print("=" * 92)
    print("            MULTI-CURRENCY TRAVEL BUDGET ANALYSIS")
    print("            Name : Jaya Surya Ravuri        Roll No : 26000542")
    print("=" * 92)
    print("Traveller : %s" % TRAVELLER)
    print("Trip      : %s" % TRIP_NAME)
    print("Budget    : Rs.%.2f" % PLANNED_BUDGET_INR)
    print("Rates     : 1 USD = Rs.83.40 | 1 SGD = Rs.61.80 | 1 MYR = Rs.17.75")
    print("            1 THB = Rs.2.32 | 1 EUR = Rs.90.15  (all rates are hypothetical)")
    print("Fees      : cash withdrawal Rs.%.0f per withdrawal, card markup %.0f%%,"
          % (ATM_FEE_PER_WITHDRAWAL, CARD_MARKUP_PERCENT))
    print("            money changer fee %.1f%% of the converted value"
          % CONVERSION_FEE_PERCENT)

    print("")
    separator("=", 92)
    print("EXPENSE WISE CONVERSION")
    separator("-", 92)
    print("%-8s %-18s %10s %4s %11s %8s %11s %-5s" %
          ("Day", "Category", "Amount", "Cur", "Value in Rs", "Fee Rs", "Total Rs", "Mode"))
    separator("-", 92)

    rows = []
    errors = 0
    for expense in EXPENSES:
        day, category, amount, currency, mode = expense      # tuple unpacking
        value, fee, total = convert_to_inr(amount, currency, mode)

        if value < 0:
            errors = errors + 1
            print("%-8s %-18s %10.2f %4s %11s %8s %11s %-5s" %
                  (day, category, amount, currency, "-", "-", "-", mode))
            print("      x no exchange rate available for %s, expense ignored" % currency)
            continue

        print("%-8s %-18s %10.2f %4s %11.2f %8.2f %11.2f %-5s" %
              (day, category, amount, currency, value, fee, total, mode))
        rows.append((day, category, amount, currency, value, fee, total, mode))

    separator("-", 92)

    grand_total = 0.0
    total_fees = 0.0
    for row in rows:
        grand_total = grand_total + row[6]
        total_fees = total_fees + row[5]
    print("%-58s %11s %8.2f %11.2f" % ("TOTAL OF ALL EXPENSES", "", total_fees, grand_total))

    # ------------------------- category wise analysis ------------------------
    category_totals = {}
    for row in rows:
        if row[1] in category_totals:
            category_totals[row[1]] = category_totals[row[1]] + row[6]
        else:
            category_totals[row[1]] = row[6]

    print("")
    separator("=", 92)
    print("CATEGORY WISE SPENDING")
    separator("-", 92)
    print("%-20s %14s %10s  %s" % ("Category", "Amount in Rs", "Share", "Bar"))
    separator("-", 92)

    for category in category_totals:
        share = category_totals[category] / grand_total * 100.0
        bar_length = int(share / 2)
        bar = ""
        for _ in range(bar_length):
            bar = bar + "#"
        flag = ""
        if share > WARNING_SHARE_PERCENT:
            flag = "  <-- HIGH"
        print("%-20s %14.2f %9.1f%%  %s%s" %
              (category, category_totals[category], share, bar, flag))

    separator("-", 92)

    # ------------------------- largest category -----------------------------
    largest_category = ""
    largest_amount = -1.0
    for category in category_totals:
        if category_totals[category] > largest_amount:
            largest_amount = category_totals[category]
            largest_category = category

    print("Largest expense category : %s (Rs.%.2f, %.1f%% of the trip)"
          % (largest_category, largest_amount,
             largest_amount / grand_total * 100.0))

    # ------------------------- budget comparison ----------------------------
    print("")
    separator("=", 92)
    print("BUDGET COMPARISON")
    separator("-", 92)
    print("%-52s %18.2f" % ("Planned budget", PLANNED_BUDGET_INR))
    print("%-52s %18.2f" % ("Actual spending (with all fees)", grand_total))
    print("%-52s %18.2f" % ("Fees and markups included", total_fees))

    remaining = PLANNED_BUDGET_INR - grand_total
    if remaining >= 0:
        print("%-52s %18.2f" % ("Remaining in the budget", remaining))
        print("%-52s %18.1f%%" % ("Budget used", grand_total / PLANNED_BUDGET_INR * 100.0))
        print("")
        print("Result : the trip is WITHIN the budget.")
        print("         Rs.%.2f is still available for emergencies or shopping." % remaining)
        daily = remaining / 8
        print("         That is about Rs.%.2f per day for the remaining days." % daily)
    else:
        over = 0 - remaining
        print("%-52s %18.2f" % ("Overspent amount", over))
        print("%-52s %18.1f%%" % ("Budget used", grand_total / PLANNED_BUDGET_INR * 100.0))
        print("")
        print("Result : the trip is OVER the budget by Rs.%.2f." % over)
        print("         To stay inside the budget the spending on %s" % largest_category)
        print("         should be reduced by at least Rs.%.2f." % over)

    # ---------------------- how the fees could be reduced --------------------
    card_markup = 0.0
    atm_fees = 0.0
    for row in rows:
        if row[7] == "card":
            card_markup = card_markup + row[5]
        elif row[7] == "cash":
            atm_fees = atm_fees + row[5]

    print("")
    separator("-", 92)
    print("WHERE THE EXTRA MONEY WENT")
    separator("-", 92)
    print("Card markup paid        : Rs.%.2f" % card_markup)
    print("Cash withdrawal fees    : Rs.%.2f" % atm_fees)
    print("Total avoidable charges : Rs.%.2f (%.1f%% of the spending)"
          % (total_fees, total_fees / grand_total * 100.0))
    if card_markup < atm_fees:
        print("Observation : the cash withdrawals cost more than the card markup,")
        print("              so fewer and bigger withdrawals would have saved money.")
    else:
        print("Observation : the card markup is the bigger charge, so paying in")
        print("              local currency cash would have saved money.")

    if errors > 0:
        print("")
        print("%d expense line(s) could not be converted because the rate was missing."
              % errors)
    separator("=", 92)
    print("End of the travel budget report")


main()
