import streamlit as st
from database import get_orders, record_payment


def render():

    st.title("💰 Laundry Payments")

    st.write(
        "Record customer payments after their laundry "
        "has been received and weighed."
    )

    orders = get_orders()

    unpaid_orders = [
        order for order in orders
        if order[10] == "Laundry Received"
        and order[11] == "Unpaid"
    ]

    paid_orders = [
        order for order in orders
        if order[11] == "Paid"
    ]

    # PAYMENT SUMMARY
    total_paid = sum(
        order[7] or 0
        for order in paid_orders
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Unpaid Orders", len(unpaid_orders))
    col2.metric("Paid Orders", len(paid_orders))
    col3.metric("Total Payments", f"₱{total_paid:,.2f}")

    st.divider()

    # UNPAID ORDERS
    st.subheader("Unpaid Orders")

    if not unpaid_orders:
        st.info("There are no unpaid orders awaiting payment.")

    else:
        for order in unpaid_orders:

            order_id = order[0]
            customer_name = order[1]
            service_name = order[4]
            actual_kg = order[6]
            total_amount = order[7]

            with st.container(border=True):

                st.markdown(
                    f"### FF-{order_id:04d} — {customer_name}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Service:** {service_name}")
                    st.write(f"**Actual Weight:** {actual_kg:.1f} kg")

                with col2:
                    st.write("**Payment Status:** Unpaid")
                    st.markdown(
                        f"### ₱{total_amount:,.2f}"
                    )

                if st.button(
                    "Confirm Payment",
                    key=f"payment_{order_id}",
                    type="primary",
                    use_container_width=True
                ):

                    record_payment(order_id)

                    st.success(
                        f"Payment for FF-{order_id:04d} "
                        "has been recorded successfully!"
                    )

                    st.rerun()

    st.divider()

    # PAYMENT HISTORY
    st.subheader("Payment History")

    if not paid_orders:
        st.info("No completed payments yet.")

    else:
        for order in paid_orders:

            with st.container(border=True):

                st.write(
                    f"**FF-{order[0]:04d} — {order[1]}**"
                )

                col1, col2 = st.columns(2)

                col1.write(order[4])
                col2.write(
                    f"₱{(order[7] or 0):,.2f}"
                )

                st.success("Paid")
