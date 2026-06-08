import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.e_u = None
        self.e_p = None
        self.show_password = False
        self.var_show = tk.IntVar(master=self.master, value=0)

        self.view()

    def view(self):
        # [THIẾT KẾ]: Màu nền tối của toàn bộ trang đăng nhập
        self.master.configure(bg="#1c1d22")

        # [THIẾT KẾ]: Khung Bo ngoài Đăng nhập (Card)
        shadow = tk.Frame(self.master, bg="#25262c", bd=0)
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=422, height=462)

        card = tk.Frame(shadow, bg="#25262c", bd=0)
        card.pack(fill="both", expand=True, padx=1, pady=1)

        # [THIẾT KẾ]: Dải màu nhấn mỏng màu xanh ngọc ở đỉnh thẻ đăng nhập
        accent_bar = tk.Frame(card, bg="#1abc9c", height=5)
        accent_bar.pack(fill="x", side="top")

        header_bg = "#25262c"
        header = tk.Frame(card, bg=header_bg)
        header.pack(fill="x", side="top")

        # [THIẾT KẾ]: Tiêu đề ứng dụng
        tk.Label(header, text="🛡️ GUNDAM KITVAULT PRO", font=("Segoe UI", 15, "bold"),
                 fg="#1abc9c", bg=header_bg).pack(pady=(20, 5))
        tk.Label(header, text="HỆ THỐNG ĐIỀU KHIỂN TRUNG TÂM", font=("Segoe UI", 8, "bold"),
                 fg="#a4b0be", bg=header_bg).pack()

        form = tk.Frame(card, bg="#25262c", padx=40)
        form.pack(pady=15, fill="both", expand=True)

        # [THIẾT KẾ]: Ô nhập tài khoản và chữ hiển thị chìm
        tk.Label(form, text="TÊN ĐĂNG NHẬP", font=("Segoe UI", 8, "bold"), bg="#25262c", fg="#a4b0be").pack(anchor="w")
        border_u, self.e_u = self.create_modern_entry(form, "Nhập tài khoản quản trị...")
        border_u.pack(fill="x", pady=(5, 12))
        self.e_u.focus()

        # [THIẾT KẾ]: Ô nhập mật khẩu bảo mật ẩn ký tự
        tk.Label(form, text="MẬT KHẨU", font=("Segoe UI", 8, "bold"), bg="#25262c", fg="#a4b0be").pack(anchor="w")
        border_p, self.e_p = self.create_modern_entry(form, "Nhập mật khẩu...", is_password=True)
        border_p.pack(fill="x", pady=(5, 5))

        # Checkbutton ẩn/hiện mật khẩu
        self.chk_show = tk.Checkbutton(form, text="Hiện mật khẩu", variable=self.var_show,
                                       command=self.toggle, font=("Segoe UI", 8), bg="#25262c",
                                       activebackground="#25262c", fg="#a4b0be", selectcolor="#1c1d22",
                                       activeforeground="#f5f6fa", onvalue=1, offvalue=0)
        self.chk_show.pack(anchor="w", pady=(0, 15))

        # Phím tắt Enter chuyển ô nhập nhanh trên bàn phím
        self.e_u.bind('<Return>', lambda e: self.e_p.focus())
        self.e_p.bind('<Return>', lambda e: self.login())

        # [THIẾT KẾ]: Nút Đăng nhập chính và hiệu ứng chuyển màu khi lướt chuột qua
        btn_login = tk.Button(form, text="XÁC NHẬN ĐĂNG NHẬP", command=self.login, bg="#1abc9c", fg="white",
                              font=("Segoe UI", 10, "bold"), bd=0, height=2, cursor="hand2",
                              activebackground="#16a085", activeforeground="white")
        btn_login.pack(fill="x", pady=(10, 10))

        btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#16a085"))
        btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#1abc9c"))

        btn_register = tk.Button(form, text="Đăng ký người vận hành mới", command=self.app_manager.show_register_page,
                                 bg="#25262c", fg="#1abc9c", font=("Segoe UI", 9, "underline"), bd=0,
                                 cursor="hand2", activebackground="#25262c", activeforeground="#16a085")
        btn_register.pack(pady=5)

    def create_modern_entry(self, parent, placeholder, is_password=False):
        """[THIẾT KẾ]: Định dạng hiệu ứng đổi màu viền ô nhập động khi click"""
        border_frame = tk.Frame(parent, bg="#3d414e", padx=1, pady=1)
        inner_frame = tk.Frame(border_frame, bg="#1c1d22", padx=10, pady=6)
        inner_frame.pack(fill="x", expand=True)

        if is_password:
            entry = tk.Entry(inner_frame, font=("Segoe UI", 10), bg="#1c1d22", fg="#f5f6fa", bd=0,
                             insertbackground="#1abc9c", selectbackground="#1c1d22", selectforeground="#f5f6fa",
                             exportselection=0, show="*")
            entry.pack(fill="x", expand=True)

            placeholder_label = tk.Label(inner_frame, text=placeholder, fg="gray", bg="#1c1d22", font=("Segoe UI", 10))
            placeholder_label.place(x=0, y=0, relheight=1)
            placeholder_label.lift()

            placeholder_label.bind("<Button-1>", lambda e: [placeholder_label.place_forget(), entry.focus()])

            entry.bind("<FocusIn>", lambda e: [border_frame.config(bg="#1abc9c"), placeholder_label.place_forget()])
            entry.bind("<FocusOut>", lambda e: [border_frame.config(bg="#3d414e"), entry.selection_clear(),
                                                placeholder_label.place(x=0, y=0,
                                                                        relheight=1) if not entry.get() else None])
        else:
            entry = tk.Entry(inner_frame, font=("Segoe UI", 10), bg="#1c1d22", fg="gray", bd=0,
                             insertbackground="#1abc9c", selectbackground="#1c1d22", selectforeground="#f5f6fa",
                             exportselection=0)
            entry.insert(0, placeholder)
            entry.pack(fill="x", expand=True)

            entry.bind("<FocusIn>", lambda e: [border_frame.config(bg="#1abc9c"),
                                               entry.delete(0, tk.END) if entry.get() == placeholder else None,
                                               entry.config(fg="#f5f6fa")])
            entry.bind("<FocusOut>", lambda e: [border_frame.config(bg="#3d414e"), entry.selection_clear(),
                                                [entry.insert(0, placeholder),
                                                 entry.config(fg="gray")] if not entry.get() else None])

        return border_frame, entry

    def toggle(self):
        """Xử lý nút công tắc ẩn/hiện mật khẩu"""
        self.show_password = not self.show_password
        if self.e_p and self.e_p.winfo_exists():
            self.e_p.config(show="" if self.show_password else "*")

    def login(self):
        """[TÍNH NĂNG]: Luồng kiểm tra thông tin đăng nhập và lưu log hệ thống"""
        if not self.e_u or not self.e_u.winfo_exists():
            return

        u, p = self.e_u.get().strip(), self.e_p.get().strip()

        if u == "Nhập tài khoản quản trị..." or not u: u = ""
        if p == "Nhập mật khẩu..." or not p: p = ""

        if not u or not p:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ Tên đăng nhập và Mật khẩu!")
            return

        sql_check = "SELECT * FROM users WHERE username=? AND password=?"

        try:
            res = self.app_manager.db.query(sql_check, (u, p))

            if res:
                self.app_manager.current_user = list(res[0])

                # Ghi lịch sử đăng nhập vào bảng dữ liệu SQL
                now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                sql_log = "INSERT INTO login_history (username, time, status) VALUES (?, ?, ?)"
                self.app_manager.db.query(sql_log, (u, now_str, "Thành công"))

                # Ghi tệp CSV sao lưu log hệ thống cục bộ
                try:
                    import os
                    import csv
                    os.makedirs("database", exist_ok=True)
                    with open("database/login_history.csv", "a", encoding="utf-8", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([u, now_str, "Thành công"])
                except Exception:
                    pass

                self.app_manager.show_menu_page()
            else:
                messagebox.showerror("Từ chối", "Tài khoản hoặc Mật khẩu không chính xác!")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể truy cập cơ sở dữ liệu: {str(e)}")