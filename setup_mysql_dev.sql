-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS tech_dev_db;
CREATE USER IF NOT EXISTS 'tech_dev'@'localhost' IDENTIFIED BY 'tech_dev_pwd';
GRANT ALL PRIVILEGES ON `tech_dev_db`.* TO 'tech_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'tech_dev'@'localhost';
FLUSH PRIVILEGES;
