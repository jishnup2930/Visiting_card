CREATE TABLE IF NOT EXISTS designation (
    id SERIAL PRIMARY KEY,
    designation_name VARCHAR(50) UNIQUE NOT NULL,
    num_of_leaves INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    fname VARCHAR(50),
    lname VARCHAR(50),
    designation VARCHAR(50) REFERENCES designation(designation_name),
    email VARCHAR(120),
    phone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS leaves (
    id SERIAL PRIMARY KEY,
    date DATE,
    employee_id INTEGER REFERENCES employees(id),
    reason VARCHAR(200),
    UNIQUE (employee_id, date)
);


