import sys
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Locate project root and server script using absolute paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_SCRIPT = os.path.join(PROJECT_ROOT, "mcp_server", "server.py")

# Ensure Python can resolve imports from project root inside subprocess
env = os.environ.copy()
env["PYTHONPATH"] = PROJECT_ROOT

async def run_agent():
    print("==================================================")
    print("🚀 Swiftrail Logistics - MCP Client Connecting...")
    print("==================================================")

    # Launch server process via STDIO
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_SCRIPT],
        env=env
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Real MCP Negotiation & Capability Handshake
            await session.initialize()
            print("\n[Handshake] Connected to FastMCP Server via STDIO!")
            
            # Retrieve exposed tools from server
            tools_response = await session.list_tools()
            available_tools = [t.name for t in tools_response.tools]
            print(f"[Handshake] Discovered Server Tools: {available_tools}")

            # 2. Test Safe Read Tool (lookup shipment details)
            shipment_id = 1
            print(f"\n--- 1. Testing Read Tool: Lookup Shipment #{shipment_id} ---")
            result_read = await session.call_tool("get_shipment_details", {"shipment_id": shipment_id})
            print(result_read.content[0].text)

            # 3. Test Progress Tool (generate warehouse audit report)
            warehouse_id = 1
            print(f"\n--- 2. Testing Progress Tool: Audit Warehouse #{warehouse_id} ---")
            result_audit = await session.call_tool("generate_warehouse_audit", {"warehouse_id": warehouse_id})
            print(result_audit.content[0].text)

            # 4. Test High-Risk Write Tool (triggers mid-call elicitation)
            print(f"\n--- 3. Testing High-Risk Write Tool: Cancel Shipment #{shipment_id} ---")
            
            # First Attempt without confirmation
            res_unconfirmed = await session.call_tool("change_shipment_status", {
                "shipment_id": shipment_id,
                "new_status": "Cancelled",
                "employee_id": 1,
                "user_confirmed": False
            })
            response_text = res_unconfirmed.content[0].text
            print(f"Server Response: {response_text}")

            # Handling Mid-Call Elicitation
            if "ELICITATION_REQUIRED" in response_text:
                print("\n⚠️ [Elicitation Triggered] Mid-call pause: High-risk action detected!")
                human_input = input("❓ Human Confirmation Needed: Are you sure you want to CANCEL this shipment? (yes/no): ")

                if human_input.strip().lower() == "yes":
                    print("\n[Elicitation Approved] Retrying action with explicit user confirmation...")
                    res_confirmed = await session.call_tool("change_shipment_status", {
                        "shipment_id": shipment_id,
                        "new_status": "Cancelled",
                        "employee_id": 1,
                        "user_confirmed": True
                    })
                    print(f"Server Response: {res_confirmed.content[0].text}")
                else:
                    print("\n❌ [Elicitation Aborted] Action cancelled by Supervisor.")

if __name__ == "__main__":
    asyncio.run(run_agent())