
import streamlit as st

from database import get_services
from utils.helpers import format_currency


def render():

    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to FreshFold! 🧺</h1>
            <p>
                Your laundry, our care.
                Convenient laundry ordering made simple.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("How FreshFold Works")

    steps = [
        ("📝", "Place an Order",
         "Submit your laundry details online."),
        ("🧺", "Bring Your Laundry",
         "Visit our shop so staff can receive and weigh it."),
        ("💰", "Confirm and Pay",
         "Staff confirms your final price. Pay at the shop."),
        ("🫧", "Laundry Processing",
         "Our staff will wash and prepare your laundry."),
        ("✅", "Ready for Pickup",
         "Claim your laundry when it is ready.")
    ]

    columns = st.columns(5)

    for index, step in enumerate(steps):
        with columns[index]:
            with st.container(border=True):
                st.markdown(f"### {step[0]}")
                st.markdown(f"**{step[1]}**")
                st.caption(step[2])

    st.divider()

    st.subheader("Our Available Services")

    services = get_services()

    if not services:
        st.info("No laundry services are currently available.")
    else:
        columns = st.columns(2)

        for index, service in enumerate(services):
            with columns[index % 2]:
                with st.container(border=True):
                    st.markdown(f"### 🧺 {service[1]}")
                    st.write(service[2])
                    st.markdown(
                        f"**{format_currency(service[3])} / kg**"
                    )

    st.divider()

    st.info(
        "Remember: Submitting an online order does not mean "
        "your laundry has already been received. "
        "Please bring your laundry to our shop."
    )
