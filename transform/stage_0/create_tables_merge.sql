create table PRODUCT_CATEGORY
(
    PRODUCT_CATEGORY_ID NUMBER not null
        primary key,
    NAME                VARCHAR2(255),
    PARENT_CATEGORY     NUMBER
                               references PRODUCT_CATEGORY
                                   on delete set null
)
;

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
)
;

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
)
;

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
)
;

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
)
;

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
)
;

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
)
;

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
)
;

create table ROLE
(
    ROLE_ID  NUMBER not null
        primary key,
    NAME     VARCHAR2(100),
    IS_ADMIN NUMBER(1)
)
;

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
)
;

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
)
;

create table DISCOUNT
(
    DISCOUNT_ID NUMBER not null
        primary key,
    PERCENTAGE  NUMBER(5, 2)
        check (Percentage >= 0 AND Percentage <= 100),
    CODE        VARCHAR2(50)
)
;

create table INVOICE
(
    INVOICE_ID NUMBER       not null,
    ORDER_ID   NUMBER       not null
        references SHOPPING_ORDER
            on delete cascade,
    TAX_ID     VARCHAR2(20) not null,
    ISSUE_DATE DATE         not null,
    primary key (INVOICE_ID, ORDER_ID)
)
;

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
)
;

create table PAYMENT_METHOD
(
    PAYMENT_METHOD_ID NUMBER not null
        constraint SYS_C0014117
            primary key,
    NAME              VARCHAR2(50)
)
;

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
)
;
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
)
;

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
)
;


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
)
;

create table SHOPPING_CART_TO_DISCOUNT
(
    SHOPPING_CART_ID NUMBER not null
        references SHOPPING_CART,
    DISCOUNT_ID      NUMBER not null
        references DISCOUNT,
    primary key (SHOPPING_CART_ID, DISCOUNT_ID)
)
;

create table CUSTOMER_BILLING_ADDRESS
(
    CUSTOMER_BILLING_ADDRESS_ID    NUMBER(10) not null
        primary key,
    STREET                         VARCHAR2(100 char),
    CITY                           VARCHAR2(100 char),
    HOUSE_NUMBER                   VARCHAR2(20 char),
    COUNTRY                        VARCHAR2(100 char),
    POSTAL_CODE                    VARCHAR2(20 char),
    ADDITIONAL_ADDRESS_INFORMATION VARCHAR2(255 char),
    CUSTOMER_ID                    NUMBER(10) not null
        references CUSTOMER
)
;

comment on table CUSTOMER_BILLING_ADDRESS is 'Stores customer billing address details.'
/

create table POINT_OF_SALE
(
    POINT_OF_SALE_ID               NUMBER(10)        not null
        primary key,
    TYPE                           VARCHAR2(50 char),
    IS_A_PHYSICAL_STORE            NUMBER(1)         not null,
    POSTAL_CODE                    VARCHAR2(20 char) not null,
    CITY                           VARCHAR2(100 char),
    COUNTRY                        VARCHAR2(100 char),
    STREET                         VARCHAR2(100 char),
    PLACE_OF_SALE_NAME             VARCHAR2(50 char) not null,
    HOUSE_NUMBER                   VARCHAR2(20 char),
    ADDITIONAL_ADDRESS_INFORMATION VARCHAR2(255 char)
)
;

comment on table POINT_OF_SALE is 'Represents a location, either physical or online, where products are sold to customers.'
/

create table CASH_REGISTRY
(
    CASH_REGISTRY_ID NUMBER(10) not null
        primary key,
    POINT_OF_SALE_ID NUMBER(10) not null
        references POINT_OF_SALE
)
;

comment on table CASH_REGISTRY is 'Represents cash registers at specific points of sale.'
/

create table SALES_PRICE_CONDITION_SET
(
    SALES_PRICE_CONDITION_SET_ID NUMBER(10)    not null
        primary key,
    START_DATE                   DATE          not null,
    END_DATE                     DATE,
    VAT_RATE                     NUMBER(5, 2)  not null,
    NETTO_PRICE                  NUMBER(10, 2) not null,
    PRODUCT_ID                   NUMBER(10)    not null
        references PRODUCT,
    POINT_OF_SALE_ID             NUMBER(10)    not null
        references POINT_OF_SALE
)
;

comment on table SALES_PRICE_CONDITION_SET is 'Represents conditions for product sales prices.'
/

create table SUPPLIED_FROM_EXTENSION
(
    BATCH_ID             NUMBER(10)    not null
        primary key,
    NUMBER_OF_CASES      NUMBER(10)    not null,
    WEIGHT               NUMBER(10, 2),
    MANUFACTORING_DATE   DATE          not null,
    BBD                  DATE,
    ORDER_DATE           DATE          not null,
    DELIVERY_DATE        DATE          not null,
    SUPPLIER_ORDER_PRICE NUMBER(10, 2) not null,
    SUPPLIER_ORDER_ID    NUMBER(10)    not null,
    POINT_OF_SALE_ID     NUMBER(10)    not null
        references POINT_OF_SALE
)
;

create table PRODUCER_EXTENSION
(
    PRODUCER_EXTENSION_ID NUMBER(10) not null,
    PRODUCER_ID           NUMBER(10) not null
        references PRODUCER
            on delete cascade,
    primary key (PRODUCER_EXTENSION_ID, PRODUCER_ID)
)
;

comment on table PRODUCER_EXTENSION is 'Extends customer information.'
/

create table PRODUCT_EXTENSION
(
    PRODUCT_EXTENSION_ID NUMBER(10)    not null,
    PRODUCT_ID           NUMBER(10)    not null
        references PRODUCT
            on delete cascade,
    SHELF_HEIGHT         NUMBER(10, 2) not null,
    SHELF_DEPTH          NUMBER(10, 2) not null,
    primary key (PRODUCT_EXTENSION_ID, PRODUCT_ID)
)
;

comment on table PRODUCT_EXTENSION is 'Adds additional details to a product.'
/

create table DISCOUNT_EXTENSION
(
    DISCOUNT_EXTENSION_ID NUMBER(10) not null,
    DISCOUNT_ID           NUMBER(10) not null
        references DISCOUNT
            on delete cascade,
    POINT_OF_SALE_ID      NUMBER(10) not null
        references POINT_OF_SALE,
    primary key (DISCOUNT_EXTENSION_ID, DISCOUNT_ID)
)
;

comment on table DISCOUNT_EXTENSION is 'Extends discount information.'
/

create table SHOPPING_CART_EXTENSION
(
    SHOPPING_CART_EXTENSION_ID NUMBER(10) not null,
    SHOPPING_CART_ID           NUMBER(10) not null
        references SHOPPING_CART
            on delete cascade,
    POINT_OF_SALE_ID           NUMBER(10) not null
        references POINT_OF_SALE,
    primary key (SHOPPING_CART_EXTENSION_ID, SHOPPING_CART_ID)
)
;

comment on table SHOPPING_CART_EXTENSION is 'Adds extra details about shopping carts.'
/

create table CUSTOMER_EXTENSION
(
    CUSTOMER_EXTENSION_ID                   NUMBER(10) not null,
    CUSTOMER_ID                             NUMBER(10) not null
        references CUSTOMER
            on delete cascade,
    GENDER                                  CHAR(1 char),
    ADDITIONAL_DELIVERY_ADDRESS_INFORMATION VARCHAR2(255 char),
    primary key (CUSTOMER_EXTENSION_ID, CUSTOMER_ID)
)
;

comment on table CUSTOMER_EXTENSION is 'Extends customer information.'
/

create table SHOPPING_ORDER_EXTENSION
(
    SHOPPING_ORDER_EXTENSION_ID NUMBER(10) not null,
    ORDER_ID                    NUMBER(10) not null
        references SHOPPING_ORDER
            on delete cascade,
    NET_PURCHASE_PRICE          NUMBER(10, 2),
    POINT_OF_SALE_ID            NUMBER(10) not null
        references POINT_OF_SALE,
    CASH_REGISTRY_ID            NUMBER(10)
                                           references CASH_REGISTRY
                                               on delete set null,
    primary key (SHOPPING_ORDER_EXTENSION_ID, ORDER_ID)
)
;

comment on table SHOPPING_ORDER_EXTENSION is 'Extends shopping orders'
/

create table DELIVERY_SERVICE_EXTENSION
(
    DELIVERY_SERVICE_EXTENSION_ID NUMBER(10) not null,
    DELIVERY_SERVICE_ID           NUMBER(10) not null
        references DELIVERY_SERVICE
            on delete cascade,
    POINT_OF_SALE_ID              NUMBER(10) not null
        references POINT_OF_SALE,
    primary key (DELIVERY_SERVICE_EXTENSION_ID, DELIVERY_SERVICE_ID)
)
;

comment on table DELIVERY_SERVICE_EXTENSION is 'Extends delivery service information.'
/

create table PAYMENT_METHOD_EXTENSION
(
    PAYMENT_METHOD_EXTENSION_ID NUMBER(10) not null,
    PAYMENT_METHOD_ID           NUMBER(10) not null
        references PAYMENT_METHOD
            on delete cascade,
    primary key (PAYMENT_METHOD_EXTENSION_ID, PAYMENT_METHOD_ID)
)
;

comment on table PAYMENT_METHOD_EXTENSION is 'Adds extra information about payment methods.'
/

create table PAYMENT_EXTENSION
(
    PAYMENT_EXTENSION_ID NUMBER(10) not null,
    PAYMENT_ID           NUMBER(10) not null
        references PAYMENT
            on delete cascade,
    TRANSACTION_NUMBER   NUMBER(10) not null,
    POINT_OF_SALE_ID     NUMBER(10) not null
        references POINT_OF_SALE,
    primary key (PAYMENT_EXTENSION_ID, PAYMENT_ID)
)
;

comment on table PAYMENT_EXTENSION is 'Extends payment information.'
/

create table SUPPLIER_EXTENSION
(
    SUPPLIER_EXTENSION_ID          NUMBER(10) not null,
    SUPPLIER_ID                    NUMBER(10) not null
        references SUPPLIER
            on delete cascade,
    ADDRESS_TYPE                   VARCHAR2(50 char),
    ADDITIONAL_ADDRESS_INFORMATION VARCHAR2(255 char),
    primary key (SUPPLIER_EXTENSION_ID, SUPPLIER_ID)
)
;

comment on table SUPPLIER_EXTENSION is 'Adds address and additional information about suppliers.'
/

create table ROLE_EXTENSION
(
    ROLE_EXTENSION_ID NUMBER(10) not null,
    ROLE_ID           NUMBER(10) not null
        references ROLE
            on delete cascade,
    primary key (ROLE_EXTENSION_ID, ROLE_ID)
)
;

comment on table ROLE_EXTENSION is 'Extends role details for employees.'
/

create table EMPLOYEE_EXTENSION
(
    EMPLOYEE_EXTENSION_ID          NUMBER(10) not null,
    EMPLOYEE_ID                    NUMBER(10) not null
        references EMPLOYEE
            on delete cascade,
    BANK_NAME                      VARCHAR2(100 char),
    BIC                            VARCHAR2(11 char),
    WORKING_HOURS_PER_WEEK         NUMBER(3),
    PROVISION_RATE                 NUMBER(5, 2),
    ADDITIONAL_ADDRESS_INFORMATION VARCHAR2(255 char),
    ADDRESS_TYPE                   VARCHAR2(50 char),
    GENDER                         VARCHAR2(1),
    PHONE_NUMBER                   VARCHAR2(15),
    EMAIL                          VARCHAR2(100),
    primary key (EMPLOYEE_EXTENSION_ID, EMPLOYEE_ID)
)
;

comment on table EMPLOYEE_EXTENSION is 'Adds extra information about employees.'
/

create table WAREHOUSE_EXTENSION
(
    WAREHOUSE_EXTENSION_ID NUMBER(10) not null,
    WAREHOUSE_ID           NUMBER(10) not null
        references WAREHOUSE
            on delete cascade,
    POINT_OF_SALE_ID       NUMBER(10) not null
        references POINT_OF_SALE,
    primary key (WAREHOUSE_EXTENSION_ID, WAREHOUSE_ID)
)
;

comment on table WAREHOUSE_EXTENSION is 'Adds extra details related to warehouses.'
/

create table PRODUCT_CATEGORY_EXTENSION
(
    PRODUCT_CATEGORY_EXTENSION_ID NUMBER(10) not null,
    PRODUCT_CATEGORY_ID           NUMBER(10) not null
        references PRODUCT_CATEGORY
            on delete cascade,
    primary key (PRODUCT_CATEGORY_EXTENSION_ID, PRODUCT_CATEGORY_ID)
)
;

comment on table PRODUCT_CATEGORY_EXTENSION is 'Extends product category information.'
/

create table POS_TO_PRODUCER_EXTENSION
(
    PRODUCER_EXTENSION_ID NUMBER(10) not null,
    PRODUCER_ID           NUMBER(10) not null,
    POINT_OF_SALE_ID      NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    primary key (PRODUCER_EXTENSION_ID, PRODUCER_ID, POINT_OF_SALE_ID),
    foreign key (PRODUCER_EXTENSION_ID, PRODUCER_ID) references PRODUCER_EXTENSION
        on delete cascade
)
;

create table POS_TO_PRODUCT_EXTENSION
(
    POINT_OF_SALE_ID     NUMBER(10)   not null
        references POINT_OF_SALE
            on delete cascade,
    PRODUCT_EXTENSION_ID NUMBER(10)   not null,
    PRODUCT_ID           NUMBER(10)   not null,
    IS_BEING_SOLD        CHAR(1 char) not null,
    MIN_AGE_REQUIREMENT  NUMBER(3)
        check (min_age_requirement >= '0'),
    primary key (POINT_OF_SALE_ID, PRODUCT_EXTENSION_ID, PRODUCT_ID),
    foreign key (PRODUCT_EXTENSION_ID, PRODUCT_ID) references PRODUCT_EXTENSION
        on delete cascade
)
;

create table POS_TO_CUSTOMER_EXTENSION
(
    CUSTOMER_EXTENSION_ID NUMBER(10) not null,
    CUSTOMER_ID           NUMBER(10) not null,
    POINT_OF_SALE_ID      NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    primary key (CUSTOMER_EXTENSION_ID, CUSTOMER_ID, POINT_OF_SALE_ID),
    foreign key (CUSTOMER_EXTENSION_ID, CUSTOMER_ID) references CUSTOMER_EXTENSION
        on delete cascade
)
;

create table POS_TO_CUSTOMER_BILLING_ADDRESS
(
    POINT_OF_SALE_ID            NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    CUSTOMER_BILLING_ADDRESS_ID NUMBER(10) not null
        references CUSTOMER_BILLING_ADDRESS
            on delete cascade,
    primary key (POINT_OF_SALE_ID, CUSTOMER_BILLING_ADDRESS_ID)
)
;

create table POS_TO_PAYMENT_METHOD_EXTENSION
(
    PAYMENT_METHOD_EXTENSION_ID NUMBER(10) not null,
    PAYMENT_METHOD_ID           NUMBER(10) not null,
    POINT_OF_SALE_ID            NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    primary key (PAYMENT_METHOD_EXTENSION_ID, PAYMENT_METHOD_ID, POINT_OF_SALE_ID),
    foreign key (PAYMENT_METHOD_EXTENSION_ID, PAYMENT_METHOD_ID) references PAYMENT_METHOD_EXTENSION
        on delete cascade
)
;

create table POS_TO_SUPPLIER_EXTENSION
(
    SUPPLIER_EXTENSION_ID NUMBER(10) not null,
    SUPPLIER_ID           NUMBER(10) not null,
    POINT_OF_SALE_ID      NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    primary key (SUPPLIER_EXTENSION_ID, SUPPLIER_ID, POINT_OF_SALE_ID),
    foreign key (SUPPLIER_EXTENSION_ID, SUPPLIER_ID) references SUPPLIER_EXTENSION
        on delete cascade
)
;

create table POS_TO_ROLE_EXTENSION
(
    POINT_OF_SALE_ID  NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    ROLE_EXTENSION_ID NUMBER(10) not null,
    ROLE_ID           NUMBER(10) not null,
    primary key (POINT_OF_SALE_ID, ROLE_EXTENSION_ID, ROLE_ID),
    foreign key (ROLE_EXTENSION_ID, ROLE_ID) references ROLE_EXTENSION
        on delete cascade
)
;

create table POS_TO_EMPLOYEE_EXTENSION
(
    EMPLOYEE_EXTENSION_ID NUMBER(10) not null,
    EMPLOYEE_ID           NUMBER(10) not null,
    POINT_OF_SALE_ID      NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    primary key (EMPLOYEE_EXTENSION_ID, EMPLOYEE_ID, POINT_OF_SALE_ID),
    foreign key (EMPLOYEE_EXTENSION_ID, EMPLOYEE_ID) references EMPLOYEE_EXTENSION
        on delete cascade
)
;

create table POS_TO_PRODUCT_CATEGORY_EXTENSION
(
    PRODUCT_CATEGORY_EXTENSION_ID NUMBER(10) not null,
    PRODUCT_CATEGORY_ID           NUMBER(10) not null,
    POINT_OF_SALE_ID              NUMBER(10) not null
        references POINT_OF_SALE
            on delete cascade,
    primary key (PRODUCT_CATEGORY_EXTENSION_ID, PRODUCT_CATEGORY_ID, POINT_OF_SALE_ID),
    foreign key (PRODUCT_CATEGORY_EXTENSION_ID, PRODUCT_CATEGORY_ID) references PRODUCT_CATEGORY_EXTENSION
        on delete cascade
)
;

create table SUPERVISION
(
    EMPLOYEE_ID   NUMBER(10) not null
        references EMPLOYEE
            on delete cascade,
    SUPERVISOR_ID NUMBER(10) not null
        references EMPLOYEE
            on delete cascade,
    primary key (EMPLOYEE_ID, SUPERVISOR_ID)
)
;

create table PRODUCT_TO_SUPPLIER_TO_SUPPLIED_FROM_EXTENSION
(
    PRODUCT_ID     NUMBER(10) not null
        references PRODUCT
            on delete cascade,
    SUPPLIER_ID    NUMBER(10) not null
        references SUPPLIER
            on delete cascade,
    BATCH_ID       NUMBER(10) not null
        references SUPPLIED_FROM_EXTENSION
            on delete cascade,
    PURCHASE_PRICE NUMBER(10, 2)
        check (purchase_price >= '0'),
    primary key (PRODUCT_ID, SUPPLIER_ID, BATCH_ID)
)
;

