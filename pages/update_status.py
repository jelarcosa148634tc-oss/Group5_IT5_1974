
import streamlit as st
from database import get_orders, update_order_status


ORDER_STATUSES = [
    "Processing",
    "Ready for Pickup",
    "Claimed"
]


def render():

    st.title("🔄 Update Laundry Status")

    st.write(
        "Track and update the progress of customer laundry orders."
    )

    orders = get_orders()

    active_orders = [
        order for order in orders
        if order[10] in [
            "Laundry Received",
            "Processing",
            "Ready for Pickup"
        ]
    ]

    if not active_orders:
        st.info("There are no active laundry orders to update.")
        return

    st.subheader("Select an Order")

    selected_order = st.selectbox(
        "Customer Order",
        active_orders,
        format_func=lambda order: (
            f"FF-{order[0]:04d} | {order[1]} | {order[10]}"
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

        st.write("**Service**")
        st.write(selected_order[4])

    with col2:
        st.write("**Current Status**")
        st.info(selected_order[10])

        st.write("**Actual Weight**")
        st.write(
            f"{selected_order[6]:.1f} kg"
            if selected_order[6] is not None
            else "Not yet weighed"
        )

        st.write("**Payment Status**")
        st.write(selected_order[11])

    st.divider()

    st.subheader("Change Order Status")

    current_status = selected_order[10]

    if current_status == "Laundry Received":
        available_statuses = ["Processing"]
    elif current_status == "Processing":
        available_statuses = ["Ready for Pickup"]
    else:
        available_statuses = ["Claimed"]

    if selected_order[11] != "Paid":
        st.warning(
            "This order must be paid before laundry processing can continue."
        )
        return

    new_status = st.selectbox(
        "New Status",
        available_statuses
    )

    if st.button(
        "Save Status Update",
        type="primary",
        use_container_width=True
    ):

        update_order_status(
            selected_order[0],
            new_status
        )

        st.success(
            f"Order FF-{selected_order[0]:04d} "
            f"has been updated to {new_status}!"
        )

        st.rerun()
