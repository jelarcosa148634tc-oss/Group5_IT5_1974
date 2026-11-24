import streamlit as st
from database import get_services


def render():

    st.title("✨ Our Laundry Services")

    st.write(
        "Choose the laundry service that fits your needs. "
        "All prices are calculated per kilogram."
    )

    services = get_services()

    if not services:
        st.info("No laundry services are currently available.")
        return

    columns = st.columns(2)

    for index, service in enumerate(services):

        service_id = service[0]
        service_name = service[1]
        description = service[2]
        price = service[3]

        with columns[index % 2]:

            with st.container(border=True):

                st.subheader(f"🧺 {service_name}")

                st.write(description)

                st.markdown(
                    f"### ₱{price:,.2f} "
                    f"<small>per kg</small>",
                    unsafe_allow_html=True
                )

                st.caption(f"Service ID: {service_id}")

    st.divider()

    st.info(
        "Final laundry charges will be calculated "
        "after our staff weighs your laundry at the shop."
    )
