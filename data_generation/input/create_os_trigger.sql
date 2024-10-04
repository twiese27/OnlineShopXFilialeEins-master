CREATE TRIGGER trg_reduce_stock
    AFTER INSERT
    ON SHOPPING_ORDER
    FOR EACH ROW
BEGIN
    UPDATE PRODUCT_TO_WAREHOUSE
    SET Stock = Stock - 1
    WHERE Product_ID = (SELECT Product_ID FROM PRODUCT_TO_SHOPPING_CART WHERE Shopping_cart_ID = :NEW.Shopping_cart_ID)
      AND Warehouse_ID = (SELECT Warehouse_ID FROM EMPLOYEE WHERE Employee_ID = :NEW.Employee_ID);
END;

--
CREATE TRIGGER trg_delete_cart_items
    BEFORE DELETE
    ON SHOPPING_CART
    FOR EACH ROW
BEGIN
    DELETE FROM PRODUCT_TO_SHOPPING_CART WHERE Shopping_cart_ID = :OLD.Shopping_cart_ID;
    DELETE FROM SHOPPING_CART_TO_DISCOUNT WHERE Shopping_cart_ID = :OLD.Shopping_cart_ID;
END;

--
CREATE TRIGGER trg_update_order_status
    AFTER INSERT
    ON PAYMENT
    FOR EACH ROW
BEGIN
    UPDATE SHOPPING_ORDER
    SET Status = 'Paid'
    WHERE Order_ID = :NEW.Order_ID;
END;

--
CREATE TRIGGER trg_check_warehouse_capacity
    BEFORE INSERT
    ON PRODUCT_TO_WAREHOUSE
    FOR EACH ROW
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

--
CREATE TRIGGER trg_update_cart_total_add
    AFTER INSERT
    ON PRODUCT_TO_SHOPPING_CART
    FOR EACH ROW
BEGIN
    UPDATE SHOPPING_CART
    SET Amount_of_products = Amount_of_products + :NEW.total_amount
    WHERE Shopping_cart_ID = :NEW.Shopping_cart_ID;
END;

--
CREATE TRIGGER trg_update_cart_total_remove
    AFTER DELETE
    ON PRODUCT_TO_SHOPPING_CART
    FOR EACH ROW
BEGIN
    UPDATE SHOPPING_CART
    SET Amount_of_products = Amount_of_products - :OLD.total_amount
    WHERE Shopping_cart_ID = :OLD.Shopping_cart_ID;
END;
