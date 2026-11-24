import streamlit as st

from styles import load_styles
from database import initialize_db, get_orders, get_services
from pages import place_order
from pages import my_orders
from pages import services as services_page
from pages import staff_dashboard
from pages import receive_laundry
from pages import payments
from pages import update_status
from pages import pending_orders
from pages import admin_dashboard
from pages import manage_services

# ==========================================
# 1. APPLICATION CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FreshFold | Laundry Management",
    page_icon="🧺",
    layout="wide"
)


# ==========================================
# 2. INITIALIZE SYSTEM
# ==========================================

load_styles()
initialize_db()


# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("# 🧺 FreshFold")
st.sidebar.caption("LAUNDRY MANAGEMENT SYSTEM")

st.sidebar.divider()

role = st.sidebar.selectbox(
    "Select User Role",
    ["Customer", "Staff", "Admin"]
)


# Navigation options based on role
navigation = {

    "Customer": [
        "Dashboard",
        "Place an Order",
        "My Orders",
        "Services"
    ],

    "Staff": [
        "Dashboard",
        "Pending Orders",
        "Receive Laundry",
        "Payments",
        "Update Order Status"
    ],

    "Admin": [
        "Dashboard",
        "Manage Services",
        "Manage Orders",
        "Reports"
    ]
}


page = st.sidebar.radio(
    "Navigation",
    navigation[role]
)


st.sidebar.divider()

st.sidebar.caption(
    "FreshFold Laundry Management System"
)


# ==========================================
# 4. MAIN APPLICATION
# ==========================================

orders = get_orders()
services = get_services()


# ==========================================
# CUSTOMER PAGES
# ==========================================

if role == "Customer":

    if page == "Dashboard":

        st.markdown("""
        <div class="hero">
            <h1>Fresh clothes, less hassle.</h1>
            <p>
                Submit your laundry order online
                and bring your clothes to our shop.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Orders",
                len(orders)
            )

        with col2:
            processing = sum(
                order[10] == "Processing"
                for order in orders
            )

            st.metric(
                "Processing",
                processing
            )

        with col3:
            ready = sum(
                order[10] == "Ready for Pickup"
                for order in orders
            )

            st.metric(
                "Ready for Pickup",
                ready
            )

        st.divider()

        st.subheader("How It Works")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 📝 Submit")
            st.write(
                "Submit your laundry order "
                "through our website."
            )

        with col2:
            st.markdown("### 🧺 Bring It In")
            st.write(
                "Bring your laundry to our shop "
                "for weighing and confirmation."
            )

        with col3:
            st.markdown("### ✨ Pick It Up")
            st.write(
                "Collect your laundry when "
                "it is ready."
            )


    elif page == "Place an Order":

        place_order.render()


    elif page == "My Orders":
        my_orders.render()


    elif page == "Services":
        services_page.render()

# ==========================================
# STAFF PAGES
# ==========================================

elif role == "Staff":

    if page == "Dashboard":
        staff_dashboard.render()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Online Orders",
            sum(
                order[10] == "Online Order Submitted"
                for order in orders
            )
        )

        col2.metric(
            "Received",
            sum(
                order[10] == "Laundry Received"
                for order in orders
            )
        )

        col3.metric(
            "Processing",
            sum(
                order[10] == "Processing"
                for order in orders
            )
        )

        col4.metric(
            "Ready for Pickup",
            sum(
                order[10] == "Ready for Pickup"
                for order in orders
            )
        )


    elif page == "Pending Orders":
        pending_orders.render()


    elif page == "Receive Laundry":
        receive_laundry.render()


    elif page == "Payments":
        payments.render()


    elif page == "Update Order Status":
        update_status.render()


# ==========================================
# ADMIN PAGES
# ==========================================

elif role == "Admin":

    if page == "Dashboard":
        admin_dashboard.render()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Orders",
            len(orders)
        )

        col2.metric(
            "Available Services",
            len(services)
        )

        col3.metric(
            "Completed Orders",
            sum(
                order[10] == "Claimed"
                for order in orders
            )
        )


    elif page == "Manage Services":
        manage_services.render()


    elif page == "Manage Orders":

        st.title("📋 Manage Orders")

        st.info(
            "Admin order monitoring will be developed here."
        )


    elif page == "Reports":

        st.title("📊 Reports")

        st.info(
            "Business reports will be developed here."
        )