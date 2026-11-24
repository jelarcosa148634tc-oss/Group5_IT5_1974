import sqlite3
from pathlib import Path


# Database file location
APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "laundry.db"


# Connect to database
def connect():
    return sqlite3.connect(DB_PATH)


# Create database tables
def initialize_db():

    with connect() as conn:

        # Services table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                price_per_kg REAL NOT NULL,
                active INTEGER DEFAULT 1
            )
        """)

        # Orders table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                contact TEXT,
                service_id INTEGER,
                service_name TEXT NOT NULL,
                estimated_kg REAL NOT NULL,
                actual_kg REAL,
                total_amount REAL,
                notes TEXT,
                created_at TEXT NOT NULL,
                status TEXT DEFAULT 'Online Order Submitted',
                payment_status TEXT DEFAULT 'Unpaid'
            )
        """)

        # Default services
        default_services = [
            ("Wash & Fold", "Wash, dry, and fold clothes.", 55.00),
            ("Wash & Dry", "Washing and drying service.", 45.00),
            ("Full Service", "Complete wash, dry, and fold.", 65.00),
            ("Special Laundry", "Special handling for bulky items.", 80.00)
        ]

        for service in default_services:

            conn.execute("""
                INSERT OR IGNORE INTO services
                (name, description, price_per_kg)
                VALUES (?, ?, ?)
            """, service)

        conn.commit()


# Get all available services
def get_services():

    with connect() as conn:

        return conn.execute("""
            SELECT id, name, description, price_per_kg
            FROM services
            WHERE active = 1
            ORDER BY id
        """).fetchall()


# Add a new service
def add_service(name, description, price):

    with connect() as conn:

        conn.execute("""
            INSERT INTO services
            (name, description, price_per_kg)
            VALUES (?, ?, ?)
        """, (name, description, price))

        conn.commit()

#Get servvice og add service
def get_all_services():
    with connect() as conn:
        return conn.execute("""
            SELECT id, name, description, price_per_kg, active
            FROM services
            ORDER BY id
        """).fetchall()


def update_service(service_id, name, description, price):
    with connect() as conn:
        conn.execute("""
            UPDATE services
            SET name = ?,
                description = ?,
                price_per_kg = ?
            WHERE id = ?
        """, (name, description, price, service_id))
        conn.commit()


def deactivate_service(service_id):
    with connect() as conn:
        conn.execute("""
            UPDATE services
            SET active = 0
            WHERE id = ?
        """, (service_id,))
        conn.commit()


# Submit a laundry order
def create_order(
    customer_name,
    contact,
    service_id,
    service_name,
    estimated_kg,
    notes
):

    from datetime import datetime

    with connect() as conn:

        cursor = conn.execute("""
            INSERT INTO orders (
                customer_name,
                contact,
                service_id,
                service_name,
                estimated_kg,
                notes,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            contact,
            service_id,
            service_name,
            estimated_kg,
            notes,
            datetime.now().strftime("%Y-%m-%d %I:%M %p")
        ))

        conn.commit()

        return cursor.lastrowid


# Get all orders
def get_orders():

    with connect() as conn:

        return conn.execute("""
            SELECT *
            FROM orders
            ORDER BY id DESC
        """).fetchall()


# Update order status
def update_order_status(order_id, status):

    with connect() as conn:

        conn.execute("""
            UPDATE orders
            SET status = ?
            WHERE id = ?
        """, (status, order_id))

        conn.commit()


# Confirm actual laundry weight and price
def receive_laundry(order_id, actual_kg, total_amount):

    with connect() as conn:

        conn.execute("""
            UPDATE orders
            SET actual_kg = ?,
                total_amount = ?,
                status = 'Laundry Received'
            WHERE id = ?
        """, (actual_kg, total_amount, order_id))

        conn.commit()


# Record payment
def record_payment(order_id):

    with connect() as conn:

        conn.execute("""
            UPDATE orders
            SET payment_status = 'Paid'
            WHERE id = ?
        """, (order_id,))

        conn.commit()

