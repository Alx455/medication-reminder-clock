CREATE DATABASE medication_clock;
USE medication_clock;

CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    age INT,
    weight_kg DECIMAL(5, 2)
);

CREATE TABLE medications (
    medication_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    medication_name VARCHAR(100),
    dosage VARCHAR(50),
    frequency INT,
    frequency_unit ENUM('days', 'hours', 'minutes'),
    start_date DATE,
    end_date DATE,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);
