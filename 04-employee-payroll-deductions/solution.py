"""
Case Study 04 : Employee Payroll and Deduction Analysis
------------------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, strings, lists, tuples, tuple unpacking.
"""

# ------------------------------ pay rules ------------------------------------
HRA_PERCENT = 20.0          # house rent allowance as % of basic
TRANSPORT_ALLOWANCE = 1600  # fixed amount every month
OVERTIME_RATE = 250         # rupees per overtime hour
PF_PERCENT = 12.0           # provident fund as % of basic
PROFESSIONAL_TAX = 200      # fixed amount

# progressive income tax on the monthly gross salary
# (from_amount, up_to_amount, rate in percent) - the last slab has no upper limit
TAX_SLABS = [
    (0, 25000, 0.0),
    (25000, 50000, 5.0),
    (50000, 100000, 10.0),
    (100000, -1, 20.0),
]

AUDIT_LIMIT = 50.0          # deductions above 50% of gross are flagged

# employee records
# (emp_id, name, designation, basic_pay, overtime_hours, incentive_percent)
EMPLOYEES = [
    ("EMP-101", "Ravuri Jaya Surya", "Software Trainee", 24000, 12, 4.0),
    ("EMP-102", "K. Divya Sri",      "Junior Engineer",  38000, 6, 6.0),
    ("EMP-103", "M. Suresh Babu",    "Senior Engineer",  62000, 18, 8.0),
    ("EMP-104", "P. Anitha",         "Team Lead",        85000, 0, 10.0),
    ("EMP-105", "T. Nagaraju",       "Manager",         120000, 4, 12.0),
    ("EMP-106", "S. Lakshmi",        "Support Executive",16500, 22, 3.0),
]


def tax_on(amount):
    """Progressive tax on the given monthly gross salary."""
    tax = 0.0
    for lower, upper, rate in TAX_SLABS:             # tuple unpacking
        if amount <= lower:
            break
        if upper == -1:
            taxable = amount - lower
        elif amount > upper:
            taxable = upper - lower
        else:
            taxable = amount - lower
        tax = tax + taxable * rate / 100.0
    return tax


def tax_breakup(amount):
    """Readable slab breakup of the tax, e.g. '25000 x 5.0% + 10000 x 10.0%'."""
    parts = []
    for lower, upper, rate in TAX_SLABS:
        if amount <= lower:
            break
        if upper == -1:
            taxable = amount - lower
        elif amount > upper:
            taxable = upper - lower
        else:
            taxable = amount - lower
        if rate > 0:
            parts.append("%d x %.1f%%" % (taxable, rate))
    if len(parts) == 0:
        return "no taxable slab used"
    text = ""
    for i in range(len(parts)):
        if i > 0:
            text = text + " + "
        text = text + parts[i]
    return text


def calculate_salary(employee):
    """Return a list of the computed salary components."""
    emp_id, name, designation, basic, ot_hours, incentive_percent = employee

    hra = basic * HRA_PERCENT / 100.0
    transport = TRANSPORT_ALLOWANCE
    overtime = ot_hours * OVERTIME_RATE
    incentive = basic * incentive_percent / 100.0

    gross = basic + hra + transport + overtime + incentive

    pf = basic * PF_PERCENT / 100.0
    tax = tax_on(gross)
    deductions = pf + tax + PROFESSIONAL_TAX
    net = gross - deductions

    deduction_percent = deductions / gross * 100.0

    return [basic, hra, transport, overtime, incentive, gross,
            pf, tax, PROFESSIONAL_TAX, deductions, net, deduction_percent]


def payslip(employee):
    """Print a payslip for one employee."""
    emp_id, name, designation, basic, ot_hours, incentive_percent = employee
    values = calculate_salary(employee)

    hra = values[1]
    transport = values[2]
    overtime = values[3]
    incentive = values[4]
    gross = values[5]
    pf = values[6]
    tax = values[7]
    deductions = values[9]
    net = values[10]
    deduction_percent = values[11]

    line = "+" + "-" * 58 + "+"
    print(line)
    print("| %-56s |" % ("EMPLOYEE PAYSLIP - MARCH 2026"))
    print(line)
    print("| Emp ID      : %-42s |" % emp_id)
    print("| Name        : %-42s |" % name)
    print("| Designation : %-42s |" % designation)
    print(line)
    print("| %-34s %21.2f |" % ("Basic Pay", basic))
    print("| %-34s %21.2f |" % ("House Rent Allowance (20% of basic)", hra))
    print("| %-34s %21.2f |" % ("Transport Allowance", transport))
    print("| %-34s %21.2f |" % ("Overtime (%d hrs x Rs.250)" % ot_hours, overtime))
    print("| %-34s %21.2f |" % ("Incentive (%.1f%% of basic)" % incentive_percent, incentive))
    print("| %-34s %21s |" % ("", "-" * 14))
    print("| %-34s %21.2f |" % ("GROSS SALARY", gross))
    print(line)
    print("| %-34s %21.2f |" % ("Provident Fund (12% of basic)", pf))
    print("| %-34s %21.2f |" % ("Income Tax", tax))
    print("| %-34s %21.2f |" % ("Professional Tax", PROFESSIONAL_TAX))
    print("| %-34s %21s |" % ("", "-" * 14))
    print("| %-34s %21.2f |" % ("TOTAL DEDUCTIONS", deductions))
    print(line)
    print("| %-34s %21.2f |" % ("NET SALARY PAYABLE", net))
    print(line)
    print("Tax slabs used : %s" % tax_breakup(gross))

    if deduction_percent > AUDIT_LIMIT:
        print("NOTE : deductions are %.1f%% of the gross salary,"
              % deduction_percent)
        print("       this payslip is kept in the audit list.")
    return values


def main():
    print("=" * 60)
    print(" EMPLOYEE PAYROLL AND DEDUCTION ANALYSIS - MARCH 2026")
    print(" Name : Jaya Surya Ravuri        Roll No : 26000542")
    print("=" * 60)
    print(" Rules : HRA 20%% of basic, transport Rs.%d, overtime Rs.%d per hour"
          % (TRANSPORT_ALLOWANCE, OVERTIME_RATE))
    print("         PF 12%% of basic, professional tax Rs.%d" % PROFESSIONAL_TAX)
    print("         Income tax slabs (monthly gross):")
    for lower, upper, rate in TAX_SLABS:
        if upper == -1:
            print("            above Rs.%-8d         -> %.1f%%" % (lower, rate))
        else:
            print("            Rs.%-6d to Rs.%-8d  -> %.1f%%" % (lower, upper, rate))

    summary = []
    audit = []

    for employee in EMPLOYEES:
        print("")
        values = payslip(employee)
        summary.append((employee[0], employee[1], values[5], values[9], values[10]))
        if values[11] > AUDIT_LIMIT:
            audit.append((employee[1], values[11]))

    print("")
    print("=" * 96)
    print(" PAYROLL SUMMARY")
    print("=" * 96)
    print("%-9s %-20s %12s %12s %12s %10s" %
          ("Emp ID", "Name", "Gross", "Deductions", "Net Pay", "Ded%"))
    print("-" * 96)

    total_gross = 0.0
    total_deductions = 0.0
    total_net = 0.0
    highest_net = -1.0
    highest_name = ""
    lowest_net = -1.0
    lowest_name = ""

    for emp_id, name, gross, deductions, net in summary:
        percent = deductions / gross * 100.0
        print("%-9s %-20s %12.2f %12.2f %12.2f %9.1f%%" %
              (emp_id, name, gross, deductions, net, percent))
        total_gross = total_gross + gross
        total_deductions = total_deductions + deductions
        total_net = total_net + net
        if net > highest_net:
            highest_net = net
            highest_name = name
        if lowest_net < 0 or net < lowest_net:
            lowest_net = net
            lowest_name = name

    print("-" * 96)
    print("%-9s %-20s %12.2f %12.2f %12.2f" %
          ("TOTAL", "6 employees", total_gross, total_deductions, total_net))
    print("=" * 96)
    print("Total gross salary of the team : Rs.%.2f" % total_gross)
    print("Total deductions               : Rs.%.2f" % total_deductions)
    print("Total amount to be transferred : Rs.%.2f" % total_net)
    print("Average net salary             : Rs.%.2f" % (total_net / len(summary)))
    print("Highest net salary             : Rs.%.2f (%s)" % (highest_net, highest_name))
    print("Lowest net salary              : Rs.%.2f (%s)" % (lowest_net, lowest_name))

    print("")
    print("AUDIT LIST (deductions more than %.0f%% of gross)" % AUDIT_LIMIT)
    print("-" * 96)
    if len(audit) == 0:
        print("No employee crossed the audit limit this month.")
    else:
        for name, percent in audit:
            print("%-20s deductions = %.1f%% of gross salary" % (name, percent))
    print("=" * 96)
    print("End of payroll report")


main()
