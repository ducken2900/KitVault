import tkinter as tk


class MenuPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.view()

    def view(self):
        user = self.app_manager.current_user
        name, role = user[2], user[4]
        navy = "#1e3799"

        header = tk.Frame(self.master, bg=navy)
        header.pack(fill="x", side="top")
        tk.Label(header, text="🛡️ BÀN ĐIỀU KHIỂN TRUNG TÂM", font=("Arial", 22, "bold"), fg="white", bg=navy).pack(
            pady=25)

        info_f = tk.Frame(self.master, bg="#f1f2f6", pady=10)
        info_f.pack(fill="x", side="top")
        tk.Label(info_f, text=f"NHÂN VIÊN: {name.upper()}", font=("Consolas", 11, "bold"), bg="#f1f2f6").pack()
        tk.Label(info_f, text=f"QUYỀN TRUY CẬP: {role.upper()}", font=("Consolas", 10), fg=navy, bg="#f1f2f6").pack()

        body = tk.Frame(self.master, bg="white")
        body.pack(expand=True, fill="both")

        button_container = tk.Frame(body, bg="white")
        button_container.place(relx=0.5, rely=0.5, anchor="center")
        
        btn_s = {"font": ("Segoe UI", 12, "bold"), "fg": "white", "bg": navy, "height": 2, "width": 40, "bd": 0,
                 "cursor": "hand2"}

        tk.Button(body, text="📦 QUẢN LÝ KHO HÀNG GUNDAM", **btn_s, command=self.app_manager.show_quanly_kho_page).pack(
            pady=10)
        tk.Button(body, text="🛒 GIAO DỊCH BÁN HÀNG", **btn_s, command=self.app_manager.show_quanly_donhang_page).pack(
            pady=10)

        # Đã loại bỏ hoàn toàn nút Quản lý khách hàng tại đây để tối ưu hóa hệ thống

        if role == "Admin" or user[0].lower() == "admin":
            adm_s = btn_s.copy()
            adm_s["bg"] = "#1e3799"
            tk.Button(body, text="👥 QUẢN LÝ NHÂN SỰ TÀI KHOẢN", **adm_s,
                      command=self.app_manager.show_quanly_taikhoan_page).pack(pady=10)
            tk.Button(body, text="📊 BÁO CÁO DOANH THU CHI TIẾT", **adm_s,
                      command=self.app_manager.show_baocao_page).pack(pady=10)

        tk.Button(self.master, text="ĐĂNG XUẤT", bg="#eb4d4b", fg="white", width=20, bd=0,
                  command=self.app_manager.show_login_page).pack(side="bottom", pady=40)