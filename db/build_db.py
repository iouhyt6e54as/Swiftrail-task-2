import sqlite3

def init_db():
    conn = sqlite3.connect("swiftrail.db")
    cursor = conn.cursor()

    # 1. Create Tables matching her updated schema
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT UNIQUE NOT NULL,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS Employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        department TEXT,
        role_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES Roles(role_id)
    );

    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Warehouses (
        warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        warehouse_name TEXT NOT NULL,
        city TEXT NOT NULL,
        address TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Vehicles (
        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT UNIQUE,
        model TEXT,
        capacity REAL,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS Drivers (
        driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT,
        vehicle_id INTEGER,
        status TEXT,
        FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
    );

    CREATE TABLE IF NOT EXISTS Shipments (
        shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        driver_id INTEGER,
        warehouse_id INTEGER,
        pickup_address TEXT NOT NULL,
        delivery_address TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        expected_delivery DATETIME,
        delivered_at DATETIME,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
        FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
    );

    CREATE TABLE IF NOT EXISTS Shipment_Status_History (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shipment_id INTEGER,
        status TEXT NOT NULL,
        updated_by INTEGER,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id),
        FOREIGN KEY (updated_by) REFERENCES Employees(employee_id)
    );
    """)

    # 2. Insert her Seed Data
    cursor.executescript("""
    INSERT OR IGNORE INTO Roles (role_id, role_name, description) VALUES
    (1, 'Operations Manager', 'Has full access to all operations'),
    (2, 'Dispatcher', 'Assigns drivers and manages deliveries'),
    (3, 'Customer Support', 'Views shipment information and assists customers'),
    (4, 'Warehouse Staff', 'Updates shipment status inside warehouses');

    INSERT OR IGNORE INTO Employees (employee_id, full_name, email, password_hash, department, role_id) VALUES
    (1, 'Ahmed Hassan', 'ahmed@swiftrail.com', 'hashed_password', 'Operations', 1),
    (2, 'Sara Mohamed', 'sara@swiftrail.com', 'hashed_password', 'Dispatch', 2),
    (3, 'Omar Ali', 'omar@swiftrail.com', 'hashed_password', 'Customer Service', 3),
    (4, 'Mona Adel', 'mona@swiftrail.com', 'hashed_password', 'Warehouse', 4),
    (5, 'Youssef Ibrahim', 'youssef@swiftrail.com', 'hashed_password', 'Dispatch', 2);

    INSERT OR IGNORE INTO Customers (customer_id, full_name, phone, email, address) VALUES
    (1, 'Mohamed Tarek', '01012345678', 'mohamed@gmail.com', 'Alexandria, Egypt'),
    (2, 'Nour Ahmed', '01198765432', 'nour@gmail.com', 'Cairo, Egypt'),
    (3, 'Ali Mahmoud', '01211112222', 'ali@gmail.com', 'Giza, Egypt'),
    (4, 'Salma Hassan', '01533334444', 'salma@gmail.com', 'Mansoura, Egypt'),
    (5, 'Yara Samir', '01055556666', 'yara@gmail.com', 'Tanta, Egypt');

    INSERT OR IGNORE INTO Warehouses (warehouse_id, warehouse_name, city, address) VALUES
    (1, 'Main Warehouse', 'Alexandria', 'Smouha'),
    (2, 'Cairo Warehouse', 'Cairo', 'Nasr City'),
    (3, 'Delta Warehouse', 'Tanta', 'Industrial Zone');

    INSERT OR IGNORE INTO Vehicles (vehicle_id, plate_number, model, capacity, status) VALUES
    (1, 'ABC123', 'Toyota Hiace', 1200, 'Available'),
    (2, 'XYZ456', 'Mercedes Sprinter', 1500, 'Available'),
    (3, 'LMN789', 'Ford Transit', 1000, 'Maintenance'),
    (4, 'QWE321', 'Nissan NV350', 900, 'Available'),
    (5, 'RTY654', 'Hyundai H350', 1300, 'Out of Service');

    INSERT OR IGNORE INTO Drivers (driver_id, full_name, phone, vehicle_id, status) VALUES
    (1, 'Mahmoud Salah', '01011111111', 1, 'Available'),
    (2, 'Karim Adel', '01022222222', 2, 'Busy'),
    (3, 'Hossam Samy', '01033333333', 3, 'Off Duty'),
    (4, 'Mostafa Ali', '01044444444', 4, 'Available'),
    (5, 'Amr Hassan', '01055555555', 5, 'Busy');

    INSERT OR IGNORE INTO Shipments (shipment_id, customer_id, driver_id, warehouse_id, pickup_address, delivery_address, status, expected_delivery, delivered_at) VALUES
    (1, 1, 1, 1, 'Alexandria Port', 'Smouha, Alexandria', 'In Transit', '2026-08-02 18:00:00', NULL),
    (2, 2, 2, 2, 'Nasr City', 'Maadi', 'Assigned', '2026-08-03 14:00:00', NULL),
    (3, 3, 4, 1, 'Smouha', 'Sidi Gaber', 'Delivered', '2026-07-29 12:00:00', '2026-07-29 11:45:00'),
    (4, 4, 1, 3, 'Tanta Industrial Zone', 'Kafr El Sheikh', 'Pending', '2026-08-04 16:00:00', NULL),
    (5, 5, 2, 2, 'Heliopolis', '6th October', 'Cancelled', '2026-08-01 10:00:00', NULL);

    INSERT OR IGNORE INTO Shipment_Status_History (shipment_id, status, updated_by) VALUES
    (1, 'Pending', 2), (1, 'Assigned', 2), (1, 'Picked Up', 4), (1, 'In Transit', 2),
    (2, 'Pending', 2), (2, 'Assigned', 2),
    (3, 'Pending', 2), (3, 'Assigned', 2), (3, 'Picked Up', 4), (3, 'Delivered', 1),
    (4, 'Pending', 4),
    (5, 'Pending', 2), (5, 'Cancelled', 1);
    """)

    conn.commit()
    conn.close()
    print("Database built and seeded successfully!")

if __name__ == "__main__":
    init_db()