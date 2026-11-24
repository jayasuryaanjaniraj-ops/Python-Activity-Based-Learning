"""
Case Study 03 : Hospital Billing and Patient Classification
-----------------------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, strings, lists, tuples, tuple unpacking.
"""

# --------------------------------- hospital rates ----------------------------
CONSULTATION_FEE = 450.0        # general consultation
SPECIALIST_FEE = 900.0          # specialist consultation
WARD_CHARGE_PER_DAY = 1200.0    # general ward
MAX_STAY_DAYS = 60              # beyond this the record is treated as invalid

# concession policy
LONG_STAY_DAYS = 7              # stay of more than 7 days gets a concession
LONG_STAY_CONCESSION = 8.0      # percent
SENIOR_AGE = 60
SENIOR_CONCESSION = 5.0         # percent
INSURANCE_SHARE = 20.0          # percent borne by the insurer

# payment policy used for the classification
POLICY_LIMIT = 25000.0          # bills above this need a payment plan
MIN_TOKEN_PERCENT = 25.0        # token amount to be paid before discharge

# patient records
# (patient_id, name, age, consultant_type, consultation,
#  diagnostics, treatment, ward_days, insurance)
PATIENTS = [
    ("P-1001", "Ravuri Jaya Surya", 20, "general", 450, 1800, 6400, 4, "self"),
    ("P-1002", "S. Lakshmi Devi",   67, "specialist", 900, 4200, 18500, 9, "insured"),
    ("P-1003", "M. Anil Kumar",     35, "general", 450, 900, 0, 1, "self"),
    ("P-1004", "T. Bhavani",        52, "specialist", 900, 12500, 42000, 12, "insured"),
    ("P-1005", "K. Ramesh",         44, "general", 450, 2600, 9800, 6, "insured"),
    ("P-1006", "V. Padmavathi",     71, "specialist", 900, 7500, 22000, 15, "self"),
    ("P-1007", "N. Kiran",          29, "general", 450, -300, 5400, 3, "self"),
    ("P-1008", "B. Sravani",        61, "general", 450, 3100, 7600, 8, "insured"),
]


def category_of(bill):
    """Classify the payable amount."""
    if bill < 5000:
        return "A - minor"
    elif bill < 15000:
        return "B - moderate"
    elif bill < 30000:
        return "C - major"
    else:
        return "D - critical"


def validate(patient):
    """Return a list of problems found in the record (empty means valid)."""
    pid, name, age, consultant, consult, diag, treat, days, insurance = patient
    problems = []

    if age < 0 or age > 120:
        problems.append("age %d is out of range" % age)
    if consult < 0:
        problems.append("consultation charge is negative")
    if diag < 0:
        problems.append("diagnostic charge %d is negative" % diag)
    if treat < 0:
        problems.append("treatment charge is negative")
    if days < 0:
        problems.append("ward days is negative")
    if days > MAX_STAY_DAYS:
        problems.append("stay of %d days exceeds the limit of %d" % (days, MAX_STAY_DAYS))
    if consultant != "general" and consultant != "specialist":
        problems.append("unknown consultant type '%s'" % consultant)
    if insurance != "self" and insurance != "insured":
        problems.append("unknown payment mode '%s'" % insurance)
    if consult > 0 and consultant == "general" and consult != CONSULTATION_FEE:
        problems.append("consultation fee does not match the general rate")
    if consult > 0 and consultant == "specialist" and consult != SPECIALIST_FEE:
        problems.append("consultation fee does not match the specialist rate")

    return problems


def bill_of(patient):
    """Compute the bill of a valid patient record."""
    pid, name, age, consultant, consult, diag, treat, days, insurance = patient

    ward = days * WARD_CHARGE_PER_DAY
    subtotal = consult + diag + treat + ward

    concession_percent = 0.0
    concession_notes = []

    if days > LONG_STAY_DAYS:
        concession_percent = concession_percent + LONG_STAY_CONCESSION
        concession_notes.append("long stay %.0f%%" % LONG_STAY_CONCESSION)
    if age >= SENIOR_AGE:
        concession_percent = concession_percent + SENIOR_CONCESSION
        concession_notes.append("senior citizen %.0f%%" % SENIOR_CONCESSION)

    concession = subtotal * concession_percent / 100.0
    after_concession = subtotal - concession

    insurer_paid = 0.0
    if insurance == "insured":
        insurer_paid = after_concession * INSURANCE_SHARE / 100.0
    payable = after_concession - insurer_paid

    if len(concession_notes) == 0:
        note_text = "none"
    else:
        note_text = " + ".join(concession_notes)

    return subtotal, ward, concession_percent, concession, insurer_paid, payable, note_text


def payment_plan(bill):
    """Decide how the patient has to pay."""
    if bill <= POLICY_LIMIT:
        return "FULL SETTLEMENT at discharge"
    token = bill * MIN_TOKEN_PERCENT / 100.0
    return "INSTALMENT PLAN - pay Rs.%.2f token now, balance in 3 EMIs" % token


def separator(char="=", width=94):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    separator()
    print("          HOSPITAL BILLING AND PATIENT CLASSIFICATION - DAILY STATEMENT")
    print("          Name : Jaya Surya Ravuri        Roll No : 26000542")
    separator()
    print("Rates    : consultation Rs.450 (general) / Rs.900 (specialist), ward Rs.1200 per day")
    print("Concession : %.0f%% for a stay longer than %d days, %.0f%% for age %d and above"
          % (LONG_STAY_CONCESSION, LONG_STAY_DAYS, SENIOR_CONCESSION, SENIOR_AGE))
    print("Insurance  : insurer bears %.0f%% of the amount after concession"
          % INSURANCE_SHARE)
    print("Payment    : bills above Rs.%.0f need a %.0f%% token and 3 instalments"
          % (POLICY_LIMIT, MIN_TOKEN_PERCENT))
    print("Categories : A < 5000 <= B < 15000 <= C < 30000 <= D")

    valid_records = []
    rejected_records = []

    for patient in PATIENTS:
        problems = validate(patient)
        if len(problems) == 0:
            valid_records.append(patient)
        else:
            rejected_records.append((patient, problems))

    print("")
    separator()
    print("BILLS OF VALID PATIENT RECORDS")
    separator("-")
    print("%-8s %-18s %3s %-10s %9s %9s %9s %5s %10s %8s" %
          ("PID", "Patient", "Age", "Consult", "Consult", "Diagnostics",
           "Treatment", "Days", "Subtotal", "Conc%"))
    separator("-")

    total_billed = 0.0
    total_collected = 0.0
    total_insured = 0.0
    counts = {"A": 0, "B": 0, "C": 0, "D": 0}

    for patient in valid_records:
        pid, name, age, consultant, consult, diag, treat, days, insurance = patient
        subtotal, ward, conc_percent, concession, insurer_paid, payable, note = bill_of(patient)

        print("%-8s %-18s %3d %-10s %9.0f %9d %9d %5d %10.2f %8.1f" %
              (pid, name, age, consultant, consult, diag, treat, days, subtotal, conc_percent))
        print("         ward charge %.2f | concession %.2f (%s) | insurer %.2f | PAYABLE %.2f"
              % (ward, concession, note, insurer_paid, payable))

        total_billed = total_billed + subtotal
        total_collected = total_collected + payable
        total_insured = total_insured + insurer_paid

        category = category_of(payable)
        counts[category[0]] = counts[category[0]] + 1

    separator("-")
    print("Subtotal billed      : Rs.%.2f" % total_billed)
    print("Collected from patients : Rs.%.2f" % total_collected)
    print("Paid by insurers     : Rs.%.2f" % total_insured)

    print("")
    separator()
    print("PATIENT CLASSIFICATION AND PAYMENT INSTRUCTION")
    separator("-")
    print("%-8s %-18s %12s  %-14s %s" % ("PID", "Patient", "Payable", "Category", "Payment route"))
    separator("-")
    for patient in valid_records:
        pid, name = patient[0], patient[1]
        payable = bill_of(patient)[5]
        category = category_of(payable)
        print("%-8s %-18s %12.2f  %-14s %s" %
              (pid, name, payable, category, payment_plan(payable)))

    separator("-")
    print("Category wise count :  A = %d   B = %d   C = %d   D = %d" %
          (counts["A"], counts["B"], counts["C"], counts["D"]))

    print("")
    separator()
    print("RECORDS REJECTED BY THE BILLING CONSTRAINTS")
    separator("-")
    if len(rejected_records) == 0:
        print("No record was rejected.")
    for patient, problems in rejected_records:
        pid, name = patient[0], patient[1]
        print("%s  %-18s" % (pid, name))
        for problem in problems:
            print("      x %s" % problem)
    separator("-")
    print("Valid records : %d      Rejected records : %d" %
          (len(valid_records), len(rejected_records)))
    separator()
    print("End of hospital billing statement")


main()
