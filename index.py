import streamlit as st

from styles import load_styles
from database import initialize_db, get_orders, get_services
from pages import place_order
from pages import my_orders

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

        st.title("✨ Our Services")

        st.write(
            "Explore our available laundry services."
        )

        for service in services:

            with st.container(border=True):

                st.subheader(service[1])

                st.write(service[2])

                st.markdown(
                    f"**₱{service[3]:,.2f} per kg**"
                )


# ==========================================
# STAFF PAGES
# ==========================================

elif role == "Staff":

    if page == "Dashboard":

        st.title("👨‍💼 Staff Dashboard")

        st.write(
            "Welcome to the staff workspace."
        )

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

        st.title("📋 Pending Orders")

        st.info(
            "Pending online orders will be displayed here."
        )


    elif page == "Receive Laundry":

        st.title("🧺 Receive Laundry")

        st.info(
            "Staff will verify orders, weigh laundry, "
            "and confirm the final price here."
        )


    elif page == "Payments":

        st.title("💰 Payments")

        st.info(
            "Staff will record customer payments here."
        )


    elif page == "Update Order Status":

        st.title("🔄 Update Order Status")

        st.info(
            "Staff will update the laundry progress here."
        )


# ==========================================
# ADMIN PAGES
# ==========================================

elif role == "Admin":

    if page == "Dashboard":

        st.title("⚙️ Admin Dashboard")

        st.write(
            "Monitor the laundry shop operations."
        )

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

        st.title("🧼 Manage Services")

        st.info(
            "Service management will be developed here."
        )


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