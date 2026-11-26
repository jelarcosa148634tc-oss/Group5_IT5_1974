import streamlit as st
from database import get_orders


def render():

    st.title("📦 My Laundry Orders")
    st.write("Track your submitted laundry orders.")

    orders = get_orders()

    if not orders:
        st.info("You haven't submitted any laundry orders yet.")
        return

    for order in orders:

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

            st.subheader(f"Order FF-{order_id:04d}")

            st.caption(f"Submitted: {created_at}")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Service**")
                st.write(service_name)

                st.write("**Estimated Weight**")
                st.write(f"{estimated_kg:.1f} kg")

                st.write("**Actual Weight**")
                st.write(
                    f"{actual_kg:.1f} kg"
                    if actual_kg is not None
                    else "Not yet weighed"
                )

            with col2:
                st.write("**Order Status**")
                st.info(status)

                st.write("**Payment**")
                st.write(payment_status)

                st.write("**Final Amount**")
                st.write(
                    f"₱{total_amount:,.2f}"
                    if total_amount is not None
                    else "To be confirmed"
                )

            if notes:
                st.write("**Special Instructions**")
                st.write(notes)

            if status == "Ready for Pickup":
                st.success("Your laundry is ready! Please visit our shop.")
            elif status == "Claimed":
                st.success("This order has been claimed. Thank you!")
            elif status == "Online Order Submitted":
                st.warning("Please bring your laundry to our shop.")
