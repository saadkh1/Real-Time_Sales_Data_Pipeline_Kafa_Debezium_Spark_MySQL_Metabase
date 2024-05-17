CREATE DATABASE IF NOT EXISTS manager_sales_db;
USE manager_sales_db;
CREATE TABLE IF NOT EXISTS manager_sales (
    pos_id INT,
    pos_name VARCHAR(255),
    article VARCHAR(255),
    quantity FLOAT,
    unit_price FLOAT,
    total FLOAT,
    sale_type VARCHAR(255),
    payment_mode VARCHAR(255),
    latitude FLOAT, 
    longitude FLOAT,
    sale_time VARCHAR(255),
    sale_year INT,
    sale_month INT,
    sale_week_number INT,
    sale_day_of_week VARCHAR(255)
);

-- mysql -h Manager_Host -u root -p
-- secret
-- USE manager_sales_db; select * from manager_sales;