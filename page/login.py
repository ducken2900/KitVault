import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # FIX: Khai báo tất cả thuộc tính ở đây để hết lỗi "defined outside __init__"
        self.e_u = None
        self.e_p = None
        self.cb_r = None
        self.var_show = tk.IntVar(value=0)

        self.view()

    def view(self):
        # Thiết lập màu sắc Navy chuyên nghiệp
        header_bg = "#1e3799"

        # Header
        header = tk.Frame(self.master, bg=header_bg)
        header.pack(fill="x")
        tk.Label(header, text="🛡️ ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 22, "bold"),
                 fg="white", bg=header_bg).pack(pady=35)

        # Khung nhập liệu (Form)
        form = tk.Frame(self.master, padx=60)
        form.pack(pady=20, fill="both")

        tk.Label(form, text="TÊN ĐĂNG NHẬP", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.e_u = tk.Entry(form, font=("Arial", 12), bd=0, highlightthickness=1, highlightbackground="#dfe6e9")
        self.e_u.pack(fill="x", pady=(5, 15), ipady=8)
        self.e_u.focus()

        tk.Label(form, text="MẬT KHẨU", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.e_p = tk.Entry(form, font=("Arial", 12), show="*", bd=0, highlightthickness=1,
                            highlightbackground="#dfe6e9")
        self.e_p.pack(fill="x", pady=(5, 5), ipady=8)

        tk.Label(form, text="VAI TRÒ TRUY CẬP", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.cb_r = ttk.Combobox(form, values=["Nhân viên", "Admin"], state="readonly", font=("Segoe UI", 10))
        self.cb_r.pack(fill="x", pady=5, ipady=5)
        self.cb_r.current(0)

        tk.Checkbutton(form, text="Hiện mật khẩu", variable=self.var_show,
                       command=self.toggle, font=("Arial", 8)).pack(anchor="w")

        # Gắn phím Enter vào ô nhập liệu
        self.e_p.bind('<Return>', lambda e: self.login())

        # Nút xác nhận
        tk.Button(self.master, text="XÁC NHẬN ĐĂNG NHẬP", command=self.login, bg=header_bg, fg="white",
                  font=("Segoe UI", 11, "bold"), bd=0, height=2, cursor="hand2").pack(fill="x", padx=60, pady=15)

        tk.Button(self.master, text="ĐĂNG KÝ NGƯỜI VẬN HÀNH MỚI", command=self.app_manager.show_register_page,
                  bg="white", fg=header_bg, font=("Segoe UI", 9, "underline"), bd=0, cursor="hand2").pack()

    def toggle(self):
        """Hàm ẩn/hiện mật khẩu an toàn"""
        if self.e_p and self.e_p.winfo_exists():
            self.e_p.config(show="" if self.var_show.get() == 1 else "*")

    def login(self):
        """Hàm xử lý đăng nhập với logic SQL sạch cảnh báo"""
        if not self.e_u or not self.e_u.winfo_exists():
            return

        u, p, r = self.e_u.get().strip(), self.e_p.get().strip(), self.cb_r.get()

        # noinspection SqlNoDataSourceInspection
        # noinspection SqlDialectInspection
        sql_check = "SELECT * FROM users WHERE username=? AND password=? AND role=?"

        try:
            res = self.app_manager.db.query(sql_check, (u, p, r))

            if res:
                self.app_manager.current_user = list(res[0])

                # noinspection SqlNoDataSourceInspection
                # noinspection SqlDialectInspection
                sql_log = "INSERT INTO login_history VALUES (?, ?, ?)"
                self.app_manager.db.query(sql_log, (u, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Thành công"))

                self.app_manager.show_menu_page()
            else:
                messagebox.showerror("Từ chối", "Thông tin đăng nhập hoặc chức vụ không đúng!")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể truy cập Database: {str(e)}")