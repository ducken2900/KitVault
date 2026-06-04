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

    def center_window(self, width, height):
        """Hàm phụ trợ: Tự động tính toán đưa cửa sổ vào giữa màn hình máy tính"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Tính toán tọa độ X, Y chuẩn giữa màn hình
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def clear_current_page(self):
        if self.current_page:
            for widget in self.root.winfo_children():
                widget.destroy()

    def show_login_page(self):
        self.clear_current_page()
        self.current_user = None
        self.center_window(450, 550) # Tự động căn giữa
        self.current_page = LoginPage(self.root, self)

    def show_menu_page(self):
        self.clear_current_page()
        # Đã xóa dòng kích thước cũ bị trùng, giữ lại kích thước Menu lớn chứa thêm nút
        self.center_window(500, 550) 
        self.current_page = MenuPage(self.root, self)

    def show_register_page(self):
        self.clear_current_page()
        self.center_window(500, 550)
        self.current_page = RegisterPage(self.root, self)

    def show_quanly_kho_page(self):
        self.clear_current_page()
        self.center_window(1250, 800)
        self.current_page = QuanLyKhoPage(self.root, self)

    def show_quanly_donhang_page(self, prefill_phone=None):
        """Mở quầy bán hàng và nhận SĐT khách tự động truyền từ ngoài vào"""
        self.clear_current_page()
        self.center_window(1300, 800)
        self.current_page = QuanLyDonHangPage(self.root, self, prefill_phone)

    def show_quanly_taikhoan_page(self):
        self.clear_current_page()
        self.center_window(1000, 650)
        self.current_page = QuanLyTaiKhoanPage(self.root, self)

    def show_baocao_page(self):  
        """Đã gộp thành 1 hàm duy nhất với kích thước chuẩn hiển thị biểu đồ"""
        self.clear_current_page()
        self.center_window(1000, 750) # Sử dụng kích thước lớn để không bị che khuất Pandas/Matplotlib
        self.current_page = BaoCaoPage(self.root, self)

    def show_sua_nhanvien_page(self, data):
        self.clear_current_page()
        self.center_window(500, 600)
        self.current_page = SuaNhanVienPage(self.root, self, data)

    def run(self):
        self.root.mainloop()