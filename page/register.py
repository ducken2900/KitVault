import tkinter as tk
from tkinter import messagebox
import sqlite3


class RegisterPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.ents = {}

        self.view()

    def view(self):
        main_navy = "#1e3799"
        self.master.configure(bg="#1c1d22")

        is_admin = self.app_manager.current_user is not None
        title = "THÊM NHÂN VIÊN MỚI" if is_admin else "ĐĂNG KÝ TÀI KHOẢN"

        shadow = tk.Frame(self.master, bg="#25262c", bd=0)
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=422, height=522)

        card = tk.Frame(shadow, bg="#25262c", bd=0)
        card.pack(fill="both", expand=True, padx=1, pady=1)

        accent_bar = tk.Frame(card, bg="#1abc9c", height=5)
        accent_bar.pack(fill="x", side="top")

        header = tk.Frame(card, bg="#25262c", pady=15)
        header.pack(fill="x", side="top")
        tk.Label(header, text="ĐĂNG KÝ", font=("Segoe UI", 16, "bold"), fg="#1abc9c", bg="#25262c").pack()
        tk.Label(header, text=title, font=("Segoe UI", 8, "bold"), fg="#a4b0be", bg="#25262c").pack(pady=(2, 0))

        form = tk.Frame(card, bg="#25262c", padx=40)
        form.pack(fill="x", pady=10)

        fields_config = [
            ("Tài khoản:", "User", "Tên đăng nhập mới...", False),
            ("Mật khẩu:", "Pass", "Mật khẩu đăng ký...", True),
            ("Họ và tên:", "Name", "Họ tên nhân viên...", False),
            ("SĐT liên hệ:", "Phone", "Số điện thoại...", False)
        ]

        for i, (txt, key, placeholder, is_pass) in enumerate(fields_config):
            tk.Label(form, text=txt, font=("Segoe UI", 9, "bold"), bg="#25262c", fg="#a4b0be").grid(row=i, column=0,
                                                                                                    sticky="w", pady=10)

            border_e, e = self.create_modern_entry(form, placeholder, is_pass)
            border_e.grid(row=i, column=1, sticky="ew", padx=(15, 0), pady=10)
            self.ents[key] = e

        form.columnconfigure(1, weight=1)

        btn_submit = tk.Button(card, text="XÁC NHẬN ĐĂNG KÝ", bg="#27ae60", fg="white",
                               font=("Segoe UI", 10, "bold"), height=2, bd=0, cursor="hand2", command=self.save)
        btn_submit.pack(fill="x", padx=40, pady=(15, 5))

        btn_submit.bind("<Enter>", lambda e: btn_submit.config(bg="#218c53"))
        btn_submit.bind("<Leave>", lambda e: btn_submit.config(bg="#27ae60"))

        tk.Button(card, text="QUAY LẠI", command=self.back, bd=0, fg="#1abc9c", bg="#25262c",
                  font=("Segoe UI", 9, "underline"), cursor="hand2", activebackground="#25262c",
                  activeforeground="#16a085").pack(pady=5)

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

    def back(self):
        if self.app_manager.current_user:
            self.app_manager.show_quanly_taikhoan_page()
        else:
            self.app_manager.show_login_page()

    def save(self):
        u = self.ents["User"].get().strip()
        p = self.ents["Pass"].get().strip()
        n = self.ents["Name"].get().strip()
        s = self.ents["Phone"].get().strip()

        if u == "Tên đăng nhập mới..." or not u: u = ""
        if p == "Mật khẩu đăng ký..." or not p: p = ""
        if n == "Họ tên nhân viên..." or not n: n = ""
        if s == "Số điện thoại..." or not s: s = ""

        if not u or not p or not n:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đủ thông tin bắt buộc (Tài khoản, Mật khẩu, Họ tên)!")
            return

        try:
            sql = "INSERT INTO users (username, password, fullname, phone, role) VALUES (?, ?, ?, ?, ?)"
            self.app_manager.db.query(sql, (u, p, n, s, "Nhân viên"))

            messagebox.showinfo("Thành công", f"Đã đăng ký thành công tài khoản người dùng '{u}'!")
            self.back()

        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi đăng ký", "Tên đăng nhập này đã tồn tại trên hệ thống! Vui lòng chọn tên khác.")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể đăng ký: {str(e)}")