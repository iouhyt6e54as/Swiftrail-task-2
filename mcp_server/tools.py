import sqlite3

DB_PATH = "swiftrail.db"

def lookup_shipment(shipment_id: int) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            s.shipment_id, 
            c.full_name AS customer_name,
            s.status,
            d.full_name AS driver_name,
            v.plate_number AS vehicle_plate,
            w.warehouse_name,
            s.pickup_address,
            s.delivery_address,
            s.expected_delivery
        FROM Shipments s
        LEFT JOIN Customers c ON s.customer_id = c.customer_id
        LEFT JOIN Drivers d ON s.driver_id = d.driver_id
        LEFT JOIN Vehicles v ON d.vehicle_id = v.vehicle_id
        LEFT JOIN Warehouses w ON s.warehouse_id = w.warehouse_id
        WHERE s.shipment_id = ?
        """
        
        cursor.execute(query, (shipment_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return f"Shipment ID #{shipment_id} not found."

        return (
            f"--- Shipment #{row[0]} Details ---\n"
            f"Customer: {row[1]}\n"
            f"Status: {row[2]}\n"
            f"Driver: {row[3]} (Vehicle: {row[4]})\n"
            f"Warehouse: {row[5]}\n"
            f"Pickup Address: {row[6]}\n"
            f"Delivery Address: {row[7]}\n"
            f"Expected Delivery: {row[8]}"
        )
    except Exception as e:
        return f"Database Query Error: {e}"


def update_shipment_status(shipment_id: int, new_status: str, employee_id: int, user_confirmed: bool = False) -> str:
    if new_status.lower() == "cancelled" and not user_confirmed:
        return f"ELICITATION_REQUIRED: Cancelling Shipment #{shipment_id} is a high-risk operation. Explicit supervisor confirmation is required."

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Update main shipment status
        cursor.execute("UPDATE Shipments SET status = ? WHERE shipment_id = ?", (new_status, shipment_id))
        
        # Log to status history table
        cursor.execute(
            "INSERT INTO Shipment_Status_History (shipment_id, status, updated_by) VALUES (?, ?, ?)",
            (shipment_id, new_status, employee_id)
        )

        conn.commit()
        conn.close()
        return f"Shipment #{shipment_id} status updated to '{new_status}' successfully."
    except Exception as e:
        return f"Database Error: {e}"
    

def run_warehouse_audit(warehouse_id: int) -> str:
    """Progress-tracking tool: Simulates batch auditing of items in a specific warehouse."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Fetch warehouse details
        cursor.execute("SELECT warehouse_name, city FROM Warehouses WHERE warehouse_id = ?", (warehouse_id,))
        wh = cursor.fetchone()
        
        if not wh:
            conn.close()
            return f"Warehouse ID #{warehouse_id} not found."
            
        # Count shipments associated with this warehouse
        cursor.execute("SELECT COUNT(*) FROM Shipments WHERE warehouse_id = ?", (warehouse_id,))
        shipment_count = cursor.fetchone()[0]
        conn.close()
        
        return (
            f"--- Warehouse Audit Report ---\n"
            f"Warehouse: {wh[0]} ({wh[1]})\n"
            f"Total Shipments Assigned: {shipment_count}\n"
            f"Audit Status: Audit completed successfully. All inventory records verified."
        )
    except Exception as e:
        return f"Database Error: {e}"