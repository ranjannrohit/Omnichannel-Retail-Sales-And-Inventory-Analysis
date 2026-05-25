
-- DROP ALL EXISTING TABLES (clean slate)

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE sales PURGE';
    EXECUTE IMMEDIATE 'DROP TABLE stores PURGE';
    EXECUTE IMMEDIATE 'DROP TABLE products PURGE';
    EXECUTE IMMEDIATE 'DROP TABLE customers PURGE';
    EXECUTE IMMEDIATE 'DROP TABLE inventory PURGE';
    EXECUTE IMMEDIATE 'DROP TABLE promotions PURGE';
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Some tables did not exist - continuing');
END;
/

-- ------------------------------------------------------------------------
-- CREATE SALES TABLE (main transaction table)--

CREATE TABLE sales (
    sale_date DATE,              -- originally 'date' (Oracle reserved word)
    store_id NUMBER,
    sku_id NUMBER,
    customer_id NUMBER,
    quantity NUMBER,
    unit_price NUMBER,
    total_value NUMBER,
    channel VARCHAR2(20),
    discount_pct NUMBER
);

----------------------------------------------------------------------------------
-- CREATE STORES TABLE
--Based on stores_cleaned.csv
CREATE TABLE stores (
    store_id NUMBER PRIMARY KEY,
    store_name VARCHAR2(100),
    city VARCHAR2(50),
    store_type VARCHAR2(20),
    opening_date DATE
);

-- ---------------------------------------------------------------------------
-- CREATE PRODUCTS TABLE
-- Based on products_cleaned.csv

CREATE TABLE products (
    sku_id NUMBER PRIMARY KEY,
    sku_name VARCHAR2(200),
    category VARCHAR2(50),
    subcategory VARCHAR2(50),
    unit_price NUMBER,
    cost_price NUMBER,
    brand VARCHAR2(100)
);

-- -------------------------------------------------------------------------------
-- CREATE CUSTOMERS TABLE
-- Based on customers_cleaned.csv

CREATE TABLE customers (
    cust_id NUMBER PRIMARY KEY,
    age NUMBER,
    gender VARCHAR2(10),
    city VARCHAR2(50),
    loyalty_segment VARCHAR2(30),
    preferred_channel VARCHAR2(30),
    registration_date DATE
);

----------------------------------------------------------------------------------
-- CREATE INVENTORY TABLE
-- Based on  inventory_cleaned.csv

CREATE TABLE inventory (
    store_id NUMBER,
    sku_id NUMBER,
    stock_on_hand NUMBER,
    reorder_point NUMBER,
    safety_stock NUMBER,
    last_restock_date DATE
);

--------------------------------------------------------------------------------
-- CREATE PROMOTIONS TABLE
-- Based on  promotions_cleaned.csv

CREATE TABLE promotions (
    promo_id NUMBER PRIMARY KEY,
    promo_name VARCHAR2(100),
    promo_type VARCHAR2(50),
    start_date DATE,
    end_date DATE,
    discount_pct NUMBER,
    target_type VARCHAR2(50),
    target_value VARCHAR2(50)
);


-- VERIFY ALL TABLES CREATED --

SELECT table_name FROM user_tables 
WHERE table_name IN ('SALES', 'STORES', 'PRODUCTS', 'CUSTOMERS', 'INVENTORY', 'PROMOTIONS')
ORDER BY table_name;
-- Drop the existing table
DROP TABLE SALES PURGE;

-- Recreate with ALL columns matching your CSV
CREATE TABLE SALES (
    SALE_DATE DATE,
    STORE_ID NUMBER,
    SKU_ID NUMBER,
    CUSTOMER_ID NUMBER,
    QUANTITY NUMBER,
    UNIT_PRICE NUMBER,
    TOTAL_VALUE NUMBER,
    CHANNEL VARCHAR2(20),
    DISCOUNT_PCT NUMBER,
    ORDER_YEAR NUMBER,
    ORDER_MONTH NUMBER,
    ORDER_DAY NUMBER,
    ORDER_DAY_OF_WEEK NUMBER,
    ORDER_WEEKEND NUMBER,
    ORDER_QUARTER NUMBER
);
DROP TABLE STORES PURGE;

CREATE TABLE STORES (
    STORE_ID NUMBER PRIMARY KEY,
    STORE_NAME VARCHAR2(100),
    CITY VARCHAR2(50),
    STORE_TYPE VARCHAR2(20)
    -- opening_date est supprimé
);
DROP TABLE INVENTORY PURGE;

CREATE TABLE INVENTORY (
    STORE_ID NUMBER,
    SKU_ID NUMBER,
    STOCK_ON_HAND NUMBER,
    REORDER_POINT NUMBER,
    SAFETY_STOCK NUMBER,
    LAST_RESTOCK_DATE DATE,
    SNAPSHOT_DATE DATE
);
------------------------------------------------------------------
--Week 2 SQL Queries in Oracle SQL Developer--
------------------------------------------------------------------
---Query 1: Total Revenue & KPIs---
SELECT 
    SUM(TOTAL_VALUE) AS TOTAL_REVENUE,
    COUNT(*) AS TOTAL_TRANSACTIONS,
    ROUND(AVG(TOTAL_VALUE), 2) AS AVG_TRANSACTION_VALUE,
    COUNT(DISTINCT CUSTOMER_ID) AS UNIQUE_CUSTOMERS
FROM SALES;
---Query 2: Sales by Channel (Online vs Store)---
SELECT 
    CHANNEL,
    SUM(TOTAL_VALUE) AS REVENUE,
    COUNT(*) AS TRANSACTIONS,
    ROUND(AVG(TOTAL_VALUE), 2) AS AVG_VALUE
FROM SALES
GROUP BY CHANNEL
ORDER BY REVENUE DESC;
---Query 3: Sales by City (using JOIN with STORES)---
SELECT 
    S.CITY,
    SUM(SA.TOTAL_VALUE) AS TOTAL_REVENUE,
    COUNT(*) AS NUM_SALES,
    ROUND(AVG(SA.TOTAL_VALUE), 2) AS AVG_SALE
FROM SALES SA
INNER JOIN STORES S ON SA.STORE_ID = S.STORE_ID
GROUP BY S.CITY
ORDER BY TOTAL_REVENUE DESC;
---Query 4: Monthly Sales Trend---
SELECT 
    ORDER_YEAR,
    ORDER_MONTH,
    SUM(TOTAL_VALUE) AS MONTHLY_REVENUE,
    COUNT(*) AS NUM_TRANSACTIONS
FROM SALES
GROUP BY ORDER_YEAR, ORDER_MONTH
ORDER BY ORDER_YEAR, ORDER_MONTH;
---Query 5: Top 10 Products by Revenue (JOIN with PRODUCTS)---
SELECT 
    P.SKU_NAME,
    P.CATEGORY,
    SUM(SA.TOTAL_VALUE) AS TOTAL_REVENUE,
    SUM(SA.QUANTITY) AS TOTAL_QUANTITY
FROM SALES SA
INNER JOIN PRODUCTS P ON SA.SKU_ID = P.SKU_ID
GROUP BY P.SKU_NAME, P.CATEGORY
ORDER BY TOTAL_REVENUE DESC
FETCH FIRST 10 ROWS ONLY;
---Query 6: Running Total per Customer (Window Function – Session 5)---
SELECT 
    CUSTOMER_ID,
    SALE_DATE,
    TOTAL_VALUE,
    SUM(TOTAL_VALUE) OVER (
        PARTITION BY CUSTOMER_ID 
        ORDER BY SALE_DATE
    ) AS RUNNING_TOTAL
FROM SALES
WHERE CUSTOMER_ID IN (1, 2, 3)
ORDER BY CUSTOMER_ID, SALE_DATE;
---Query 7: Previous Purchase (LAG function – Session 5)---
SELECT 
    CUSTOMER_ID,
    SALE_DATE,
    TOTAL_VALUE,
    LAG(TOTAL_VALUE) OVER (
        PARTITION BY CUSTOMER_ID 
        ORDER BY SALE_DATE
    ) AS PREVIOUS_PURCHASE,
    TOTAL_VALUE - LAG(TOTAL_VALUE) OVER (
        PARTITION BY CUSTOMER_ID 
        ORDER BY SALE_DATE
    ) AS GROWTH
FROM SALES
WHERE CUSTOMER_ID IN (1, 2, 3)
ORDER BY CUSTOMER_ID, SALE_DATE;
---Query 8: Top 10 Customers by Spending (RANK function)---
SELECT 
    CUSTOMER_ID,
    SUM(TOTAL_VALUE) AS TOTAL_SPENT,
    RANK() OVER (ORDER BY SUM(TOTAL_VALUE) DESC) AS SPENDING_RANK
FROM SALES
WHERE CUSTOMER_ID > 0
GROUP BY CUSTOMER_ID
ORDER BY SPENDING_RANK
FETCH FIRST 10 ROWS ONLY;