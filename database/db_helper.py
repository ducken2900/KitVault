import sqlite3
import os


class DatabaseHelper:
    def __init__(self):
        # 🔴 KHẮC PHỤC LỖI 5: Sử dụng đường dẫn tuyệt đối động dựa trên thư mục chứa tệp tin hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "gundam_store.db")
        self.init_db()

    def get_conn(self):
        """Kết nối cơ sở dữ liệu SQLite"""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Khởi tạo tất cả cấu trúc bảng của cửa hàng"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self.get_conn()
        cursor = conn.cursor()

        # Bảng Người dùng (Nhân viên)
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                            password TEXT,
                            fullname TEXT,
                            phone TEXT,
                            role TEXT
                        )''')

        # Bảng Kho hàng Gundam
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

        # Bảng Đơn hàng (Hóa đơn bán ra)
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            time TEXT,
                            product_id TEXT,
                            product_name TEXT,
                            price REAL,
                            seller TEXT,
                            customer_phone TEXT
                        )''')

        # Bảng Khách hàng thành viên
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            phone TEXT PRIMARY KEY,
                            name TEXT,
                            total_spent REAL DEFAULT 0
                        )''')

        # Bảng Lịch sử nhập hàng
        cursor.execute('''CREATE TABLE IF NOT EXISTS purchase_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            time TEXT,
                            product_id TEXT,
                            product_name TEXT,
                            quantity INTEGER,
                            price REAL,
                            operator TEXT
                        )''')

        # Bảng Nhật ký hệ thống
        cursor.execute('''CREATE TABLE IF NOT EXISTS login_history (
                            username TEXT,
                            time TEXT,
                            status TEXT
                        )''')

        # Tạo bảng lưu thông tin Pre-order chi tiết nếu chưa có
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

        # Tài khoản mặc định hệ thống
        cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin', '123', 'Chủ Cửa Hàng', '090', 'Admin')")
        cursor.execute("INSERT OR IGNORE INTO users VALUES ('a', '1', 'Quản Trị Viên', '000', 'Admin')")

        conn.commit()
        conn.close()

    def query(self, sql, params=()):
        """Thực thi mọi câu lệnh truy vấn SQL"""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data