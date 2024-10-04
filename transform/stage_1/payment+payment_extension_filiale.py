import oracledb
import csv
import os
from datetime import datetime

user = 'fil1'
pw = 'fil1'
dsn = '134.106.62.237:1521/dbprak2'

output_dir = 'transform_exports/fi'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def get_payment_method_id(payment_method):
    """
    Maps the payment method to the corresponding PAYMENT_METHOD_ID.
    - Debit: 8
    - Credit Card: 3
    - Cash: 9
    - Employee or Supplier Payment: 4
    """
    if payment_method == 'Debit':
        return 8
    elif payment_method == 'Credit Card':
        return 3
    elif payment_method == 'Cash':
        return 9
    else:
        return 4  # For Employee and Supplier payments


def export_payments_and_extensions_to_csv(cursor):
    payment_id = 1  # Startet bei 1 und wird für jede Zahlung hochgezählt
    payment_extension_id = 1  # Startet bei 1 und wird für jede Erweiterung hochgezählt
    csv_filename_payment = os.path.join(output_dir, "PAYMENT.csv")
    csv_filename_extension = os.path.join(output_dir, "PAYMENT_EXTENSION.csv")

    with open(csv_filename_payment, mode='w', newline='', encoding='utf-8') as payment_file, \
            open(csv_filename_extension, mode='w', newline='', encoding='utf-8') as extension_file:

        payment_writer = csv.writer(payment_file, delimiter=';')
        extension_writer = csv.writer(extension_file, delimiter=';')

        payment_writer.writerow(["PAYMENT_ID", "PAYMENT_DATE", "CASH_FLOW", "SUPPLIER_ID", "ORDER_ID", "EMPLOYEE_ID", "WAREHOUSE_ID", "PAYMENT_METHOD_ID"])
        extension_writer.writerow(["PAYMENT_EXTENSION_ID", "PAYMENT_ID", "TRANSACTION_NUMBER", "POINT_OF_SALE_ID"])

        # 1. Employee payments (salary_per_month, negative cash flow, method_id = 4)
        cursor.execute("""
            SELECT EMPLOYEE_ID, SALARY_PER_MONTH, SYSDATE AS PAYMENT_DATE
            FROM EMPLOYEE
            WHERE PLACE_OF_SALE_ID IS NOT NULL  -- Exclude warehouses
        """)
        employee_payments = cursor.fetchall()
        for emp_id, salary, payment_date in employee_payments:
            payment_writer.writerow([payment_id, payment_date, -salary, None, None, emp_id, None, 4])
            extension_writer.writerow([payment_extension_id, payment_id, None, 1])
            payment_id += 1
            payment_extension_id += 1

        # 2. Supplier payments (price from supplier_order, positive cash flow, method_id = 4)
        cursor.execute("""
            SELECT SUPPLIER_ORDER_ID, SUPPLIER_ID, PRICE, ORDER_DATE
            FROM SUPPLIER_ORDER
        """)
        supplier_payments = cursor.fetchall()
        for order_id, supplier_id, price, order_date in supplier_payments:
            payment_writer.writerow([payment_id, order_date, price, supplier_id, None, None, None, 4])
            extension_writer.writerow([payment_extension_id, payment_id, None, 1])
            payment_id += 1
            payment_extension_id += 1

        # 3. Purchase payments (gross_purchase_price, positive cash flow, method_id based on payment_method)
        cursor.execute("""
            SELECT PURCHASE_ID, GROSS_PURCHASE_PRICE, PAYMENT_METHOD, TIME_OF_PURCHASE, TRANSACTION_NUMBER
            FROM PURCHASE
        """)
        purchase_payments = cursor.fetchall()
        for purchase_id, gross_price, payment_method, purchase_time, transaction_number in purchase_payments:
            method_id = get_payment_method_id(payment_method)
            payment_writer.writerow([payment_id, purchase_time, gross_price, None, purchase_id, None, None, method_id])
            extension_writer.writerow([payment_extension_id, payment_id, transaction_number, 1])
            payment_id += 1
            payment_extension_id += 1

    print(f"Payments exported to {csv_filename_payment}")
    print(f"Payment Extensions exported to {csv_filename_extension}")


with oracledb.connect(user=user, password=pw, dsn=dsn) as connection:
    with connection.cursor() as cursor:
        start = datetime.now()

        export_payments_and_extensions_to_csv(cursor)

        print(f"Export finished in {(datetime.now() - start).total_seconds()} seconds")
