import tkinter as tk
from tkinter import ttk
from database.db_helper import DatabaseHelper
from page.login import LoginPage
from page.menu import MenuPage
from page.register import RegisterPage
from page.quanly_kho import QuanLyKhoPage
from page.quanly_taikhoan import QuanLyTaiKhoanPage
from page.sua_nhanvien import SuaNhanVienPage
from page.baocao import BaoCaoPage
from page.quanly_donhang import QuanLyDonHangPage


class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HỆ THỐNG QUẢN LÝ GUNDAM STORE")
        # Tự động tối đa hóa cửa sổ (Full màn hình) ngay khi chạy ứng dụng
        try:
            self.root.state('zoomed')  # Tương thích Windows & macOS
        except Exception:
            try:
                self.root.attributes('-zoomed', True)  # Tương thích Linux
            except Exception:
                # Dự phòng thủ công đo độ phân giải màn hình thực tế
                w = self.root.winfo_screenwidth()
                h = self.root.winfo_screenheight()
                self.root.geometry(f"{w}x{h}+0+0")
        self.db = DatabaseHelper()
        self.current_page = None
        self.current_user = None

        self.setup_style()
        self.show_login_page()

    @staticmethod
    def setup_style():
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#dfe6e9")
        style.map("Treeview", background=[('selected', '#1e3799')], foreground=[('selected', 'white')])
        style.configure("TNotebook.Tab", padding=[20, 8], font=("Segoe UI", 9, "bold"))

    def clear_current_page(self):
        if self.current_page:
            for widget in self.root.winfo_children():
                widget.destroy()

    def show_login_page(self):
        self.clear_current_page()
        self.current_user = None  # Khóa bảo mật: Reset phiên làm việc cũ khi đăng xuất
        self.current_page = LoginPage(self.root, self)

    def show_menu_page(self):
        self.clear_current_page()
        self.current_page = MenuPage(self.root, self)

    def show_register_page(self):
        self.clear_current_page()
        self.current_page = RegisterPage(self.root, self)

    def show_quanly_kho_page(self):
        self.clear_current_page()
        self.current_page = QuanLyKhoPage(self.root, self)

    def show_quanly_donhang_page(self, prefill_phone=None):
        self.clear_current_page()
        self.current_page = QuanLyDonHangPage(self.root, self, prefill_phone)

    def show_quanly_taikhoan_page(self):
        self.clear_current_page()
        self.current_page = QuanLyTaiKhoanPage(self.root, self)

    def show_baocao_page(self):
        self.clear_current_page()
        self.current_page = BaoCaoPage(self.root, self)

    def show_sua_nhanvien_page(self, data):
        self.clear_current_page()
        self.current_page = SuaNhanVienPage(self.root, self, data)

    def show_baocao_page(self):  # HÀM MỞ TRANG BÁO CÁO
        self.clear_current_page()
        self.root.geometry("1280x800")
        self.current_page = BaoCaoPage(self.root, self)

    def run(self):
        self.root.mainloop()