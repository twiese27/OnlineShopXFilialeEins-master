import oracledb
import csv
import os
from datetime import datetime

user = 'onlineshop_admin'
pw = 'onlineshop_admin'
dsn = '134.106.62.241:1521/dbprak2'

output_dir = 'os'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def export_table_to_csv(table_name, cursor):
    # Hole die Spaltennamen
    cursor.execute(f"SELECT * FROM {table_name} WHERE ROWNUM = 1")
    colnames = [i[0] for i in cursor.description]

    # Sortiere nach der ersten Spalte (vermutlich die ID-Spalte)
    id_column = colnames[0]

    # Führe die Abfrage mit ORDER BY auf der ersten Spalte durch
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY {id_column}")
    rows = cursor.fetchall()

    csv_filename = os.path.join(output_dir, f"{table_name}.csv")

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(colnames)  # Schreibe die Spaltennamen in die erste Zeile
        writer.writerows(rows)  # Schreibe die sortierten Datensätze

    print(f"Exported {table_name} to {csv_filename}")



with oracledb.connect(user=user, password=pw, dsn=dsn) as connection:
    with connection.cursor() as cursor:
        tables = [
            'CUSTOMER', 'DELIVERY_NOTE', 'DELIVERY_SERVICE', 'DISCOUNT', 'EMPLOYEE', 'INVOICE',
            'PAYMENT', 'PAYMENT_METHOD', 'PRODUCER', 'PRODUCT', 'PRODUCT_CATEGORY', 'PRODUCT_TO_SHOPPING_CART',
            'PRODUCT_TO_SUPPLIER', 'PRODUCT_TO_WAREHOUSE', 'ROLE', 'SHOPPING_CART', 'SHOPPING_CART_TO_DISCOUNT',
            'SHOPPING_ORDER', 'SUPPLIER', 'WAREHOUSE'
        ]

        start = datetime.now()

        for table in tables:
            export_table_to_csv(table, cursor)

        print(f"Export finished in {(datetime.now() - start).total_seconds()} seconds")
