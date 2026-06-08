import sqlite3
import os

class DatabaseHelper:
    def __init__(self):
        # Đường dẫn cơ sở dữ liệu động tránh lỗi môi trường
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "gundam_store.db")
        self.init_db()

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Khởi tạo cấu trúc các bảng dữ liệu của cửa hàng"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self.get_conn()
        cursor = conn.cursor()

        # Quản lý thông tin tài khoản nhân sự và quyền hạn
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                            password TEXT,
                            fullname TEXT,
                            phone TEXT,
                            role TEXT
                        )''')

        # Quản lý thông tin sản phẩm và trạng thái kho hàng
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            grade TEXT,
                            stock INTEGER,
                            pre_order INTEGER,
                            price REAL,
                            entry_date TEXT,
                            status TEXT
                        )''')

        # Quản lý hóa đơn bán lẻ trực tiếp tại quầy
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            time TEXT,
                            product_id TEXT,
                            product_name TEXT,
                            price REAL,
                            seller TEXT,
                            customer_phone TEXT
                        )''')

        # Quản lý thông tin chi tiết đặt hàng trước (Pre-order)
        cursor.execute('''CREATE TABLE IF NOT EXISTS preorder_registrations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            phone TEXT,
                            product_id TEXT,
                            product_name TEXT,
                            order_date TEXT,
                            price REAL,
                            quantity INTEGER,
                            deposit REAL
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS login_history (
                            username TEXT,
                            time TEXT,
                            status TEXT
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS purchase_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            time TEXT,
                            product_id TEXT,
                            product_name TEXT,
                            quantity INTEGER,
                            price REAL,
                            operator TEXT
                        )''')

        # Thêm các tài khoản quản trị hệ thống mặc định
        cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin', '123', 'Chủ Cửa Hàng', '090', 'Admin')")
        cursor.execute("INSERT OR IGNORE INTO users VALUES ('a', '1', 'Quản Trị Viên', '000', 'Admin')")

        conn.commit()
        conn.close()

    def query(self, sql, params=()):
        """Thực thi truy vấn cơ sở dữ liệu"""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data