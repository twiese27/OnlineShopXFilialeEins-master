import csv

OS_DATA_PATH = '../../dumps/os'
TRANS_OS_DATA_PATH = '../stage_1/transform_exports/os'

# FI_DATA_PATH = '../../dumps/fi'
TRANS_FI_DATA_PATH = '../stage_1/transform_exports/fi'

DELIMITER = ';'


class OptionalIDReplacement:
    index: int
    data: dict[int, int]  # {old_id: new_id}

    def __init__(self, index: int, data: dict[int, int]):
        self.index = index
        self.data = data

    def apply(self, row: list):
        row[self.index] = self.data[int(row[self.index])]


def read_csv(file_path: str) -> list:
    with open(file_path, newline='') as f:
        data = csv.reader(f, delimiter=DELIMITER)
        next(data)
        return list(data)


def add_fi2os(file_name: str, optional_replacements: list[OptionalIDReplacement] = None) \
        -> tuple[list[tuple], dict[int, int]]:
    os_data: list = read_csv(OS_DATA_PATH + file_name)
    fi_trans_data: list = read_csv(TRANS_FI_DATA_PATH + file_name)

    final_data: list[tuple] = []
    remapped_ids = {}
    index = len(os_data)
    for row in fi_trans_data:
        new_id = index + int(row[0])
        remapped_ids[int(row[0])] = new_id
        row[0] = new_id

        if optional_replacements:
            for opt_r in optional_replacements:
                opt_r.apply(row)

        final_data.append(*row)

    return final_data, remapped_ids


# add fi to the end of os
def product_category_merge():
    return read_csv(TRANS_FI_DATA_PATH + '/PRODUCT_CATEGORY.csv')


# add everything after 114 from fi
def producer_merge():
    return read_csv(TRANS_FI_DATA_PATH + '/PRODUCER.csv')[114:]


# add fi to the end of os
def product_merge():
    product_remap = {}
    for x in range(1560):
        product_remap[x + 1] = x

    fi_data, remap = add_fi2os('/PRODUCT.csv')
    product_remap.update(remap)

    return fi_data, product_remap


# add fi to the end of os
def supplier_merge() -> tuple[list[tuple], dict[int, int]]:
    return add_fi2os('/SUPPLIER.csv')


# add fi to the end of os
def warehouse_merge():
    return add_fi2os('/WAREHOUSE.csv')


# add fi to the end of os
def customer_merge() -> tuple[list[tuple], dict[int, int]]:
    return add_fi2os('/CUSTOMER.csv')


# fi data with shifted customer_id
def shopping_cart_merge(customer_remap: dict[int, int]):
    opt_r = OptionalIDReplacement(4, customer_remap)
    return add_fi2os('/SHOPPING_CART.csv', [opt_r])


# no new data from fi
def delivery_service_merge():
    pass


# add fi to the end of os
def role_merge() -> tuple[list[tuple], dict[int, int]]:
    return add_fi2os('/ROLE.csv')


# add fi to the end of os, role_id has already been shifted
def employee_merge() -> tuple[list[tuple], dict[int, int]]:
    return add_fi2os('/EMPLOYEE.csv')


# added fi to the end of os, shopping_card_id and employee_id shifted
def shopping_order_merge(shopping_card_remap: dict[int, int], employee_remap: dict[int, int]) \
        -> tuple[list[tuple], dict[int, int]]:
    opt_r_shopping_card = OptionalIDReplacement(3, shopping_card_remap)
    opt_r_employee = OptionalIDReplacement(4, employee_remap)
    return add_fi2os('/SHOPPING_ORDER.csv', [opt_r_shopping_card, opt_r_employee])


# no new data from fi
def discount_merge():
    pass


# no new data from fi
def invoice_merge():
    pass


# no new data from fi
def delivery_note_merge():
    pass


# add fi to the end of os
def payment_method_merge() -> tuple[list[tuple], dict[int, int]]:
    return add_fi2os('/PAYMENT_METHOD.csv')


# os-Datensätze beginnen bei ID = 0 !! TODO: still in work by Linus
def payment_merge():
    pass


# TODO: still in work by Dominique
def product_to_supplier_merge():
    pass


# TODO: still in work by Linus
def product_to_shopping_cart_merge():
    pass


# TODO: still in work by Dominique
def product_to_warehouse_merge():
    pass


# no new fi data
def shopping_cart_to_discount_merge():
    pass


# only fi data
def customer_billing_address_merge():
    return read_csv(TRANS_FI_DATA_PATH + '/CUSTOMER_BILLING_ADDRESS.csv')


# only fi data available
def point_of_sale_merge() -> list[tuple]:
    return read_csv(TRANS_FI_DATA_PATH + '/POINT_OF_SALE.csv')


# only fi data available
def cash_registry_merge() -> list[tuple]:
    return read_csv(TRANS_FI_DATA_PATH + '/CASH_REGISTRY.csv')


# only fi data available, shift to product_id
def sales_price_condition_set_merge(product_remap: dict[int, int]):
    data = read_csv(TRANS_FI_DATA_PATH + '/SALES_PRICE_CONDITION_SET.csv')
    for x in range(len(data)):
        data[x][1] = product_remap[data[x][1]]

    return data


# only fi data available
def supplied_from_extension_merge():
    return read_csv(TRANS_FI_DATA_PATH + '/SUPPLIED_FROM_EXTENSION.csv')


# os is included in fi, so only fi is loaded
def producer_extension_merge():
    return read_csv(TRANS_FI_DATA_PATH + '/PRODUCER_EXTENSION.csv')


# 1-1560 from fi, then 1560-end from os, then 0 + 1561-end from fi
def product_extension_merge(product_remap: dict[int, int]) -> list[tuple]:
    data = read_csv(TRANS_OS_DATA_PATH + '/PRODUCT_EXTENSION.csv')
    fi_data = read_csv(TRANS_FI_DATA_PATH + '/PRODUCT_EXTENSION.csv')
    for x in range(1560):
        full_data = fi_data[x + 1]
        full_data[1] = product_remap[full_data[1]]
        data[x] = full_data

    current_id = len(data)
    for row in fi_data:
        current_id += 1
        row[0] = current_id
        data.append(tuple(row))

    return data


# only os data available
def discount_extension_merge() -> list[tuple]:
    return read_csv(TRANS_OS_DATA_PATH + '/DISCOUNT_EXTENSION.csv')


# os data + fi data with shifted shopping_cart_id
def shopping_cart_extension_merge(shopping_cart_remap: dict[int, int]) -> list[tuple]:
    os_data = read_csv(TRANS_OS_DATA_PATH + '/SHOPPING_CART.csv')
    opt_r = OptionalIDReplacement(1, shopping_cart_remap)
    fi_data, _ = add_fi2os('/SHOPPING_CART_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# os data + fi data with shifted customer_id
def customer_extension_merge(customer_remap: dict[int, int]):
    os_data = read_csv(TRANS_OS_DATA_PATH + '/CUSTOMER_EXTENSION.csv')
    opt_r = OptionalIDReplacement(1, customer_remap)
    fi_data, _ = add_fi2os('/CUSTOMER_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# os data + fi data with shifted shopping_order_id
def shopping_order_extension_merge(shopping_order_remap: dict[int, int]) -> list[tuple]:
    os_data = read_csv(TRANS_OS_DATA_PATH + '/SHOPPING_ORDER_EXTENSION.csv')
    opt_r = OptionalIDReplacement(1, shopping_order_remap)
    fi_data, _ = add_fi2os('/SHOPPING_ORDER_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# only os data available
def delivery_service_extension_merge():
    return read_csv(TRANS_OS_DATA_PATH + '/DELIVERY_SERVICE_EXTENSION.csv')


# os data + fi data with shifted payment_method_id
def payment_method_extension_merge(payment_method_remap: dict[int, int]):
    os_data = read_csv(TRANS_OS_DATA_PATH + '/PAYMENT_METHOD_EXTENSION.csv')
    opt_r = OptionalIDReplacement(1, payment_method_remap)
    fi_data, _ = add_fi2os('/PAYMENT_METHOD_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# os data + fi data
def payment_extension_merge():
    os_data = read_csv(TRANS_OS_DATA_PATH + '/PAYMENT_EXTENSION.csv')
    fi_data, _ = add_fi2os('/PAYMENT_METHOD_EXTENSION.csv')

    return os_data + fi_data


# os data + fi data with shifted supplier_id
def supplier_extension_merge(supplier_remap: dict[int, int]) -> list[tuple]:
    os_data = read_csv(TRANS_OS_DATA_PATH + '/SUPPLIER_EXTENSION.csv')
    opt_r = OptionalIDReplacement(1, supplier_remap)
    fi_data, _ = add_fi2os('/SUPPLIER_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# os data + fi data with shifted role_id
def role_extension_merge(role_remap: dict[int, int]) -> list[tuple]:
    os_data = read_csv(TRANS_OS_DATA_PATH + '/ROLE_EXTENSION.csv')
    opt_r = OptionalIDReplacement(1, role_remap)
    fi_data, _ = add_fi2os('/ROLE_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# os data + fi data with shifted employee_id
def employee_extension_merge(employee_remap: dict[int, int]):
    os_data = read_csv(TRANS_OS_DATA_PATH + '/EMPLOYEE_EXTENSION.csv')
    opt_r = OptionalIDReplacement(1, employee_remap)
    fi_data, _ = add_fi2os('/EMPLOYEE_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# os data + fi data with shifted warehouse_id
def warehouse_extension_merge(warehouse_remap: dict[int, int]):
    os_data = read_csv(TRANS_OS_DATA_PATH + '/WAREHOUSE_EXTENSION.csv')
    opt_r = OptionalIDReplacement(1, warehouse_remap)
    fi_data, _ = add_fi2os('/WAREHOUSE_EXTENSION.csv', [opt_r])

    return os_data + fi_data


# os data + fi data
def product_category_extension_merge():
    os_data = read_csv(TRANS_OS_DATA_PATH + '/PRODUCT_CATEGORY_EXTENSION.csv')
    fi_data = read_csv(TRANS_FI_DATA_PATH + '/PRODUCT_CATEGORY_EXTENSION.csv')

    return os_data + fi_data


def pos_to_producer_extension_merge(producer_extension_remap: dict[int, int], ):
    pass  # TODO: create this


def pos_to_product_extension_merge():
    pass  # TODO: create this


def pos_to_customer_extension_merge():
    pass  # TODO: create this


def pos_to_customer_billing_address_merge():
    pass  # TODO: create this


def pos_to_payment_method_extension_merge():
    pass  # TODO: create this


def pos_to_supplier_extension_merge():
    pass  # TODO: create this


def pos_to_role_extension_merge():
    pass  # TODO: create this


def pos_to_employee_extension_merge():
    pass  # TODO: create this


def pos_to_product_category_extension_merge():
    pass  # TODO: create this


# only fi data available
def supervision_merge(employee_remap: dict[int, int]):
    data = read_csv(TRANS_FI_DATA_PATH + '/SUPERVISOR.csv')

    for x in range(len(data)):
        data[x][0] = employee_remap[int(data[x][0])]
        data[x][1] = employee_remap[int(data[x][1])]

    return data


# only fi data available, shift to product_id
def product_to_supplier_to_supplied_from_extension_merge(product_remap: dict[int, int]):
    data = read_csv(TRANS_FI_DATA_PATH + '/PRODUCT_TO_SUPPLIER_TO_SUPPLIED_FROM_EXTENSION.csv')
    for x in range(len(data)):
        data[x][0] = product_remap[data[x][0]]

    return data
