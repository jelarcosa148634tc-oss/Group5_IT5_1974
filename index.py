import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Laundry Shop Management System",
    page_icon="🧺",
    layout="wide"
)

# Homepage
st.title("🧺 Laundry Shop Management System")

st.header("Welcome to our Laundry Shop!")

st.write(
    "Your convenient laundry service. "
    "Submit your order online and bring your laundry "
    "to our shop for processing."
)

st.divider()

# Services
st.subheader("Our Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧼 Wash & Fold")
    st.write("Laundry washing and folding service.")

with col2:
    st.markdown("### 🌬️ Wash & Dry")
    st.write("Laundry washing and drying service.")

with col3:
    st.markdown("### ✨ Full Service")
    st.write("Wash, dry, and fold your laundry.")

st.divider()

# Order button
st.subheader("Ready to do your laundry?")

st.write(
    "Place your order online and bring your laundry "
    "to our shop."
)

if st.button("Place an Order"):
    st.info("Order placement will be available soon!")