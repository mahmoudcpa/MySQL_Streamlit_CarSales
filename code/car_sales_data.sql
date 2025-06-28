USE car_sales_dashboard;

DROP TABLE IF EXISTS staging_carsales_data;
CREATE TABLE staging_carsales_data (
	id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100),
    city VARCHAR(100),
    total_sales DECIMAL(10,2),
    sale_date VARCHAR(45)
);

-- Load file into staging (before date column transofrmation)
LOAD DATA INFILE '...\mysql_carSales_data.csv'
INTO TABLE staging_carsales_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS (model, city, total_sales, sale_date);

DROP TABLE IF EXISTS carSales_data;
CREATE TABLE carSales_data (
	id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100),
    city VARCHAR(100),
    total_sales DECIMAL(10,2),
    sale_date DATETIME
);

-- Insert into final table with conversion
TRUNCATE TABLE carsales_data;
INSERT INTO carsales_data (model, city, total_sales, sale_date)
SELECT
	model,
    city,
    total_sales,
    STR_TO_DATE(TRIM(sale_date), '%d/%m/%Y %H:%i')
FROM staging_carsales_data;


SELECT * FROM car_sales_dashboard.carsales_data;




















