CREATE DATABASE Swiftrail_Logistics;

USE Swiftrail_Logistics;

CREATE TABLE Roles (
    role_id INT IDENTITY(1,1) PRIMARY KEY,
    role_name NVARCHAR(50) NOT NULL UNIQUE,
    description NVARCHAR(255)
);

CREATE TABLE Employees (
    employee_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    department NVARCHAR(100),
    role_id INT NOT NULL,

    CONSTRAINT FK_Employees_Roles
    FOREIGN KEY (role_id)
    REFERENCES Roles(role_id)
);


CREATE TABLE Customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    phone NVARCHAR(20) NOT NULL,
    email NVARCHAR(100),
    address NVARCHAR(255) NOT NULL
);


CREATE TABLE Warehouses (
    warehouse_id INT IDENTITY(1,1) PRIMARY KEY,
    warehouse_name NVARCHAR(100) NOT NULL,
    city NVARCHAR(100) NOT NULL,
    address NVARCHAR(255) NOT NULL
);


CREATE TABLE Vehicles (
    vehicle_id INT IDENTITY(1,1) PRIMARY KEY,
    plate_number NVARCHAR(20) NOT NULL UNIQUE,
    model NVARCHAR(50),
    capacity DECIMAL(8,2),
    status NVARCHAR(30)
        CHECK (status IN ('Available','Maintenance','Out of Service'))
);



CREATE TABLE Drivers (
    driver_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    phone NVARCHAR(20),
    vehicle_id INT,
    status NVARCHAR(30)
        CHECK (status IN ('Available','Busy','Off Duty')),

    CONSTRAINT FK_Drivers_Vehicles
    FOREIGN KEY (vehicle_id)
    REFERENCES Vehicles(vehicle_id)
);



CREATE TABLE Shipments (
    shipment_id INT IDENTITY(1,1) PRIMARY KEY,

    customer_id INT NOT NULL,

    driver_id INT,

    warehouse_id INT NOT NULL,

    pickup_address NVARCHAR(255) NOT NULL,

    delivery_address NVARCHAR(255) NOT NULL,

    status NVARCHAR(30)
        CHECK (status IN (
            'Pending',
            'Assigned',
            'Picked Up',
            'In Transit',
            'Delivered',
            'Cancelled'
        )),

    created_at DATETIME DEFAULT GETDATE(),

    expected_delivery DATETIME,

    delivered_at DATETIME,

    CONSTRAINT FK_Shipments_Customers
    FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id),

    CONSTRAINT FK_Shipments_Drivers
    FOREIGN KEY (driver_id)
    REFERENCES Drivers(driver_id),

    CONSTRAINT FK_Shipments_Warehouses
    FOREIGN KEY (warehouse_id)
    REFERENCES Warehouses(warehouse_id)
);



CREATE TABLE Shipment_Status_History (

    history_id INT IDENTITY(1,1) PRIMARY KEY,

    shipment_id INT NOT NULL,

    status NVARCHAR(30),

    updated_by INT NOT NULL,

    updated_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT FK_History_Shipments
    FOREIGN KEY (shipment_id)
    REFERENCES Shipments(shipment_id),

    CONSTRAINT FK_History_Employees
    FOREIGN KEY (updated_by)
    REFERENCES Employees(employee_id)
);