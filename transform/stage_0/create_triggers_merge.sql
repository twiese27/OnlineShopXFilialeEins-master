--
create or replace trigger TRG_DELETE_CART_ITEMS
    before delete
    on SHOPPING_CART
    for each row
BEGIN
    DELETE FROM PRODUCT_TO_SHOPPING_CART WHERE Shopping_cart_ID = :OLD.Shopping_cart_ID;
    DELETE FROM SHOPPING_CART_TO_DISCOUNT WHERE Shopping_cart_ID = :OLD.Shopping_cart_ID;
END;

--
create or replace trigger TRG_REDUCE_STOCK
    after insert
    on SHOPPING_ORDER
    for each row
BEGIN
    UPDATE PRODUCT_TO_WAREHOUSE
    SET Stock = Stock - 1
    WHERE Product_ID = (SELECT Product_ID FROM PRODUCT_TO_SHOPPING_CART WHERE Shopping_cart_ID = :NEW.Shopping_cart_ID)
      AND Warehouse_ID = (SELECT Warehouse_ID FROM EMPLOYEE WHERE Employee_ID = :NEW.Employee_ID);
END;

--
create or replace trigger TRG_UPDATE_ORDER_STATUS
    after insert
    on PAYMENT
    for each row
BEGIN
    UPDATE SHOPPING_ORDER
    SET Status = 'Paid'
    WHERE Order_ID = :NEW.Order_ID;
END;

--
create or replace trigger TRG_UPDATE_CART_TOTAL_ADD
    after insert
    on PRODUCT_TO_SHOPPING_CART
    for each row
BEGIN
    UPDATE SHOPPING_CART
    SET Amount_of_products = Amount_of_products + :NEW.total_amount
    WHERE Shopping_cart_ID = :NEW.Shopping_cart_ID;
END;

--
create or replace trigger TRG_UPDATE_CART_TOTAL_REMOVE
    after delete
    on PRODUCT_TO_SHOPPING_CART
    for each row
BEGIN
    UPDATE SHOPPING_CART
    SET Amount_of_products = Amount_of_products - :OLD.total_amount
    WHERE Shopping_cart_ID = :OLD.Shopping_cart_ID;
END;

--
create or replace trigger TRG_CHECK_WAREHOUSE_CAPACITY
    before insert
    on PRODUCT_TO_WAREHOUSE
    for each row
DECLARE
    available_capacity NUMBER;
BEGIN
    SELECT Capacity
    INTO available_capacity
    FROM WAREHOUSE
    WHERE Warehouse_ID = :NEW.Warehouse_ID;

    IF :NEW.Stock > available_capacity THEN
        RAISE_APPLICATION_ERROR(-20001, 'Insufficient warehouse capacity.');
    END IF;
END;