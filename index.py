import streamlit as st
import sqlite3
from datetime import datetime
from pathlib import Path

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "laundry.db"

st.set_page_config(page_title="FreshFold | Laundry Management", page_icon="🧺", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f5f7f6; }
[data-testid="stSidebar"] { background: #172b25; }
[data-testid="stSidebar"] * { color: #f4f7f5 !important; }
[data-testid="stSidebar"] .stRadio label { padding: 7px 9px; border-radius: 8px; }
h1, h2, h3 { font-family: 'Manrope', sans-serif; letter-spacing: -0.02em; }
.hero { background: linear-gradient(120deg,#176b4a,#103c30); padding: 28px 32px; border-radius: 18px; color: white; }
.hero h1 { color: white !important; margin: 0; font-size: 2.2rem; }
.hero p { color: #d7eee3; margin-bottom: 0; }
.small-muted { color: #6c7a73; font-size: .9rem; }
div[data-testid="stMetric"] { background: white; border: 1px solid #e4eae6; padding: 14px 18px; border-radius: 14px; }
div.stButton > button { border-radius: 9px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ---------- Database ----------
def connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def initialize_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            price_per_kg REAL NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            contact TEXT,
            service_id INTEGER,
            service_name TEXT NOT NULL,
            estimated_kg REAL NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Online Order Submitted',
            final_kg REAL,
            total_amount REAL,
            payment_status TEXT NOT NULL DEFAULT 'Unpaid',
            FOREIGN KEY(service_id) REFERENCES services(id)
        )""")
        defaults = [
            ("Wash & Fold", "Wash, dry, and neatly fold everyday clothes.", 55.00),
            ("Wash & Dry", "Washing and drying service.", 45.00),
            ("Full Service", "Complete wash, dry, and fold service.", 65.00),
            ("Blanket / Special", "Special handling for bulky items.", 80.00),
        ]
        for name, desc, price in defaults:
            con.execute("INSERT OR IGNORE INTO services(name,description,price_per_kg) VALUES(?,?,?)", (name,desc,price))
        con.commit()

initialize_db()

def get_services(active_only=True):
    with connect() as con:
        query = "SELECT id,name,description,price_per_kg,active FROM services"
        if active_only: query += " WHERE active=1"
        return con.execute(query+" ORDER BY id").fetchall()

def get_orders():
    with connect() as con:
        return con.execute("""SELECT id,customer_name,contact,service_name,estimated_kg,created_at,status,
        final_kg,total_amount,payment_status,notes FROM orders ORDER BY id DESC""").fetchall()

def update_order(order_id, status=None, final_kg=None, total=None, payment_status=None):
    with connect() as con:
        if status is not None:
            con.execute("UPDATE orders SET status=? WHERE id=?", (status,order_id))
        if final_kg is not None:
            con.execute("UPDATE orders SET final_kg=?,total_amount=? WHERE id=?", (final_kg,total,order_id))
        if payment_status is not None:
            con.execute("UPDATE orders SET payment_status=? WHERE id=?", (payment_status,order_id))
        con.commit()

def create_order(name, contact, service, kg, notes):
    with connect() as con:
        con.execute("""INSERT INTO orders(customer_name,contact,service_id,service_name,estimated_kg,notes,created_at)
        VALUES(?,?,?,?,?,?,?)""", (name,contact,service[0],service[1],kg,notes,datetime.now().strftime("%Y-%m-%d %I:%M %p")))
        con.commit()
        return con.execute("SELECT last_insert_rowid()").fetchone()[0]

def money(value):
    return f"₱{float(value or 0):,.2f}"

# ---------- Sidebar / navigation ----------
st.sidebar.markdown("## 🧺 FreshFold")
st.sidebar.caption("LAUNDRY MANAGEMENT SYSTEM")
st.sidebar.divider()
role = st.sidebar.selectbox("Demo role", ["Customer", "Staff", "Admin"], help="Role switcher for demonstration. Replace with secure login before deployment.")
menus = {
    "Customer": ["Dashboard", "Place an Order", "My Orders", "Services"],
    "Staff": ["Dashboard", "Pending Orders", "Receive Laundry", "Payments", "Order Status"],
    "Admin": ["Dashboard", "Manage Services", "All Orders", "Reports"]
}
page = st.sidebar.radio("Navigation", menus[role], label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.markdown("**Project Demo**")
st.sidebar.caption("Orders are saved locally in laundry.db.")
st.sidebar.warning("Demo role selector — not secure authentication.")

# ---------- Helpers ----------
def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def order_table(rows):
    if not rows:
        st.info("No orders to display yet.")
        return
    import pandas as pd
    df = pd.DataFrame(rows, columns=["Order #","Customer","Contact","Service","Est. kg","Submitted","Status","Final kg","Amount","Payment","Notes"])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------- Customer ----------
if role == "Customer":
    if page == "Dashboard":
        hero("Fresh clothes, less hassle.", "Submit your order online, then bring your laundry to the shop.")
        st.write("")
        orders = get_orders()
        my_orders = orders # Demo: all orders shown until customer accounts are implemented
        c1,c2,c3 = st.columns(3)
        c1.metric("Orders submitted", len(my_orders))
        c2.metric("Processing", sum(o[6]=="Processing" for o in my_orders))
        c3.metric("Ready for pickup", sum(o[6]=="Ready for Pickup" for o in my_orders))
        st.subheader("How it works")
        a,b,c = st.columns(3)
        a.markdown("### ① Submit\nPlace an online order.")
        b.markdown("### ② Bring it in\nStaff weighs and confirms your laundry.")
        c.markdown("### ③ Pick up\nCollect when it is ready.")
        st.caption("Payment is made at the shop after staff confirms the actual weight.")
    elif page == "Place an Order":
        hero("Place a laundry order", "Fill out the details below. Staff will confirm the actual weight and price in-store.")
        services = get_services()
        if not services:
            st.warning("No services currently available.")
        else:
            with st.form("order_form"):
                name = st.text_input("Customer name *")
                contact = st.text_input("Contact number or email")
                service_choice = st.selectbox("Service *", services, format_func=lambda s: f"{s[1]} — ₱{s[3]:.2f}/kg")
                kg = st.number_input("Estimated weight (kg)", min_value=0.5, max_value=100.0, value=3.0, step=0.5)
                notes = st.text_area("Special instructions (optional)")
                submitted = st.form_submit_button("Submit Order", use_container_width=True)
                if submitted:
                    if not name.strip():
                        st.error("Please enter your name.")
                    else:
                        order_id = create_order(name.strip(), contact.strip(), service_choice, kg, notes.strip())
                        st.success(f"Order submitted! Your reference number is FF-{order_id:04d}. Bring your laundry to the shop.")
    elif page == "My Orders":
        hero("My orders", "Track the progress of your laundry.")
        st.info("Prototype note: customer accounts and private order filtering will be added later. This view currently displays demo orders.")
        order_table(get_orders())
    elif page == "Services":
        hero("Our services", "Choose the service that best fits your laundry needs.")
        for s in get_services():
            with st.container(border=True):
                st.subheader(s[1])
                st.write(s[2])
                st.markdown(f"**Starting rate: {money(s[3])} / kg**")

# ---------- Staff ----------
elif role == "Staff":
    if page == "Dashboard":
        hero("Staff workspace", "Receive laundry, confirm weight, record payment, and update order progress.")
        orders = get_orders()
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Submitted", sum(o[6]=="Online Order Submitted" for o in orders))
        c2.metric("Received", sum(o[6]=="Laundry Received" for o in orders))
        c3.metric("Processing", sum(o[6]=="Processing" for o in orders))
        c4.metric("Ready", sum(o[6]=="Ready for Pickup" for o in orders))
        st.subheader("Recent orders")
        order_table(orders[:8])
    elif page == "Pending Orders":
        hero("Pending online orders", "Check orders customers submitted before they arrive.")
        pending = [o for o in get_orders() if o[6]=="Online Order Submitted"]
        order_table(pending)
    elif page == "Receive Laundry":
        hero("Receive laundry", "Verify the reference, weigh the actual laundry, and confirm the final price.")
        pending = [o for o in get_orders() if o[6] in ("Online Order Submitted","Laundry Received")]
        if pending:
            chosen = st.selectbox("Select order", pending, format_func=lambda o: f"FF-{o[0]:04d} · {o[1]} · {o[3]}")
            actual = st.number_input("Actual weight (kg)", min_value=0.1, value=float(chosen[4]), step=0.1, key="actual_weight")
            service = next((s for s in get_services(False) if s[1]==chosen[3]), None)
            rate = service[3] if service else 0
            total = actual * rate
            st.metric("Final price", money(total), f"{money(rate)} / kg")
            if st.button("Confirm Laundry Received", type="primary"):
                update_order(chosen[0], status="Laundry Received", final_kg=actual, total=total)
                st.success("Weight and final price recorded.")
                st.rerun()
        else:
            st.info("No orders waiting to be received.")
    elif page == "Payments":
        hero("Payments", "Record payment at the shop when laundry is received.")
        unpaid = [o for o in get_orders() if o[6] in ("Laundry Received","Processing") and o[9]=="Unpaid"]
        if unpaid:
            chosen = st.selectbox("Select unpaid order", unpaid, format_func=lambda o: f"FF-{o[0]:04d} · {o[1]} · {money(o[8])}")
            st.write(f"Amount due: **{money(chosen[8])}**")
            method = st.selectbox("Payment method", ["Cash","GCash","Other"])
            if st.button("Mark as Paid", type="primary"):
                update_order(chosen[0], payment_status="Paid")
                st.success(f"Payment recorded ({method}).")
                st.rerun()
        else:
            st.info("No unpaid received orders.")
    elif page == "Order Status":
        hero("Update order status", "Move orders through the laundry workflow.")
        rows = get_orders()
        if rows:
            chosen = st.selectbox("Select order", rows, format_func=lambda o: f"FF-{o[0]:04d} · {o[1]} · {o[6]}")
            new_status = st.selectbox("New status", ["Laundry Received","Paid","Processing","Ready for Pickup","Claimed"], index=0)
            if st.button("Update Status", type="primary"):
                update_order(chosen[0], status=new_status)
                st.success("Order status updated.")
                st.rerun()
        else:
            st.info("No orders available.")

# ---------- Admin ----------
elif role == "Admin":
    if page == "Dashboard":
        hero("Admin dashboard", "Overview of orders, services, and shop activity.")
        orders = get_orders()
        revenue = sum(float(o[8] or 0) for o in orders if o[9]=="Paid")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total orders",len(orders))
        c2.metric("Paid transactions",sum(o[9]=="Paid" for o in orders))
        c3.metric("Estimated revenue",money(revenue))
        c4.metric("Active services",len(get_services()))
        st.subheader("Latest orders")
        order_table(orders[:10])
    elif page == "Manage Services":
        hero("Manage services", "Add services or update rates. Changes apply to new orders.")
        services = get_services(False)
        with st.form("add_service"):
            name = st.text_input("Service name")
            desc = st.text_input("Description")
            price = st.number_input("Price per kg (₱)", min_value=0.0, value=50.0, step=5.0)
            add = st.form_submit_button("Add Service")
            if add:
                if name.strip():
                    try:
                        with connect() as con:
                            con.execute("INSERT INTO services(name,description,price_per_kg) VALUES(?,?,?)",(name.strip(),desc.strip(),price))
                            con.commit()
                        st.success("Service added.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("A service with that name already exists.")
                else:
                    st.error("Service name is required.")
        st.subheader("Existing services")
        for s in services:
            with st.container(border=True):
                st.write(f"**{s[1]}** — {money(s[3])}/kg")
                st.caption(s[2])
                col1,col2 = st.columns([3,1])
                new_price = col1.number_input("Update rate", min_value=0.0, value=float(s[3]), step=5.0, key=f"rate_{s[0]}")
                if col2.button("Save rate",key=f"save_{s[0]}"):
                    with connect() as con:
                        con.execute("UPDATE services SET price_per_kg=? WHERE id=?",(new_price,s[0]))
                        con.commit()
                    st.success("Rate updated.")
                    st.rerun()
    elif page == "All Orders":
        hero("All orders", "View the complete order history.")
        order_table(get_orders())
    elif page == "Reports":
        hero("Reports", "Summary of demo activity.")
        orders = get_orders()
        import pandas as pd
        if orders:
            st.write("Orders by status")
            counts = {}
            for o in orders: counts[o[6]] = counts.get(o[6],0)+1
            st.bar_chart(counts)
            st.write("Order data")
            order_table(orders)
            csv = pd.DataFrame(orders, columns=["Order #","Customer","Contact","Service","Estimated kg","Submitted","Status","Final kg","Amount","Payment","Notes"]).to_csv(index=False).encode("utf-8")
            st.download_button("Download order report (CSV)",csv,"laundry_orders.csv","text/csv")
        else:
            st.info("Reports will appear after orders are submitted.")

st.sidebar.caption("FreshFold • Student project prototype")
