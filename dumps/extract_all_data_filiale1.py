import oracledb
import csv
import os
from datetime import datetime

user = 'fil1'
pw = 'fil1'
dsn = '134.106.62.237:1521/dbprak2'

output_dir = 'db_exports_filiale1'
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
            'ADDRESS',
            'BATCH',
            'CASH_REGISTRY',
            'CUSTOMER',
            'CUSTOMER_HAS_ADDRESS',
            'DEPARTMENT',
            'EMPLOYEE',
            'EMPLOYEE_HAS_ADDRESS',
            'PACKAGE',
            'PLACE_OF_SALE',
            'PLACE_OF_SALE_COOPERATES_WITH_SUPPLIER',
            'PLACE_OF_SALE_HAS_DEPARTMENT',
            'PLACE_OF_SALE_SELLS_PRODUCT',
            'PRODUCT',
            'PRODUCT_CATEGORY',
            'PURCHASE',
            'PURCHASE_CONTAINS_PRODUCT',
            'PURCHASE_UPDATE_QUEUE',
            'SALES_PRICE_CONDITION_SET',
            'SUPPLIER',
            'SUPPLIER_ORDER'
        ]

        start = datetime.now()

        for table in tables:
            export_table_to_csv(table, cursor)

        print(f"Export finished in {(datetime.now() - start).total_seconds()} seconds")
