USE tech_test_db;
-- Create the carts table
CREATE TABLE carts (
    id VARCHAR(60) PRIMARY KEY,
    user_id VARCHAR(60) NOT NULL,
    product_id VARCHAR(60) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);