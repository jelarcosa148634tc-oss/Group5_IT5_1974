
import streamlit as st
from database import get_orders


def render():

    st.title("👨‍💼 Staff Dashboard")

    st.write("Monitor incoming laundry orders and shop operations.")

    orders = get_orders()

    # ORDER SUMMARY
    online_orders = sum(
        order[10] == "Online Order Submitted"
        for order in orders
    )

    received = sum(
        order[10] == "Laundry Received"
        for order in orders
    )

    processing = sum(
        order[10] == "Processing"
        for order in orders
    )

    ready = sum(
        order[10] == "Ready for Pickup"
        for order in orders
    )

    claimed = sum(
        order[10] == "Claimed"
        for order in orders
    )

    st.subheader("Order Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Online Orders", online_orders)
    col2.metric("Laundry Received", received)
    col3.metric("Processing", processing)

    col4, col5, col6 = st.columns(3)

    col4.metric("Ready for Pickup", ready)
    col5.metric("Claimed", claimed)
    col6.metric("Total Orders", len(orders))

    st.divider()

    # RECENT ORDERS
    st.subheader("Recent Laundry Orders")

    if not orders:
        st.info("No laundry orders have been submitted yet.")
        return

    for order in orders[:5]:

        order_id = order[0]
        customer_name = order[1]
        service_name = order[4]
        estimated_kg = order[5]
        status = order[10]

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**FF-{order_id:04d} — {customer_name}**")
                st.caption(f"{service_name} • {estimated_kg:.1f} kg")

            with col2:
                st.info(status)
