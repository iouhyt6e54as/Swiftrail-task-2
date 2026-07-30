from pydantic import BaseModel, Field
from typing import Optional

class ShipmentLookupInput(BaseModel):
    shipment_id: int = Field(..., description="The unique ID of the shipment to query.")

class ShipmentStatusUpdateInput(BaseModel):
    shipment_id: int = Field(..., description="The ID of the shipment to update.")
    new_status: str = Field(..., description="The new status (Pending, Assigned, In Transit, Delivered, Cancelled).")
    employee_id: int = Field(..., description="The ID of the employee performing the update.")
    user_confirmed: bool = Field(False, description="Set to True if user explicitly confirmed high-risk operations like Cancellation.")

class WarehouseAuditInput(BaseModel):
    warehouse_id: int = Field(..., description="The ID of the warehouse to audit.")

class DelayApologyInput(BaseModel):
    customer_name: str = Field(..., description="Customer's full name.")
    train_id: str = Field(..., description="Train or shipment identifier.")
    delay_minutes: int = Field(..., description="Length of delay in minutes.")