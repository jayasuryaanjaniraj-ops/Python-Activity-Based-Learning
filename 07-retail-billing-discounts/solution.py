"""
Case Study 07 : Retail Billing with Multiple Discount Rules
----------------------------------------------------------
Python Activity-Based Learning
Name    : Jaya Surya Ravuri
Roll No : 26000542

Syllabus topics used : variables, data types, operators, conditional
statements, loops, strings, lists, tuples, tuple unpacking.
"""

# ------------------------------- shop details --------------------------------
SHOP_NAME = "Sri Lakshmi Super Market, Vijayawada"
BILL_NO = "VJA/2026/0417"
CUSTOMER = "Ravuri Jaya Surya"
CUSTOMER_PHONE = "98XXXXXX42"

# ------------------------------ product master -------------------------------
# (code, name, category, unit_price, tax_percent)
PRODUCTS = [
    ("R101", "Rice 25 kg bag",       "grocery", 1450.00, 5.0),
    ("R102", "Sunflower oil 5 L",    "grocery",  780.00, 5.0),
    ("R103", "Toor dal 2 kg",        "grocery",  310.00, 5.0),
    ("D201", "Detergent 4 kg",       "household", 420.00, 18.0),
    ("D202", "Dish wash gel 750 ml", "household", 185.00, 18.0),
    ("C301", "Chocolate gift pack",  "confectionery", 650.00, 18.0),
    ("C302", "Biscuit combo pack",   "confectionery", 240.00, 18.0),
    ("E401", "LED bulb 9 W",         "electrical", 130.00, 12.0),
    ("E402", "Extension board",      "electrical", 560.00, 12.0),
]

# ------------------------------- basket --------------------------------------
# (product_code, quantity)
BASKET = [
    ("R101", 1),
    ("R103", 2),
    ("R102", 2),
    ("D201", 1),
    ("C301", 3),
    ("C302", 4),
    ("E401", 3),
    ("E402", 2),
    ("D202", -2),
    ("X999", 2),
]

# ----------------------------- discount rules --------------------------------
# category discount : (category, minimum line value, discount percent)
CATEGORY_DISCOUNTS = [
    ("grocery", 2000.0, 5.0),
    ("household", 400.0, 8.0),
    ("confectionery", 900.0, 10.0),
    ("electrical", 1000.0, 6.0),
]

BILL_DISCOUNT_THRESHOLD = 5000.0     # bill value above which an extra discount
BILL_DISCOUNT_PERCENT = 5.0           # is given
MAX_DISCOUNT_AMOUNT = 900.0           # maximum total discount allowed
HOME_DELIVERY_CHARGE = 60.0
FREE_DELIVERY_ABOVE = 3000.0


def find_product(code):
    """Return the product tuple for the given code, or None."""
    for product in PRODUCTS:
        if product[0] == code:
            return product
    return None


def category_discount_percent(category, line_value):
    """Return the discount percent applicable for a category line."""
    for cat, minimum, percent in CATEGORY_DISCOUNTS:
        if cat == category and line_value >= minimum:
            return percent
    return 0.0


def separator(char="-", width=88):
    line = ""
    for _ in range(width):
        line = line + char
    print(line)


def main():
    print("=" * 88)
    print(" " * 22 + SHOP_NAME)
    print(" " * 20 + "TAX INVOICE / RETAIL BILL")
    separator("=", 88)
    print("Bill No : %s        Date : 17-03-2026        Time : 18:42" % BILL_NO)
    print("Customer: %s      Mobile : %s" % (CUSTOMER, CUSTOMER_PHONE))
    separator("=", 88)
    print("%-6s %-22s %-14s %4s %9s %9s %6s %10s" %
          ("Code", "Product", "Category", "Qty", "Rate", "Value", "Tax%", "Tax Rs"))

    items = []
    errors = []
    category_totals = {}
    tax_total = 0.0
    gross_total = 0.0

    for code, qty in BASKET:                        # tuple unpacking
        product = find_product(code)

        if product is None:
            errors.append("Product code %s is not in the master list - line skipped"
                          % code)
            continue
        if qty <= 0:
            errors.append("Quantity %d for %s is not valid - line skipped"
                          % (qty, product[1]))
            continue

        p_code, name, category, price, tax_percent = product
        value = price * qty
        tax = value * tax_percent / 100.0

        print("%-6s %-22s %-14s %4d %9.2f %9.2f %6.1f %10.2f" %
              (p_code, name, category, qty, price, value, tax_percent, tax))

        items.append((p_code, name, category, qty, price, value, tax_percent, tax))

        if category in category_totals:
            category_totals[category] = category_totals[category] + value
        else:
            category_totals[category] = value

        gross_total = gross_total + value
        tax_total = tax_total + tax

    separator("-", 88)

    if len(items) == 0:
        print("No valid item in the basket, the bill cannot be generated.")
        return

    print("%-44s %27.2f %6s %10.2f" % ("TOTAL OF THE ITEMS", gross_total, "", tax_total))
    separator("=", 88)

    # ------------------------ category wise discounts ------------------------
    print("DISCOUNT CALCULATION")
    separator("-", 88)
    print("%-16s %14s %10s %10s %12s" %
          ("Category", "Line value", "Min needed", "Disc%", "Discount Rs"))
    separator("-", 88)

    category_discount_total = 0.0
    for category in category_totals:
        line_value = category_totals[category]
        percent = category_discount_percent(category, line_value)
        discount = line_value * percent / 100.0
        category_discount_total = category_discount_total + discount

        minimum_needed = 0.0
        for cat, minimum, pct in CATEGORY_DISCOUNTS:
            if cat == category:
                minimum_needed = minimum

        note = ""
        if percent == 0.0:
            note = "  (below the Rs.%.0f limit)" % minimum_needed
        print("%-16s %14.2f %10.0f %9.1f%% %12.2f%s" %
              (category, line_value, minimum_needed, percent, discount, note))

    separator("-", 88)

    # ---------------------------- bill discount ----------------------------
    bill_discount = 0.0
    if gross_total >= BILL_DISCOUNT_THRESHOLD:
        bill_discount = gross_total * BILL_DISCOUNT_PERCENT / 100.0
        bill_discount_note = "extra %.0f%% because the bill crossed Rs.%.0f" % (
            BILL_DISCOUNT_PERCENT, BILL_DISCOUNT_THRESHOLD)
    else:
        bill_discount_note = "not applicable, bill is below Rs.%.0f" % BILL_DISCOUNT_THRESHOLD

    total_discount = category_discount_total + bill_discount
    capped = False
    if total_discount > MAX_DISCOUNT_AMOUNT:
        total_discount = MAX_DISCOUNT_AMOUNT
        capped = True

    print("%-46s %20.2f" % ("Category discount total", category_discount_total))
    print("%-46s %20.2f" % ("Bill level discount", bill_discount))
    print("%-46s %20.2f" % ("Total discount before the cap", category_discount_total + bill_discount))
    if capped:
        print("%-46s %20.2f" % ("Maximum discount allowed (cap applied)", MAX_DISCOUNT_AMOUNT))
    print("%-46s %20.2f" % ("TOTAL DISCOUNT ALLOWED", total_discount))
    print("Note : %s" % bill_discount_note)

    # ---------------------------- final amounts ----------------------------
    net_value = gross_total - total_discount
    delivery = 0.0
    if net_value < FREE_DELIVERY_ABOVE:
        delivery = HOME_DELIVERY_CHARGE
    payable = net_value + tax_total + delivery
    rounded = round(payable)
    rounding = rounded - payable

    print("")
    separator("=", 88)
    print("AMOUNT SUMMARY")
    separator("-", 88)
    print("%-52s %18.2f" % ("Value of the goods", gross_total))
    print("%-52s %18.2f" % ("Less : total discount", 0 - total_discount))
    print("%-52s %18.2f" % ("Value after discount", net_value))
    print("%-52s %18.2f" % ("Add : GST / tax", tax_total))
    if delivery > 0:
        print("%-52s %18.2f" % ("Add : home delivery charges", delivery))
    else:
        print("%-52s %18s" % ("Home delivery", "FREE"))
    print("%-52s %18.2f" % ("Rounded off", rounding))
    separator("-", 88)
    print("%-52s %18.2f" % ("NET AMOUNT PAYABLE", rounded))
    separator("=", 88)

    saving_percent = total_discount / gross_total * 100.0
    print("You saved Rs.%.2f (%.1f%%) on this purchase." % (total_discount, saving_percent))

    # ---------------------------- basket details ----------------------------
    print("")
    separator("-", 88)
    print("ITEMS BOUGHT")
    separator("-", 88)
    total_quantity = 0
    highest_value = -1.0
    highest_item = ""
    for item in items:
        total_quantity = total_quantity + item[3]
        if item[5] > highest_value:
            highest_value = item[5]
            highest_item = item[1]
        print("%-22s %3d x %8.2f = %10.2f" % (item[1], item[3], item[4], item[5]))

    separator("-", 88)
    print("Number of item lines : %d" % len(items))
    print("Total quantity       : %d" % total_quantity)
    print("Costliest line       : %s (Rs.%.2f)" % (highest_item, highest_value))

    if len(errors) > 0:
        print("")
        separator("-", 88)
        print("LINES THAT COULD NOT BE BILLED")
        separator("-", 88)
        for error in errors:
            print("  x %s" % error)
    separator("=", 88)
    print("Thank you for shopping with us. Please visit again.")
    separator("=", 88)


main()
