import streamlit as st
from database import get_orders


def render():

    st.title("📋 Manage Laundry Orders")

    st.write(
        "Monitor all customer orders and their progress "
        "throughout the laundry process."
    )

    orders = get_orders()

    if not orders:
        st.info("No laundry orders have been recorded yet.")
        return

    # FILTERS
    st.subheader("Filter Orders")

    statuses = sorted(set(order[10] for order in orders))

    col1, col2 = st.columns(2)

    with col1:
        selected_status = st.selectbox(
            "Order Status",
            ["All"] + statuses
        )

    with col2:
        search_reference = st.text_input(
            "Search Order Reference or Customer Name"
        )

    filtered_orders = orders

    if selected_status != "All":
        filtered_orders = [
            order for order in filtered_orders
            if order[10] == selected_status
        ]

    if search_reference.strip():

        search = search_reference.strip().lower()

        filtered_orders = [
            order for order in filtered_orders
            if search in f"FF-{order[0]:04d}".lower()
            or search in order[1].lower()
        ]

    st.divider()

    st.subheader(f"Orders ({len(filtered_orders)})")

    if not filtered_orders:
        st.warning("No orders match your filters.")
        return

    # ORDER RECORDS
    for order in filtered_orders:

        order_id = order[0]
        customer_name = order[1]
        contact = order[2]
        service_name = order[4]
        estimated_kg = order[5]
        actual_kg = order[6]
        total_amount = order[7]
        notes = order[8]
        created_at = order[9]
        status = order[10]
        payment_status = order[11]

        with st.container(border=True):

            st.markdown(
                f"### FF-{order_id:04d} — {customer_name}"
            )

            st.caption(f"Submitted: {created_at}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("**Contact**")
                st.write(contact or "Not provided")

                st.write("**Service**")
                st.write(service_name)

            with col2:
                st.write("**Estimated Weight**")
                st.write(f"{estimated_kg:.1f} kg")

                st.write("**Actual Weight**")
                st.write(
                    f"{actual_kg:.1f} kg"
                    if actual_kg is not None
                    else "Not yet weighed"
                )

            with col3:
                st.write("**Order Status**")
                st.write(status)

                st.write("**Payment**")
                st.write(payment_status)

                st.write("**Final Amount**")
                st.write(
                    f"₱{total_amount:,.2f}"
                    if total_amount is not None
                    else "Not yet calculated"
                )

            if notes:
                st.write("**Special Instructions**")
                st.info(notes)
