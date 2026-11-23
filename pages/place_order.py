import streamlit as st

from database import get_services, create_order


def render():

    st.title("🧺 Place a Laundry Order")

    st.write(
        "Submit your laundry details below. "
        "Bring your laundry to our shop after "
        "submitting your order."
    )

    st.info(
        "The final weight and price will be "
        "confirmed by our staff when you bring "
        "your laundry to the shop."
    )

    services = get_services()

    if not services:
        st.warning("No available services.")
        return

    # ORDER FORM
    with st.form("laundry_order_form"):

        st.subheader("Customer Information")

        customer_name = st.text_input(
            "Full Name *"
        )

        contact = st.text_input(
            "Contact Number or Email"
        )

        st.subheader("Laundry Details")

        service = st.selectbox(
            "Select Service *",
            services,
            format_func=lambda s: (
                f"{s[1]} - ₱{s[3]:.2f}/kg"
            )
        )

        estimated_weight = st.number_input(
            "Estimated Weight (kg)",
            min_value=0.5,
            max_value=100.0,
            value=3.0,
            step=0.5
        )

        notes = st.text_area(
            "Special Instructions",
            placeholder=(
                "Example: Separate white clothes "
                "or special fabric instructions."
            )
        )

        submitted = st.form_submit_button(
            "Submit Laundry Order",
            use_container_width=True,
            type="primary"
        )

    # PROCESS ORDER
    if submitted:

        if not customer_name.strip():

            st.error(
                "Please enter your full name."
            )

        else:

            order_id = create_order(
                customer_name=customer_name.strip(),
                contact=contact.strip(),
                service_id=service[0],
                service_name=service[1],
                estimated_kg=estimated_weight,
                notes=notes.strip()
            )

            st.success(
                "Your laundry order has been submitted!"
            )

            st.markdown(
                f"""
                ### Your Order Reference

                **FF-{order_id:04d}**

                Please bring your laundry to our shop
                and present this reference number
                to our staff.
                """
            )

            st.balloons()