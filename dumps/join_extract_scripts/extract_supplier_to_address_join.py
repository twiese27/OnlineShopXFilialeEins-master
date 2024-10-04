import oracledb
import csv
import os
from datetime import datetime

user = 'fil1'
pw = 'fil1'
dsn = '134.106.62.237:1521/dbprak2'

output_dir = '../fi'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def export_join_to_csv(sql_query, output_filename, cursor):
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    colnames = [i[0] for i in cursor.description]

    csv_filename = os.path.join(output_dir, output_filename)

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')  # Trennzeichen auf Semikolon gesetzt
        writer.writerow(colnames)
        writer.writerows(rows)

    print(f"Exported join query result to {csv_filename}")


with oracledb.connect(user=user, password=pw, dsn=dsn) as connection:
    with connection.cursor() as cursor:
        start = datetime.now()

        join_query = """
        SELECT * FROM SUPPLIER
        JOIN ADDRESS
        ON SUPPLIER.SUPPLIER_ID = ADDRESS.SUPPLIER_ID
        """

        export_join_to_csv(join_query, "supplier_to_address_join.csv", cursor)

        print(f"Export finished in {(datetime.now() - start).total_seconds()} seconds")
