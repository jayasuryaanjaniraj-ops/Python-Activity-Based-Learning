# Flowcharts — Python Activity-Based Learning

Name: **Jaya Surya Ravuri** · Roll No: **26000542**

All ten flowcharts are collected here so that they are easy to read in one place.
The same flowchart is also kept inside the `README.md` of its own case-study folder.

## Symbols used

```
 ┌─────────────┐
 │  PROCESS    │   rectangle      -> a computation or an assignment
 └──────┬──────┘
        ▼
 ╱─────────────╲
╱  CONDITION ?  ╲   diamond        -> a decision (YES / NO branches)
╲─────────────╱
        ▼
    ┌────────┐
    │ START  │      rounded      -> start / stop of the program
    └────────┘
```

---

## 1. University Scholarship Allocation

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
   ┌──────────────────────────────┐
   │ Read policy limits           │
   │ MIN_AGG=60, MIN_SUB=50,      │
   │ MIN_ATT=75, MAX_INCOME=500000│
   └──────────────┬───────────────┘
                  ▼
      ┌───────────────────────┐
      │ eligible = []         │
      │ rejected = []         │
      └───────────┬───────────┘
                  ▼
     ┌────────────────────────┐◄───────────────────┐
     │ FOR each applicant     │                    │
     └───────────┬────────────┘                    │
                 ▼                                 │
     ┌────────────────────────┐                    │
     │ UNPACK applicant ->    │                    │
     │ roll,name,marks,att,inc│                    │
     └───────────┬────────────┘                    │
                 ▼                                 │
     ┌────────────────────────┐                    │
     │ aggregate = sum/len    │                    │
     │ reasons = []           │                    │
     └───────────┬────────────┘                    │
                 ▼                                 │
    ╱──────────────────────────────────╲           │
   ╱  aggregate<60 OR any mark<50 OR    ╲          │
   ╲  attendance<75 OR income>500000 ?  ╱          │
    ╲──────────────────────────────────╱           │
                 │                                 │
        ┌────────┴─────────┐                       │
       YES                 NO                      │
        │                  │                      │
        ▼                  ▼                      │
 ┌───────────────┐  ┌──────────────────┐            │
 │ append to     │  │ append to        │            │
 │ rejected with │  │ eligible list    │            │
 │ reason(s)     │  │                  │            │
 └───────┬───────┘  └────────┬─────────┘            │
         └──────────┬────────┘                      │
                    ▼                               │
           ╱─────────────────╲                      │
          ╱ more applicants ? ╲─────── YES ─────────┘
          ╲───────────────────╱
                    │ NO
                    ▼
     ┌────────────────────────────────┐
     │ SORT eligible by key:          │
     │ (-aggregate, -attendance,      │
     │  +income, +roll)               │
     └───────────────┬────────────────┘
                     ▼
     ┌────────────────────────────────┐
     │ PRINT ranked table + tie log   │
     │ PRINT rejected list + summary  │
     └───────────────┬────────────────┘
                     ▼
              ┌─────────────┐
              │    STOP     │
              └─────────────┘
```

---

## 2. Progressive Electricity Billing

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
   ┌───────────────────────────────┐
   │ Read slab table, fixed charge,│
   │ duty%, surcharge%, rebate%    │
   └───────────────┬───────────────┘
                   ▼
      ┌────────────────────────┐◄──────────────────┐
      │ FOR each month         │                   │
      └───────────┬────────────┘                   │
                  ▼                                │
      ┌────────────────────────┐                   │
      │ UNPACK (month, units)  │                   │
      └───────────┬────────────┘                   │
                  ▼                                │
      ┌────────────────────────┐                   │
      │ energy = 0             │                   │
      │ FOR each slab          │                   │
      └───────────┬────────────┘                   │
                  ▼                                │
      ┌────────────────────────┐                   │
      │ remaining = units-used │                   │
      └───────────┬────────────┘                   │
                  ▼                                │
    ╱────────────────────────────╲                 │
   ╱  remaining > 0 ?             ╲── NO ──┐       │
   ╲                              ╱        │       │
    ╲────────────────────────────╱         │       │
                 │ YES                     │       │
                 ▼                         │       │
   ╱────────────────────────────╲          │       │
  ╱  remaining > slab width ?    ╲         │       │
  ╲                              ╱         │       │
   ╲────────────────────────────╱          │       │
        │ YES           │ NO               │       │
        ▼               ▼                  │       │
 ┌─────────────┐ ┌──────────────────┐      │       │
 │ energy +=   │ │ energy += rem ×  │      │       │
 │ width × rate│ │ rate, remaining=0│      │       │
 └──────┬──────┘ └────────┬─────────┘      │       │
        └──────────┬──────┘                │       │
                   ▼                       │       │
                  (())◄────────────────────┘       │
                   ▼                               │
      ┌────────────────────────┐                   │
      │ bill = energy + fixed  │                   │
      │ bill += duty + surcharge                   │
      │ bill -= rebate         │                   │
      └───────────┬────────────┘                   │
                  ▼                                │
    ╱────────────────────────────╲                 │
   ╱  previous bill exists ?      ╲── NO ──┐       │
   ╲                              ╱        │       │
    ╲────────────────────────────╱         │       │
                 │ YES                     │       │
                 ▼                         │       │
   ┌──────────────────────────────┐        │       │
   │ change% = (bill-prev)/prev   │        │       │
   │ PRINT "UNUSUAL RISE" if >25% │        │       │
   └───────────────┬──────────────┘        │       │
                   │◄──────────────────────┘       │
                   ▼                               │
          ╱─────────────────╲                      │
         ╱  more months ?    ╲──────── YES ────────┘
         ╲───────────────────╱
                   │ NO
                   ▼
        ┌─────────────────────┐
        │ PRINT bill register │
        └──────────┬──────────┘
                   ▼
             ┌──────────┐
             │   STOP   │
             └──────────┘
```

---

## 3. Hospital Billing and Patient Classification

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌────────────────────────────────┐
  │ Read charge rates, concession   │
  │ rules, payment policy limits    │
  └───────────────┬────────────────┘
                  ▼
     ┌────────────────────────┐◄────────────────────┐
     │ FOR each patient       │                     │
     └───────────┬────────────┘                     │
                 ▼                                  │
     ┌────────────────────────┐                     │
     │ UNPACK record -> id,    │                    │
     │ consultation, diagnostics, treatment, days   │
     └───────────┬────────────┘                     │
                 ▼                                  │
     ┌────────────────────────┐                     │
     │ validate: any charge < 0 ?                   │
     │ any bill line missing / days > 60 ?          │
     └───────────┬────────────┘                     │
                 ▼                                  │
    ╱─────────────────────────────────╲             │
   ╱  constraint violated ?            ╲─ YES ─┐    │
   ╲                                   ╱       │    │
    ╲─────────────────────────────────╱        │    │
                 │ NO                          │    │
                 ▼                             ▼    │
     ┌────────────────────────┐   ┌──────────────────┐
     │ subtotal = sum of three│   │ PRINT "REJECTED  │
     │ + ward charge × days   │   │ - invalid record"│
     └───────────┬────────────┘   └────────┬─────────┘
                 ▼                         │        │
    ╱─────────────────────────────────╲    │        │
   ╱  days > 10 ?                     ╲    │        │
   ╲                                   ╱   │        │
    ╲─────────────────────────────────╱    │        │
         │ YES            │ NO             │        │
         ▼                ▼                │        │
  ┌──────────────┐ ┌──────────────┐        │        │
  │ concession=  │ │ concession=  │        │        │
  │ 10%          │ │ 0%           │        │        │
  └──────┬───────┘ └──────┬───────┘        │        │
         └────────┬───────┘                │        │
                  ▼                         │        │
    ╱─────────────────────────────────╲     │        │
   ╱  payment status = "INSURED" ?     ╲    │        │
   ╲                                   ╱    │        │
    ╲─────────────────────────────────╱     │        │
         │ YES            │ NO             │        │
         ▼                ▼                │        │
  ┌──────────────┐ ┌──────────────┐        │        │
  │ net = sub -  │ │ net = sub -  │        │        │
  │ 20% insurer  │ │ concession   │        │        │
  └──────┬───────┘ └──────┬───────┘        │        │
         └────────┬───────┘                │        │
                  ▼                         │        │
     ┌────────────────────────┐             │        │
     │ classify patient by net│             │        │
     │ bill slab (A/B/C/D)    │             │        │
     └───────────┬────────────┘             │        │
                 ▼                          │        │
     ┌────────────────────────┐             │        │
     │ PRINT bill + category  │             │        │
     └───────────┬────────────┘             │        │
                 ▼                          │        │
        ╱─────────────────╲                 │        │
       ╱  more patients ?  ╲── YES ─────────┼────────┘
       ╲───────────────────╱                │
                 │ NO                       │
                 ▼                          │
     ┌────────────────────────┐◄────────────┘
     │ PRINT category summary │
     │ (count + total per cat)│
     └───────────┬────────────┘
                 ▼
           ┌──────────┐
           │   STOP   │
           └──────────┘
```

---

## 4. Employee Payroll and Deduction Analysis

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌──────────────────────────────────┐
  │ Read basic pay, allowance %, OT   │
  │ rate, incentive %, tax slabs      │
  └───────────────┬──────────────────┘
                  ▼
     ┌────────────────────────┐◄──────────────────┐
     │ FOR each employee      │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ UNPACK (id,name,basic, │                   │
     │ hra%,ot_hours,incentive)                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ hra = basic × hra%/100 │                   │
     │ ot  = ot_hours × rate  │                   │
     │ inc = basic × inc%/100 │                   │
     │ gross = basic+hra+ot+inc                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ pf = 12% of basic      │                   │
     │ tax = 0, taxable=gross │                   │
     │ FOR each tax slab      │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
   ╱───────────────────────────────╲              │
  ╱  taxable > slab upper ?        ╲── NO ──┐     │
  ╲                               ╱         │     │
   ╲─────────────────────────────╱          │     │
               │ YES                        │     │
               ▼                            │     │
   ┌────────────────────────┐               │     │
   │ tax += (upper-lower)×  │               │     │
   │ slab rate; taxable=0   │               │     │
   └───────────┬────────────┘               │     │
               ▼                            │     │
              (())◄─────────────────────────┘     │
               ▼                                  │
   ┌────────────────────────┐                     │
   │ tax += taxable × rate  │                     │
   │ deductions = pf + tax  │                     │
   │ net = gross - deductions                     │
   └───────────┬────────────┘                     │
               ▼                                  │
   ╱───────────────────────────────╲              │
  ╱  deductions > 50% of gross ?   ╲─ YES ─┐      │
  ╲                               ╱       │      │
   ╲─────────────────────────────╱        │      │
               │ NO                      ▼      │
               │            ┌──────────────────────┐
               │            │ flag record for audit│
               │            └──────────┬───────────┘
               ▼                       │          │
   ┌────────────────────────┐◄─────────┘          │
   │ PRINT formatted salary │                     │
   │ statement (payslip)    │                     │
   └───────────┬────────────┘                     │
               ▼                                  │
      ╱─────────────────╲                         │
     ╱  more employees ? ╲──────── YES ────────────┘
     ╲───────────────────╱
               │ NO
               ▼
   ┌────────────────────────┐
   │ PRINT payroll totals   │
   └───────────┬────────────┘
               ▼
         ┌──────────┐
         │   STOP   │
         └──────────┘
```

---

## 5. Multi-Plan Telecommunications Cost Optimization

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌────────────────────────────────┐
  │ Read usage (data, calls, sms,  │
  │ validity) and plan table       │
  └───────────────┬────────────────┘
                  ▼
     ┌────────────────────────┐◄──────────────────┐
     │ FOR each plan          │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ UNPACK (name, price,   │                   │
     │ data, calls, sms, days)│                   │
     └───────────┬────────────┘                   │
                 ▼                                │
   ╱───────────────────────────────╲              │
  ╱  required validity > plan days ╲─ YES ─┐      │
  ╲                               ╱       │      │
   ╲─────────────────────────────╱        │      │
               │ NO                      ▼      │
               │              ┌───────────────────┐
               │              │ mark NOT ELIGIBLE │
               │              └────────┬──────────┘
               ▼                       │         │
   ┌────────────────────────┐◄─────────┘         │
   │ excess_data = max(0, used - data)           │
   │ excess_call = max(0, used - calls)          │
   │ excess_sms  = max(0, used - sms)            │
   └───────────┬────────────┘                    │
               ▼                                 │
   ┌────────────────────────────────┐            │
   │ total = price                  │            │
   │      + excess_data × rate      │            │
   │      + excess_call × rate      │            │
   │      + excess_sms  × rate      │            │
   └───────────┬────────────────────┘            │
               ▼                                 │
   ╱───────────────────────────────╲             │
  ╱  total <= budget ?             ╲─ NO ──┐     │
  ╲                               ╱       │     │
   ╲─────────────────────────────╱        │     │
               │ YES                     ▼     │
               ▼            ┌────────────────────┐
   ┌────────────────────┐   │ keep as "over      │
   │ store as feasible  │   │ budget" option     │
   └─────────┬──────────┘   └─────────┬──────────┘
             └──────────┬─────────────┘           │
                        ▼                        │
          ╱─────────────────────╲                │
         ╱  more plans ?         ╲── YES ─────────┘
         ╲───────────────────────╱
                        │ NO
                        ▼
          ╱─────────────────────╲
         ╱  feasible list empty ? ╲── YES ──► PRINT "no plan fits budget"
         ╲───────────────────────╱
                        │ NO
                        ▼
   ┌────────────────────────────────┐
   │ SORT feasible by total (asc),   │
   │ tie-break by more validity days │
   └───────────────┬────────────────┘
                   ▼
   ┌────────────────────────────────┐
   │ PRINT comparison table          │
   │ PRINT best plan + savings vs 2nd│
   └───────────────┬────────────────┘
                   ▼
             ┌──────────┐
             │   STOP   │
             └──────────┘
```

---

## 6. Railway Fare and Reservation Calculator

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌──────────────────────────────────┐
  │ Read train, distance slabs, class │
  │ multipliers, concession table     │
  └───────────────┬──────────────────┘
                  ▼
     ┌────────────────────────┐◄────────────────────┐
     │ FOR each passenger     │                     │
     └───────────┬────────────┘                     │
                 ▼                                  │
     ┌────────────────────────┐                     │
     │ UNPACK (name, age,     │                     │
     │ class, is_cancelled)   │                     │
     └───────────┬────────────┘                     │
                 ▼                                  │
     ┌────────────────────────┐                     │
     │ base = 0               │                     │
     │ FOR each distance slab │                     │
     └───────────┬────────────┘                     │
                 ▼                                  │
   ╱───────────────────────────────╲               │
  ╱  distance inside this slab ?   ╲── NO ──┐      │
  ╲                               ╱         │      │
   ╲─────────────────────────────╱          │      │
               │ YES                        │      │
               ▼                            │      │
   ┌────────────────────────┐               │      │
   │ base += km_in_slab×rate│               │      │
   │ (stop after last slab) │               │      │
   └───────────┬────────────┘               │      │
               ▼                            │      │
              (())◄─────────────────────────┘      │
               ▼                                   │
   ┌────────────────────────┐                      │
   │ fare = base × class    │                      │
   │ multiplier             │                      │
   └───────────┬────────────┘                      │
               ▼                                   │
   ╱───────────────────────────────╲               │
  ╱  age < 12 ?                    ╲              │
  ╲                               ╱               │
   ╲─────────────────────────────╱                │
        │ YES        │ NO                          │
        ▼            ▼                            │
 ┌────────────┐  ╱──────────────────────╲         │
 │ fare -50%  │ ╱  age >= 60 or female ? ╲         │
 └─────┬──────┘ ╲                      ╱          │
       │         ╲────────────────────╱           │
       │           │ YES       │ NO                │
       │           ▼           ▼                  │
       │    ┌────────────┐ ┌────────────┐         │
       │    │ fare -30%  │ │ no change  │         │
       │    └─────┬──────┘ └─────┬──────┘         │
       └──────────┴──────────────┘                │
                        ▼                          │
   ┌────────────────────────────────┐             │
   │ fare += reservation fee        │             │
   │ fare += service tax            │             │
   └───────────┬────────────────────┘             │
               ▼                                  │
   ╱───────────────────────────────╲              │
  ╱  is_cancelled ?                ╲─ YES ──┐     │
  ╲                               ╱        │     │
   ╲─────────────────────────────╱         │     │
               │ NO                       ▼     │
               │            ┌────────────────────────┐
               │            │ refund = fare − penalty│
               │            │ (penalty by hours)     │
               │            └───────────┬────────────┘
               ▼                        │        │
   ┌────────────────────────┐◄──────────┘        │
   │ PRINT passenger ticket │                     │
   └───────────┬────────────┘                     │
               ▼                                  │
      ╱────────────────────╲                      │
     ╱  more passengers ?   ╲──────── YES ─────────┘
     ╲──────────────────────╱
               │ NO
               ▼
   ┌────────────────────────┐
   │ PRINT PNR total, count │
   └───────────┬────────────┘
               ▼
         ┌──────────┐
         │   STOP   │
         └──────────┘
```

---

## 7. Retail Billing with Multiple Discount Rules

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌────────────────────────────────┐
  │ Read product master (code, name,│
  │ price, category, tax%)          │
  └───────────────┬────────────────┘
                  ▼
     ┌────────────────────────┐◄──────────────────┐
     │ FOR each basket item   │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ UNPACK (code, qty)     │                   │
     │ look up product master │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
   ╱───────────────────────────────╲              │
  ╱  code found and qty > 0 ?      ╲─ NO ──┐      │
  ╲                               ╱       │      │
   ╲─────────────────────────────╱        │      │
               │ YES                      ▼      │
               │            ┌──────────────────────┐
               │            │ skip line, add error │
               │            └──────────┬───────────┘
               ▼                       │         │
   ┌────────────────────────┐◄─────────┘         │
   │ line = price × qty     │                     │
   │ tax  = line × tax%/100 │                     │
   │ total += line + tax    │                     │
   └───────────┬────────────┘                     │
               ▼                                  │
      ╱────────────────────╲                      │
     ╱  more basket items ? ╲─────── YES ──────────┘
     ╲──────────────────────╱
               │ NO
               ▼
   ┌────────────────────────────────┐
   │ category discount:             │
   │ FOR each category, if its line │
   │ total >= threshold → discount  │
   └───────────────┬────────────────┘
                   ▼
   ╱───────────────────────────────╲
  ╱  bill_total >= 5000 ?          ╲─ YES ─► extra 5% (capped at ₹750)
  ╲                               ╱
   ╲─────────────────────────────╱
                   ▼
   ╱───────────────────────────────╲
  ╱  total_discount > max limit ?  ╲─ YES ─► clamp to max limit
  ╲                               ╱
   ╲─────────────────────────────╱
                   ▼
   ┌────────────────────────────────┐
   │ payable = total - discount +   │
   │ delivery + rounding adjustment │
   └───────────────┬────────────────┘
                   ▼
   ┌────────────────────────────────┐
   │ PRINT itemised invoice         │
   │ PRINT discount breakdown       │
   └───────────────┬────────────────┘
                   ▼
             ┌──────────┐
             │   STOP   │
             └──────────┘
```

---

## 8. Manufacturing Cost and Profitability Analysis

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌────────────────────────────────┐
  │ Read material rates, labour     │
  │ rate, machine hour rate,        │
  │ wastage %, selling price, target│
  └───────────────┬────────────────┘
                  ▼
     ┌────────────────────────┐◄──────────────────┐
     │ FOR each product batch │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ UNPACK (product, units,│                   │
     │ material_kg, lab_hours,│                   │
     │ machine_hours, price)  │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ wastage = material_kg ×│                   │
     │ wastage% / 100         │                   │
     │ usable  = material -   │                   │
     │ wastage                │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
   ╱───────────────────────────────╲              │
  ╱  usable <= 0 ?                 ╲─ YES ──┐     │
  ╲                               ╱        │     │
   ╲─────────────────────────────╱         │     │
               │ NO                       ▼     │
               │            ┌──────────────────────┐
               │            │ reject batch (100%   │
               │            │ wastage / bad input) │
               │            └──────────┬───────────┘
               ▼                       │         │
   ┌────────────────────────┐◄─────────┘         │
   │ mat_cost = usable ×    │                     │
   │ material rate          │                     │
   │ lab_cost = lab_hours × │                     │
   │ labour rate            │                     │
   │ mach_cost= mach_hours× │                     │
   │ machine rate           │                     │
   └───────────┬────────────┘                     │
               ▼                                  │
   ┌────────────────────────┐                     │
   │ cost_per_unit = (mat + │                     │
   │ lab + mach)/units      │                     │
   │ revenue = units × price│                     │
   │ profit  = revenue -    │                     │
   │ total cost             │                     │
   └───────────┬────────────┘                     │
               ▼                                  │
   ╱───────────────────────────────╲              │
  ╱  profit <= 0 ?                 ╲─ YES ─► "LOSS"
  ╲                               ╱
   ╲─────────────────────────────╱
               │ NO
               ▼
   ╱───────────────────────────────╲
  ╱  margin >= target margin ?     ╲─ NO ──► "BELOW TARGET"
  ╲                               ╱
   ╲─────────────────────────────╱
               │ YES
               ▼
      ┌──────────────────────┐
      │ "MEETS TARGET"       │
      └──────────┬───────────┘
                 ▼
        ╱────────────────────╲
       ╱  more batches ?      ╲── YES ───────────┘
       ╲──────────────────────╱
                 │ NO
                 ▼
   ┌────────────────────────────────┐
   │ PRINT cost sheet per product   │
   │ PRINT best / worst product     │
   └───────────────┬────────────────┘
                   ▼
             ┌──────────┐
             │   STOP   │
             └──────────┘
```

---

## 9. Multi-Currency Travel Budget Analysis

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌────────────────────────────────┐
  │ Read exchange rates, fee %,    │
  │ planned budget (in INR)        │
  └───────────────┬────────────────┘
                  ▼
     ┌────────────────────────┐◄──────────────────┐
     │ FOR each expense       │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
     ┌────────────────────────┐                   │
     │ UNPACK (category,      │                   │
     │ amount, currency)      │                   │
     └───────────┬────────────┘                   │
                 ▼                                │
   ╱───────────────────────────────╲              │
  ╱  currency in rate table ?      ╲─ NO ──┐      │
  ╲                               ╱       │      │
   ╲─────────────────────────────╱        │      │
               │ YES                      ▼      │
               │            ┌──────────────────────┐
               │            │ flag "rate missing", │
               │            │ skip expense         │
               │            └──────────┬───────────┘
               ▼                       │         │
   ┌────────────────────────┐◄─────────┘         │
   │ conv_fee = amount ×    │                     │
   │ fee% / 100             │                     │
   │ inr = (amount+conv_fee)│                     │
   │     × rate             │                     │
   └───────────┬────────────┘                     │
               ▼                                  │
   ┌────────────────────────┐                     │
   │ category_total += inr  │                     │
   │ grand_total    += inr  │                     │
   └───────────┬────────────┘                     │
               ▼                                  │
      ╱────────────────────╲                      │
     ╱  more expenses ?     ╲─────── YES ──────────┘
     ╲──────────────────────╱
               │ NO
               ▼
   ┌────────────────────────────────┐
   │ find category with max total   │
   │ (loop through category_totals) │
   └───────────────┬────────────────┘
                   ▼
   ╱───────────────────────────────╲
  ╱  grand_total <= budget ?       ╲─ YES ─► "WITHIN BUDGET"
  ╲                               ╱            │
   ╲─────────────────────────────╱             │
               │ NO                            │
               ▼                               │
   ┌────────────────────────┐                  │
   │ over = grand - budget  │                  │
   │ "OVER BUDGET by ..."   │                  │
   └───────────┬────────────┘                  │
               ▼                               │
   ┌────────────────────────┐◄─────────────────┘
   │ PRINT expense table in │
   │ INR + share %, largest │
   │ category, budget verdict│
   └───────────┬────────────┘
               ▼
         ┌──────────┐
         │   STOP   │
         └──────────┘
```

---

## 10. Campus Event Financial Planning

```
        ┌─────────────┐
        │    START    │
        └──────┬──────┘
               ▼
  ┌────────────────────────────────┐
  │ Read cost heads (venue, equip, │
  │ catering per head, transport,  │
  │ certificates) + sponsorship    │
  └───────────────┬────────────────┘
                  ▼
   ┌────────────────────────┐
   │ fixed = venue+equip+   │
   │ transport+certificates │
   │ variable = catering/head│
   └───────────┬────────────┘
               ▼
   ┌────────────────────────┐
   │ total_cost(n) = fixed  │
   │ + variable × n         │
   └───────────┬────────────┘
               ▼
   ╱───────────────────────────────╲
  ╱  sponsorship > total_cost ?    ╲─ YES ─► "fully sponsored, fee = 0"
  ╲                               ╱
   ╲─────────────────────────────╱
               │ NO
               ▼
   ┌────────────────────────┐
   │ shortfall = total −    │
   │ sponsorship            │
   │ fee = shortfall / n    │
   └───────────┬────────────┘
               ▼
   ╱───────────────────────────────╲
  ╱  fee > max_fee ?               ╲─ YES ─► increase n, recompute
  ╲                               ╱
   ╲─────────────────────────────╱
               │ NO
               ▼
   ┌────────────────────────────────┐
   │ break-even: smallest n with    │
   │ n × fee >= total_cost(n)       │
   └───────────────┬────────────────┘
                   ▼
   ┌────────────────────────────────┐
   │ FOR n = 1 to max_participants  │
   │   compute fee, keep first n    │
   │   where fee <= max_fee         │
   └───────────────┬────────────────┘
                   ▼
   ┌────────────────────────────────┐
   │ PRINT budget table, per-head   │
   │ contribution, break-even count │
   └───────────────┬────────────────┘
                   ▼
             ┌──────────┐
             │   STOP   │
             └──────────┘
```

---

*End of flowcharts — Jaya Surya Ravuri (26000542)*
