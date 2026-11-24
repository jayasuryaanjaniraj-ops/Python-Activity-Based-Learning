"""
Case Study 01 : University Scholarship Allocation
-----------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, lists, tuples, tuple unpacking.
"""

# ------------------------- policy of the scholarship -------------------------
MIN_AGGREGATE = 60.0          # minimum aggregate percentage
MIN_SUBJECT_MARK = 50         # minimum mark in every subject
MIN_ATTENDANCE = 75.0         # minimum attendance percentage
MAX_FAMILY_INCOME = 500000    # annual family income limit (in rupees)
QUOTA = 4                     # number of scholarships to be awarded

SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "CS"]

# ------------------------- applicant records ---------------------------------
# each record is a tuple :
# (roll_no, name, list_of_5_marks, attendance%, annual_family_income)
APPLICANTS = [
    ("26000601", "A. Meghana",   [82, 76, 90, 71, 85], 92.0, 320000),
    ("26000602", "B. Karthik",   [55, 48, 62, 70, 58], 78.0, 480000),
    ("26000603", "C. Vaishnavi", [74, 69, 71, 66, 80], 84.0, 610000),
    ("26000604", "D. Sandeep",   [61, 57, 64, 59, 66], 76.0, 495000),
    ("26000605", "E. Fatima",    [91, 88, 94, 87, 96], 97.0, 250000),
    ("26000606", "F. Ganesh",    [58, 52, 49, 63, 55], 71.0, 300000),
    ("26000607", "G. Harshini",  [77, 72, 68, 74, 70], 80.0, 540000),
    ("26000608", "H. Ishwarya",  [64, 58, 66, 60, 59], 88.0, 410000),
    ("26000609", "I. Praveen",   [88, 84, 79, 90, 86], 92.0, 350000),
    ("26000610", "J. Nandini",   [70, 65, 72, 68, 74], 69.0, 220000),
]


def evaluate_applicant(applicant):
    """Check one applicant.

    Returns (is_eligible, aggregate, list_of_reasons).
    """
    roll_no, name, marks, attendance, income = applicant      # tuple unpacking

    aggregate = 0
    for mark in marks:
        aggregate = aggregate + mark
    aggregate = aggregate / len(marks)

    reasons = []

    if aggregate < MIN_AGGREGATE:
        reasons.append("aggregate %.1f is below %.0f" % (aggregate, MIN_AGGREGATE))

    for i in range(len(marks)):                               # subject wise check
        if marks[i] < MIN_SUBJECT_MARK:
            reasons.append("%s mark %d is below %d" % (SUBJECTS[i], marks[i], MIN_SUBJECT_MARK))

    if attendance < MIN_ATTENDANCE:
        reasons.append("attendance %.1f%% is below %.0f%%" % (attendance, MIN_ATTENDANCE))

    if income > MAX_FAMILY_INCOME:
        reasons.append("family income %d is above %d" % (income, MAX_FAMILY_INCOME))

    if len(reasons) == 0:
        return True, aggregate, reasons
    return False, aggregate, reasons


def ranking_key(record):
    """Tie breaking rule : aggregate high -> attendance high -> income low -> roll no low."""
    roll_no, name, aggregate, attendance, income = record
    return (-aggregate, -attendance, income, roll_no)


def print_line(char, width=78):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    print_line("=")
    print("        UNIVERSITY SCHOLARSHIP ALLOCATION - ELIGIBILITY REPORT")
    print("        Name : Jaya Surya Ravuri        Roll No : 26000542")
    print_line("=")
    print("Policy : aggregate >= %.0f | every subject >= %d | attendance >= %.0f%% | income <= Rs.%d"
          % (MIN_AGGREGATE, MIN_SUBJECT_MARK, MIN_ATTENDANCE, MAX_FAMILY_INCOME))
    print("Scholarships available (quota) : %d" % QUOTA)

    eligible = []
    rejected = []

    for applicant in APPLICANTS:
        ok, aggregate, reasons = evaluate_applicant(applicant)
        roll_no, name = applicant[0], applicant[1]
        if ok:
            attendance = applicant[3]
            income = applicant[4]
            eligible.append((roll_no, name, aggregate, attendance, income))
        else:
            rejected.append((roll_no, name, aggregate, reasons))

    # ranking the eligible applicants
    eligible.sort(key=ranking_key)

    print("")
    print("1. MERIT LIST OF ELIGIBLE APPLICANTS")
    print_line("-")
    print("%-4s %-10s %-14s %9s %9s %10s" %
          ("Rank", "Roll No", "Name", "Aggregate", "Attend%", "Income"))
    print_line("-")

    rank = 0
    for record in eligible:
        roll_no, name, aggregate, attendance, income = record      # tuple unpacking
        rank = rank + 1
        print("%-4d %-10s %-14s %9.2f %9.1f %10d" %
              (rank, roll_no, name, aggregate, attendance, income))

    if len(eligible) == 0:
        print("No applicant is eligible for the scholarship.")

    print_line("-")
    print("Total eligible : %d      Total rejected : %d" % (len(eligible), len(rejected)))

    # tie resolution log
    print("")
    print("2. TIE RESOLUTION LOG")
    print_line("-")
    ties_found = 0
    for i in range(len(eligible) - 1):
        current = eligible[i]
        nxt = eligible[i + 1]
        if abs(current[2] - nxt[2]) < 0.005:
            ties_found = ties_found + 1
            print("Tie on aggregate %.2f between %s and %s" %
                  (current[2], current[1], nxt[1]))
            if abs(current[3] - nxt[3]) > 0.005:
                print("   -> attendance decides : %.1f%% vs %.1f%%" % (current[3], nxt[3]))
            elif current[4] != nxt[4]:
                print("   -> income decides     : Rs.%d vs Rs.%d" % (current[4], nxt[4]))
            else:
                print("   -> roll number decides: %s vs %s" % (current[0], nxt[0]))
    if ties_found == 0:
        print("No tie was found in this batch, so every rank is decided by aggregate.")

    # rejected applicants with their reasons
    print("")
    print("3. APPLICATIONS NOT CONSIDERED (with reasons)")
    print_line("-")
    for record in rejected:
        roll_no, name, aggregate, reasons = record
        print("%s  %-14s aggregate = %.2f" % (roll_no, name, aggregate))
        for reason in reasons:
            print("      x %s" % reason)
    print_line("-")

    # final award list
    print("")
    print("4. FINAL AWARD LIST (top %d as per quota)" % QUOTA)
    print_line("-")
    award_count = min(QUOTA, len(eligible))
    for i in range(award_count):
        print("Scholarship %d : %s (%s) - aggregate %.2f" %
              (i + 1, eligible[i][1], eligible[i][0], eligible[i][2]))
    waiting = len(eligible) - award_count
    if waiting > 0:
        print("Waiting list   : %d eligible applicant(s) could not be accommodated." % waiting)
    print_line("=")
    print("End of report - University Scholarship Allocation")


main()
