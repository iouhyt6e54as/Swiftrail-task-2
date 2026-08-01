import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastmcp import FastMCP
from mcp_server.resources import read_refund_policy
from mcp_server.prompts import draft_delay_apology
from mcp_server.tools import lookup_shipment, update_shipment_status, run_warehouse_audit

# 1. Initialize FastMCP Server
mcp = FastMCP("SwiftRail-Logistics-MCP-Server")

# 2. Register Static Resource (Policy Document - Protocol Concern #4)
@mcp.resource("resource://swiftrail/refund_policy")
def refund_policy_resource() -> str:
    """Exposes Swiftrail policy document as a read-only resource."""
    return read_refund_policy()

# 3. Register Prompt Template (Protocol Concern #5)
@mcp.prompt("draft_delay_apology")
def apology_prompt(customer_name: str, train_id: str, delay_minutes: int) -> str:
    """Drafts a standardized apology customer service template."""
    return draft_delay_apology(customer_name, train_id, delay_minutes)

# 4. Register Read Tool (Safe Database Lookup)
@mcp.tool()
def get_shipment_details(shipment_id: int) -> str:
    """Look up shipment details, customer, driver, and warehouse status in DB."""
    return lookup_shipment(shipment_id)

# 5. Register Write Tool (Restricted DB Update with Elicitation - Protocol Concern #3 & #8)
@mcp.tool()
def change_shipment_status(shipment_id: int, new_status: str, employee_id: int, user_confirmed: bool = False) -> str:
    """Update shipment status in DB. Cancelling a shipment triggers mid-call human approval."""
    return update_shipment_status(shipment_id, new_status, employee_id, user_confirmed)

# 6. Register Progress Tracking Tool (Protocol Concern #7)
@mcp.tool()
def generate_warehouse_audit(warehouse_id: int) -> str:
    """Runs a warehouse inventory audit report with real-time progress updates."""
    return run_warehouse_audit(warehouse_id)

if __name__ == "__main__":
    mcp.run()
