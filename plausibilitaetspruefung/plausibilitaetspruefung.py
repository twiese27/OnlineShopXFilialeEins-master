import csv

OS_PATH = '../dumps/os'
FIL_PATH = '../dumps/fi'
DUPLICATES_PATH = 'duplicates'
DELIMITER = ';'


def check_product():
    sku_list = set()
    name_list = set()
    sku_duplicates = set()
    name_duplicates = set()
    count = 0
    for_csv: list[tuple] = []

    producer_map: dict[str, str] = {}
    with open(f'{OS_PATH}/PRODUCER.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            producer_map[line[0]] = line[5]

    with open(f'{OS_PATH}/PRODUCT.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            count += 1
            sku = line[11]
            if sku in sku_list:
                sku_duplicates.add(sku)
            else:
                sku_list.add(sku)

            name = f"{producer_map[line[10]]}: {line[3]} ({line[8]})"
            if name in name_list:
                name_duplicates.add(name)
                for_csv.append(('onlineshop', line[0], producer_map[line[10]], line[3], line[8]))
            else:
                name_list.add(name)

    with open(f'{FIL_PATH}/PRODUCT.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            count += 1
            sku = line[3]
            if sku in sku_list:
                sku_duplicates.add(sku)
            else:
                sku_list.add(sku)

            name = f"{line[4]}: {line[5]} ({line[6]})"
            if name in name_list:
                name_duplicates.add(name)
                for_csv.append(('filiale', line[0], line[4], line[5], line[6]))
            else:
                name_list.add(name)

    print(f'Products ({count}):')
    if len(sku_duplicates) > 0:
        print(f'{len(sku_duplicates)} SKU duplicates found')
    else:
        print('No SKU Duplicates')

    if len(name_duplicates) > 0:
        print(f'{len(name_duplicates)} Name + Brand duplicates found')
    else:
        print('No Name + Brand Duplicates')
    print()

    with open(f'{DUPLICATES_PATH}/product.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        writer.writerows(for_csv)


def check_customer():
    name_list = set()
    name_duplicates = set()
    count = 0
    for_csv: list[tuple] = []

    with open(f'{OS_PATH}/CUSTOMER.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)
        for line in data:
            count += 1
            middle_name = line[5] if line[5] else ""
            name = f"{line[12]} {middle_name} {line[6]}: {line[10]}"
            if name in name_list:
                name_duplicates.add(name)
                for_csv.append(('onlineshop', line[0], line[12], line[5], line[6]))
            else:
                name_list.add(name)

    with open(f'{FIL_PATH}/CUSTOMER.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            count += 1
            name = f"{line[1]} {line[2]}: {line[3]}"
            if name in name_list:
                name_duplicates.add(name)
                for_csv.append(('filiale', line[0], line[1], line[2]))
            else:
                name_list.add(name)

    print(f'Customers ({count}):')
    if len(name_duplicates) > 0:
        print(f'{len(name_duplicates)} Name duplicates found')
    else:
        print('No name Duplicates')
    print()

    with open(f'{DUPLICATES_PATH}/customer.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        writer.writerows(for_csv)


def check_supplier():
    name_list = set()
    name_duplicates = set()
    count = 0

    address_map: dict[str, str] = {}
    with open(f'{FIL_PATH}/ADDRESS.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            s_id = line[1]
            if not s_id:
                continue

            address_map[s_id] = line[5]

    with open(f'{OS_PATH}/SUPPLIER.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            count += 1
            name = line[6] + " " + line[3]
            if name in name_list:
                name_duplicates.add(name)
            else:
                name_list.add(name)


    with open(f'{FIL_PATH}/SUPPLIER.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            count += 1
            name = line[1] + " " + address_map[line[0]]
            if name in name_list:
                name_duplicates.add(name)
            else:
                name_list.add(name)

    print(f'Suppliers ({count}):')
    if len(name_duplicates) > 0:
        print(f'{len(name_duplicates)} Name duplicates found')
    else:
        print('No name Duplicates')
    print()


def check_producer():
    name_list = set()
    name_duplicates = set()
    count = 0
    for_csv: list[tuple] = []

    with open(f'{OS_PATH}/PRODUCER.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        for line in data:
            count += 1
            name = line[5]
            if name in name_list:
                name_duplicates.add(name)
                for_csv.append(('onlineshop', line[0], line[5]))
            else:
                name_list.add(name)

    with open(f'{FIL_PATH}/PRODUCT.csv', 'r') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)

        producers = {line[4] for line in data}

        for producer in producers:
            count += 1
            if producer in name_list:
                name_duplicates.add(producer)
                for_csv.append(('filiale', producer))
            else:
                name_list.add(producer)

    print(f'Producers ({count}):')
    if len(name_duplicates) > 0:
        print(f'{len(name_duplicates)} Name duplicates found')
    else:
        print('No name Duplicates')
    print()

    with open(f'{DUPLICATES_PATH}/producer.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        writer.writerows(for_csv)

check_product()
check_customer()
check_supplier()
check_producer()
