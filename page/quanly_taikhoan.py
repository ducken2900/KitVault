import tkinter as tk
from tkinter import ttk, messagebox


class QuanLyTaiKhoanPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.color_navy = "#2d2f36"
        self.color_dark = "#1c1d22"
        self.color_light = "#1c1d22"
        self.color_card = "#2d2f36"
        self.color_border = "#3d414e"
        self.color_success = "#2ecc71"
        self.color_warning = "#f39c12"
        self.color_danger = "#e74c3c"
        self.color_info = "#00a8ff"
        self.color_teal = "#1abc9c"

        self.tree1 = None
        self.tree2 = None
        self.search_user_entry = None
        self.btn_save = None

        self.ents = {}
        self.edit_mode = False

        self.setup_dark_styles()
        self.view()
        self.load_users()
        self.load_history()

    def setup_dark_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#22242b",
                        foreground="#f5f6fa",
                        fieldbackground="#22242b",
                        rowheight=35,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 10, "bold"),
                        background="#2d2f36",
                        foreground="white",
                        borderwidth=1,
                        bordercolor="#3d414e")
        style.map("Treeview",
                  background=[('selected', self.color_teal), ('!selected', '#22242b')],
                  foreground=[('selected', 'white'), ('!selected', '#f5f6fa')])

        style.configure("TNotebook", background="#1c1d22", borderwidth=0)
        style.configure("TNotebook.Tab",
                        background="#2d2f36",
                        foreground="#a4b0be",
                        borderwidth=1,
                        bordercolor="#3d414e",
                        padding=[15, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", "#1e3799")],
                  foreground=[("selected", "white")])

    def view(self):
        header = tk.Frame(self.master, bg=self.color_navy, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        accent = tk.Frame(header, bg=self.color_teal, height=4)
        accent.pack(fill="x", side="top")

        tk.Label(header, text="👤 QUẢN TRỊ NHÂN SỰ & HỆ THỐNG", font=("Segoe UI", 16, "bold"),
                 fg="white", bg=self.color_navy).pack(side="left", padx=20, pady=(5, 0))

        btn_back = tk.Button(header, text="QUAY LẠI MENU", command=self.app_manager.show_menu_page,
                             bg=self.color_danger, fg="white", font=("Arial", 8, "bold"), bd=0, padx=15)
        btn_back.pack(side="right", padx=20, pady=(5, 0))
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#c0392b"))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg=self.color_danger))

        body = tk.Frame(self.master, bg=self.color_dark)
        body.pack(fill="both", expand=True, padx=20, pady=10)

        nb = ttk.Notebook(body)
        nb.pack(fill="both", expand=True)

        tab_nv = tk.Frame(nb, bg="#22242b")
        nb.add(tab_nv, text=" 👥 Danh sách nhân viên ")

        search_f = tk.Frame(tab_nv, bg="#22242b", pady=10, padx=10)
        search_f.pack(fill="x")

        tk.Label(search_f, text="🔍 TÌM NHÂN VIÊN:", font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").pack(side="left", padx=5)
        self.search_user_entry = tk.Entry(search_f, font=("Segoe UI", 10), bg=self.color_dark, fg="white", insertbackground="white", bd=1, relief="solid")
        self.search_user_entry.config(highlightbackground=self.color_border)
        self.search_user_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=2)
        self.search_user_entry.bind('<KeyRelease>', lambda e: self.load_users())

        btn_add = tk.Button(search_f, text="➕ Thêm nhân viên", bg=self.color_success, fg="white", font=("Segoe UI", 8, "bold"),
                            command=lambda: self.open_user_popup(edit_mode=False), bd=0, padx=12, pady=5, cursor="hand2")
        btn_add.pack(side="right", padx=3)
        btn_add.bind("<Enter>", lambda e: btn_add.config(bg="#218c53"))
        btn_add.bind("<Leave>", lambda e: btn_add.config(bg=self.color_success))

        btn_edit = tk.Button(search_f, text="✏️ Sửa nhân viên", bg=self.color_warning, fg="white", font=("Segoe UI", 8, "bold"),
                             command=lambda: self.open_user_popup(edit_mode=True), bd=0, padx=12, pady=5, cursor="hand2")
        btn_edit.pack(side="right", padx=3)
        btn_edit.bind("<Enter>", lambda e: btn_edit.config(bg="#d35400"))
        btn_edit.bind("<Leave>", lambda e: btn_edit.config(bg=self.color_warning))

        btn_refresh = tk.Button(search_f, text="🔄 Làm mới bảng", bg="#34495e", fg="white", font=("Segoe UI", 8, "bold"),
                                command=self.refresh_users, bd=0, padx=12, pady=5, cursor="hand2")
        btn_refresh.pack(side="right", padx=3)
        btn_refresh.bind("<Enter>", lambda e: btn_refresh.config(bg="#2c3e50"))
        btn_refresh.bind("<Leave>", lambda e: btn_refresh.config(bg="#34495e"))

        btn_delete = tk.Button(search_f, text="🗑️ Xóa tài khoản chọn", bg=self.color_danger, fg="white", font=("Segoe UI", 8, "bold"),
                               command=self.delete_user, bd=0, padx=12, pady=5, cursor="hand2")
        btn_delete.pack(side="right", padx=3)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#c0392b"))
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg=self.color_danger))

        tree_f = tk.Frame(tab_nv, bg="#22242b")
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "U", "N", "P", "R")
        self.tree1 = ttk.Treeview(tree_f, columns=cols, show="headings", height=5, selectmode="extended")

        heads = ["STT", "TÊN ĐĂNG NHẬP", "HỌ VÀ TÊN", "SỐ ĐIỆN THOẠI", "VAI TRÒ"]
        for c, h in zip(cols, heads):
            self.tree1.heading(c, text=h)
            w = 50 if c == "STT" else 150
            if c == "N": w = 220
            self.tree1.column(c, width=w, anchor="center" if c != "N" else "w")

        self.tree1.pack(side="left", fill="both", expand=True)
        sb1 = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=sb1.set)
        sb1.pack(side="right", fill="y")
        self.tree1.bind("<Double-1>", lambda e: self.open_user_popup(edit_mode=True))

        tab_ls = tk.Frame(nb, bg="#22242b")
        nb.add(tab_ls, text=" 📜 Nhật ký hệ thống ")

        tree_f2 = tk.Frame(tab_ls, bg="#22242b")
        tree_f2.pack(fill="both", expand=True, padx=10, pady=10)

        cols2 = ("STT", "U", "T", "A")
        self.tree2 = ttk.Treeview(tree_f2, columns=cols2, show="headings", height=5)
        heads2 = ["STT", "TÀI KHOẢN", "THỜI GIAN ĐĂNG NHẬP", "TRẠNG THÁI"]
        for c, h in zip(cols2, heads2):
            self.tree2.heading(c, text=h)
            w = 50 if c == "STT" else 200
            self.tree2.column(c, width=w, anchor="center")

        self.tree2.pack(side="left", fill="both", expand=True)
        sb2 = ttk.Scrollbar(tree_f2, orient="vertical", command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y")

    def on_user_select(self, event):
        sel = self.tree1.selection()
        if not sel: return

        if len(sel) > 1:
            self.clear_form()
            return

        vals = self.tree1.item(sel[0], "values")
        username = vals[1]

        res = self.app_manager.db.query("SELECT password FROM users WHERE username=?", (username,))
        password = res[0][0] if res else ""

        self.ents["Username"].config(state="normal")
        self.ents["Username"].delete(0, tk.END)
        self.ents["Username"].insert(0, username)
        self.ents["Username"].config(state="disabled", disabledbackground="#1c1d22", disabledforeground="#a4b0be")

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
        sel = self.tree1.selection()
        if len(sel) > 1:
            messagebox.showwarning("Cảnh báo hiệu chỉnh",
                                   "Bạn chỉ được phép chọn duy nhất 1 tài khoản nhân viên để tiến hành chỉnh sửa!")
            return

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
                    messagebox.showerror("Lỗi",
                                         f"Tên đăng nhập '{username}' đã tồn tại! Vui lòng chọn tên đăng nhập khác.")
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
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn nhân viên cần xóa trong danh sách bảng!")
            return

        count = len(sel)

        if count == 1:
            vals = self.tree1.item(sel[0], "values")
            username = vals[1]
            fullname = vals[2]

            if username.lower() in ["admin", "a"]:
                messagebox.showerror("Bảo mật hệ thống",
                                     "Không được phép xóa tài khoản quản trị viên tối cao (Admin/a)!")
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

        else:
            has_admin = False
            for item in sel:
                vals = self.tree1.item(item, "values")
                if vals[1].lower() in ["admin", "a"]:
                    has_admin = True
                    break
            if has_admin:
                messagebox.showerror("Lỗi bảo mật",
                                     "Danh sách chọn có chứa tài khoản quản trị viên tối cao (Admin/a). Không được phép xóa hàng loạt các tài khoản này!")
                return

            if messagebox.askyesno("Xác nhận xóa hàng loạt",
                                   f"Bạn có chắc chắn muốn xóa vĩnh viễn cả {count} tài khoản nhân viên đã chọn?"):
                try:
                    for item in sel:
                        vals = self.tree1.item(item, "values")
                        self.app_manager.db.query("DELETE FROM users WHERE username=?", (vals[1],))
                    messagebox.showinfo("Thành công", f"Đã xóa thành công {count} tài khoản nhân viên khỏi hệ thống!")
                    self.clear_form()
                    self.load_users()
                except Exception as e:
                    messagebox.showerror("Lỗi hệ thống", f"Không thể thực hiện xóa hàng loạt: {e}")

    def refresh_users(self):
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

        term = f"%{self.search_user_entry.get().lower().strip()}%"
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

    def open_user_popup(self, edit_mode=False):
        u_val, p_val, n_val, s_val, r_val = "", "", "", "", "Nhân viên"

        if edit_mode:
            sel = self.tree1.selection()
            if not sel:
                messagebox.showwarning("Thông báo", "Vui lòng chọn 1 tài khoản nhân viên trên bảng để chỉnh sửa!")
                return
            if len(sel) > 1:
                messagebox.showwarning("Thông báo",
                                       "Bạn chỉ được phép chọn duy nhất 1 tài khoản nhân viên để chỉnh sửa!")
                return

            vals = self.tree1.item(sel[0], "values")
            u_val = vals[1]
            n_val = vals[2]
            s_val = vals[3]
            r_val = vals[4]

            res = self.app_manager.db.query("SELECT password FROM users WHERE username=?", (u_val,))
            p_val = res[0][0] if res else ""

        pop = tk.Toplevel(self.master)
        pop.title("Cập Nhật Nhân Sự" if edit_mode else "Thêm Nhân Viên Mới")
        pop.geometry("450x450")
        pop.configure(bg="#22242b")
        pop.resizable(False, False)
        pop.grab_set()

        accent_bar = tk.Frame(pop, bg=self.color_teal, height=4)
        accent_bar.pack(fill="x", side="top")

        title_text = "✏️ CẬP NHẬT NHÂN VIÊN" if edit_mode else "➕ THÊM NHÂN VIÊN MỚI"
        tk.Label(pop, text=title_text, font=("Segoe UI", 14, "bold"), bg="#22242b", fg=self.color_teal).pack(
            pady=(20, 15))

        form = tk.Frame(pop, bg="#22242b", padx=30)
        form.pack(fill="both", expand=True)

        fields = [
            ("Tên đăng nhập:", "Username", u_val, not edit_mode),
            ("Mật khẩu:", "Password", p_val, True),
            ("Họ và tên:", "Fullname", n_val, True),
            ("Số điện thoại:", "Phone", s_val, True),
            ("Vai trò:", "Role", r_val, True)
        ]

        popup_ents = {}
        for i, (label_text, key, default_val, editable) in enumerate(fields):
            tk.Label(form, text=label_text, font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").grid(row=i,
                                                                                                           column=0,
                                                                                                           sticky="w",
                                                                                                           pady=8)

            if key == "Role":
                e = ttk.Combobox(form, values=["Admin", "Nhân viên"], state="readonly")
                e.set(default_val)
            else:
                e = tk.Entry(form, font=("Segoe UI", 10), bg=self.color_dark, fg="white", insertbackground="#1abc9c",
                             selectbackground=self.color_dark, selectforeground="white", exportselection=0, bd=1,
                             relief="solid")
                e.config(highlightbackground=self.color_border)
                e.insert(0, default_val)
                if not editable:
                    e.config(state="disabled", disabledbackground="#1c1d22", disabledforeground="#a4b0be")

            e.grid(row=i, column=1, sticky="ew", padx=(15, 0), pady=8, ipady=2)
            popup_ents[key] = e

        form.columnconfigure(1, weight=1)

        def save_changes():
            u = popup_ents["Username"].get().strip()
            p = popup_ents["Password"].get().strip()
            n = popup_ents["Fullname"].get().strip()
            s = popup_ents["Phone"].get().strip()
            r = popup_ents["Role"].get()

            if not u or not p or not n:
                messagebox.showerror("Lỗi nhập liệu", "Vui lòng điền đầy đủ Tên đăng nhập, Mật khẩu và Họ tên!")
                return

            try:
                if edit_mode:
                    self.app_manager.db.query(
                        "UPDATE users SET password=?, fullname=?, phone=?, role=? WHERE username=?",
                        (p, n, s, r, u)
                    )
                    messagebox.showinfo("Thành công", f"Đã cập nhật thông tin nhân viên '{n}' thành công!")
                else:
                    exists = self.app_manager.db.query("SELECT username FROM users WHERE username=?", (u,))
                    if exists:
                        messagebox.showerror("Lỗi",
                                             f"Tên đăng nhập '{u}' đã tồn tại! Vui lòng chọn tên đăng nhập khác.")
                        return

                    self.app_manager.db.query(
                        "INSERT INTO users (username, password, fullname, phone, role) VALUES (?, ?, ?, ?, ?)",
                        (u, p, n, s, r)
                    )
                    messagebox.showinfo("Thành công", f"Đã thêm mới nhân viên '{n}' thành công!")

                pop.destroy()
                self.load_users()
            except Exception as ex:
                messagebox.showerror("Lỗi hệ thống", f"Không thể lưu thông tin nhân viên: {str(ex)}")

        btn_container = tk.Frame(pop, bg="#22242b", pady=15)
        btn_container.pack(fill="x", side="bottom")

        btn_save = tk.Button(btn_container, text="💾 XÁC NHẬN", command=save_changes,
                             bg=self.color_success, fg="white", font=("Segoe UI", 10, "bold"),
                             bd=0, height=2, width=15, cursor="hand2")
        btn_save.pack(side="left", padx=(50, 10), expand=True)

        btn_cancel = tk.Button(btn_container, text="❌ HỦY BỎ", command=pop.destroy,
                               bg="#34495e", fg="white", font=("Segoe UI", 10, "bold"),
                               bd=0, height=2, width=15, cursor="hand2")
        btn_cancel.pack(side="right", padx=(10, 50), expand=True)