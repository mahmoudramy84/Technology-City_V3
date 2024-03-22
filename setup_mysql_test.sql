-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS tech_test_db;
CREATE USER IF NOT EXISTS 'tech_test'@'localhost' IDENTIFIED BY 'tech_test_pwd';
GRANT ALL PRIVILEGES ON `tech_test_db`.* TO 'tech_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'tech_test'@'localhost';
FLUSH PRIVILEGES;
