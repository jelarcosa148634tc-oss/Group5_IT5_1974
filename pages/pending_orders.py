
import streamlit as st
from database import get_orders


def render():

    st.title("📋 Pending Laundry Orders")

    st.write(
        "View customer orders that have been submitted "
        "online and are waiting for laundry drop-off."
    )

    orders = get_orders()

    pending_orders = [
        order for order in orders
        if order[10] == "Online Order Submitted"
    ]

    st.metric("Pending Orders", len(pending_orders))

    st.divider()

    if not pending_orders:
        st.success("There are no pending orders right now.")
        return

    for order in pending_orders:

        order_id = order[0]
        customer_name = order[1]
        contact = order[2]
        service_name = order[4]
        estimated_kg = order[5]
        notes = order[8]
        created_at = order[9]

        with st.container(border=True):

            st.subheader(f"FF-{order_id:04d}")

            st.caption(f"Submitted: {created_at}")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Customer Name**")
                st.write(customer_name)

                st.write("**Contact Information**")
                st.write(contact or "Not provided")

            with col2:
                st.write("**Laundry Service**")
                st.write(service_name)

                st.write("**Estimated Weight**")
                st.write(f"{estimated_kg:.1f} kg")

            if notes:
                st.write("**Special Instructions**")
                st.info(notes)

            st.warning("Waiting for customer to bring laundry to the shop.")
