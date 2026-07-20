-- app_db: sample schema for db-sentinel development/testing
-- Generic operations schema (customers + orders) — NOT derived from any
-- employer's real schema, purely illustrative data for backup testing.

CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    amount_cents INT NOT NULL,
    status ENUM('pending', 'paid', 'cancelled') NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO customers (full_name, email) VALUES
    ('Ana Silva', 'ana.silva@example.com'),
    ('Bruno Costa', 'bruno.costa@example.com'),
    ('Carla Dias', 'carla.dias@example.com'),
    ('Duarte Melo', 'duarte.melo@example.com'),
    ('Elsa Ramos', 'elsa.ramos@example.com'),
    ('Filipe Sousa', 'filipe.sousa@example.com');

INSERT INTO orders (customer_id, amount_cents, status) VALUES
    (1, 12990, 'paid'),
    (1, 4500,  'pending'),
    (2, 8990,  'paid'),
    (3, 15000, 'cancelled'),
    (4, 2999,  'paid'),
    (5, 7650,  'pending'),
    (6, 11200, 'paid');
