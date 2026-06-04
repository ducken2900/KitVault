import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from common.button import CustomButton


class QuanLyTaiKhoanPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # --- CẤU HÌNH MÀU SẮC ĐỒNG BỘ ---
        self.color_navy = "#1e3799"
        self.color_dark = "#2d3436"
        self.color_light = "#f1f2f6"
        self.color_success = "#27ae60"  # Xanh lá
        self.color_warning = "#e67e22"  # Cam
        self.color_danger = "#d63031"   # Đỏ

        # Khởi tạo các thuộc tính giao diện
        self.tree1 = None
        self.tree2 = None
        self.search_user_entry = None
        self.btn_save = None
        self.nb = None  # Khởi tạo đối tượng Notebook quản lý Tab

        self.ents = {}
        self.edit_mode = False

        self.view()
        self.load_users()
        self.load_history()

    def view(self):
        # Header Navy Blue hiển thị tiêu đề hệ thống quản trị
        header = tk.Frame(self.master, bg=self.color_navy)
        header.pack(fill="x")
        tk.Label(header, text="👤 QUẢN TRỊ NHÂN SỰ & HỆ THỐNG", font=("Segoe UI", 18, "bold"),
                 fg="white", bg=self.color_navy).pack(pady=20)

        # Body chính làm nền chứa dữ liệu
        body = tk.Frame(self.master, bg=self.color_light)
        body.pack(fill="both", expand=True, padx=20, pady=10)

        # Hệ thống Tab Notebook phân chia chức năng
        self.nb = ttk.Notebook(body)
        self.nb.pack(fill="both", expand=True)

        # --- TAB 1: DANH SÁCH NHÂN VIÊN ---
        tab_nv = tk.Frame(self.nb, bg="white")
        self.nb.add(tab_nv, text=" 👥 Danh sách nhân viên ")

        # Thanh tìm kiếm & bộ nút bấm công cụ nhanh phía trên
        search_f = tk.Frame(tab_nv, bg="white", pady=10)
        search_f.pack(fill="x", padx=10)

        tk.Label(search_f, text="🔍 Tìm nhân viên:", font=("Arial", 10, "bold"), bg="white").pack(side="left", padx=5)
        self.search_user_entry = tk.Entry(search_f, font=("Arial", 11), bd=1, relief="solid")
        self.search_user_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=3)
        self.search_user_entry.bind('<KeyRelease>', lambda e: self.load_users())

        tk.Button(search_f, text="🗑️ Xóa tài khoản chọn", bg=self.color_danger, fg="white", font=("Arial", 9, "bold"),
                  command=self.delete_user, bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        tk.Button(search_f, text="🔄 Làm mới bảng", bg=self.color_dark, fg="white", font=("Arial", 9),
                  command=self.refresh_users, bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        # Bảng hiển thị Treeview danh sách nhân viên
        tree_f = tk.Frame(tab_nv)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "U", "N", "P", "R")
        self.tree1 = ttk.Treeview(tree_f, columns=cols, show="headings", height=5)

        heads = ["STT", "TÊN ĐĂNG NHẬP", "HỌ VÀ TÊN", "SỐ ĐIỆN THOẠI", "VAI TRÒ"]
        for c, h in zip(cols, heads):
            self.tree1.heading(c, text=h)
            w = 50 if c == "STT" else 150
            if c == "N": w = 220
            self.tree1.column(c, width=w, anchor="center" if c != "N" else "w")

        self.tree1.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_f, command=self.tree1.yview).pack(side="right", fill="y")
        self.tree1.bind("<<TreeviewSelect>>", self.on_user_select)

        # Bảng điều khiển nhập liệu tích hợp ngay bên dưới bảng (Inline Form)
        form_f = tk.LabelFrame(tab_nv, text=" 📝 THÔNG TIN NHÂN SỰ ", bg="white",
                               font=("Segoe UI", 9, "bold"), fg=self.color_navy, padx=15, pady=10)
        form_f.pack(fill="x", padx=10, pady=(10, 15))

        inputs_container = tk.Frame(form_f, bg="white")
        inputs_container.pack(fill="x")

        # Cấu trúc form biểu mẫu nhập liệu
        fields = [
            ("Tên đăng nhập:", "Username", 12, True),
            ("Mật khẩu:", "Password", 12, True),
            ("Họ và tên:", "Fullname", 20, True),
            ("Số điện thoại:", "Phone", 12, True),
            ("Vai trò:", "Role", 12, False)
        ]

        for i, (txt, key, width_val, is_entry) in enumerate(fields):
            col = i * 2
            tk.Label(inputs_container, text=txt, bg="white", font=("Arial", 9, "bold")).grid(row=0, column=col,
                                                                                            sticky="w", padx=(10, 2))
            if is_entry:
                e = tk.Entry(inputs_container, font=("Arial", 10), bd=1, relief="solid", width=width_val)
                e.grid(row=0, column=col + 1, padx=5, ipady=2)
            else:
                e = ttk.Combobox(inputs_container, values=["Admin", "Nhân viên"], state="readonly", width=width_val)
                e.grid(row=0, column=col + 1, padx=5)
                e.current(1)
            self.ents[key] = e

        # Nút bấm thao tác lưu dữ liệu trên Form
        btn_container = tk.Frame(inputs_container, bg="white")
        btn_container.grid(row=0, column=10, padx=(15, 0), sticky="e")

        self.btn_save = tk.Button(btn_container, text="➕ THÊM MỚI", command=self.save_user_logic,
                                  bg=self.color_success, fg="white", font=("Segoe UI", 8, "bold"),
                                  width=12, height=1, bd=0, cursor="hand2")
        self.btn_save.pack(side="left", padx=2)

        tk.Button(btn_container, text="🧹 RESET", command=self.clear_form,
                  bg=self.color_dark, fg="white", font=("Segoe UI", 8), width=10, height=1, bd=0, cursor="hand2").pack(
            side="left", padx=2)

        inputs_container.columnconfigure(1, weight=1)
        inputs_container.columnconfigure(3, weight=1)
        inputs_container.columnconfigure(5, weight=2)

        # --- TAB 2: NHẬT KÝ ĐĂNG NHẬP ---
        tab_ls = tk.Frame(self.nb, bg="white")
        self.nb.add(tab_ls, text=" 📜 Nhật ký hệ thống ")

        tree_f2 = tk.Frame(tab_ls)
        tree_f2.pack(fill="both", expand=True, padx=10, pady=10)

        cols2 = ("STT", "U", "T", "A")
        self.tree2 = ttk.Treeview(tree_f2, columns=cols2, show="headings", height=5)
        heads2 = ["STT", "TÀI KHOẢN", "THỜI GIAN ĐĂNG NHẬP", "TRẠNG THÁI"]
        for c, h in zip(cols2, heads2):
            self.tree2.heading(c, text=h)
            w = 50 if c == "STT" else 200
            self.tree2.column(c, width=w, anchor="center")

        self.tree2.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_f2, command=self.tree2.yview).pack(side="right", fill="y")

        # Chân trang điều hướng an toàn bám sát cửa sổ
        footer_bar = tk.Frame(self.master, bg=self.color_light)
        footer_bar.pack(fill="x", pady=(10, 0))

        tk.Button(footer_bar, text="⬅ QUAY LẠI MENU CHÍNH", command=self.app_manager.show_menu_page,
                  bg="#2d3436", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=25, pady=8, cursor="hand2").pack(
            anchor="center")

    def on_user_select(self, event):
        sel = self.tree1.selection()
        if not sel: return
        vals = self.tree1.item(sel[0], "values")

        username = vals[1]

        # Đồng bộ lấy dữ liệu qua SQL phục vụ cập nhật biểu mẫu nhập liệu
        res = self.app_manager.db.query("SELECT password FROM users WHERE username=?", (username,))
        password = res[0][0] if res else ""

        self.ents["Username"].config(state="normal")
        self.ents["Username"].delete(0, tk.END)
        self.ents["Username"].insert(0, username)
        self.ents["Username"].config(state="disabled")  # Khóa bảo vệ trường ID tài khoản chính

        self.ents["Password"].delete(0, tk.END)
        self.ents["Password"].insert(0, password)

        self.ents["Fullname"].delete(0, tk.END)
        self.ents["Fullname"].insert(0, vals[2])

        self.ents["Phone"].delete(0, tk.END)
        self.ents["Phone"].insert(0, vals[3])

        self.ents["Role"].set(vals[4])

        self.edit_mode = True
        self.btn_save.config(text="📝 CẬP NHẬT", bg=self.color_warning)

    def save_user_logic(self):
        """XỬ LÝ LƯU HOẶC CẬP NHẬT THÔNG TIN NHÂN SỰ TRỰC TIẾP QUA SQL"""
        username = self.ents["Username"].get().strip()
        password = self.ents["Password"].get().strip()
        fullname = self.ents["Fullname"].get().strip()
        phone = self.ents["Phone"].get().strip()
        role = self.ents["Role"].get()

        if not username or not password or not fullname:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng điền đầy đủ Tên đăng nhập, Mật khẩu và Họ tên!")
            return

        try:
            if self.edit_mode:
                self.app_manager.db.query(
                    "UPDATE users SET password=?, fullname=?, phone=?, role=? WHERE username=?",
                    (password, fullname, phone, role, username)
                )
                messagebox.showinfo("Thành công", f"Đã cập nhật thông tin nhân viên '{fullname}' thành công!")
            else:
                exists = self.app_manager.db.query("SELECT username FROM users WHERE username=?", (username,))
                if exists:
                    messagebox.showerror("Lỗi", f"Tên đăng nhập '{username}' đã tồn tại!")
                    return

                self.app_manager.db.query(
                    "INSERT INTO users (username, password, fullname, phone, role) VALUES (?, ?, ?, ?, ?)",
                    (username, password, fullname, phone, role)
                )
                messagebox.showinfo("Thành công", f"Đã thêm mới nhân viên '{fullname}' thành công!")

            self.clear_form()
            self.load_users()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể lưu thông tin nhân viên: {str(e)}")

    def delete_user(self):
        """XÓA TÀI KHOẢN NHÂN VIÊN VỚI CƠ CHẾ BẢO VỆ ADMIN"""
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("!", "Vui lòng chọn nhân viên cần thao tác!")
            return

        vals = self.tree1.item(sel[0], "values")
        username = vals[1]
        fullname = vals[2]

        # Kiểm tra ngăn chặn hành vi xóa quyền quản trị hệ thống cốt lõi
        if username.lower() in ["admin", "a"]:
            messagebox.showerror("Bảo mật hệ thống", "Không được phép xóa tài khoản quản trị viên tối cao (Admin/a)!")
            return

        if messagebox.askyesno("Xác nhận xóa",
                               f"Bạn có chắc chắn muốn xóa vĩnh viễn tài khoản nhân viên '{fullname}' (User: {username})?"):
            try:
                self.app_manager.db.query("DELETE FROM users WHERE username=?", (username,))
                messagebox.showinfo("Thành công", f"Đã xóa tài khoản nhân viên '{fullname}'!")
                self.clear_form()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể xóa nhân viên: {e}")

    def refresh_users(self):
        if self.search_user_entry:
            self.search_user_entry.delete(0, tk.END)
        self.clear_form()
        self.load_users()
        self.load_history()

    def clear_form(self):
        self.edit_mode = False
        self.ents["Username"].config(state="normal")
        self.ents["Username"].delete(0, tk.END)
        self.ents["Password"].delete(0, tk.END)
        self.ents["Fullname"].delete(0, tk.END)
        self.ents["Phone"].delete(0, tk.END)
        self.ents["Role"].current(1)
        self.btn_save.config(text="➕ THÊM MỚI", bg=self.color_success)

    def load_users(self):
        if not self.tree1: return
        for i in self.tree1.get_children(): self.tree1.delete(i)

        user_input = self.search_user_entry.get().lower().strip() if self.search_user_entry else ""
        term = f"%{user_input}%"
        sql = "SELECT username, fullname, phone, role FROM users WHERE username LIKE ? OR fullname LIKE ?"

        try:
            rows = self.app_manager.db.query(sql, (term, term))
            for idx, r in enumerate(rows, 1):
                self.tree1.insert("", "end", values=(idx, r[0], r[1], r[2], r[3]))
        except Exception as e:
            print(f"Lỗi tải nhân viên: {e}")

    def load_history(self):
        if not self.tree2: return
        for i in self.tree2.get_children(): self.tree2.delete(i)

        sql = "SELECT username, time, status FROM login_history ORDER BY time DESC"
        try:
            rows = self.app_manager.db.query(sql)
            for idx, r in enumerate(rows, 1):
                self.tree2.insert("", "end", values=(idx, r[0], r[1], r[2]))
        except Exception as e:
            print(f"Lỗi tải lịch sử đăng nhập: {e}")