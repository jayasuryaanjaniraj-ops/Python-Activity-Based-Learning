# Python Activity-Based Learning

**Subject:** Python Programming
**Activity:** Select any 10 case studies and develop complete Python solutions

**Name:** Jaya Surya Ravuri
**Roll No:** 26000542

---

## Case studies selected

| # | Case study (question number in the activity sheet) | Folder |
|---|---|---|
| 1 | University Scholarship Allocation (#1) | [01-university-scholarship-allocation](01-university-scholarship-allocation/) |
| 2 | Progressive Electricity Billing (#2) | [02-progressive-electricity-billing](02-progressive-electricity-billing/) |
| 3 | Hospital Billing and Patient Classification (#3) | [03-hospital-billing-classification](03-hospital-billing-classification/) |
| 4 | Employee Payroll and Deduction Analysis (#4) | [04-employee-payroll-deductions](04-employee-payroll-deductions/) |
| 5 | Multi-Plan Telecommunications Cost Optimization (#5) | [05-telecom-plan-optimization](05-telecom-plan-optimization/) |
| 6 | Railway Fare and Reservation Calculator (#6) | [06-railway-fare-reservation](06-railway-fare-reservation/) |
| 7 | Retail Billing with Multiple Discount Rules (#7) | [07-retail-billing-discounts](07-retail-billing-discounts/) |
| 8 | Manufacturing Cost and Profitability Analysis (#8) | [08-manufacturing-cost-profitability](08-manufacturing-cost-profitability/) |
| 9 | Multi-Currency Travel Budget Analysis (#9) | [09-travel-budget-multicurrency](09-travel-budget-multicurrency/) |
| 10 | Campus Event Financial Planning (#10) | [10-campus-event-financial-planning](10-campus-event-financial-planning/) |

All ten flowcharts are also collected in one place: [FLOWCHARTS.md](FLOWCHARTS.md)

## What is submitted in each folder

Every case study folder contains the deliverables asked for in the activity:

| File | Contents |
|---|---|
| `README.md` | problem statement, objectives, assumptions, algorithm, flowchart, pseudocode, test case table, output and conclusion |
| `solution.py` | the Python program |
| `test_cases.py` | the test cases written to check the program |
| `output.txt` | the output of the program |
| `output_screenshot.png` | screenshot of the output |

## Syllabus topics covered

Only the assigned syllabus is used — no external library, no file handling and no
classes.

| Topic | Where it is used |
|---|---|
| Variables and data types | every program |
| Operators | percentages, slab rates, comparisons |
| Conditional statements | eligibility, classification, discount and penalty rules |
| Loops | slab computation, record processing, break even search |
| Strings | `%` formatting, `join`, alignment of the reports |
| Pattern generation | bar chart of `#` in case 9, the payslip box in case 4 |
| Lists | records, baskets, expense lists, results |
| Nested lists | lists inside the records and result rows |
| Tuples | tariff tables, product master, passenger and batch records |
| Tuple operations | indexing, comparison, sorting key |
| Tuple unpacking | `a, b, c = record` in every program |

## How to run

Only Python 3 is needed, no packages.

```bash
# run any solution
python3 01-university-scholarship-allocation/solution.py

# run the test cases of any case study
python3 01-university-scholarship-allocation/test_cases.py
```

The programs are not interactive — all the input data is kept inside the program
so that the output is the same on every machine.

## Checking all ten at once

```bash
for d in 0*/; do
    echo "== $d"
    python3 "$d/solution.py" > /dev/null && echo "  solution ok"
    python3 "$d/test_cases.py" | tail -2
done
```

Test case summary of the ten case studies:

| Case study | Test cases | Result |
|---|---|---|
| 01 University Scholarship Allocation | 12 | all passed |
| 02 Progressive Electricity Billing | 15 | all passed |
| 03 Hospital Billing and Classification | 21 | all passed |
| 04 Employee Payroll and Deductions | 20 | all passed |
| 05 Telecom Plan Optimization | 20 | all passed |
| 06 Railway Fare and Reservation | 32 | all passed |
| 07 Retail Billing with Discounts | 25 | all passed |
| 08 Manufacturing Cost and Profitability | 26 | all passed |
| 09 Travel Budget (Multi-Currency) | 27 | all passed |
| 10 Campus Event Financial Planning | 23 | all passed |
| **Total** | **221** | **all passed** |

## Notes

- All the data used in the programs (names, marks, prices, tariffs, distances,
  exchange rates) is hypothetical sample data.
- The names in the sample records are made up except my own name, which is used
  as the first record of every program so that the printout shows whose work it
  is.
- Every program prints the name and the roll number in its header so the output
  screenshot can be identified easily.
- Submission link: this repository (`Python-Activity-Based-Learning`), submitted
  after the Dussehra holidays.
