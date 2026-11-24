"""
Case Study 10 : Campus Event Financial Planning
----------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, strings, lists, tuples, tuple unpacking.
"""

# ------------------------------ event details --------------------------------
EVENT_NAME = "TECHNOVA 2026 - National Level Technical Fest"
COLLEGE = "Department of Computer Science"
ORGANISER = "Ravuri Jaya Surya"
ROLL_NO = "26000542"
EVENT_DAYS = 2

# ------------------------------- cost heads ---------------------------------
# fixed costs : (head, amount)
FIXED_COSTS = [
    ("Venue rent (2 days)", 18000.0),
    ("Sound and projection", 9500.0),
    ("Stage decoration", 6500.0),
    ("Transport for guests", 7000.0),
    ("Printing and banners", 4200.0),
]

# variable costs : (head, amount per participant)
VARIABLE_COSTS = [
    ("Catering (2 lunches + snacks)", 150.0),
    ("Participation certificate", 20.0),
    ("Event kit and badge", 40.0),
]

# ------------------------------ income details -------------------------------
SPONSORSHIP = 40000.0           # amount promised by the sponsors
MAX_PARTICIPATION_FEE = 260.0   # maximum fee a participant is willing to pay
EXPECTED_PARTICIPANTS = 150     # registrations expected by the committee
MAX_PARTICIPANTS = 400          # the venue cannot hold more than this


def totals():
    """Return (fixed_total, variable_per_head) after reading the cost heads."""
    fixed = 0.0
    for head, amount in FIXED_COSTS:                   # tuple unpacking
        fixed = fixed + amount

    variable = 0.0
    for head, amount in VARIABLE_COSTS:
        variable = variable + amount

    return fixed, variable


def total_cost(participants):
    """Total cost of the event for the given number of participants."""
    fixed, variable = totals()
    return fixed + variable * participants


def participation_fee(participants):
    """Fee to be collected from each participant."""
    if participants <= 0:
        return 0.0
    shortfall = total_cost(participants) - SPONSORSHIP
    if shortfall <= 0:
        return 0.0
    return shortfall / participants


def money(value):
    """Format a number the Indian way with two decimals."""
    return "Rs.%.2f" % value


def separator(char="-", width=92):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    fixed_total, variable_per_head = totals()

    print("=" * 92)
    print("                 CAMPUS EVENT FINANCIAL PLANNING")
    print("                 Name : Jaya Surya Ravuri        Roll No : 26000542")
    print("=" * 92)
    print("Event     : %s" % EVENT_NAME)
    print("College   : %s" % COLLEGE)
    print("Organiser : %s (%s)" % (ORGANISER, ROLL_NO))
    print("Duration  : %d days" % EVENT_DAYS)

    print("")
    separator("=", 92)
    print("COST SHEET")
    separator("-", 92)
    print("%-34s %12s %14s %14s" % ("Cost head", "Type", "Amount", "For 150 heads"))
    separator("-", 92)

    for head, amount in FIXED_COSTS:
        print("%-34s %12s %14.2f %14.2f" % (head, "fixed", amount, amount))

    for head, amount in VARIABLE_COSTS:
        print("%-34s %12s %14.2f %14.2f" %
              (head, "per head", amount, amount * EXPECTED_PARTICIPANTS))

    separator("-", 92)
    print("%-34s %12s %14.2f %14.2f" %
          ("TOTAL", "", fixed_total, total_cost(EXPECTED_PARTICIPANTS)))
    print("%-34s %12s %14.2f" % ("Fixed cost of the event", "", fixed_total))
    print("%-34s %12s %14.2f" % ("Variable cost per participant", "", variable_per_head))

    # ------------------------------ funding gap -----------------------------
    print("")
    separator("=", 92)
    print("FUNDING POSITION")
    separator("-", 92)
    expected_cost = total_cost(EXPECTED_PARTICIPANTS)
    gap_expected = expected_cost - SPONSORSHIP

    print("%-52s %18.2f" % ("Sponsorship received", SPONSORSHIP))
    print("%-52s %18.2f" % ("Total cost for %d participants" % EXPECTED_PARTICIPANTS,
                            expected_cost))

    if gap_expected <= 0:
        print("%-52s %18.2f" % ("Sponsorship covers the whole event, surplus",
                                gap_expected))
        print("")
        print("The event is fully sponsored, so no registration fee is needed.")
        print("The surplus of %s can be used as the prize money." % money(0 - gap_expected))
        print("")
        separator("=", 92)
        print("End of the event financial plan")
        return

    print("%-52s %18.2f" % ("Shortfall to be met from registration fees", gap_expected))
    fee_expected = gap_expected / EXPECTED_PARTICIPANTS
    print("%-52s %18.2f" % ("Contribution needed per participant", fee_expected))
    print("%-52s %18.2f" % ("Maximum fee a participant will pay", MAX_PARTICIPATION_FEE))

    if fee_expected <= MAX_PARTICIPATION_FEE:
        print("Result : the expected %d registrations are enough, the fee of %s"
              % (EXPECTED_PARTICIPANTS, money(fee_expected)))
        print("         is within the acceptable limit of %s." % money(MAX_PARTICIPATION_FEE))
    else:
        print("Result : the expected registrations are NOT enough with this fee.")
        print("         We must either increase the sponsorship or reduce a cost head.")

    # ------------------------- scenario table ------------------------------
    print("")
    separator("=", 92)
    print("SCENARIO ANALYSIS FOR DIFFERENT REGISTRATION COUNTS")
    separator("-", 92)
    print("%-14s %14s %14s %14s %12s %s" %
          ("Participants", "Total cost", "Sponsorship", "Fee per head", "Verdict", ""))
    separator("-", 92)

    scenario = [40, 80, 120, EXPECTED_PARTICIPANTS, 200, 260, 300, MAX_PARTICIPANTS]
    best_count = 0
    for count in scenario:
        cost = total_cost(count)
        gap = cost - SPONSORSHIP
        if gap <= 0:
            fee = 0.0
        else:
            fee = gap / count

        if fee == 0:
            verdict = "fully sponsored"
        elif fee <= MAX_PARTICIPATION_FEE:
            verdict = "FEASIBLE"
        else:
            verdict = "fee too high"
            if best_count == 0:
                best_count = count

        print("%-14d %14.2f %14.2f %14.2f %-12s" %
              (count, cost, SPONSORSHIP, fee, verdict))

    # ------------------------- break even count ----------------------------
    print("")
    separator("=", 92)
    print("BREAK EVEN ANALYSIS")
    separator("-", 92)

    break_even = 0
    for count in range(1, MAX_PARTICIPANTS + 1):
        if participation_fee(count) <= MAX_PARTICIPATION_FEE:
            break_even = count
            break

    if break_even == 0:
        print("Even with %d participants the fee stays above %s, so the event"
              % (MAX_PARTICIPANTS, money(MAX_PARTICIPATION_FEE)))
        print("cannot break even without more sponsorship.")
        print("")
        separator("=", 92)
        print("End of the event financial plan")
        return

    print("Minimum registrations needed to break even : %d" % break_even)
    print("Fee at that count                          : %s"
          % money(participation_fee(break_even)))
    print("Total cost at that count                   : %s"
          % money(total_cost(break_even)))
    print("Total collection (fees + sponsorship)      : %s"
          % money(participation_fee(break_even) * break_even + SPONSORSHIP))
    print("Registration fee if only 100 people come   : %s"
          % money(participation_fee(100)))

    # what happens if only one less participant registers
    if break_even > 1:
        lower_count = break_even - 1
        print("")
        print("With only %d participants the fee would have to be %s,"
              % (lower_count, money(participation_fee(lower_count))))
        print("which is above the acceptable limit - so %d is the exact break even count."
              % break_even)
    print("")
    print("Rule used : a count n works only when")
    print("            n x fee(n) + sponsorship >= total cost(n),")
    print("            that is, fee(n) = (total cost - sponsorship) / n <= %s."
          % money(MAX_PARTICIPATION_FEE))

    # ------------------------- final plan ----------------------------------
    print("")
    separator("=", 92)
    print("FINAL PLAN FOR %d PARTICIPANTS" % EXPECTED_PARTICIPANTS)
    separator("-", 92)

    final_cost = total_cost(EXPECTED_PARTICIPANTS)
    final_fee = participation_fee(EXPECTED_PARTICIPANTS)
    collected = final_fee * EXPECTED_PARTICIPANTS
    balance = collected + SPONSORSHIP - final_cost

    print("%-52s %18.2f" % ("Registration fee per participant", final_fee))
    print("%-52s %18.2f" % ("Total registration collection", collected))
    print("%-52s %18.2f" % ("Sponsorship", SPONSORSHIP))
    print("%-52s %18.2f" % ("Total income", collected + SPONSORSHIP))
    print("%-52s %18.2f" % ("Total expenditure", final_cost))
    print("%-52s %18.2f" % ("Balance in hand", balance))

    if balance > 0:
        print("")
        print("The event ends with a surplus of %s, which can be kept as the" % money(balance))
        print("prize fund for the next edition of the fest.")
    elif balance == 0:
        print("")
        print("The fees and the sponsorship exactly meet the expenditure,")
        print("so the event breaks even with %d participants." % EXPECTED_PARTICIPANTS)
    else:
        print("")
        print("The plan still falls short by %s, so one more sponsor is needed."
              % money(0 - balance))

    # sensitivity : what if the sponsorship falls by 20 percent
    print("")
    separator("-", 92)
    print("RISK CHECK")
    separator("-", 92)
    reduced_sponsorship = SPONSORSHIP * 0.80
    reduced_gap = final_cost - reduced_sponsorship
    reduced_fee = reduced_gap / EXPECTED_PARTICIPANTS
    print("If the sponsorship comes down by 20%% to %s," % money(reduced_sponsorship))
    print("the fee per participant rises from %s to %s."
          % (money(final_fee), money(reduced_fee)))
    if reduced_fee > MAX_PARTICIPATION_FEE:
        print("That is above the limit of %s, so the committee should keep a"
              % money(MAX_PARTICIPATION_FEE))
        print("backup sponsor or reduce the decoration budget.")
    else:
        print("That is still within the limit of %s." % money(MAX_PARTICIPATION_FEE))

    separator("=", 92)
    print("End of the event financial plan")


main()
