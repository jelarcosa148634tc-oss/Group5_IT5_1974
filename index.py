import streamlit as st

st.set_page_config(
    page_title="Laundry Management System",
    page_icon="🧺",
    layout="wide"
)

# SIDEBAR
st.sidebar.title("🧺 Laundry System")
st.sidebar.caption("Management System")

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Place an Order",
        "My Orders",
        "Services",
        "Account"
    ]
)

st.sidebar.divider()

st.sidebar.button("Logout", use_container_width=True)

# MAIN CONTENT
if menu == "Dashboard":

    st.title("Dashboard")
    st.write("Welcome to our Laundry Shop Management System!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("My Orders", 0)

    with col2:
        st.metric("Processing", 0)

    with col3:
        st.metric("Ready for Pickup", 0)

    st.subheader("Welcome!")

    st.write(
        "Manage your laundry orders conveniently "
        "through our online system."
    )

elif menu == "Place an Order":

    st.title("Place an Order")
    st.write("Submit your laundry order here.")

elif menu == "My Orders":

    st.title("My Orders")
    st.write("View and track your laundry orders.")

elif menu == "Services":

    st.title("Our Services")
    st.write("Explore our available laundry services.")

elif menu == "Account":

    st.title("My Account")
    st.write("Manage your account information.")