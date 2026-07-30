INSERT INTO Roles (role_name, description)
VALUES
('Operations Manager', 'Has full access to all operations'),
('Dispatcher', 'Assigns drivers and manages deliveries'),
('Customer Support', 'Views shipment information and assists customers'),
('Warehouse Staff', 'Updates shipment status inside warehouses');


INSERT INTO Employees (full_name, email, password_hash, department, role_id)
VALUES
('Ahmed Hassan', 'ahmed@swiftrail.com', 'hashed_password', 'Operations', 1),
('Sara Mohamed', 'sara@swiftrail.com', 'hashed_password', 'Dispatch', 2),
('Omar Ali', 'omar@swiftrail.com', 'hashed_password', 'Customer Service', 3),
('Mona Adel', 'mona@swiftrail.com', 'hashed_password', 'Warehouse', 4),
('Youssef Ibrahim', 'youssef@swiftrail.com', 'hashed_password', 'Dispatch', 2);


INSERT INTO Customers (full_name, phone, email, address)
VALUES
('Mohamed Tarek', '01012345678', 'mohamed@gmail.com', 'Alexandria, Egypt'),
('Nour Ahmed', '01198765432', 'nour@gmail.com', 'Cairo, Egypt'),
('Ali Mahmoud', '01211112222', 'ali@gmail.com', 'Giza, Egypt'),
('Salma Hassan', '01533334444', 'salma@gmail.com', 'Mansoura, Egypt'),
('Yara Samir', '01055556666', 'yara@gmail.com', 'Tanta, Egypt');



INSERT INTO Warehouses (warehouse_name, city, address)
VALUES
('Main Warehouse', 'Alexandria', 'Smouha'),
('Cairo Warehouse', 'Cairo', 'Nasr City'),
('Delta Warehouse', 'Tanta', 'Industrial Zone');


INSERT INTO Vehicles (plate_number, model, capacity, status)
VALUES
('ABC123', 'Toyota Hiace', 1200, 'Available'),
('XYZ456', 'Mercedes Sprinter', 1500, 'Available'),
('LMN789', 'Ford Transit', 1000, 'Maintenance'),
('QWE321', 'Nissan NV350', 900, 'Available'),
('RTY654', 'Hyundai H350', 1300, 'Out of Service');



INSERT INTO Drivers (full_name, phone, vehicle_id, status)
VALUES
('Mahmoud Salah', '01011111111', 1, 'Available'),
('Karim Adel', '01022222222', 2, 'Busy'),
('Hossam Samy', '01033333333', 3, 'Off Duty'),
('Mostafa Ali', '01044444444', 4, 'Available'),
('Amr Hassan', '01055555555', 5, 'Busy');



INSERT INTO Shipments
(customer_id, driver_id, warehouse_id,
pickup_address, delivery_address,
status, expected_delivery, delivered_at)

VALUES

(1,1,1,
'Alexandria Port',
'Smouha, Alexandria',
'In Transit',
'2026-08-02 18:00:00',
NULL),

(2,2,2,
'Nasr City',
'Maadi',
'Assigned',
'2026-08-03 14:00:00',
NULL),

(3,4,1,
'Smouha',
'Sidi Gaber',
'Delivered',
'2026-07-29 12:00:00',
'2026-07-29 11:45:00'),

(4,1,3,
'Tanta Industrial Zone',
'Kafr El Sheikh',
'Pending',
'2026-08-04 16:00:00',
NULL),

(5,2,2,
'Heliopolis',
'6th October',
'Cancelled',
'2026-08-01 10:00:00',
NULL);





INSERT INTO Shipment_Status_History
(shipment_id, status, updated_by)

VALUES

(1,'Pending',2),
(1,'Assigned',2),
(1,'Picked Up',4),
(1,'In Transit',2),

(2,'Pending',2),
(2,'Assigned',2),

(3,'Pending',2),
(3,'Assigned',2),
(3,'Picked Up',4),
(3,'Delivered',1),

(4,'Pending',4),

(5,'Pending',2),
(5,'Cancelled',1);





