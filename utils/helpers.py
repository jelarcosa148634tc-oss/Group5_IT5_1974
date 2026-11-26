from datetime import datetime


def format_order_reference(order_id):
    """Generate a readable FreshFold order reference."""
    return f"FF-{order_id:04d}"


def format_currency(amount):
    """Format an amount as Philippine pesos."""
    return f"₱{(amount or 0):,.2f}"


def format_date(date_string):
    """Format an order date for display."""
    if not date_string:
        return "Not available"

    try:
        date = datetime.strptime(
            date_string,
            "%Y-%m-%d %I:%M %p"
        )
        return date.strftime("%b %d, %Y")
    except ValueError:
        return date_string


def format_time(date_string):
    """Extract the time from an order date."""
    if not date_string:
        return "Not available"

    try:
        date = datetime.strptime(
            date_string,
            "%Y-%m-%d %I:%M %p"
        )
        return date.strftime("%I:%M %p")
    except ValueError:
        return date_string


def get_status_icon(status):
    """Return an icon based on the laundry order status."""
    icons = {
        "Online Order Submitted": "📥",
        "Laundry Received": "🧺",
        "Processing": "🫧",
        "Ready for Pickup": "✅",
        "Claimed": "🎉"
    }

    return icons.get(status, "📋")


def get_payment_label(payment_status):
    """Return a readable payment status."""
    if payment_status == "Paid":
        return "Paid"

    return "Unpaid"