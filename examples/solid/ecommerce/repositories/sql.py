import sqlite3

from .order_repository import OrderRepository
from models.order import Order
from models.product import Product


class SQLOrderRepository(OrderRepository):

    def __init__(self, db_path: str = ":memory:"):
        """Initialize SQLite connection and create tables if they don't exist."""
        self.db_path = db_path
        self.db_connection = sqlite3.connect(db_path, check_same_thread=False)
        self.db_connection.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        """Create orders and order_items tables if they don't exist."""
        cursor = self.db_connection.cursor()
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                is_paid BOOLEAN NOT NULL DEFAULT 0,
                user_id TEXT,
                user_name TEXT,
                user_email TEXT
            )
        """)
        
        # Create order_items table to store products associated with orders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                product_price REAL NOT NULL,
                product_description TEXT,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        """)
        
        self.db_connection.commit()

    def create_order(self, order: Order) -> Order:
        """Insert a new order into the database."""
        cursor = self.db_connection.cursor()

        cursor.execute(
            "INSERT INTO orders (id, is_paid) VALUES (?, ?)",
            (order.id, order.is_paid)
        )

        # If order has purchaser information, update the orders row with user info
        if getattr(order, "purchaser", None):
            cursor.execute(
                "UPDATE orders SET user_id = ?, user_name = ?, user_email = ? WHERE id = ?",
                (getattr(order.purchaser, "id", None), getattr(order.purchaser, "name", None), getattr(order.purchaser, "email", None), order.id)
            )

        # Insert products associated with the order
        for product in order.products:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, product_price, product_description)
                VALUES (?, ?, ?, ?, ?)
            """, (order.id, product.id, product.name, product.price, product.description))

        self.db_connection.commit()
        return order

    def get_order_by_id(self, order_id: str) -> Order:
        """Retrieve an order by its ID."""
        cursor = self.db_connection.cursor()
        
        # Get order
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order_row = cursor.fetchone()
        
        if not order_row:
            return None
        
        # Get products for this order
        cursor.execute("""
            SELECT product_id, product_name, product_price, product_description
            FROM order_items WHERE order_id = ?
        """, (order_id,))
        product_rows = cursor.fetchall()
        
        # Reconstruct Order object with products
        products = []
        for row in product_rows:
            # row columns: product_id, product_name, product_price, product_description
            p = Product(name=row["product_name"], price=row["product_price"], description=row["product_description"])
            # preserve original id from DB
            try:
                p.id = row["product_id"]
            except Exception:
                pass
            products.append(p)
        
        # Reconstruct purchaser if present
        purchaser = None
        if order_row["user_name"] is not None:
            from models.user import User
            purchaser = User(order_row["user_name"], order_row["user_email"])
            # restore stored id
            try:
                purchaser.id = order_row["user_id"]
            except Exception:
                pass

        # Order now auto-generates id; create and restore stored id
        order = Order(products=products, purchaser=purchaser)
        try:
            order.id = order_row["id"]
        except Exception:
            pass
        order.is_paid = bool(order_row["is_paid"])
        return order

    def get_orders_by_user(self, user_id: str) -> list[Order]:
        """Retrieve all orders for a given user id."""
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM orders WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            order = self.get_order_by_id(row["id"])
            if order:
                orders.append(order)
        return orders

    def update_order(self, order: Order) -> Order:
        """Update an existing order."""
        cursor = self.db_connection.cursor()
        
        # Check if order exists
        cursor.execute("SELECT id FROM orders WHERE id = ?", (order.id,))
        if not cursor.fetchone():
            raise ValueError(f"Order with id {order.id} not found")
        
        # Update order is_paid status
        cursor.execute(
            "UPDATE orders SET is_paid = ? WHERE id = ?",
            (order.is_paid, order.id)
        )
        # Update purchaser info as well
        if getattr(order, "purchaser", None):
            cursor.execute(
                "UPDATE orders SET user_id = ?, user_name = ?, user_email = ? WHERE id = ?",
                (getattr(order.purchaser, "id", None), getattr(order.purchaser, "name", None), getattr(order.purchaser, "email", None), order.id)
            )
        
        # Delete old products and insert new ones
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order.id,))
        
        for product in order.products:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, product_name, product_price, product_description)
                VALUES (?, ?, ?, ?, ?)
            """, (order.id, product.id, product.name, product.price, product.description))
        
        self.db_connection.commit()
        return order

    def delete_order(self, order_id: str) -> None:
        """Delete an order by its ID."""
        cursor = self.db_connection.cursor()
        
        # Check if order exists
        cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
        if not cursor.fetchone():
            raise ValueError(f"Order with id {order_id} not found")
        
        # Delete order items first (foreign key constraint)
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        
        # Delete order
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        
        self.db_connection.commit()

    def close(self):
        """Close the database connection."""
        self.db_connection.close()