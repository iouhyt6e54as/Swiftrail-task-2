def draft_delay_apology(customer_name: str, train_id: str, delay_minutes: int) -> str:
    """Generates a standardized customer service response template for delayed trains."""
    return f"""
    Dear {customer_name},

    We sincerely apologize for the delay of {delay_minutes} minutes on SwiftRail Train #{train_id}. 
    We understand how valuable your time is and regret any inconvenience caused to your journey.

    If your delay was greater than 15 minutes, you may be eligible for a ticket refund according to our policy.

    Best regards,
    SwiftRail Customer Support
    """