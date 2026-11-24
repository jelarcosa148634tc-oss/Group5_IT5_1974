
import streamlit as st
from database import get_orders, receive_laundry


def render():

    st.title("🧺 Receive Customer Laundry")

    st.write(
        "Verify the customer's online order, weigh the laundry, "
        "and confirm the final service charge."
    )

    orders = get_orders()

    pending_orders = [
        order for order in orders
        if order[10] == "Online Order Submitted"
    ]

    if not pending_orders:
        st.info("There are no online orders waiting for laundry drop-off.")
        return

    st.subheader("Orders Awaiting Drop-off")

    selected_order = st.selectbox(
        "Select Customer Order",
        pending_orders,
        format_func=lambda order: (
            f"FF-{order[0]:04d} | {order[1]} | "
            f"{order[4]} | Estimated: {order[5]:.1f} kg"
        )
    )

    st.divider()

    st.subheader("Order Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Order Reference**")
        st.write(f"FF-{selected_order[0]:04d}")

        st.write("**Customer Name**")
        st.write(selected_order[1])

        st.write("**Contact**")
        st.write(selected_order[2] or "Not provided")

    with col2:
        st.write("**Laundry Service**")
        st.write(selected_order[4])

        st.write("**Estimated Weight**")
        st.write(f"{selected_order[5]:.1f} kg")

    if selected_order[8]:
        st.write("**Special Instructions**")
        st.info(selected_order[8])

    st.divider()

    st.subheader("Weigh Laundry")

    actual_weight = st.number_input(
        "Actual Laundry Weight (kg)",
        min_value=0.1,
        max_value=100.0,
        value=float(selected_order[5]),
        step=0.1
    )

    service_price = next(
        (
            service[3]
            for service in __import__(
                "database"
            ).get_services()
            if service[0] == selected_order[3]
        ),
        None
    )

    if service_price is None:
        st.error("The original service is no longer available.")
        return

    final_amount = actual_weight * service_price

    st.metric(
        "Final Laundry Charge",
        f"₱{final_amount:,.2f}"
    )

    st.caption(
        f"Calculation: {actual_weight:.1f} kg × "
        f"₱{service_price:.2f} per kg"
    )

    if st.button(
        "Confirm Laundry Received",
        type="primary",
        use_container_width=True
    ):

        receive_laundry(
            selected_order[0],
            actual_weight,
            final_amount
        )

        st.success(
            f"Order FF-{selected_order[0]:04d} "
            "has been marked as Laundry Received!"
        )

        st.info(
            "The customer can now proceed with payment at the shop."
        )
