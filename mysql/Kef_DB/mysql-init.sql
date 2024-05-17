CREATE DATABASE IF NOT EXISTS kef_sales_db;
USE kef_sales_db;
CREATE TABLE IF NOT EXISTS kef_sales (
    pos_id INT,
    pos_name VARCHAR(255),
    article VARCHAR(255),
    quantity FLOAT,
    unit_price FLOAT,
    total FLOAT,
    sale_type VARCHAR(255),
    payment_mode VARCHAR(255),
    latitude VARCHAR(255), 
    longitude VARCHAR(255),
    sale_time VARCHAR(255)
);

-- mysql -h Kef_Host -u root -p
-- secret
-- USE kef_sales_db; select * from kef_sales;