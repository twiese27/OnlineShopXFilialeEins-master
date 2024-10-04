create table PRODUCT_CATEGORY
(
    PRODUCT_CATEGORY_ID NUMBER not null
        primary key,
    NAME                VARCHAR2(255),
    PARENT_CATEGORY     NUMBER
                               references PRODUCT_CATEGORY
                                   on delete set null
);

create table PRODUCER
(
    PRODUCER_ID  NUMBER not null
        primary key,
    POSTAL_CODE  VARCHAR2(10),
    STREET       VARCHAR2(255),
    CITY         VARCHAR2(100),
    HOUSE_NUMBER VARCHAR2(10),
    NAME         VARCHAR2(255),
    COUNTRY      VARCHAR2(100)
);

create table PRODUCT
(
    PRODUCT_ID          NUMBER        not null
        primary key,
    CASES_PER_PALLET    NUMBER
        check (Cases_per_pallet >= 0),
    UNITS_PER_CASE      NUMBER
        check (Units_per_case >= 0),
    PRODUCT_NAME        VARCHAR2(255),
    SRP                 NUMBER(10, 2)
        check (SRP >= 0),
    RECYCLABLE_PACKAGE  NUMBER(1),
    LOW_FAT             NUMBER(1),
    RETAIL_PRICE        NUMBER(10, 2) not null
        check (Retail_price >= 0),
    GROSS_WEIGHT        NUMBER(10, 3)
        check (gross_weight > 0),
    SHELF_WIDTH         NUMBER(10, 2)
        check (shelf_width > 0),
    PRODUCER_ID         NUMBER        not null
        references PRODUCER
            on delete set null,
    SKU                 NUMBER        not null,
    PRODUCT_CATEGORY_ID NUMBER
        references PRODUCT_CATEGORY
            on delete cascade,
    NET_WEIGHT          NUMBER
);

create table SUPPLIER
(
    SUPPLIER_ID          NUMBER not null
        primary key,
    HOUSE_NUMBER         VARCHAR2(10),
    CITY                 VARCHAR2(100),
    POSTAL_CODE          VARCHAR2(10),
    STREET               VARCHAR2(255),
    COUNTRY              VARCHAR2(100),
    NAME                 VARCHAR2(255),
    IBAN                 VARCHAR2(34),
    PHONE_NUMBER         VARCHAR2(15),
    CONTACT_PERSON       VARCHAR2(255),
    CONTACT_PERSON_EMAIL VARCHAR2(255)
);

create table WAREHOUSE
(
    WAREHOUSE_ID NUMBER not null
        primary key,
    STREET       VARCHAR2(255),
    CITY         VARCHAR2(100),
    COUNTRY      VARCHAR2(100),
    POSTAL_CODE  VARCHAR2(10),
    HOUSE_NUMBER VARCHAR2(10),
    CAPACITY     NUMBER
        check (Capacity >= 0)
);

create table CUSTOMER
(
    CUSTOMER_ID  NUMBER       not null
        primary key,
    STREET       VARCHAR2(255),
    HOUSE_NUMBER VARCHAR2(10),
    POSTAL_CODE  VARCHAR2(10) not null,
    CITY         VARCHAR2(100),
    MIDDLE_NAME  VARCHAR2(100),
    LASTNAME     VARCHAR2(100),
    IBAN         VARCHAR2(34),
    BIRTH_DATE   DATE,
    CREATED_ON   DATE,
    EMAIL        VARCHAR2(100),
    COUNTRY      VARCHAR2(100),
    FORENAME     VARCHAR2(20)
);

create table SHOPPING_CART
(
    SHOPPING_CART_ID   NUMBER not null
        primary key,
    DELETED_ON         DATE,
    CREATED_ON         DATE,
    AMOUNT_OF_PRODUCTS NUMBER not null
        check (Amount_of_products >= 0),
    CUSTOMER_ID        NUMBER
                              references CUSTOMER
                                  on delete set null
);

create table DELIVERY_SERVICE
(
    DELIVERY_SERVICE_ID NUMBER not null
        primary key,
    CITY                VARCHAR2(100),
    STREET              VARCHAR2(255),
    COUNTRY             VARCHAR2(100),
    POSTAL_CODE         VARCHAR2(10),
    HOUSE_NUMBER        VARCHAR2(10),
    NAME                VARCHAR2(255),
    PHONE_NUMBER        VARCHAR2(15),
    IBAN                VARCHAR2(100),
    CONTACT_PERSON      VARCHAR2(100)
);

create table ROLE
(
    ROLE_ID  NUMBER not null
        primary key,
    NAME     VARCHAR2(100),
    IS_ADMIN NUMBER(1)
);

create table EMPLOYEE
(
    EMPLOYEE_ID   NUMBER not null
        primary key,
    HOUSE_NUMBER  VARCHAR2(10),
    CITY          VARCHAR2(100),
    POSTAL_CODE   VARCHAR2(10),
    COUNTRY       VARCHAR2(100),
    STREET        VARCHAR2(255),
    LASTNAME      VARCHAR2(100),
    FORENAME      VARCHAR2(100),
    MIDDLE_NAME   VARCHAR2(100),
    BIRTH_DATE    DATE,
    SALARY        NUMBER(10, 2)
        check (Salary >= 0),
    IBAN          VARCHAR2(34),
    TAX_CLASS     NUMBER
        check (Tax_class >= 1 AND Tax_class <= 6),
    WORKING_SINCE DATE,
    WAREHOUSE_ID  NUMBER
                         references WAREHOUSE
                             on delete set null,
    ROLE_ID       NUMBER not null
        references ROLE
            on delete set null
);

create table SHOPPING_ORDER
(
    ORDER_ID            NUMBER not null
        primary key,
    STATUS              VARCHAR2(50),
    ORDER_TIME          TIMESTAMP(6),
    SHOPPING_CART_ID    NUMBER not null
        references SHOPPING_CART
            on delete set null,
    EMPLOYEE_ID         NUMBER
                               references EMPLOYEE
                                   on delete set null,
    DELIVERY_SERVICE_ID NUMBER
                               references DELIVERY_SERVICE
                                   on delete set null,
    TOTAL_PRICE         NUMBER(10, 2)
);

create table DISCOUNT
(
    DISCOUNT_ID NUMBER not null
        primary key,
    PERCENTAGE  NUMBER(5, 2)
        check (Percentage >= 0 AND Percentage <= 100),
    CODE        VARCHAR2(50)
);

create table INVOICE
(
    INVOICE_ID NUMBER       not null,
    ORDER_ID   NUMBER       not null
        references SHOPPING_ORDER
            on delete cascade,
    TAX_ID     VARCHAR2(20) not null,
    ISSUE_DATE DATE         not null,
    primary key (INVOICE_ID, ORDER_ID)
);

create table DELIVERY_NOTE
(
    DELIVERY_ID   NUMBER not null,
    ORDER_ID      NUMBER not null
        references SHOPPING_ORDER
            on delete cascade,
    ISSUE_TIME    TIMESTAMP(6),
    ARRIVAL_TIME  TIMESTAMP(6),
    PICK_UP_TIME  TIMESTAMP(6),
    SHIPPING_COST NUMBER,
    primary key (DELIVERY_ID, ORDER_ID)
);

create table PAYMENT_METHOD
(
    PAYMENT_METHOD_ID NUMBER not null
        constraint SYS_C0014117
            primary key,
    NAME              VARCHAR2(50)
);

create table PAYMENT
(
    PAYMENT_ID        NUMBER not null
        primary key,
    PAYMENT_DATE      DATE,
    CASH_FLOW         NUMBER(10, 2),
    SUPPLIER_ID       NUMBER
                             references SUPPLIER
                                 on delete set null,
    ORDER_ID          NUMBER
                             references SHOPPING_ORDER
                                 on delete set null,
    EMPLOYEE_ID       NUMBER
                             references EMPLOYEE
                                 on delete set null,
    WAREHOUSE_ID      NUMBER
                             references WAREHOUSE
                                 on delete set null,
    PAYMENT_METHOD_ID NUMBER not null
        constraint FK_PAYMENT_METHOD
            references PAYMENT_METHOD
                on delete set null
);

create table PRODUCT_TO_SUPPLIER
(
    PRODUCT_ID     NUMBER not null
        references PRODUCT
            on delete cascade,
    SUPPLIER_ID    NUMBER not null
        references SUPPLIER
            on delete cascade,
    PURCHASE_PRICE NUMBER(10, 2)
        check (Purchase_price >= 0),
    primary key (PRODUCT_ID, SUPPLIER_ID)
);

create table PRODUCT_TO_SHOPPING_CART
(
    PRODUCT_ID       NUMBER not null
        references PRODUCT
            on delete cascade,
    SHOPPING_CART_ID NUMBER not null
        references SHOPPING_CART
            on delete cascade,
    TOTAL_AMOUNT     NUMBER
        check (Total_amount >= 0),
    primary key (PRODUCT_ID, SHOPPING_CART_ID)
);

create table PRODUCT_TO_WAREHOUSE
(
    PRODUCT_ID       NUMBER not null
        references PRODUCT
            on delete cascade,
    WAREHOUSE_ID     NUMBER not null
        references WAREHOUSE
            on delete cascade,
    STOCK            NUMBER
        check (Stock >= 0),
    STORAGE_LOCATION VARCHAR2(255),
    primary key (PRODUCT_ID, WAREHOUSE_ID)
);

create table SHOPPING_CART_TO_DISCOUNT
(
    SHOPPING_CART_ID NUMBER not null
        references SHOPPING_CART,
    DISCOUNT_ID      NUMBER not null
        references DISCOUNT,
    primary key (SHOPPING_CART_ID, DISCOUNT_ID)
);
