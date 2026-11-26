
def filter_orders_by_status(orders, status):
    """Filter orders using their current status."""
    if status == "All":
        return orders

    return [
        order for order in orders
        if order[10] == status
    ]


def filter_orders_by_payment(orders, payment_status):
    """Filter orders by payment status."""
    if payment_status == "All":
        return orders

    return [
        order for order in orders
        if order[11] == payment_status
    ]


def search_orders(orders, keyword):
    """Search orders by reference number or customer name."""
    keyword = keyword.strip().lower()

    if not keyword:
        return orders

    results = []

    for order in orders:
        order_id = f"FF-{order[0]:04d}".lower()
        customer_name = str(order[1]).lower()

        if keyword in order_id or keyword in customer_name:
            results.append(order)

    return results


def count_orders_by_status(orders):
    """Count how many orders belong to each status."""
    statuses = [
        "Online Order Submitted",
        "Laundry Received",
        "Processing",
        "Ready for Pickup",
        "Claimed"
    ]

    return {
        status: sum(
            order[10] == status
            for order in orders
        )
        for status in statuses
    }


def calculate_total_revenue(orders):
    """Calculate revenue from paid orders."""
    return sum(
        (order[7] or 0)
        for order in orders
        if order[11] == "Paid"
    )


def calculate_total_unpaid(orders):
    """Calculate the total amount still unpaid."""
    return sum(
        (order[7] or 0)
        for order in orders
        if order[11] == "Unpaid"
        and order[7] is not None
    )


def get_recent_orders(orders, limit=5):
    """Return the most recent orders."""
    return sorted(
        orders,
        key=lambda order: order[0],
        reverse=True
    )[:limit]


def get_customer_orders(orders, customer_name):
    """Find orders belonging to a specific customer name."""
    customer_name = customer_name.strip().lower()

    return [
        order for order in orders
        if str(order[1]).strip().lower() == customer_name
    ]
