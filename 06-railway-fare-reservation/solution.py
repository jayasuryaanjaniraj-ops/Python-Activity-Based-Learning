"""
Case Study 06 : Railway Fare and Reservation Calculator
------------------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, strings, lists, tuples, tuple unpacking.
"""

# ------------------------------- train data ----------------------------------
TRAIN_NO = "12704"
TRAIN_NAME = "Falaknuma Express (Secunderabad - Howrah)"
DISTANCE_KM = 1548
FROM_STATION = "Secunderabad (SC)"
TO_STATION = "Howrah (HWH)"

# distance slabs : (from_km, up_to_km, rate per km for sleeper)
DISTANCE_SLABS = [
    (1, 200, 0.85),
    (201, 500, 0.72),
    (501, 1000, 0.61),
    (1001, 2000, 0.55),
    (2001, -1, 0.48),
]

# class multiplier on the sleeper fare
CLASS_MULTIPLIER = [
    ("2S", 0.55),
    ("SL", 1.00),
    ("3A", 2.45),
    ("2A", 3.40),
    ("1A", 5.60),
]

RESERVATION_FEE = 40          # per passenger
SERVICE_TAX_PERCENT = 5.0     # on the total fare
INSURANCE_PREMIUM = 0.5       # per passenger, in rupees
AUTOFILL_AMOUNT = 30          # paid only when the train is NOT confirmed
CHILD_AGE = 5                 # below this age the fare is nil
YOUTH_AGE_LIMIT = 12          # below this age the concession applies
SENIOR_AGE = 60               # senior citizen concession
CHILD_CONCESSION = 50.0       # percent
SENIOR_CONCESSION = 30.0      # percent
WOMEN_CONCESSION = 30.0       # percent for lady passengers

# cancellation penalty as (hours before departure, percent deducted)
CANCELLATION_SLABS = [
    (48, 10),      # more than 48 hours
    (24, 25),      # 24 to 48 hours
    (12, 50),      # 12 to 24 hours
    (4, 75),       # 4 to 12 hours
    (0, 90),       # less than 4 hours
]

# passenger records
# (pnr_line_no, name, age, gender, travel_class, booking_status,
#  cancelled, hours_before_departure)
PASSENGERS = [
    (1, "Ravuri Jaya Surya", 20, "M", "SL", "CNF", "no", 0),
    (2, "Ravuri Anjani Raj", 16, "M", "SL", "CNF", "no", 0),
    (3, "S. Lakshmi Devi",   67, "F", "3A", "CNF", "no", 0),
    (4, "K. Baby Aarav",      3, "M", "SL", "CNF", "no", 0),
    (5, "M. Divya",          24, "F", "2S", "WL",  "no", 0),
    (6, "T. Ramesh",         45, "M", "2A", "CNF", "yes", 30),
    (7, "P. Sravani",        10, "F", "SL", "RAC", "no", 0),
    (8, "B. Nagamani",       63, "F", "1A", "CNF", "no", 0),
]


def slab_fare(distance):
    """Progressive distance slab fare for the sleeper class."""
    fare = 0.0
    for lower, upper, rate in DISTANCE_SLABS:            # tuple unpacking
        if distance <= lower - 1:
            break
        if upper == -1:
            km = distance - lower + 1
        elif distance > upper:
            km = upper - lower + 1
        else:
            km = distance - lower + 1
        if km > 0:
            fare = fare + km * rate
    return fare


def class_multiplier(travel_class):
    """Return the multiplier for the given class."""
    for cls, value in CLASS_MULTIPLIER:
        if cls == travel_class:
            return value
    return 1.00


def concession_percent(age, gender):
    """Return (percent, note) of the concession applicable."""
    if age < CHILD_AGE:
        return 100.0, "child below %d years - no fare" % CHILD_AGE
    if age < YOUTH_AGE_LIMIT:
        return CHILD_CONCESSION, "child concession %.0f%%" % CHILD_CONCESSION
    if age >= SENIOR_AGE:
        if gender == "F":
            return SENIOR_CONCESSION + WOMEN_CONCESSION, \
                   "senior citizen %.0f%% + lady passenger %.0f%%" % (
                       SENIOR_CONCESSION, WOMEN_CONCESSION)
        return SENIOR_CONCESSION, "senior citizen concession %.0f%%" % SENIOR_CONCESSION
    if gender == "F":
        return WOMEN_CONCESSION, "lady passenger concession %.0f%%" % WOMEN_CONCESSION
    return 0.0, "no concession"


def cancellation_penalty(hours):
    """Return (percent, note) of the cancellation penalty."""
    for limit, percent in CANCELLATION_SLABS:
        if hours > limit:
            return percent, "cancelled %d hours before departure" % hours
    # nothing matched, so the last slab applies
    return CANCELLATION_SLABS[len(CANCELLATION_SLABS) - 1][1], \
           "cancelled %d hours before departure" % hours


def calculate_passenger(passenger):
    """Compute all the fare details of one passenger."""
    (line, name, age, gender, travel_class, status,
     cancelled, hours) = passenger                      # tuple unpacking

    base = slab_fare(DISTANCE_KM) * class_multiplier(travel_class)
    percent, note = concession_percent(age, gender)
    concession = base * percent / 100.0
    fare_after_concession = base - concession

    reservation = RESERVATION_FEE
    if age < CHILD_AGE:
        reservation = 0                                  # no reservation for infants
    insurance = INSURANCE_PREMIUM
    autofill = 0
    if status != "CNF":
        autofill = AUTOFILL_AMOUNT

    subtotal = fare_after_concession + reservation + insurance + autofill
    service_tax = subtotal * SERVICE_TAX_PERCENT / 100.0
    total = subtotal + service_tax

    refund = 0.0
    penalty = 0.0
    penalty_note = ""
    if cancelled == "yes":
        penalty_percent, penalty_note = cancellation_penalty(hours)
        penalty = total * penalty_percent / 100.0
        refund = total - penalty
        total = 0.0

    return [line, name, age, gender, travel_class, status, base, percent,
            concession, fare_after_concession, reservation, insurance, autofill,
            service_tax, total, refund, penalty, note, penalty_note, cancelled]


def separator(char="=", width=104):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    separator()
    print("             RAILWAY FARE AND RESERVATION CALCULATOR - E-TICKET")
    print("             Name : Jaya Surya Ravuri        Roll No : 26000542")
    separator()
    print("Train      : %s %s" % (TRAIN_NO, TRAIN_NAME))
    print("Journey    : %s to %s, %d km" % (FROM_STATION, TO_STATION, DISTANCE_KM))
    print("Sleeper fare for this distance : Rs.%.2f" % slab_fare(DISTANCE_KM))
    print("Class multipliers : 2S x0.55, SL x1.00, 3A x2.45, 2A x3.40, 1A x5.60")
    print("Concessions : child below %d free, below %d = %.0f%%, age %d+ = %.0f%%"
          % (CHILD_AGE, YOUTH_AGE_LIMIT, CHILD_CONCESSION, SENIOR_AGE, SENIOR_CONCESSION))
    print("              lady passengers get %.0f%% (added to the senior concession)"
          % WOMEN_CONCESSION)
    print("Charges     : reservation Rs.%d, insurance Rs.%.2f, service tax %.0f%%,"
          % (RESERVATION_FEE, INSURANCE_PREMIUM, SERVICE_TAX_PERCENT))
    print("              Tatkal style autofill Rs.%d only for non confirmed tickets"
          % AUTOFILL_AMOUNT)

    details = []
    for passenger in PASSENGERS:
        details.append(calculate_passenger(passenger))

    print("")
    separator()
    print("PASSENGER WISE FARE DETAILS")
    separator("-")
    print("%-3s %-18s %3s %2s %-4s %-4s %9s %6s %9s %8s %8s %9s" %
          ("No", "Passenger", "Age", "G", "Cls", "Sts", "Base", "Conc%",
           "Concession", "Charges", "Tax", "Total"))
    separator("-")

    ticket_total = 0.0
    for d in details:
        line, name, age, gender, cls, status, base, percent, concession, after = d[0:10]
        reservation, insurance, autofill, tax, total = d[10:15]
        if d[19] == "yes":
            print("%-3d %-18s %3d %2s %-4s %-4s %9.2f %6.1f %9.2f %8.2f %8.2f %9s" %
                  (line, name, age, gender, cls, status, base, percent,
                   concession, reservation + insurance + autofill, tax, "CANCELLED"))
        else:
            print("%-3d %-18s %3d %2s %-4s %-4s %9.2f %6.1f %9.2f %8.2f %8.2f %9.2f" %
                  (line, name, age, gender, cls, status, base, percent,
                   concession, reservation + insurance + autofill, tax, total))
            ticket_total = ticket_total + total

    separator("-")
    print("Amount payable for this PNR : Rs.%.2f" % ticket_total)

    print("")
    separator()
    print("CONCESSION NOTES AND CANCELLATION DETAILS")
    separator("-")
    for d in details:
        print("%d. %-18s %-4s age %2d - %s" % (d[0], d[1], d[4], d[2], d[17]))
        if d[19] == "yes":
            print("     %s | penalty Rs.%.2f | refund Rs.%.2f"
                  % (d[18], d[16], d[15]))

    print("")
    separator()
    print("BOOKING SUMMARY")
    separator("-")
    confirmed = 0
    waiting = 0
    cancelled = 0
    refund_total = 0.0
    penalty_total = 0.0
    highest_fare = -1.0
    highest_name = ""
    for d in details:
        if d[19] == "yes":
            cancelled = cancelled + 1
            refund_total = refund_total + d[15]
            penalty_total = penalty_total + d[16]
        elif d[5] == "CNF":
            confirmed = confirmed + 1
        else:
            waiting = waiting + 1
        if d[19] == "no" and d[14] > highest_fare:
            highest_fare = d[14]
            highest_name = d[1]

    print("Confirmed passengers      : %d" % confirmed)
    print("Waiting / RAC passengers  : %d" % waiting)
    print("Cancelled passengers      : %d" % cancelled)
    print("Total collected           : Rs.%.2f" % ticket_total)
    print("Total refunded            : Rs.%.2f" % refund_total)
    print("Total retained as penalty : Rs.%.2f" % penalty_total)
    print("Highest fare in this PNR  : Rs.%.2f (%s)" % (highest_fare, highest_name))
    separator()
    print("End of the railway fare statement")


main()
