import streamlit as st
from database import get_orders, get_services


def render():

    st.title("⚙️ Admin Dashboard")

    st.write(
        "Welcome to the FreshFold administration panel. "
        "Monitor your laundry shop operations."
    )

    orders = get_orders()
    services = get_services()

    # ORDER STATISTICS
    total_orders = len(orders)

    total_customers = len(set(
        order[1].strip().lower()
        for order in orders
    ))

    available_services = len(services)

    completed_orders = sum(
        order[10] == "Claimed"
        for order in orders
    )

    total_revenue = sum(
        (order[7] or 0)
        for order in orders
        if order[11] == "Paid"
    )

    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", total_orders)
    col2.metric("Total Customers", total_customers)
    col3.metric("Available Services", available_services)
    col4.metric("Completed Orders", completed_orders)

    st.metric(
        "Total Recorded Revenue",
        f"₱{total_revenue:,.2f}"
    )

    st.divider()

    # ORDER STATUS OVERVIEW
    st.subheader("Order Status Overview")

    statuses = [
        "Online Order Submitted",
        "Laundry Received",
        "Processing",
        "Ready for Pickup",
        "Claimed"
    ]

    for status in statuses:

        count = sum(
            order[10] == status
            for order in orders
        )

        st.write(f"**{status}**")

        st.progress(
            count / total_orders if total_orders else 0
        )

        st.caption(f"{count} order(s)")

    st.divider()

    # RECENT ORDERS
    st.subheader("Recent Laundry Orders")

    if not orders:
        st.info("No laundry orders have been recorded yet.")
        return

    for order in orders[:5]:

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"**FF-{order[0]:04d} — {order[1]}**"
                )

                st.caption(
                    f"{order[4]} • {order[5]:.1f} kg"
                )

            with col2:
                st.write(order[10])
                st.caption(order[11])
