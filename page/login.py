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
        self.var_show.set(0)

        self.view()

    def view(self):
        # Màu nền tối Obsidian mờ cho màn hình chính của Windows giúp bảo vệ mắt
        self.master.configure(bg="#1c1d22")

        # Khung viền mờ tối của thẻ Card chính giữa trung tâm màn hình
        shadow = tk.Frame(self.master, bg="#25262c", bd=0)
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=422, height=462)

        # Thẻ Card xám tối chính
        card = tk.Frame(shadow, bg="#25262c", bd=0)
        card.pack(fill="both", expand=True, padx=1, pady=1)

        # Dải màu nhấn công nghệ màu xanh ngọc dịu mắt ở đầu Card
        accent_bar = tk.Frame(card, bg="#1abc9c", height=5)
        accent_bar.pack(fill="x", side="top")

        # Header bên trong Card thương hiệu Việt hóa hoàn toàn
        header_bg = "#25262c"
        header = tk.Frame(card, bg=header_bg)
        header.pack(fill="x", side="top")
        tk.Label(header, text="🛡️ GUNDAM KITVAULT PRO", font=("Segoe UI", 15, "bold"),
                 fg="#1abc9c", bg=header_bg).pack(pady=(20, 5))
        tk.Label(header, text="HỆ THỐNG ĐIỀU KHIỂN TRUNG TÂM", font=("Segoe UI", 8, "bold"),
                 fg="#a4b0be", bg=header_bg).pack()

        # Khung chứa các trường nhập liệu
        form = tk.Frame(card, bg="#25262c", padx=40)
        form.pack(pady=15, fill="both", expand=True)

        tk.Label(form, text="TÊN ĐĂNG NHẬP", font=("Segoe UI", 8, "bold"), bg="#25262c", fg="#a4b0be").pack(anchor="w")
        border_u, self.e_u = self.create_modern_entry(form, "Nhập tài khoản quản trị...")
        border_u.pack(fill="x", pady=(5, 12))
        self.e_u.focus()

        tk.Label(form, text="MẬT KHẨU", font=("Segoe UI", 8, "bold"), bg="#25262c", fg="#a4b0be").pack(anchor="w")
        border_p, self.e_p = self.create_modern_entry(form, "Nhập mật khẩu...", is_password=True)
        border_p.pack(fill="x", pady=(5, 5))

        self.chk_show = tk.Checkbutton(form, text="Hiện mật khẩu", variable=self.var_show,
                                       command=self.toggle, font=("Segoe UI", 8), bg="#25262c",
                                       activebackground="#25262c", fg="#a4b0be", selectcolor="#1c1d22",
                                       activeforeground="#f5f6fa", onvalue=1, offvalue=0)
        self.chk_show.pack(anchor="w", pady=(0, 15))

        # Gắn phím Enter vào cả 2 ô nhập liệu để đăng nhập siêu tốc
        def move_to_password(e):
            self.e_p.focus()
            return "break"

        self.e_u.bind('<Return>', move_to_password)
        self.e_p.bind('<Return>', lambda e: self.login())

        # Nút xác nhận đăng ký tài khoản phẳng xanh ngọc
        btn_login = tk.Button(form, text="XÁC NHẬN ĐĂNG NHẬP", command=self.login, bg="#1abc9c", fg="white",
                              font=("Segoe UI", 10, "bold"), bd=0, height=2, cursor="hand2",
                              activebackground="#16a085", activeforeground="white")
        btn_login.pack(fill="x", pady=(10, 10))

        # Hiệu ứng đổi màu di chuột (Hover Effect)
        btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#16a085"))
        btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#1abc9c"))

        # Đường dẫn đăng ký tối giản Việt hóa
        btn_register = tk.Button(form, text="Đăng ký người vận hành mới", command=self.app_manager.show_register_page,
                                 bg="#25262c", fg="#1abc9c", font=("Segoe UI", 9, "underline"), bd=0,
                                 cursor="hand2", activebackground="#25262c", activeforeground="#16a085")
        btn_register.pack(pady=5)

    def create_modern_entry(self, parent, placeholder, is_password=False):
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

            def on_label_click(event):
                placeholder_label.place_forget()
                entry.focus()

            placeholder_label.bind("<Button-1>", on_label_click)

            def focus_in(e):
                border_frame.config(bg="#1abc9c")
                placeholder_label.place_forget()

            def focus_out(e):
                border_frame.config(bg="#3d414e")
                entry.selection_clear()
                if not entry.get():
                    placeholder_label.place(x=0, y=0, relheight=1)
                    placeholder_label.lift()

            entry.bind("<FocusIn>", focus_in)
            entry.bind("<FocusOut>", focus_out)

        else:
            entry = tk.Entry(inner_frame, font=("Segoe UI", 10), bg="#1c1d22", fg="gray", bd=0,
                             insertbackground="#1abc9c", selectbackground="#1c1d22", selectforeground="#f5f6fa",
                             exportselection=0)
            entry.insert(0, placeholder)
            entry.pack(fill="x", expand=True)

            def focus_in(e):
                border_frame.config(bg="#1abc9c")
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg="#f5f6fa")

            def focus_out(e):
                border_frame.config(bg="#3d414e")
                entry.selection_clear()
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg="gray")

            entry.bind("<FocusIn>", focus_in)
            entry.bind("<FocusOut>", focus_out)

        return border_frame, entry

    def toggle(self):
        self.show_password = not self.show_password
        if self.e_p and self.e_p.winfo_exists():
            if self.show_password:
                self.e_p.config(show="")
            else:
                self.e_p.config(show="*")

    def login(self):
        """Hàm xử lý đăng nhập tự động nhận diện chức vụ từ database"""
        if not self.e_u or not self.e_u.winfo_exists():
            return

        u, p = self.e_u.get().strip(), self.e_p.get().strip()

        # Kiểm tra lọc nếu dữ liệu gõ trùng với gợi ý mờ
        if u == "Nhập tài khoản quản trị..." or not u:
            u = ""
        if p == "Nhập mật khẩu..." or not p:
            p = ""

        if not u or not p:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ Tên đăng nhập và Mật khẩu!")
            return

        sql_check = "SELECT * FROM users WHERE username=? AND password=?"

        try:
            res = self.app_manager.db.query(sql_check, (u, p))

            if res:
                self.app_manager.current_user = list(res[0])

                # Ghi nhật ký đăng nhập hệ thống thành công
                sql_log = "INSERT INTO login_history (username, time, status) VALUES (?, ?, ?)"
                self.app_manager.db.query(sql_log, (u, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Thành công"))

                self.app_manager.show_menu_page()
            else:
                messagebox.showerror("Từ chối", "Tài khoản hoặc Mật khẩu không chính xác!")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể truy cập cơ sở dữ liệu: {str(e)}")
