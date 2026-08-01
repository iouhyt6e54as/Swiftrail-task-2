import os

POLICY_FILE_PATH = os.path.join(os.path.dirname(__file__), "docs", "refund_policy.txt")

def read_refund_policy() -> str:
    """Reads and returns Swiftrail's official refund policy document."""
    if os.path.exists(POLICY_FILE_PATH):
        with open(POLICY_FILE_PATH, "r") as f:
            return f.read()
    return "Refund policy document not found."