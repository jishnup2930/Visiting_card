CREATE TABLE IF NOT EXISTS designation (
    id SERIAL,
    designation_name VARCHAR(150) PRIMARY KEY,
    num_of_leaves INTEGER NOT NULL,
    UNIQUE (id, designation_name)
);



CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    fname VARCHAR(50),
    lname VARCHAR(50),
    designation VARCHAR(150) REFERENCES designation(designation_name),
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

INSERT INTO designation (designation_name, num_of_leaves)
VALUES  ('Staff Engineer', 20),
        ('Senior Engineer', 18),
        ('Junior Engineer', 12),
        ('Tech. Lead', 12),
        ('Project Manager', 15);