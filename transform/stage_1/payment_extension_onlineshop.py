import csv
import os

output_dir = 'transform_exports/os'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

csv_filename_extension = os.path.join(output_dir, "PAYMENT_EXTENSION.csv")

with open(csv_filename_extension, mode='w', newline='', encoding='utf-8') as extension_file:
    extension_writer = csv.writer(extension_file, delimiter=';')

    # Header für die Payment Extension CSV-Datei
    extension_writer.writerow(["PAYMENT_EXTENSION_ID", "PAYMENT_ID", "TRANSACTION_NUMBER", "POINT_OF_SALE_ID"])

    # Generierung der Einträge
    for payment_id in range(88764):
        payment_extension_id = payment_id
        transaction_number = None
        point_of_sale_id = 2
        extension_writer.writerow([payment_extension_id, payment_id, transaction_number, point_of_sale_id])

print(f"Payment Extensions with IDs 0 to 88763 exported to {csv_filename_extension}")
