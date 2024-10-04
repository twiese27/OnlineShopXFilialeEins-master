from copy import deepcopy

import oracledb
from datetime import datetime, timedelta, date
import csv
from faker import Faker
from random import randint, uniform, choice, random, choices
import string

# variables
## values
TOTAL_PRODUCT_AMOUNT: int = 16470
TOTAL_SUPPLIER_AMOUNT: int = 500
MAX_PER_SUPPLIER: int = 200
MAX_PER_PRODUCT: int = 5
TOTAL_CUSTOMER_AMOUNT: int = 10000
AVERAGE_DISCOUNT_USAGE: float = 0.2
TOTAL_WAREHOUSE_AMOUNT: int = 2
TOTAL_EMPLOYEE_AMOUNT: int = 100

## sql
user = 'onlineshop_admin'
pw = 'onlineshop_admin'
dsn = '134.106.62.241:1521/dbprak2'

## words
adjective_words = {
    'Handcrafted', 'Rustic', 'Tasty', 'Incredible', 'Ergonomic', 'Sleek', 'Modern', 'Elegant', 'Electronic',
    'Unbranded', 'Gorgeous', 'Awesome', 'Luxurious', 'Fantastic', 'Refined', 'Generic', 'Small',
    'Handmade', 'Licensed', 'Intelligent', 'Practical'
}

color_words = {
    'blue', 'mint green', 'orange', 'green', 'olive', 'cyan', 'turquoise', 'magenta', 'silver', 'teal', 'grey', 'white',
    'salmon', 'black', 'violet', 'purple', 'lime', 'sky blue', 'yellow', 'pink', 'red', 'gold'
}

product_words_prices: list[tuple[str, int]] = [
    ('Hamburger', 4.99), ('Chocolate Candy', 1.49), ('Fresh Vegetables', 2.99), ('Sauces', 3.49), ('Cleaners', 5.99),
    ('Eggs', 2.79), ('Personal Hygiene', 6.49), ('Paper Dishes', 2.99), ('Shower Soap', 4.29), ('Pot Scrubbers', 1.99),
    ('Fresh Fruit', 3.59), ('Fresh Fish', 12.99), ('Dips', 3.99), ('Cold Remedies', 7.99), ('Dehydrated Soup', 1.29),
    ('Shrimp', 14.99), ('Frozen Vegetables', 2.49), ('Screwdrivers', 8.99), ('Cooking Oil', 4.49), ('Popsicles', 3.29),
    ('Chips', 2.99), ('Sponges', 1.49), ('French Fries', 2.79), ('Crackers', 2.49), ('Nasal Sprays', 6.99),
    ('Sour Cream', 1.99), ('Juice', 3.49), ('TV Dinner', 3.99), ('Tofu', 2.49), ('Clams', 9.99), ('Toothbrushes', 2.99),
    ('Pots and Pans', 19.99), ('Frozen Chicken', 7.49), ('Tools', 15.99), ('Canned Vegetables', 1.29), ('Beer', 8.99),
    ('Hard Candy', 1.99), ('Auto Magazines', 4.99), ('Deli Salads', 4.49), ('Pot Cleaners', 2.49), ('Bagels', 3.49),
    ('Pizza', 8.99), ('Cereal', 3.99), ('Home Magazines', 5.99), ('Sugar', 2.49), ('Soda', 1.49), ('Muffins', 3.29),
    ('Conditioner', 4.99), ('Fashion Magazines', 6.99), ('Oysters', 13.99), ('Candles', 2.99), ('Acetaminophen', 5.49),
    ('Waffles', 2.99), ('Jam', 3.49), ('Pretzels', 2.29), ('Deli Meats', 6.99), ('Tuna', 1.99), ('Cheese', 4.79),
    ('Computer Magazines', 7.99), ('Dishwasher Soap', 5.49), ('Gum', 0.99), ('Flavored Drinks', 1.99),
    ('Cottage Cheese', 2.79), ('Fresh Chicken', 5.99), ('Plastic Utensils', 3.29), ('Preserves', 3.79), ('Nuts', 4.49),
    ('Yogurt', 1.29), ('Chocolate', 2.49), ('Spices', 3.99), ('Coffee', 8.99), ('Dried Fruit', 5.49),
    ('Pancake Mix', 2.99),
    ('Pancakes', 3.49), ('Pasta', 1.79), ('Peanut Butter', 3.49), ('Paper Wipes', 2.99), ('Toilet Brushes', 4.99),
    ('Non-Alcoholic Wine', 6.99), ('Shampoo', 4.79), ('Ibuprofen', 5.99), ('Lightbulbs', 3.99), ('Anchovies', 4.99),
    ('Wine', 11.99), ('Dried Meat', 5.99), ('Cookies', 3.29), ('Bologna', 2.99), ('Mouthwash', 5.49),
    ('Sports Magazines', 4.99), ('Shellfish', 12.49), ('Ice Cream', 4.49), ('Sliced Bread', 2.49), ('Batteries', 6.99),
    ('Hot Dogs', 3.49), ('Sunglasses', 12.99), ('Canned Fruit', 1.99), ('Popcorn', 2.99), ('Soup', 1.99),
    ('Sardines', 2.49),
    ('Donuts', 3.29), ('Maps', 4.99), ('Aspirin', 5.49), ('Dish Soap', 2.99), ('Jelly', 2.79), ('Rice', 1.99),
    ('Milk', 2.49), ('Deodorizers', 3.99)
]

discount_codes: list[tuple[int, tuple]] = [
    (5.00, 'WELCOME5'), (10.00, 'SUMMER10'), (15.00, 'WINTER15'), (20.00, 'SPRING20'), (25.00, 'FALL25'),
    (30.00, 'NEWYEAR30'), (35.00, 'HOLIDAY35'), (40.00, 'BLACKFRIDAY40'), (45.00, 'CYBERMONDAY45'),
    (50.00, 'CLEARANCE50'), (5.50, 'WELCOME_BACK5'), (7.50, 'LUCKY7'), (12.00, 'SUMMER_END12'),
    (17.50, 'WINTER_SALE17'), (22.00, 'SPRING_BLOOM22'), (27.50, 'FALL_HARVEST27'),
    (32.00, 'NEWYEAR_SPECIAL32'), (37.50, 'HOLIDAY_SALE37'), (42.00, 'BLACK_FRIDAY42'), (47.50, 'CYBER_MONDAY47'),
    (52.00, 'YEAR_END52'), (5.25, 'WELCOME_2024'), (10.50, 'SUMMER_FUN10'), (15.75, 'WINTER_CHILL15'),
    (21.00, 'SPRING_FLING21'), (26.25, 'FALL_FEST26'), (31.50, 'NEWYEAR_BLAST31'), (36.75, 'HOLIDAY_JOY36'),
    (42.00, 'BLACK_FRIDAY_BONUS42'), (47.25, 'CYBER_MONDAY_EXTRA47'), (52.50, 'YEAR_END_CLEAR52'),
    (5.00, 'WELCOME_BACK_AGAIN5'), (10.00, 'SUMMER_HEAT10'), (15.00, 'WINTER_FREEZE15'), (20.00, 'SPRING_GLOW20'),
    (25.00, 'FALL_FROST25'), (30.00, 'NEWYEAR_FLASH30'), (35.00, 'HOLIDAY_HURRY35'), (40.00, 'BLACK_FRIDAY_FLASH40'),
    (45.00, 'CYBER_MONDAY_MADNESS45'), (50.00, 'YEAR_END_MADNESS50'), (55.00, 'SUPER_SAVINGS55'),
    (60.00, 'EXTREME_SALE60'), (65.00, 'HUGE_DISCOUNT65'), (70.00, 'MEGA_SALE70'), (75.00, 'ULTIMATE_SAVINGS75'),
    (80.00, 'FINAL_CLEARANCE80'), (85.00, 'INSANE_DEAL85'), (90.00, 'CLOSING_OUT90'), (95.00, 'LAST_CHANCE95'),
    (5.00, 'FIVE_OFF'), (7.50, 'LUCKY_FIVE'), (10.00, 'TEN_OFF'), (12.50, 'LUCKY_TEN'), (15.00, 'FIFTEEN_OFF'),
    (17.50, 'LUCKY_FIFTEEN'), (20.00, 'TWENTY_OFF'), (25.00, 'TWENTYFIVE_OFF'), (30.00, 'THIRTY_OFF'),
    (35.00, 'THIRTYFIVE_OFF'), (40.00, 'FORTY_OFF'), (45.00, 'FORTYFIVE_OFF'), (50.00, 'FIFTY_OFF'),
    (55.00, 'FIFTYFIVE_OFF'), (60.00, 'SIXTY_OFF'), (65.00, 'SIXTYFIVE_OFF'), (70.00, 'SEVENTY_OFF'),
    (75.00, 'SEVENTYFIVE_OFF'), (80.00, 'EIGHTY_OFF'), (85.00, 'EIGHTYFIVE_OFF'), (90.00, 'NINETY_OFF'),
    (95.00, 'NINETYFIVE_OFF'), (5.50, 'MID_WEEK_SALE'), (10.50, 'WEEKEND_SALE'), (15.50, 'MONTH_END'),
    (20.50, 'QUARTERLY_SALE'), (25.50, 'HALF_YEAR_SALE'), (30.50, 'ANNUAL_SALE'), (35.50, 'FESTIVAL_SALE'),
    (40.50, 'ANNIVERSARY_SALE'), (45.50, 'SUMMER_SALE'), (50.50, 'WINTER_SALE'), (55.50, 'FALL_SALE'),
    (60.50, 'SPRING_SALE'), (65.50, 'NEW_YEAR_SALE'), (70.50, 'END_OF_SEASON'), (75.50, 'FLASH_SALE'),
    (80.50, 'LIMITED_TIME'), (85.50, 'EXCLUSIVE_OFFER'), (90.50, 'VIP_SALE'), (95.50, 'MEMBER_ONLY'),
    (5.00, 'EARLY_BIRD'), (7.00, 'MORNING_DEAL'), (12.00, 'AFTERNOON_SALE'), (17.00, 'EVENING_SALE'),
    (22.00, 'NIGHT_SALE'), (27.00, 'DAILY_DEAL'), (32.00, 'WEEKLY_SPECIAL'), (37.00, 'MONTHLY_SPECIAL'),
    (42.00, 'YEARLY_SPECIAL'), (47.00, 'BONUS_SALE'), (52.00, 'CASHBACK_SPECIAL'), (57.00, 'LOYALTY_SALE'),
    (62.00, 'FRIEND_REFERRAL'), (67.00, 'FAMILY_DISCOUNT'), (72.00, 'GROUP_SALE'), (77.00, 'CORPORATE_OFFER'),
    (82.00, 'BULK_SALE'), (87.00, 'GIFT_CARD'), (92.00, 'FESTIVE_OFFER'), (5.00, 'FIVE_PERCENT'),
    (10.00, 'TEN_PERCENT'), (15.00, 'FIFTEEN_PERCENT'), (20.00, 'TWENTY_PERCENT'), (25.00, 'TWENTYFIVE_PERCENT'),
    (30.00, 'THIRTY_PERCENT'), (35.00, 'THIRTYFIVE_PERCENT'), (40.00, 'FORTY_PERCENT'), (45.00, 'FORTYFIVE_PERCENT'),
    (50.00, 'FIFTY_PERCENT'), (55.00, 'FIFTYFIVE_PERCENT'), (60.00, 'SIXTY_PERCENT'), (65.00, 'SIXTYFIVE_PERCENT'),
    (70.00, 'SEVENTY_PERCENT'), (75.00, 'SEVENTYFIVE_PERCENT'), (80.00, 'EIGHTY_PERCENT'),
    (85.00, 'EIGHTYFIVE_PERCENT'), (90.00, 'NINETY_PERCENT'), (95.00, 'NINETYFIVE_PERCENT'), (100.00, 'FREE100'),
    (5.00, 'STARTER_DEAL5'), (10.00, 'BASIC_DEAL10'), (15.00, 'STANDARD_DEAL15'), (20.00, 'PREMIUM_DEAL20'),
    (25.00, 'PROFESSIONAL_DEAL25'), (30.00, 'EXPERT_DEAL30'), (35.00, 'MASTER_DEAL35'), (40.00, 'ULTIMATE_DEAL40'),
    (45.00, 'MAXIMUM_DEAL45'), (50.00, 'EXTREME_DEAL50'), (55.00, 'TOP_DEAL55'), (60.00, 'HUGE_DEAL60'),
    (65.00, 'MEGA_DEAL65'), (70.00, 'GIGANTIC_DEAL70'), (75.00, 'MONSTER_DEAL75'), (80.00, 'COLOSSAL_DEAL80'),
    (85.00, 'TITANIC_DEAL85'), (90.00, 'HERCULEAN_DEAL90'), (95.00, 'ASTOUNDING_DEAL95'), (100.00, 'UNBELIEVABLE100')
]

city_mapping = {
    'Berlin': {'postal_code': '10115', 'street': 'Chausseestrasse', 'house_number': '8'},
    'Munich': {'postal_code': '80331', 'street': 'Marienplatz', 'house_number': '12'},
    'Oldenburg': {'postal_code': '26122', 'street': 'Lange Strasse', 'house_number': '23'},
    'Bremen': {'postal_code': '28195', 'street': 'Obernstrasse', 'house_number': '5'},
}

role_employee_map = {
    'Admin': {'is_admin': 1, 'salary': (50000, 80000), 'weight': 5},
    'Customer Support': {'is_admin': 0, 'salary': (30000, 50000), 'weight': 20},
    'Warehouse Manager': {'is_admin': 0, 'salary': (40000, 70000), 'weight': 15},
    'Sales Manager': {'is_admin': 0, 'salary': (45000, 75000), 'weight': 10},
    'Finance Manager': {'is_admin': 0, 'salary': (55000, 85000), 'weight': 8},
    'IT Support': {'is_admin': 0, 'salary': (40000, 70000), 'weight': 15},
    'Marketing Manager': {'is_admin': 0, 'salary': (45000, 75000), 'weight': 10},
    'Product Manager': {'is_admin': 0, 'salary': (50000, 80000), 'weight': 8},
    'HR Manager': {'is_admin': 0, 'salary': (45000, 75000), 'weight': 10},
    'Content Manager': {'is_admin': 0, 'salary': (40000, 70000), 'weight': 12},
    'Logistics Manager': {'is_admin': 0, 'salary': (50000, 80000), 'weight': 10},
    'CEO': {'is_admin': 1, 'salary': (100000, 150000), 'amount': 1}
}

order_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]

shipping_costs = [.99, 1.99, 2.99, 5.99, 8.99]

fake = Faker()

if len(adjective_words) * len(color_words) * len(product_words_prices) < TOTAL_PRODUCT_AMOUNT:
    raise "Not enough words for the needed products"

if 500 * 200 < TOTAL_PRODUCT_AMOUNT * MAX_PER_PRODUCT:
    raise "There might not be enough suppliers"


def get_producer_names() -> list[str]:
    with open('data_generation/input/products.csv', 'r') as f:
        raw_existing_products = csv.reader(f, delimiter=';')
        raw_existing_products.__next__()
        return list({x[2] for x in raw_existing_products})


def get_random_date(years_back: int = 1):
    return datetime.fromtimestamp(uniform(
        datetime.now().replace(year=(datetime.now().year - years_back)).timestamp(),
        datetime.now().timestamp()
    ))


def generate_categories_from_csv() -> tuple[list[tuple], dict[str, int], dict[int, str]]:
    print("Generating categories...")
    with open('data_generation/input/product_categories.csv', 'r') as f:
        raw_product_categories = csv.reader(f, delimiter=';')
        raw_product_categories.__next__()

        counter = 0
        data: list[tuple] = []
        name2id: dict[str, int] = dict()
        old_category_ids: dict[int, str] = dict()
        for raw_category in raw_product_categories:
            old_category_ids[int(raw_category[0])] = raw_category[1]

            if raw_category[4] not in name2id.keys():
                counter += 1
                name2id[raw_category[4]] = counter
                data.append((counter, raw_category[4], None))

            if raw_category[3] not in name2id.keys():
                counter += 1
                name2id[raw_category[3]] = counter
                data.append((counter, raw_category[3], name2id[raw_category[4]]))

            if raw_category[2] not in name2id.keys():
                counter += 1
                name2id[raw_category[2]] = counter
                data.append((counter, raw_category[2], name2id[raw_category[3]]))

            if raw_category[1] not in name2id.keys():
                counter += 1
                name2id[raw_category[1]] = counter
                data.append((counter, raw_category[1], name2id[raw_category[2]]))

        return data, name2id, old_category_ids


def generate_producers(names: list[str]) -> list[tuple]:
    print("Generating producers...")
    with open('data_generation/input/products.csv', 'r') as f:
        raw_existing_products = csv.reader(f, delimiter=';')
        raw_existing_products.__next__()

    producer_id = 1
    data: list[tuple] = []
    for producer_name in names:
        data.append((
            producer_id,
            producer_name,
            fake.country(),
            fake.city(),
            fake.postalcode(),
            fake.street_name(),
            str(randint(1, 200))
        ))
        producer_id += 1

    return data


def generate_products_from_csv(
        producers: list[str], category_name2new_id: dict[str, int], old_id2category_name: dict[int, str]
) -> tuple[list[tuple], list[int]]:
    print("Generating products from csv...")
    with open('data_generation/input/products.csv', 'r') as f:
        raw_existing_products = csv.reader(f, delimiter=';')
        raw_existing_products.__next__()

        product_id = 0
        data: list[tuple] = []
        skus: list[int] = []
        for raw_product in raw_existing_products:
            cases_per_pallet = int(raw_product[11])
            units_per_case = int(raw_product[10])
            product_name = raw_product[3]
            srp = float(raw_product[5].replace(',', '.'))
            recyclable_package = 1 if raw_product[8] == 'True' else 0
            low_fat = 1 if raw_product[9] == 'True' else 0
            retail_price = float(raw_product[5].replace(',', '.')) + 1
            gross_weight = float(raw_product[6].replace(',', '.'))
            shelf_width = float(raw_product[12].replace(',', '.'))
            producer_id = producers.index(raw_product[2]) + 1
            sku = int(raw_product[4])
            skus.append(sku)
            product_category_id = category_name2new_id[old_id2category_name[int(raw_product[0])]]
            net_weight = float(raw_product[7].replace(',', '.'))
            data.append((
                product_id, cases_per_pallet, units_per_case, product_name, srp, recyclable_package, low_fat,
                retail_price, gross_weight, shelf_width, producer_id, sku, product_category_id, net_weight
            ))
            product_id += 1

        return data, skus


def generate_new_products(start: int, product_amount: int, producer_amount: int, usable_category_ids: list[int], used_skus: list[int]) -> list[tuple]:
    print("Generating new products...")
    counter = start
    data = []
    for adjective in adjective_words:
        for color in color_words:
            for product, price in product_words_prices:
                if counter >= product_amount:
                    break

                cases_per_pallet = randint(0, 100)
                units_per_case = randint(1, 50)
                product_name = f"{adjective} {color} {product}"
                srp = round(uniform(price * .75, price * 1.5), 2)
                recyclable_package = randint(0, 1)
                low_fat = randint(0, 1)
                retail_price = round(uniform(srp * 0.9, srp * 1.1), 2)
                gross_weight = round(uniform(0.1, 10.0), 3)
                shelf_width = round(uniform(1.0, 30.0), 2)
                producer_id = randint(1, producer_amount)

                while True:
                    sku = randint(1000000000000, 9999999999999)
                    if sku not in used_skus:
                        break


                product_category_id = choice(usable_category_ids)
                net_weight = round(uniform(0.1, 10.0), 3)

                data.append((
                    counter, cases_per_pallet, units_per_case, product_name, srp, recyclable_package, low_fat,
                    retail_price, gross_weight, shelf_width, producer_id, sku, product_category_id, net_weight
                ))

                counter += 1

    return data


def generate_suppliers(supplier_amount: int) -> list[tuple]:
    print("Generating suppliers...")
    data: list[tuple] = []
    for supplier_id in range(1, supplier_amount + 1):
        country = fake.country()
        city = fake.city()
        postal_code = fake.zipcode()
        street = fake.street_name()
        house_number = str(randint(1, 200))
        name = fake.company()
        iban = fake.iban()
        contact_person = f"{fake.first_name()} {fake.last_name()}"
        phone_number = fake.basic_phone_number()
        email = fake.email()

        data.append((
            supplier_id, country, city, postal_code, street, house_number, name, iban, contact_person, phone_number,
            email
        ))

    return data


def generate_product2supplier(product_amount: int) -> list[tuple]:
    print("Generating product2supplier...")
    how_much_supplying: dict[int, int] = dict()
    data: list[tuple] = []
    for product_id in range(product_amount):
        suppliers: int = randint(1, MAX_PER_PRODUCT)
        current_supplier = []
        for i in range(suppliers):
            while True:
                supplier_id = randint(1, TOTAL_SUPPLIER_AMOUNT)
                if supplier_id in current_supplier:
                    continue

                if supplier_id not in how_much_supplying:
                    how_much_supplying[supplier_id] = 1
                    break
                else:
                    if how_much_supplying[supplier_id] < MAX_PER_SUPPLIER:
                        how_much_supplying[supplier_id] += 1
                        break

            current_supplier.append(supplier_id)

            price = round(uniform(.80, 8.00), 2)
            data.append((product_id, supplier_id, price))
    return data


def generate_customers(customer_amount: int):
    print("Generating customers...")
    data: list[tuple] = []
    for customer_id in range(1, customer_amount + 1):
        street = fake.street_name()
        house_number = str(randint(1, 200))
        postal_code = fake.zipcode()
        city = fake.city()
        forename = fake.first_name()
        middle_name = fake.first_name() if choice([True, False]) else None
        lastname = fake.last_name()
        iban = fake.iban()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
        created_on = fake.date_between(start_date='-10y', end_date='today')
        email = fake.email()
        country = fake.country()

        data.append((
            customer_id,
            street,
            house_number,
            postal_code,
            city,
            forename,
            middle_name,
            lastname,
            iban,
            birth_date,
            created_on,
            email,
            country
        ))

    return data


def generate_shopping_carts(customer_amount: int, per_shopping_cart: dict[int, int]) -> list[tuple]:
    print("Generating shopping carts...")
    shopping_cart_id = 1
    data: list[tuple] = []
    with open("data_generation/input/retail.dat", 'r') as file:
        reader = file.readlines()
        for _ in reader:
            deleted_on = None
            created_on = fake.date_between(datetime(2020, 1, 1), datetime(2023, 12, 31))
            customer_id = randint(1, customer_amount)

            data.append((shopping_cart_id, deleted_on, created_on, per_shopping_cart[shopping_cart_id], customer_id))
            shopping_cart_id += 1

    return data


def generate_product2shopping_cart(products: list[tuple]) -> tuple[list[tuple], dict[int, int], dict[int, int]]:
    print("Generating product2shopping cart...")
    shopping_cart_id = 1
    data: list[tuple] = []
    shopping_cart_product_amounts: dict[int, int] = dict()
    shopping_cart_total_prices: dict[int, int] = dict()
    with open("data_generation/input/retail.dat", 'r') as file:
        reader = file.readlines()
        for line in reader:
            product_ids = [int(x) for x in line.strip().split()]
            product_amount = 0
            price_amount = 0
            for product_id in product_ids:
                amount = randint(1, 10)
                price_amount += products[product_id][7] * amount
                data.append((
                    product_id, shopping_cart_id, amount
                ))
                product_amount += amount

            shopping_cart_product_amounts[shopping_cart_id] = product_amount
            shopping_cart_total_prices[shopping_cart_id] = price_amount
            shopping_cart_id += 1

    return data, shopping_cart_product_amounts, shopping_cart_total_prices


def generate_discounts(discount_code: list[tuple[int, tuple]]) -> list[tuple]:
    print("Generating discounts...")
    data: list[tuple] = []

    for code_id, (amount, code) in enumerate(discount_code, 1):
        data.append((code_id, amount, code))

    return data


def generate_shopping_cart2discount(shopping_cart_amount: int, discount_amount: int) -> list[tuple]:
    print("Generating shopping cart2discount...")
    data: list[tuple] = []
    for shopping_cart_id in range(1, shopping_cart_amount + 1):
        if random() >= AVERAGE_DISCOUNT_USAGE:
            continue
        data.append((shopping_cart_id, randint(1, discount_amount)))

    return data


delivery_service_data = [
    (1, 'Berlin', 'Kurfürstendamm', 'Germany', '10707', '15', 'DHL', '+4930123456789', 'DE89370400440532013000',
     'Max Mustermann'),
    (2, 'Munich', 'Leopoldstraße', 'Germany', '80802', '3', 'UPS', '+4989123456789', 'DE44500105175407324931',
     'Erika Mustermann'),
    (3, 'Hamburg', 'Jungfernstieg', 'Germany', '20095', '27', 'GLS', '+4940123456789', 'DE75512108001245126199',
     'Hans Müller'),
    (4, 'Cologne', 'Schildergasse', 'Germany', '50667', '100', 'Hermes', '+4922123456789', 'DE98500105175550332857',
     'Petra Schmidt'),
    (5, 'Frankfurt', 'Zeil', 'Germany', '60313', '85', 'DPD', '+4969123456789', 'DE21500205175544625587',
     'Martin Fischer'),
    (6, 'Stuttgart', 'Königstraße', 'Germany', '70173', '50', 'FedEx', '+4971123456789', 'DE69500505175567452057',
     'Anna Schwarz'),
    (7, 'Düsseldorf', 'Königsallee', 'Germany', '40212', '33', 'TNT', '+4921123456789', 'DE43500605175567593400',
     'Stefan Wagner'),
    (8, 'Dresden', 'Prager Straße', 'Germany', '01069', '19', 'PostNL', '+4935123456789', 'DE90500705175567843420',
     'Michaela Bauer'),
    (9, 'Leipzig', 'Petersstraße', 'Germany', '04109', '12', 'Royal Mail', '+4934123456789', 'DE50500805175567843477',
     'Thomas Becker'),
    (10, 'Bremen', 'Sögestraße', 'Germany', '28195', '5', 'DB Schenker', '+4942123456789', 'DE43500905175567594565',
     'Claudia Neumann'),
    (11, 'Hannover', 'Georgstraße', 'Germany', '30159', '30', 'Chronopost', '+4951123456789', 'DE40501005175567456789',
     'Julia Meier'),
    (12, 'Nuremberg', 'Königstraße', 'Germany', '90402', '9', 'Parcelforce', '+4991123456789', 'DE38501105175567459876',
     'Robert Klein')
]


def generate_roles(role_data: dict) -> list[tuple]:
    print("Generating roles...")
    data: list[tuple] = []

    for role_id, (role_name, values) in enumerate(role_data.items(), 1):
        data.append((role_id, role_name, values['is_admin']))

    return data


def generate_warehouses(warehouse_amount: int) -> list[tuple]:
    print("Generating warehouse...")
    data: list[tuple] = []
    for warehouse_id in range(1, warehouse_amount + 1):
        city = list(city_mapping.keys())[warehouse_id - 1]
        postal_code = city_mapping[city]['postal_code']
        street = city_mapping[city]['street']
        house_number = city_mapping[city]['house_number']
        capacity = randint(8500, 33470)
        data.append((warehouse_id, 'Germany', city, postal_code, street, house_number, capacity))
    return data


def generate_employees(employee_amount: int, role_map: dict, warehouse_amount: int) -> list[tuple]:
    print("Generating employees...")
    data: list[tuple] = []

    defined_roles: dict[str, int] = {}
    for role_id, (role_name, values) in enumerate(role_map.items(), 1):
        if 'amount' in values:
            defined_roles[role_name] = values['amount']

    role_name = ''
    for employee_id in range(1, employee_amount + 1):

        if sum(defined_roles.values()) > 0:
            for role_name, amount in defined_roles.items():
                if amount > 0:
                    defined_roles[role_name] -= 1
                    break
        else:
            role_name: str = choices(
                list(role_map.keys()),
                [(x['weight'] if 'weight' in x else 0) for x in role_map.values()],
                k=1
            )[0]

        house_number = fake.building_number()
        city = fake.city()
        postal_code = fake.postcode()
        country = fake.country()
        street = fake.street_name()
        lastname = fake.last_name()
        forename = fake.first_name()
        middle_name = fake.first_name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
        salary = randint(*role_map[role_name]['salary'])
        iban = fake.iban()
        tax_class = randint(1, 6)
        working_since = get_random_date(5)
        warehouse_id = randint(1, warehouse_amount)
        role_id: int = list(role_map.keys()).index(role_name) + 1

        data.append((
            employee_id, house_number, city, postal_code, country, street, lastname, forename, middle_name, birth_date,
            salary, iban, tax_class, working_since, warehouse_id, role_id
        ))

    return data


def generate_shopping_orders(shopping_cart_amount: int, employee_amount: int, delivery_service_amount: int,
                             total_prices: dict[int, int]) -> list[tuple]:
    print("Generating shopping orders...")
    data: list[tuple] = []
    for order_id in range(1, shopping_cart_amount + 1):
        status = choice(order_statuses)
        order_time = get_random_date()
        employee_id = randint(1, employee_amount)
        delivery_service_id = randint(1, delivery_service_amount)

        data.append((
            order_id,
            status,
            order_time,
            order_id,  # SHOPPING_CART_ID, gleich der ORDER_ID
            employee_id,
            delivery_service_id,
            total_prices[order_id]
        ))

    return data


def generate_invoices(shopping_cart_amount: int) -> list[tuple]:
    print("Generating invoices...")

    def generate_random_tax_id():
        tax_id_numbers = [randint(0, 9) for _ in range(10)]

        factor = 10
        total = 0
        for digit in tax_id_numbers:
            factor = (factor + digit) % 10
            if factor == 0:
                factor = 10
            check_digit = (2 * factor) % 11
            total += check_digit

        check_digit = (11 - total % 11) % 10

        tax_id_numbers.append(check_digit)

        return ''.join(map(str, tax_id_numbers))

    data: list[tuple] = []
    for invoice_id in range(1, shopping_cart_amount + 1):
        tax_id = generate_random_tax_id()
        issue_date = fake.date_between(start_date='-11m', end_date='today')
        data.append((
            invoice_id, invoice_id, tax_id, issue_date
        ))

    return data


def generate_delivery_notes(shopping_cart_amount: int, shipping_cost_options: list[float]) -> list[tuple]:
    print("Generating delivery notes...")
    data: list[tuple] = []
    for delivery_note_id in range(1, shopping_cart_amount + 1):
        issue_time = get_random_date()
        arrival_time = get_random_date()
        pick_up_time = get_random_date()
        shipping_cost = choice(shipping_cost_options)
        data.append((
            delivery_note_id, delivery_note_id, issue_time, arrival_time, pick_up_time, shipping_cost
        ))
    return data


def generate_product2warehouse(product_amount: int, warehouse_amount: int) -> list[tuple]:
    print("Generating product2warehouse...")
    data: list[tuple] = []
    for product_id in range(product_amount):
        warehouses_for_product = choice([[], [1], [2], [1, 2]])  # TO-DO don't ignore warehouse amount
        for warehouse_id in warehouses_for_product:
            stock = randint(0, 1000)  # TO-DO don't ignore warehouse limits
            storage_location = f'{randint(1, 9):03}{choice(string.ascii_uppercase)}{choice(string.ascii_uppercase)}{randint(1, 99):02}'
            data.append((
                product_id,
                warehouse_id,
                stock,
                storage_location
            ))

    return data


payment_method_data = [
    (1, 'PayPal'),
    (2, 'Klarna'),
    (3, 'Credit Card'),
    (4, 'Bank Transfer'),
    (5, 'Gift Card'),
    (6, 'Apple Pay'),
    (7, 'Google Pay')
]


def generate_payments(orders: list[tuple], payment_method_ids: list[int], supplier_amount: int, employees: list[tuple],
                      warehouse_amount: int) -> list[tuple]:
    print("Generating payments...")
    data: list[tuple] = []
    payment_id = 0

    # payments from orders
    c = 0
    for order_id in range(1, len(orders) + 1):
        payment_method_id = choice(list(payment_method_ids))
        cash_flow = orders[order_id - 1][6]  # TO-DO add shipping costs
        payment_date = date.fromtimestamp(
            (orders[order_id - 1][2] + timedelta(days=randint(0, 30))).timestamp()
        )
        if c == 0:
            print(orders[order_id - 1][2], payment_date)
            c += 1

        data.append((
            payment_id,
            payment_date,
            cash_flow,
            None,  # SUPPLIER_ID (keiner für Orders)
            order_id,  # ORDER_ID
            None,  # EMPLOYEE_ID (keiner für Orders)
            None,  # WAREHOUSE_ID (keiner für Orders)
            payment_method_id
        ))
        payment_id += 1

    # payments for suppliers
    for supplier_id in range(1, supplier_amount + 1):
        cash_flow = round(uniform(-10000, -1000), 2)  # Zufälliger negativer Betrag
        payment_date = datetime.now() - timedelta(days=randint(1, 365))
        data.append((
            payment_id,
            payment_date,
            cash_flow,
            supplier_id,  # SUPPLIER_ID
            None,  # ORDER_ID (keiner für Supplier)
            None,  # EMPLOYEE_ID (keiner für Supplier)
            None,  # WAREHOUSE_ID (keiner für Supplier)
            4  # Bank Transfer
        ))
        payment_id += 1

    # payments for employees
    for employee in employees:
        cash_flow = -employee[10]
        payment_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        data.append((
            payment_id,
            payment_date,
            cash_flow,
            None,  # SUPPLIER_ID (keiner für Employees)
            None,  # ORDER_ID (keiner für Employees)
            employee[0],  # EMPLOYEE_ID
            None,  # WAREHOUSE_ID (keiner für Employees)
            4  # Bank Transfer
        ))
        payment_id += 1

    # payments for rents for warehouses
    for warehouse_id in range(1, warehouse_amount + 1):
        cash_flow = round(uniform(-20000, -10000), 2)  # Zufälliger negativer Betrag für Lagerkosten
        payment_date = datetime.now() - timedelta(days=randint(1, 365))
        data.append((
            payment_id,
            payment_date,
            cash_flow,
            None,  # SUPPLIER_ID (keiner für Warehouses)
            None,  # ORDER_ID (keiner für Warehouses)
            None,  # EMPLOYEE_ID (keiner für Warehouses)
            warehouse_id,  # WAREHOUSE_ID
            4  # Bank Transfer
        ))
        payment_id += 1

    return data


# execution
print("Beginning data generation")
producer_names = get_producer_names()
category_data, c_name2new_id, old_id2c_name = generate_categories_from_csv()
producer_data = generate_producers(producer_names)

old_product_data, sku_list = generate_products_from_csv(producer_names, c_name2new_id, old_id2c_name)
new_product_data = generate_new_products(
    len(old_product_data), TOTAL_PRODUCT_AMOUNT, len(producer_names),
    [c_name2new_id[v] for v in old_id2c_name.values()], sku_list
)
product_data = old_product_data + new_product_data

supplier_data = generate_suppliers(TOTAL_SUPPLIER_AMOUNT)
product2supplier_data = generate_product2supplier(TOTAL_PRODUCT_AMOUNT)
customer_data = generate_customers(TOTAL_CUSTOMER_AMOUNT)
product2shopping_cart_data, amount_per_shopping_cart, price_per_shopping_cart = generate_product2shopping_cart(
    product_data)
shopping_cart_data = generate_shopping_carts(TOTAL_CUSTOMER_AMOUNT, amount_per_shopping_cart)
discount_data = generate_discounts(discount_codes)
shopping_cart2discount_data = generate_shopping_cart2discount(len(shopping_cart_data), len(discount_data))
roles_data = generate_roles(role_employee_map)
warehouses_data = generate_warehouses(TOTAL_WAREHOUSE_AMOUNT)
employees_data = generate_employees(TOTAL_EMPLOYEE_AMOUNT, deepcopy(role_employee_map), TOTAL_WAREHOUSE_AMOUNT)
shopping_order_data = generate_shopping_orders(
    len(shopping_cart_data), TOTAL_EMPLOYEE_AMOUNT, len(delivery_service_data), price_per_shopping_cart)
invoice_data = generate_invoices(len(shopping_cart_data))
delivery_note_data = generate_delivery_notes(len(shopping_cart_data), shipping_costs)
product2warehouse_data = generate_product2warehouse(TOTAL_PRODUCT_AMOUNT, TOTAL_WAREHOUSE_AMOUNT)
payment_data = generate_payments(shopping_order_data, [x[0] for x in payment_method_data], TOTAL_SUPPLIER_AMOUNT,
                                 employees_data, TOTAL_WAREHOUSE_AMOUNT)

query_data_collection: list[tuple[str, list]] = [
    (
        "product_category",
        "INSERT INTO PRODUCT_CATEGORY (product_category_id, name, parent_category) VALUES (:1, :2, :3)",
        category_data
    ), (
        "producer",
        "INSERT INTO PRODUCER (producer_id, NAME, COUNTRY, city, postal_code, street, house_number) VALUES (:1, :2, :3, :4, :5, :6, :7)",
        producer_data
    ), (
        "product",
        "INSERT INTO PRODUCT (product_id, cases_per_pallet, units_per_case, product_name, srp, recyclable_package, low_fat, retail_price, gross_weight, shelf_width, producer_id, sku, product_category_id, net_weight) "
        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)",
        product_data
    ), (
        "supplier",
        "INSERT INTO SUPPLIER (supplier_id, country, city, postal_code, street, house_number, name, iban, contact_person, phone_number, contact_person_email) "
        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",
        supplier_data
    ), (
        "product_to_supplier",
        "INSERT INTO PRODUCT_TO_SUPPLIER (product_id, supplier_id, purchase_price) VALUES (:1, :2, :3)",
        product2supplier_data
    ), (
        "customer",
        "INSERT INTO CUSTOMER (CUSTOMER_ID, STREET, HOUSE_NUMBER, POSTAL_CODE, CITY, FORENAME, MIDDLE_NAME, LASTNAME, IBAN, BIRTH_DATE, CREATED_ON, EMAIL, COUNTRY) "
        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)",
        customer_data
    ), (
        "shopping_cart",
        "INSERT INTO SHOPPING_CART (SHOPPING_CART_ID, DELETED_ON, CREATED_ON, AMOUNT_OF_PRODUCTS, CUSTOMER_ID) "
        "VALUES (:1, :2, :3, :4, :5)",
        shopping_cart_data
    ), (
        "product_to_shopping_cart",
        "INSERT INTO PRODUCT_TO_SHOPPING_CART (PRODUCT_ID, SHOPPING_CART_ID, TOTAL_AMOUNT) VALUES (:1, :2, :3)",
        product2shopping_cart_data
    ), (
        "discount",
        "INSERT INTO DISCOUNT (DISCOUNT_ID, PERCENTAGE, CODE) VALUES (:1, :2, :3)",
        discount_data
    ), (
        "shopping_cart_to_discount",
        "INSERT INTO SHOPPING_CART_TO_DISCOUNT (SHOPPING_CART_ID, DISCOUNT_ID) VALUES (:1, :2)",
        shopping_cart2discount_data
    ), (
        "delivery_service",
        "INSERT INTO DELIVERY_SERVICE (DELIVERY_SERVICE_ID, CITY, STREET, COUNTRY, POSTAL_CODE, HOUSE_NUMBER, NAME, PHONE_NUMBER, IBAN, CONTACT_PERSON) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)",
        delivery_service_data
    ), (
        "role",
        "INSERT INTO ROLE (ROLE_ID, NAME, IS_ADMIN) VALUES (:1, :2, :3)",
        roles_data
    ), (
        "warehouse",
        "INSERT INTO WAREHOUSE (WAREHOUSE_ID, COUNTRY, CITY, POSTAL_CODE, STREET, HOUSE_NUMBER, CAPACITY) VALUES (:1, :2, :3, :4, :5, :6, :7)",
        warehouses_data
    ), (
        "employee",
        "INSERT INTO EMPLOYEE (EMPLOYEE_ID, HOUSE_NUMBER, CITY, POSTAL_CODE, COUNTRY, STREET, LASTNAME, FORENAME, MIDDLE_NAME, BIRTH_DATE, SALARY, IBAN, TAX_CLASS, WORKING_SINCE, WAREHOUSE_ID, ROLE_ID) "
        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16)",
        employees_data
    ), (
        "shopping_order",
        "INSERT INTO SHOPPING_ORDER (ORDER_ID, STATUS, ORDER_TIME, SHOPPING_CART_ID, EMPLOYEE_ID, DELIVERY_SERVICE_ID, TOTAL_PRICE) VALUES (:1, :2, :3, :4, :5, :6, :7)",
        shopping_order_data
    ), (
        "invoice",
        "INSERT INTO INVOICE (INVOICE_ID, ORDER_ID, TAX_ID, ISSUE_DATE) VALUES (:1, :2, :3, :4)",
        invoice_data
    ), (
        "delivery_note",
        "INSERT INTO DELIVERY_NOTE (DELIVERY_ID, ORDER_ID, ISSUE_TIME, ARRIVAL_TIME, PICK_UP_TIME, SHIPPING_COST) "
        "VALUES (:1, :2, :3, :4, :5, :6) ",
        delivery_note_data
    ), (
        "product_to_warehouse",
        "INSERT INTO PRODUCT_TO_WAREHOUSE (PRODUCT_ID, WAREHOUSE_ID, STOCK, STORAGE_LOCATION) VALUES (:1, :2, :3, :4)",
        product2warehouse_data
    ), (
        "payment_method",
        "INSERT INTO PAYMENT_METHOD (PAYMENT_METHOD_ID, NAME) VALUES (:1, :2)",
        payment_method_data
    ), (
        "payment",
        "INSERT INTO PAYMENT (PAYMENT_ID, PAYMENT_DATE, CASH_FLOW, SUPPLIER_ID, ORDER_ID, EMPLOYEE_ID, WAREHOUSE_ID, PAYMENT_METHOD_ID) "
        "VALUES (:1, :2, :3, :4, :5, :6, :7, :8)",
        payment_data
    )
]


def execute_queries(insert_query_collection: list[tuple[str, list]]) -> None:
    with open('data_generation/input/drop_os_db.sql', 'r') as f:
        drop_tables_query: str = f.read()

    with open('data_generation/input/create_os_db.sql', 'r') as f:
        create_tables_query: str = f.read()

    with open('data_generation/input/create_os_trigger.sql', 'r') as f:
        create_trigger_query: str = f.read()

    total_queries = 0
    with oracledb.connect(user=user, password=pw, dsn=dsn) as connection:
        with connection.cursor() as cursor:

            print("Dropping tables...")
            start_time = datetime.now()
            for q in drop_tables_query.split(";"):
                try:
                    cursor.execute(q)
                except Exception as error:
                    print(error.args[0])
            deleted_timestamp = datetime.now()
            delete_time = (deleted_timestamp - start_time).total_seconds()
            print(f"Dropped {drop_tables_query.count(';')} tables in {delete_time} seconds")

            print("Creating tables...")
            for q in create_tables_query.split(";"):
                if q.isspace():
                    continue
                cursor.execute(q)

            create_timestamp = datetime.now()
            create_time = (create_timestamp - deleted_timestamp).total_seconds()
            print(f"Created {create_tables_query.count(';')} tables in {create_time} seconds")

            print("Filling tables with data...")
            for name, query, data in insert_query_collection:
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
                if q.isspace():
                    continue
                cursor.execute(q)

            trigger_timestamp = datetime.now()
            trigger_time = (trigger_timestamp - fill_timestamp).total_seconds()
            print(f"Created {create_trigger_query.count('--') + 1} triggers in {trigger_time} seconds")

        connection.commit()


print("Beginning export")
execute_queries(query_data_collection)
