
import streamlit as st
from database import get_orders


def render():

    st.title("📊 Business Reports")

    st.write(
        "Review FreshFold's laundry operations, "
        "revenue, and order performance."
    )

    orders = get_orders()

    if not orders:
        st.info("No data is available for reports yet.")
        return

    # BUSINESS SUMMARY
    total_orders = len(orders)

    paid_orders = [
        order for order in orders
        if order[11] == "Paid"
    ]

    unpaid_orders = [
        order for order in orders
        if order[11] == "Unpaid"
    ]

    total_revenue = sum(
        order[7] or 0
        for order in paid_orders
    )

    completed_orders = sum(
        order[10] == "Claimed"
        for order in orders
    )

    col1, col2 = st.columns(2)

    col1.metric("Total Orders", total_orders)
    col2.metric("Total Revenue", f"₱{total_revenue:,.2f}")

    col3, col4 = st.columns(2)

    col3.metric("Paid Orders", len(paid_orders))
    col4.metric("Unpaid Orders", len(unpaid_orders))

    st.metric("Claimed Orders", completed_orders)

    st.divider()

    # ORDER STATUS REPORT
    st.subheader("📦 Orders by Status")

    status_counts = {}

    for order in orders:

        status = order[10]

        status_counts[status] = (
            status_counts.get(status, 0) + 1
        )

    for status, count in status_counts.items():

        st.write(f"**{status}**")

        st.progress(count / total_orders)

        st.caption(f"{count} order(s)")

    st.divider()

    # REVENUE BY SERVICE
    st.subheader("💰 Revenue by Laundry Service")

    service_revenue = {}

    for order in paid_orders:

        service = order[4]
        amount = order[7] or 0

        service_revenue[service] = (
            service_revenue.get(service, 0) + amount
        )

    if service_revenue:

        for service, revenue in service_revenue.items():

            st.write(f"**{service}**")
            st.write(f"₱{revenue:,.2f}")

    else:
        st.info("No recorded revenue yet.")

    st.divider()

    # PAYMENT SUMMARY
    st.subheader("💳 Payment Summary")

    paid_percentage = (
        len(paid_orders) / total_orders
    ) * 100

    st.write("Payment Completion Rate")

    st.progress(paid_percentage / 100)

    st.caption(f"{paid_percentage:.1f}% of orders have been paid.")
