-- leads_db: sample schema for db-sentinel development/testing
-- Generic lead-capture schema — NOT derived from any employer's real
-- schema, purely illustrative data for backup testing.

CREATE DATABASE IF NOT EXISTS leads_db;
USE leads_db;

CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL,
    phone VARCHAR(30),
    source VARCHAR(60) NOT NULL DEFAULT 'website_form',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lead_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lead_id INT NOT NULL,
    event_type ENUM('form_submitted', 'email_sent', 'contacted', 'converted') NOT NULL,
    event_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

INSERT INTO leads (name, email, phone, source) VALUES
    ('Gabriel Nunes', 'gabriel.nunes@example.com', '+351911111111', 'website_form'),
    ('Helena Pinto', 'helena.pinto@example.com', '+351922222222', 'landing_page'),
    ('Igor Marques', 'igor.marques@example.com', NULL, 'website_form'),
    ('Joana Rocha', 'joana.rocha@example.com', '+351933333333', 'referral');

INSERT INTO lead_events (lead_id, event_type) VALUES
    (1, 'form_submitted'),
    (1, 'email_sent'),
    (2, 'form_submitted'),
    (2, 'contacted'),
    (2, 'converted'),
    (3, 'form_submitted'),
    (4, 'form_submitted'),
    (4, 'email_sent');
