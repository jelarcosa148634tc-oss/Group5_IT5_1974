import sqlite3
import streamlit as st

from database import (
    get_all_services,
    add_service,
    update_service,
    deactivate_service
)


def render():

    st.title("🧼 Manage Laundry Services")

    st.write(
        "Add, edit, and manage the laundry services "
        "offered by FreshFold."
    )

    services = get_all_services()

    # ADD NEW SERVICE
    st.subheader("➕ Add New Service")

    with st.form("add_service_form"):

        service_name = st.text_input("Service Name")

        description = st.text_area("Service Description")

        price = st.number_input(
            "Price per Kilogram (₱)",
            min_value=1.0,
            value=55.0,
            step=5.0
        )

        submitted = st.form_submit_button(
            "Add Service",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if not service_name.strip():
            st.error("Please enter a service name.")

        else:
            try:
                add_service(
                    service_name.strip(),
                    description.strip(),
                    price
                )

                st.success("New laundry service added!")
                st.rerun()

            except sqlite3.IntegrityError:
                st.error("A service with this name already exists.")

    st.divider()

    # EXISTING SERVICES
    st.subheader("📋 Existing Services")

    if not services:
        st.info("No services have been added yet.")
        return

    for service in services:

        service_id = service[0]
        name = service[1]
        description = service[2]
        service_price = service[3]
        active = service[4]

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {name}")
                st.write(description or "No description")
                st.write(f"**₱{service_price:,.2f} per kg**")

            with col2:
                if active:
                    st.success("Active")
                else:
                    st.warning("Inactive")

            # EDIT SERVICE
            with st.expander("Edit Service"):

                with st.form(f"edit_service_{service_id}"):

                    new_name = st.text_input(
                        "Service Name",
                        value=name
                    )

                    new_description = st.text_area(
                        "Description",
                        value=description or ""
                    )

                    new_price = st.number_input(
                        "Price per Kilogram (₱)",
                        min_value=1.0,
                        value=float(service_price),
                        step=5.0
                    )

                    update_button = st.form_submit_button(
                        "Save Changes"
                    )

                if update_button:

                    if not new_name.strip():
                        st.error("Service name cannot be empty.")

                    else:
                        try:
                            update_service(
                                service_id,
                                new_name.strip(),
                                new_description.strip(),
                                new_price
                            )

                            st.success("Service updated!")
                            st.rerun()

                        except sqlite3.IntegrityError:
                            st.error(
                                "Another service already uses that name."
                            )

            # DEACTIVATE SERVICE
            if active:

                if st.button(
                    "Deactivate Service",
                    key=f"deactivate_{service_id}"
                ):

                    deactivate_service(service_id)

                    st.success("Service deactivated.")
                    st.rerun()
