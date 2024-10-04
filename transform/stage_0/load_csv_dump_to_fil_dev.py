import oracledb
import csv
from datetime import datetime

## sql
user = 'onlineshop_dev'
pw = 'onlineshop_dev'
dsn = '134.106.62.237:1521/dbprak2'


DROP_TABLE_PATH = 'drop_tables_merge.sql'
TABLE_PATH= 'create_tables_merge.sql'
TRIGGER_PATH = 'create_triggers_merge.sql'
DATA_PATH = '../../dumps/os'


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None


def parse_number(num_str, precision=2):
    try:
        return round(float(num_str), precision)
    except ValueError:
        return None


def read_csv(file_path, table_name):
    data = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if table_name == 'PRODUCT_CATEGORY':
                data.append((
                    int(row['PRODUCT_CATEGORY_ID']),
                    row['NAME'],
                    int(row['PARENT_CATEGORY']) if row['PARENT_CATEGORY'] else None
                ))
            elif table_name == 'PRODUCER':
                data.append((
                    int(row['PRODUCER_ID']),
                    row['POSTAL_CODE'],
                    row['STREET'],
                    row['CITY'],
                    row['HOUSE_NUMBER'],
                    row['NAME'],
                    row['COUNTRY']
                ))
            elif table_name == 'PRODUCT':
                data.append((
                    int(row['PRODUCT_ID']),
                    parse_number(row['CASES_PER_PALLET']),
                    parse_number(row['UNITS_PER_CASE']),
                    row['PRODUCT_NAME'],
                    parse_number(row['SRP'], 2),
                    int(row['RECYCLABLE_PACKAGE']),
                    int(row['LOW_FAT']),
                    parse_number(row['RETAIL_PRICE'], 2),
                    parse_number(row['GROSS_WEIGHT'], 3),
                    parse_number(row['SHELF_WIDTH'], 2),
                    int(row['PRODUCER_ID']),
                    int(row['SKU']),
                    int(row['PRODUCT_CATEGORY_ID']),
                    parse_number(row['NET_WEIGHT'])
                ))
            elif table_name == 'SUPPLIER':
                data.append((
                    int(row['SUPPLIER_ID']),
                    row['HOUSE_NUMBER'],
                    row['CITY'],
                    row['POSTAL_CODE'],
                    row['STREET'],
                    row['COUNTRY'],
                    row['NAME'],
                    row['IBAN'],
                    row['PHONE_NUMBER'],
                    row['CONTACT_PERSON'],
                    row['CONTACT_PERSON_EMAIL']
                ))
            elif table_name == 'WAREHOUSE':
                data.append((
                    int(row['WAREHOUSE_ID']),
                    row['STREET'],
                    row['CITY'],
                    row['COUNTRY'],
                    row['POSTAL_CODE'],
                    row['HOUSE_NUMBER'],
                    parse_number(row['CAPACITY'])
                ))
            elif table_name == 'CUSTOMER':
                data.append((
                    int(row['CUSTOMER_ID']),
                    row['STREET'],
                    row['HOUSE_NUMBER'],
                    row['POSTAL_CODE'],
                    row['CITY'],
                    row['MIDDLE_NAME'],
                    row['LASTNAME'],
                    row['IBAN'],
                    parse_date(row['BIRTH_DATE']),
                    parse_date(row['CREATED_ON']),
                    row['EMAIL'],
                    row['COUNTRY'],
                    row['FORENAME']
                ))
            elif table_name == 'SHOPPING_CART':
                data.append((
                    int(row['SHOPPING_CART_ID']),
                    parse_date(row['DELETED_ON']),
                    parse_date(row['CREATED_ON']),
                    int(row['AMOUNT_OF_PRODUCTS']),
                    int(row['CUSTOMER_ID']) if row['CUSTOMER_ID'] else None
                ))
            elif table_name == 'DELIVERY_SERVICE':
                data.append((
                    int(row['DELIVERY_SERVICE_ID']),
                    row['CITY'],
                    row['STREET'],
                    row['COUNTRY'],
                    row['POSTAL_CODE'],
                    row['HOUSE_NUMBER'],
                    row['NAME'],
                    row['PHONE_NUMBER'],
                    row['IBAN'],
                    row['CONTACT_PERSON']
                ))
            elif table_name == 'ROLE':
                data.append((
                    int(row['ROLE_ID']),
                    row['NAME'],
                    int(row['IS_ADMIN'])
                ))
            elif table_name == 'EMPLOYEE':
                data.append((
                    int(row['EMPLOYEE_ID']),
                    row['HOUSE_NUMBER'],
                    row['CITY'],
                    row['POSTAL_CODE'],
                    row['COUNTRY'],
                    row['STREET'],
                    row['LASTNAME'],
                    row['FORENAME'],
                    row['MIDDLE_NAME'],
                    parse_date(row['BIRTH_DATE']),
                    parse_number(row['SALARY'], 2),
                    row['IBAN'],
                    int(row['TAX_CLASS']),
                    parse_date(row['WORKING_SINCE']),
                    int(row['WAREHOUSE_ID']) if row['WAREHOUSE_ID'] else None,
                    int(row['ROLE_ID'])
                ))
            elif table_name == 'SHOPPING_ORDER':
                data.append((
                    int(row['ORDER_ID']),
                    row['STATUS'],
                    parse_date(row['ORDER_TIME']),
                    int(row['SHOPPING_CART_ID']),
                    int(row['EMPLOYEE_ID']) if row['EMPLOYEE_ID'] else None,
                    int(row['DELIVERY_SERVICE_ID']) if row['DELIVERY_SERVICE_ID'] else None,
                    parse_number(row['TOTAL_PRICE'], 2)
                ))
            elif table_name == 'DISCOUNT':
                data.append((
                    int(row['DISCOUNT_ID']),
                    parse_number(row['PERCENTAGE'], 2),
                    row['CODE']
                ))
            elif table_name == 'INVOICE':
                data.append((
                    int(row['INVOICE_ID']),
                    int(row['ORDER_ID']),
                    row['TAX_ID'],
                    parse_date(row['ISSUE_DATE'])
                ))
            elif table_name == 'DELIVERY_NOTE':
                data.append((
                    int(row['DELIVERY_ID']),
                    int(row['ORDER_ID']),
                    parse_date(row['ISSUE_TIME']),
                    parse_date(row['ARRIVAL_TIME']),
                    parse_date(row['PICK_UP_TIME']),
                    parse_number(row['SHIPPING_COST'], 2)
                ))
            elif table_name == 'PAYMENT_METHOD':
                data.append((
                    int(row['PAYMENT_METHOD_ID']),
                    row['NAME']
                ))
            elif table_name == 'PAYMENT':
                data.append((
                    int(row['PAYMENT_ID']),
                    parse_date(row['PAYMENT_DATE']),
                    parse_number(row['CASH_FLOW'], 2),
                    int(row['SUPPLIER_ID']) if row['SUPPLIER_ID'] else None,
                    int(row['ORDER_ID']) if row['ORDER_ID'] else None,
                    int(row['EMPLOYEE_ID']) if row['EMPLOYEE_ID'] else None,
                    int(row['WAREHOUSE_ID']) if row['WAREHOUSE_ID'] else None,
                    int(row['PAYMENT_METHOD_ID'])
                ))
            elif table_name == 'PRODUCT_TO_SUPPLIER':
                data.append((
                    int(row['PRODUCT_ID']),
                    int(row['SUPPLIER_ID']),
                    parse_number(row['PURCHASE_PRICE'], 2)
                ))
            elif table_name == 'PRODUCT_TO_SHOPPING_CART':
                data.append((
                    int(row['PRODUCT_ID']),
                    int(row['SHOPPING_CART_ID']),
                    parse_number(row['TOTAL_AMOUNT'])
                ))
            elif table_name == 'PRODUCT_TO_WAREHOUSE':
                data.append((
                    int(row['PRODUCT_ID']),
                    int(row['WAREHOUSE_ID']),
                    parse_number(row['STOCK']),
                    row['STORAGE_LOCATION']
                ))
            elif table_name == 'SHOPPING_CART_TO_DISCOUNT':
                data.append((
                    int(row['SHOPPING_CART_ID']),
                    int(row['DISCOUNT_ID'])
                ))
    return data


def process_all_csv():
    tables = [
        (
            "PRODUCT_CATEGORY",
            "INSERT INTO PRODUCT_CATEGORY (PRODUCT_CATEGORY_ID,NAME,PARENT_CATEGORY) VALUES (:1, :2, :3)"
        ), (
            "PRODUCER",
            "INSERT INTO PRODUCER (PRODUCER_ID,POSTAL_CODE,STREET,CITY,HOUSE_NUMBER,NAME,COUNTRY) VALUES (:1, :2, :3, :4, :5, :6, :7)"
        ), (
            "PRODUCT",
            "INSERT INTO PRODUCT (PRODUCT_ID,CASES_PER_PALLET,UNITS_PER_CASE,PRODUCT_NAME,SRP,RECYCLABLE_PACKAGE,LOW_FAT,RETAIL_PRICE,GROSS_WEIGHT,SHELF_WIDTH,PRODUCER_ID,SKU,PRODUCT_CATEGORY_ID,NET_WEIGHT) "
            "VALUES (:1, :2, :3, :4, :5, CASE WHEN :6 = '0' THEN 0 ELSE 1 END, CASE WHEN :7 = '0' THEN 0 ELSE 1 END, :8, :9, :10, :11, :12, :13, :14)"
        ), (
            "SUPPLIER",
            "INSERT INTO SUPPLIER (SUPPLIER_ID,HOUSE_NUMBER,CITY,POSTAL_CODE,STREET,COUNTRY,NAME,IBAN,PHONE_NUMBER,CONTACT_PERSON,CONTACT_PERSON_EMAIL) "
            "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)"
        ), (
            "PRODUCT_TO_SUPPLIER",
            "INSERT INTO PRODUCT_TO_SUPPLIER (PRODUCT_ID,SUPPLIER_ID,PURCHASE_PRICE) VALUES (:1, :2, :3)"
        ), (
            "CUSTOMER",
            "INSERT INTO CUSTOMER (CUSTOMER_ID,STREET,HOUSE_NUMBER,POSTAL_CODE,CITY,MIDDLE_NAME,LASTNAME,IBAN,BIRTH_DATE,CREATED_ON,EMAIL,COUNTRY,FORENAME) "
            "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)"
        ), (
            "SHOPPING_CART",
            "INSERT INTO SHOPPING_CART (SHOPPING_CART_ID, DELETED_ON, CREATED_ON, AMOUNT_OF_PRODUCTS, CUSTOMER_ID) "
            "VALUES (:1, :2, :3, :4, :5)"
        ), (
            "PRODUCT_TO_SHOPPING_CART",
            "INSERT INTO PRODUCT_TO_SHOPPING_CART (PRODUCT_ID,SHOPPING_CART_ID,TOTAL_AMOUNT) VALUES (:1, :2, :3)"
        ), (
            "DISCOUNT",
            "INSERT INTO DISCOUNT (DISCOUNT_ID,PERCENTAGE,CODE) VALUES (:1, :2, :3)"
        ), (
            "SHOPPING_CART_TO_DISCOUNT",
            "INSERT INTO SHOPPING_CART_TO_DISCOUNT (SHOPPING_CART_ID,DISCOUNT_ID) VALUES (:1, :2)"
        ), (
            "DELIVERY_SERVICE",
            "INSERT INTO DELIVERY_SERVICE (DELIVERY_SERVICE_ID,CITY,STREET,COUNTRY,POSTAL_CODE,HOUSE_NUMBER,NAME,PHONE_NUMBER,IBAN,CONTACT_PERSON) "
            "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"
        ), (
            "ROLE",
            "INSERT INTO ROLE (ROLE_ID,NAME,IS_ADMIN) VALUES (:1, :2, :3)"
        ), (
            "WAREHOUSE",
            "INSERT INTO WAREHOUSE (WAREHOUSE_ID,STREET,CITY,COUNTRY,POSTAL_CODE,HOUSE_NUMBER,CAPACITY) VALUES (:1, :2, :3, :4, :5, :6, :7)"
        ), (
            "EMPLOYEE",
            "INSERT INTO EMPLOYEE (EMPLOYEE_ID,HOUSE_NUMBER,CITY,POSTAL_CODE,COUNTRY,STREET,LASTNAME,FORENAME,MIDDLE_NAME,BIRTH_DATE,SALARY,IBAN,TAX_CLASS,WORKING_SINCE,WAREHOUSE_ID,ROLE_ID) "
            "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16)"
        ), (
            "SHOPPING_ORDER",
            "INSERT INTO SHOPPING_ORDER (ORDER_ID,STATUS,ORDER_TIME,SHOPPING_CART_ID,EMPLOYEE_ID,DELIVERY_SERVICE_ID,TOTAL_PRICE) VALUES (:1, :2, :3, :4, :5, :6, :7)"
        ), (
            "INVOICE",
            "INSERT INTO INVOICE (INVOICE_ID,ORDER_ID,TAX_ID,ISSUE_DATE) VALUES (:1, :2, :3, :4)"
        ), (
            "DELIVERY_NOTE",
            "INSERT INTO DELIVERY_NOTE (DELIVERY_ID,ORDER_ID,ISSUE_TIME,ARRIVAL_TIME,PICK_UP_TIME,SHIPPING_COST) "
            "VALUES (:1, :2, :3, :4, :5, :6) "
        ), (
            "PRODUCT_TO_WAREHOUSE",
            "INSERT INTO PRODUCT_TO_WAREHOUSE (PRODUCT_ID,WAREHOUSE_ID,STOCK,STORAGE_LOCATION) VALUES (:1, :2, :3, :4)"
        ), (
            "PAYMENT_METHOD",
            "INSERT INTO PAYMENT_METHOD (PAYMENT_METHOD_ID,NAME) VALUES (:1, :2)"
        ), (
            "PAYMENT",
            "INSERT INTO PAYMENT (PAYMENT_ID,PAYMENT_DATE,CASH_FLOW,SUPPLIER_ID,ORDER_ID,EMPLOYEE_ID,WAREHOUSE_ID,PAYMENT_METHOD_ID) "
            "VALUES (:1, :2, :3, :4, :5, :6, :7, :8)"
        )
    ]

    with open(DROP_TABLE_PATH, 'r') as f:
        drop_tables_query: str = f.read()

    with open(TABLE_PATH, 'r') as f:
        create_tables_query: str = f.read()

    with open(TRIGGER_PATH, 'r') as f:
        create_trigger_query: str = f.read()

    total_queries = 0
    with oracledb.connect(user=user, password=pw, dsn=dsn) as connection:
        with connection.cursor() as cursor:
            print("Dropping tables...")
            start_time = datetime.now()
            for q in drop_tables_query.split(";"):
                if not q.strip():
                    continue
                try:
                    cursor.execute(q)
                except Exception as error:
                    print(error.args[0])
                    print(q)
            deleted_timestamp = datetime.now()
            delete_time = (deleted_timestamp - start_time).total_seconds()
            print(f"Dropped {drop_tables_query.count(';')} tables in {delete_time} seconds")

            print("Creating tables...")
            table_count = 0
            for q in create_tables_query.split(";"):
                if not q.strip():
                    continue
                if not q.strip().startswith('comment'):
                    table_count += 1
                cursor.execute(q)

            create_timestamp = datetime.now()
            create_time = (create_timestamp - deleted_timestamp).total_seconds()
            print(f"Created {table_count} tables in {create_time} seconds")

            for table, query in tables:
                file_path = f'{DATA_PATH}/{table}.csv'
                data = read_csv(file_path, table)
                print(f'Processed {len(data)} records for table {table}')

                print(query)
                try:
                    cursor.executemany(query, data)
                except Exception as e:
                    print(data[:10])
                    raise e
                total_queries += len(data)
            fill_timestamp = datetime.now()
            fill_time = (fill_timestamp - create_timestamp).total_seconds()
            print(
                f"Fill tables with {total_queries} queries in {fill_time} seconds ({round(fill_time / total_queries, 3)}ms per 1k queries)")

            print("Creating triggers...")
            for q in create_trigger_query.split("--"):
                if not q.strip():
                    continue
                try:
                    cursor.execute(q)
                except Exception as e:
                    print('query:', q.strip())
                    raise e

            trigger_timestamp = datetime.now()
            trigger_time = (trigger_timestamp - fill_timestamp).total_seconds()
            print(f"Created {create_trigger_query.count('--')} triggers in {trigger_time} seconds")

        connection.commit()


process_all_csv()
