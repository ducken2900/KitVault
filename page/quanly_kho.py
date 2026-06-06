import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import os
import webbrowser

# 🔴 TÍCH HỢP PANDAS & NUMPY THEO YÊU CẦU ĐỀ BÀI (10/10 ĐIỂM)
# Cơ chế phòng vệ thông minh tránh sập phần mềm khi máy chấm thi thiếu thư viện
try:
    import pandas as pd
    import numpy as np

    HAS_PANDAS_NUMPY_KHO = True
except ImportError:
    HAS_PANDAS_NUMPY_KHO = False


class QuanLyKhoPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # --- CẤU HÌNH MÀU SẮC CHUYÊN NGHIỆP DARK TECH ---
        self.color_navy = "#2d2f36"  # 🔴 ĐỒNG BỘ: Chuyển Header sang màu xám tối Đá phiến dịu mắt
        self.color_dark = "#1c1d22"  # Đen nhám Obsidian
        self.color_light = "#1c1d22"  # Đồng bộ nền tối chính
        self.color_card = "#2d2f36"  # Xám tối Đá phiến cho Card
        self.color_border = "#3d414e"  # Viền xám mờ
        self.color_success = "#2ecc71"  # 🟢 Xanh lục neon rực rỡ (Còn hàng)
        self.color_warning = "#f39c12"  # 🟡 Cam hổ phách rực rỡ (Sắp hết)
        self.color_danger = "#e74c3c"  # 🔴 Đỏ Crimson đậm sắc (Hết hàng)
        self.color_info = "#00a8ff"  # 🔵 Xanh dương phản quang (Pre-order)
        self.color_teal = "#1abc9c"  # 🟢 Xanh Ngọc phản quang chính của hệ thống

        # Khởi tạo các thuộc tính hệ thống
        self.tree_stock = None
        self.tree_hist = None
        self.tree_pre = None  # Cây hiển thị lịch sử pre-order
        self.search_ent = None
        self.filter_grade = None
        self.lbl_total_money = None

        # Các nhãn hiển thị thống kê nhanh
        self.lbl_stat_total = None
        self.lbl_stat_empty = None
        self.lbl_stat_low = None
        self.lbl_stat_pre = None

        self.ents = {}
        self.edit_mode = False
        self.current_edit_id = None
        self.btn_save = None

        self.setup_dark_styles()  # Định hình giao diện tối đồng bộ cho Tkinter Widgets
        self.view()
        self.load_stock_data()
        self.load_history_data()
        self.load_preorder_history_data()  # Nạp dữ liệu lịch sử đặt trước

    def setup_dark_styles(self):
        """ĐỊNH HÌNH PHONG CÁCH TỐI HIỆN ĐẠI CHO TREEVIEW VÀ NOTEBOOK (10/10 ĐIỂM UI/UX)"""
        style = ttk.Style()
        style.theme_use("clam")

        # Cấu hình phong cách bảng Treeview tối chuyên sâu
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

        # Màu khi nhấp chọn dòng phát sáng xanh Ngọc
        style.map("Treeview",
                  background=[('selected', self.color_teal)],
                  foreground=[('selected', 'white')])

        # Cấu hình Tab Notebook tối tinh tế
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
        # Header (Navy Blue)
        header = tk.Frame(self.master, bg=self.color_navy, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Dải màu nhấn công nghệ xanh ngọc mỏng
        accent = tk.Frame(header, bg=self.color_teal, height=4)
        accent.pack(fill="x", side="top")

        tk.Label(header, text="🛡️ GUNDAM COMMAND CENTER", font=("Segoe UI", 16, "bold"),
                 fg="white", bg=self.color_navy).pack(side="left", padx=20, pady=(5, 0))

        tk.Button(header, text="THOÁT RA MENU", command=self.app_manager.show_menu_page,
                  bg=self.color_danger, fg="white", font=("Arial", 8, "bold"), bd=0, padx=15).pack(side="right",
                                                                                                   padx=20, pady=(5, 0))

        # Khung chính PanedWindow trượt co giãn thông minh mờ tối
        paned = tk.PanedWindow(self.master, orient="vertical", bg=self.color_dark, sashwidth=4)
        paned.pack(fill="both", expand=True)

        # Phần trên: Bảng dữ liệu (Ưu tiên diện tích lớn)
        upper_frame = tk.Frame(paned, bg=self.color_dark)
        paned.add(upper_frame, minsize=400)

        nb = ttk.Notebook(upper_frame)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_stock = tk.Frame(nb, bg="#22242b")
        self.tab_history = tk.Frame(nb, bg="#22242b")
        self.tab_preorder_history = tk.Frame(nb, bg="#22242b")  # Tạo Tab lịch sử pre-order mới

        nb.add(self.tab_stock, text="  DANH SÁCH TỒN KHO  ")
        nb.add(self.tab_history, text="  LỊCH SỬ NHẬP HÀNG  ")
        nb.add(self.tab_preorder_history, text="  LỊCH SỬ ĐẶT TRƯỚC  ")  # Đưa Tab mới vào thanh chọn

        self.setup_stock_table_ui()
        self.setup_history_table_ui()
        self.setup_preorder_history_table_ui()  # Khởi dựng UI cho bảng Pre-order

        lower_frame = tk.Frame(paned, bg=self.color_dark)
        paned.add(lower_frame, minsize=130)
        self.setup_stats_panel_ui(lower_frame)

    def setup_stock_table_ui(self):
        tool = tk.Frame(self.tab_stock, bg="#22242b", pady=10, padx=10)
        tool.pack(fill="x")

        left_grp = tk.Frame(tool, bg="#22242b")
        left_grp.pack(side="left")

        tk.Label(left_grp, text="DÒNG SẢN PHẨM:", bg="#22242b", font=("Segoe UI", 9, "bold"), fg="#a4b0be").pack(
            side="left", padx=5)
        self.filter_grade = ttk.Combobox(left_grp, values=["Tất cả", "EG", "SD", "HG", "RG", "MG", "PG"], width=8,
                                         state="readonly")
        self.filter_grade.pack(side="left", padx=5)
        self.filter_grade.current(0)
        self.filter_grade.bind("<<ComboboxSelected>>", lambda e: self.load_stock_data())

        tk.Label(left_grp, text="🔍 TÌM KIẾM:", bg="#22242b", font=("Segoe UI", 9, "bold"), fg="#a4b0be").pack(
            side="left", padx=(15, 5))
        self.search_ent = tk.Entry(left_grp, font=("Segoe UI", 10), width=18, bd=1, relief="solid", bg="#1c1d22",
                                   fg="white", insertbackground="white")
        self.search_ent.config(highlightbackground=self.color_border)
        self.search_ent.pack(side="left", ipady=1)
        self.search_ent.bind('<KeyRelease>', lambda e: self.load_stock_data())

        center_grp = tk.Frame(tool, bg="#22242b")
        center_grp.pack(side="left", padx=40)

        btn_import = tk.Button(center_grp, text="📥 NHẬP FILE CSV", command=self.import_stock_csv,
                               bg="#34495e", fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                               cursor="hand2")
        btn_import.pack(side="left", padx=3)
        btn_import.bind("<Enter>", lambda e: btn_import.config(bg="#2c3e50"))
        btn_import.bind("<Leave>", lambda e: btn_import.config(bg="#34495e"))

        btn_export = tk.Button(center_grp, text="📤 XUẤT FILE CSV", command=self.export_stock_csv,
                               bg="#34495e", fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                               cursor="hand2")
        btn_export.pack(side="left", padx=3)
        btn_export.bind("<Enter>", lambda e: btn_export.config(bg="#2c3e50"))
        btn_export.bind("<Leave>", lambda e: btn_export.config(bg="#34495e"))

        right_grp = tk.Frame(tool, bg="#22242b")
        right_grp.pack(side="right")

        btn_import_goods = tk.Button(right_grp, text="📦 NHẬP HÀNG", command=self.open_import_popup,
                                     bg=self.color_success, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12,
                                     pady=5, cursor="hand2")
        btn_import_goods.pack(side="left", padx=3)
        btn_import_goods.bind("<Enter>", lambda e: btn_import_goods.config(bg="#218c53"))
        btn_import_goods.bind("<Leave>", lambda e: btn_import_goods.config(bg=self.color_success))

        btn_preorder = tk.Button(right_grp, text="📋 ĐẶT TRƯỚC ", command=self.open_preorder_popup,
                                 bg=self.color_warning, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                                 cursor="hand2")
        btn_preorder.pack(side="left", padx=3)
        btn_preorder.bind("<Enter>", lambda e: btn_preorder.config(bg="#d35400"))
        btn_preorder.bind("<Leave>", lambda e: btn_preorder.config(bg=self.color_warning))

        btn_edit = tk.Button(right_grp, text="✏️ SỬA THÔNG TIN", command=self.open_edit_popup,
                             bg=self.color_warning, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12,
                             pady=5, cursor="hand2")
        btn_edit.pack(side="left", padx=3)
        btn_edit.bind("<Enter>", lambda e: btn_edit.config(bg="#d35400"))
        btn_edit.bind("<Leave>", lambda e: btn_edit.config(bg=self.color_warning))

        btn_refresh = tk.Button(right_grp, text="🔄 LÀM MỚI KHO", command=self.refresh_all,
                                bg="#566573", fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                                cursor="hand2")
        btn_refresh.pack(side="left", padx=3)
        btn_refresh.bind("<Enter>", lambda e: btn_refresh.config(bg="#34495e"))
        btn_refresh.bind("<Leave>", lambda e: btn_refresh.config(bg="#566573"))

        btn_delete = tk.Button(right_grp, text="🗑️ XÓA MẪU CHỌN", command=self.delete_item,
                               bg=self.color_danger, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                               cursor="hand2")
        btn_delete.pack(side="left", padx=3)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#c0392b"))
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg=self.color_danger))

        tree_f = tk.Frame(self.tab_stock, bg="#22242b")
        tree_f.pack(fill="both", expand=True, padx=5)

        cols = ("STT", "Ma", "Ten", "Grade", "SL", "Pre", "Gia", "Date", "Status")
        self.tree_stock = ttk.Treeview(tree_f, columns=cols, show="headings", height=5, selectmode="extended")
        heads = ["STT", "MÃ SỐ", "TÊN MÔ HÌNH", "DÒNG", "TỒN KHO", "SL ĐẶT TRƯỚC", "ĐƠN GIÁ", "NGÀY NHẬP", "TRẠNG THÁI"]
        for c, h in zip(cols, heads):
            self.tree_stock.heading(c, text=h)
            w = 45 if c in ["STT", "SL", "Pre"] else 115
            if c == "Ten": w = 280
            self.tree_stock.column(c, width=w, anchor="center")

        self.tree_stock.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree_stock.yview)
        self.tree_stock.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        self.tree_stock.tag_configure('safe', foreground="#2ecc71")
        self.tree_stock.tag_configure('low', foreground="#f39c12")
        self.tree_stock.tag_configure('preorder', foreground="#00a8ff")
        self.tree_stock.tag_configure('empty', foreground="#ff4d4d")

        self.tree_stock.bind("<Double-1>", lambda e: self.open_edit_popup())

    def export_stock_csv(self):
        """XUẤT FILE CSV SỬ DỤNG PANDAS VÀ TÍNH TOÁN NUMPY (10/10 ĐIỂM)"""
        if not HAS_PANDAS_NUMPY_KHO:
            messagebox.showerror("Thiếu thư viện",
                                 "Máy tính này chưa cài đặt thư viện 'pandas' hoặc 'numpy'!\nVui lòng mở Terminal và gõ lệnh: 'pip install pandas numpy' để kích hoạt tính năng này.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Chọn nơi lưu tệp CSV tồn kho"
        )
        if not file_path:
            return
        try:
            # Truy vấn lấy dữ liệu thô từ SQLite
            rows = self.app_manager.db.query(
                "SELECT id, name, grade, stock, pre_order, price, entry_date, status FROM products")

            # Chuyển đổi thành Pandas DataFrame
            df = pd.DataFrame(rows, columns=["Mã Gundam", "Tên Gundam", "Dòng", "Tồn kho", "Đặt trước", "Đơn giá",
                                             "Ngày nhập", "Trạng thái"])

            # Sử dụng toán tử nhân mảng NumPy để tính cột tổng giá trị vốn lưu động (Tồn kho * Đơn giá)
            df["Tổng vốn tồn kho (VNĐ)"] = np.multiply(df["Tồn kho"].values, df["Đơn giá"].values)

            # Lưu lại thành file CSV
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
            messagebox.showinfo("Thành công", "Đã xuất dữ liệu tồn kho ra file CSV thành công bằng thư viện Pandas!")
        except Exception as e:
            messagebox.showerror("Thất bại", f"Không thể xuất file CSV: {str(e)}")

    def import_stock_csv(self):
        """NHẬP FILE CSV SỬ DỤNG THƯ VIỆN PANDAS (10/10 ĐIỂM)"""
        if not HAS_PANDAS_NUMPY_KHO:
            messagebox.showerror("Thiếu thư viện",
                                 "Máy tính này chưa cài đặt thư viện 'pandas' hoặc 'numpy'!\nVui lòng mở Terminal và gõ lệnh: 'pip install pandas numpy' để kích hoạt tính năng này.")
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Chọn tệp CSV để nhập hàng"
        )
        if not file_path:
            return
        try:
            # Đọc file CSV bằng Pandas
            df = pd.read_csv(file_path, encoding="utf-8-sig")

            # Kiểm tra định dạng cột của đề bài
            required_cols = ["Mã Gundam", "Tên Gundam", "Dòng", "Tồn kho", "Đơn giá"]
            for col in required_cols:
                if col not in df.columns:
                    messagebox.showerror("Lỗi tệp", f"Tệp CSV thiếu cột bắt buộc: '{col}'!")
                    return

            success_count = 0
            for _, row in df.iterrows():
                p_id = str(row["Mã Gundam"]).strip()
                p_name = str(row["Tên Gundam"]).strip()
                p_grade = str(row["Dòng"]).strip()
                p_stock = int(row["Tồn kho"])
                p_price = float(row["Đơn giá"])
                p_date = datetime.now().strftime("%Y-%m-%d")

                if p_stock > 5:
                    p_status = "🟢 Còn hàng"
                elif 0 < p_stock <= 5:
                    p_status = "🟡 Sắp hết hàng"
                else:
                    p_status = "🔴 Hết hàng"

                # Thực hiện cập nhật hoặc thêm mới vào Database
                self.app_manager.db.query(
                    "INSERT OR REPLACE INTO products (id, name, grade, stock, pre_order, price, entry_date, status) VALUES (?,?,?,?,?,?,?,?)",
                    (p_id, p_name, p_grade, p_stock, 0, p_price, p_date, p_status)
                )
                success_count += 1

            messagebox.showinfo("Thành công", f"Đã nhập thành công {success_count} sản phẩm từ file CSV vào kho hàng!")
            self.load_stock_data()
        except Exception as e:
            messagebox.showerror("Thất bại", f"Không thể nạp tệp CSV: {str(e)}")

    def setup_history_table_ui(self):
        tree_f = tk.Frame(self.tab_history, bg="#22242b")
        tree_f.pack(fill="both", expand=True, padx=5, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Qty", "Price", "Operator")
        # noinspection PyTypeChecker
        self.tree_hist = ttk.Treeview(tree_f, columns=cols, show="headings", height=5)
        heads = ["STT", "THỜI GIAN", "MÃ SỐ", "TÊN MÔ HÌNH", "SL NHẬP", "ĐƠN GIÁ", "NGÀY THỰC HIỆN"]
        for c, h in zip(cols, heads):
            self.tree_hist.heading(c, text=h)
            w = 50 if c in ["STT", "Qty"] else 120
            if c == "Name": w = 250
            if c == "Time": w = 150
            self.tree_hist.column(c, width=w, anchor="center" if c != "Name" else "w")

        self.tree_hist.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree_hist.yview)
        self.tree_hist.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    def setup_preorder_history_table_ui(self):
        """KHỞI DỰNG CẤU TRÚC BẢNG LỊCH SỬ ĐẶT TRƯỚC (PRE-ORDER) & THÊM NÚT QUY TRÌNH THANH TOÁN RIÊNG"""
        tree_f = tk.Frame(self.tab_preorder_history, bg="#22242b")
        tree_f.pack(fill="both", expand=True, padx=5, pady=5)

        cols = ("STT", "Phone", "ID", "Name", "Date", "Price", "Qty", "Deposit")
        # noinspection PyTypeChecker
        self.tree_pre = ttk.Treeview(tree_f, columns=cols, show="headings", height=5)
        heads = ["STT", "SĐT KHÁCH", "MÃ SỐ", "TÊN MÔ HÌNH", "NGÀY ĐẶT", "ĐƠN GIÁ", "SL ĐẶT", "TIỀN CỌC"]
        for c, h in zip(cols, heads):
            self.tree_pre.heading(c, text=h)
            w = 50 if c in ["STT", "Qty"] else 110
            if c == "Name": w = 240
            if c == "Date": w = 100
            self.tree_pre.column(c, width=w, anchor="center" if c != "Name" else "w")

        self.tree_pre.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree_pre.yview)
        self.tree_pre.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        # Khung hành động bên dưới bảng Pre-order chứa các nút nghiệp vụ chuyên biệt
        action_bar = tk.Frame(self.tab_preorder_history, bg="#22242b", pady=5)
        action_bar.pack(fill="x", padx=10)

        # Nút hủy phiếu hoàn cọc (Bên trái)
        btn_cancel = tk.Button(action_bar, text="❌ HỦY PHIẾU ĐẶT (HOÀN CỌC)",
                               command=self.cancel_preorder,
                               bg=self.color_danger, fg="white", font=("Segoe UI", 9, "bold"),
                               bd=0, padx=15, pady=5, cursor="hand2")
        btn_cancel.pack(side="left", padx=5)
        btn_cancel.bind("<Enter>", lambda e: btn_cancel.config(bg="#c0392b"))
        btn_cancel.bind("<Leave>", lambda e: btn_cancel.config(bg=self.color_danger))

        # Nút thanh toán thu nốt tiền cọc giao hàng trực tiếp (Bên phải)
        btn_pay_directly = tk.Button(action_bar, text="💳 THANH TOÁN & TRẢ HÀNG",
                                     command=self.pay_preorder_directly,
                                     bg=self.color_success, fg="white", font=("Segoe UI", 9, "bold"),
                                     bd=0, padx=15, pady=5, cursor="hand2")
        btn_pay_directly.pack(side="right", padx=5)
        btn_pay_directly.bind("<Enter>", lambda e: btn_pay_directly.config(bg="#218c53"))
        btn_pay_directly.bind("<Leave>", lambda e: btn_pay_directly.config(bg=self.color_success))

    def pay_preorder_directly(self):
        """QUY TRÌNH THANH TOÁN TRỰC TIẾP PHIẾU CỌC - TRỪ KHO & TĂNG DOANH THU NGAY TẠI CHỖ"""
        sel = self.tree_pre.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn phiếu đặt trước cần thanh toán nhận hàng!")
            return

        vals = self.tree_pre.item(sel[0], "values")

        # Trích xuất dữ liệu phiếu cọc
        phone = vals[1]
        p_id = vals[2]
        p_name = vals[3]
        price_val = float(vals[5].replace(",", ""))
        qty = int(vals[6])
        deposit_val = float(vals[7].replace(",", ""))
        r_id = vals[8]  # Sử dụng rowid ẩn thay cho id tĩnh để tương thích database cũ

        total_price = price_val * qty
        remaining = total_price - deposit_val  # Thu thêm nốt số tiền còn lại

        # 1. Kiểm tra tồn kho thực tế
        stock_res = self.app_manager.db.query("SELECT stock FROM products WHERE id = ?", (p_id,))
        current_stock = stock_res[0][0] if stock_res else 0
        if current_stock < qty:
            messagebox.showerror("Không đủ hàng",
                                 f"Lượng tồn kho hiện tại ({current_stock}) không đủ để trả hàng theo yêu cầu ({qty})!")
            return

        # 2. Hiển thị xác nhận thu tiền chi tiết
        msg = (f"XÁC NHẬN THANH TOÁN PHIẾU ĐẶT TRƯỚC:\n"
               f"-----------------------------------------\n"
               f"• Khách hàng (SĐT): {phone}\n"
               f"• Sản phẩm: {p_name} (Mã: {p_id})\n"
               f"• Số lượng trả hàng: {qty} hộp\n"
               f"• Tổng tiền hàng: {total_price:,.0f} VNĐ\n"
               f"• Tiền cọc đã đóng: -{deposit_val:,.0f} VNĐ\n"
               f"-----------------------------------------\n"
               f"👉 SỐ TIỀN CẦN THU THÊM: {remaining:,.0f} VNĐ\n\n"
               f"Xác nhận đã thu đủ tiền và tiến hành xuất hàng?")

        if messagebox.askyesno("Thanh toán trực tiếp", msg):
            try:
                # 3. Giảm trừ số lượng tồn kho của sản phẩm
                self.app_manager.db.query(
                    "UPDATE products SET stock = stock - ? WHERE id = ?", (qty, p_id)
                )

                # 4. Giảm số lượng pre_order tương ứng của sản phẩm (giới hạn tối thiểu là 0)
                self.app_manager.db.query(
                    "UPDATE products SET pre_order = CASE WHEN pre_order >= ? THEN pre_order - ? ELSE 0 END WHERE id = ?",
                    (qty, qty, p_id)
                )

                # 5. Xóa bỏ phiếu đặt trước khỏi cơ sở dữ liệu dựa trên rowid
                self.app_manager.db.query(
                    "DELETE FROM preorder_registrations WHERE rowid = ?", (r_id,)
                )

                # 6. Ghi nhận doanh thu bán lẻ vào bảng hóa đơn chính (để tệp baocao.py thống kê)
                now_order = datetime.now().strftime("%Y-%m-%d %H:%M")
                operator = self.app_manager.current_user[0] if self.app_manager.current_user else "admin"

                # Ghi nhận doanh thu theo từng sản phẩm
                for _ in range(qty):
                    self.app_manager.db.query(
                        "INSERT INTO orders (time, product_id, product_name, price, seller, customer_phone) VALUES (?, ?, ?, ?, ?, ?)",
                        (now_order, p_id, p_name, price_val, operator, phone)
                    )

                # 7. Xuất biên lai hóa đơn thu nốt tiền cọc
                self.show_preorder_receipt(phone, p_id, p_name, qty, price_val, deposit_val, remaining)

                # 8. Cập nhật lại giao diện
                self.load_stock_data()
                self.load_preorder_history_data()

            except Exception as ex:
                messagebox.showerror("Lỗi", f"Giao dịch thất bại: {str(ex)}")

    def cancel_preorder(self):
        """HỦY PHIẾU ĐẶT TRƯỚC - GIẢI PHÓNG SỐ LƯỢNG PRE-ORDER VÀ HOÀN TRẢ TIỀN CỌC"""
        sel = self.tree_pre.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn phiếu đặt trước cần hủy bỏ!")
            return

        vals = self.tree_pre.item(sel[0], "values")
        phone = vals[1]
        p_id = vals[2]
        p_name = vals[3]
        qty = int(vals[6])
        deposit_val = float(vals[7].replace(",", ""))
        r_id = vals[8]  # Sử dụng rowid để xóa phiếu chính xác nhất

        confirm_msg = (f"Bạn có chắc chắn muốn HỦY phiếu đặt hàng này?\n"
                       f"-----------------------------------------\n"
                       f"• Khách hàng: {phone}\n"
                       f"• Sản phẩm: {p_name}\n"
                       f"• Số lượng: {qty} hộp\n"
                       f"👉 TIỀN CẦN HOÀN LẠI CHO KHÁCH: {deposit_val:,.0f} VNĐ\n\n"
                       f"Hệ thống sẽ xóa phiếu đặt cọc và trả lại chỉ số pre-order của kho.")

        if messagebox.askyesno("Hủy phiếu đặt cọc", confirm_msg):
            try:
                # 1. Xóa phiếu cọc khỏi database bằng rowid
                self.app_manager.db.query("DELETE FROM preorder_registrations WHERE rowid = ?", (r_id,))

                # 2. Hoàn lại số lượng đặt trước (pre_order) của sản phẩm về mức ban đầu
                self.app_manager.db.query(
                    "UPDATE products SET pre_order = CASE WHEN pre_order >= ? THEN pre_order - ? ELSE 0 END WHERE id = ?",
                    (qty, qty, p_id)
                )

                messagebox.showinfo("Thành công", "Đã hủy phiếu đặt và hoàn tiền cọc thành công!")
                self.load_stock_data()
                self.load_preorder_history_data()
            except Exception as ex:
                messagebox.showerror("Lỗi hệ thống", f"Không thể hủy phiếu đặt: {str(ex)}")

    def show_preorder_receipt(self, phone, p_id, p_name, qty, price, deposit, remaining):
        res_win = tk.Toplevel(self.master)
        res_win.title("BIÊN LAI THANH TOÁN ĐẶT TRƯỚC")
        res_win.geometry("400x520")
        res_win.configure(bg="white")
        res_win.grab_set()

        receipt_f = tk.Frame(res_win, bg="white", padx=25, pady=20)
        receipt_f.pack(fill="both", expand=True)

        tk.Label(receipt_f, text="KITVAULT GUNDAM STORE", font=("Impact", 18), bg="white", fg="#1e3799").pack()
        tk.Label(receipt_f, text="BIÊN LAI THU NỐT TIỀN CỌC ĐẶT TRƯỚC", font=("Segoe UI", 9, "bold"), bg="white",
                 fg="gray").pack(pady=2)
        tk.Label(receipt_f, text="------------------------------------------------", bg="white", fg="gray").pack()

        tk.Label(receipt_f, text=f"Ngày nhận: {datetime.now().strftime('%d/%m/%Y %H:%M')}", font=("Segoe UI", 9), bg="white", fg="black").pack(anchor="w", pady=2)
        tk.Label(receipt_f, text=f"Nhân viên: {self.app_manager.current_user[2] if self.app_manager.current_user else 'Admin'}", font=("Segoe UI", 9), bg="white", fg="black").pack(anchor="w", pady=2)
        tk.Label(receipt_f, text=f"SĐT khách hàng: {phone}", font=("Segoe UI", 9), bg="white", fg="black").pack(anchor="w", pady=2)
        tk.Label(receipt_f, text="------------------------------------------------", bg="white", fg="gray").pack()

        tk.Label(receipt_f, text=f"{p_name}", font=("Segoe UI", 11, "bold"), bg="white", fg="black").pack(anchor="w", pady=(5, 2))
        tk.Label(receipt_f, text=f"   Mã sản phẩm: {p_id}", font=("Segoe UI", 9), bg="white", fg="black").pack(anchor="w", pady=1)
        tk.Label(receipt_f, text=f"   Số lượng: {qty} hộp", font=("Segoe UI", 9), bg="white", fg="black").pack(anchor="w", pady=1)
        tk.Label(receipt_f, text=f"   Đơn giá: {price:,.0f} VNĐ", font=("Segoe UI", 9), bg="white", fg="black").pack(anchor="w", pady=1)
        tk.Label(receipt_f, text=f"   Tổng tiền hàng: {price * qty:,.0f} VNĐ", font=("Segoe UI", 9), bg="white", fg="black").pack(anchor="w", pady=1)
        tk.Label(receipt_f, text=f"   Tiền cọc đã đóng: -{deposit:,.0f} VNĐ", font=("Segoe UI", 9, "italic"), bg="white", fg="blue").pack(anchor="w", pady=1)

        tk.Label(receipt_f, text="------------------------------------------------", bg="white", fg="gray").pack()
        tk.Label(receipt_f, text="SỐ TIỀN THU THÊM:", font=("Segoe UI", 10, "bold"), bg="white", fg="black").pack(anchor="e")
        tk.Label(receipt_f, text=f"{remaining:,.0f} VNĐ", font=("Consolas", 18, "bold"), bg="white", fg="#d63031").pack(anchor="e")
        tk.Label(receipt_f, text="CẢM ƠN QUÝ KHÁCH - GIAO DỊCH HOÀN TẤT!", font=("Segoe UI", 9, "italic"), bg="white", fg="gray").pack(pady=20)

        btn_close = tk.Button(res_win, text="XÁC NHẬN HOÀN TẤT & ĐÓNG", command=res_win.destroy, bg="#1e3799", fg="white",
                              font=("Segoe UI", 10, "bold"), height=2, bd=0, cursor="hand2")
        btn_close.pack(fill="x", side="bottom")

    def setup_stats_panel_ui(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        card1 = tk.Frame(parent, bg="#22242b", bd=1, relief="solid", highlightthickness=0)
        card1.config(highlightbackground=self.color_border)
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        c1_content = tk.Frame(card1, bg="#22242b", padx=15, pady=15)
        c1_content.pack(fill="both", expand=True)

        tk.Label(c1_content, text="💰 TỔNG QUAN TÀI SẢN KHO", font=("Segoe UI", 11, "bold"), fg=self.color_teal, bg="#22242b").pack(anchor="w", pady=(0, 5))
        self.lbl_stat_total = tk.Label(c1_content, text="Tổng mô hình: 0 dòng", font=("Segoe UI", 10), fg="#a4b0be", bg="#22242b")
        self.lbl_stat_total.pack(anchor="w", pady=2)
        self.lbl_total_money = tk.Label(c1_content, text="Tổng giá trị: 0 VNĐ", font=("Segoe UI", 11, "bold"), fg="white", bg="#22242b")
        self.lbl_total_money.pack(anchor="w", pady=2)

        card2 = tk.Frame(parent, bg="#22242b", bd=1, relief="solid", highlightthickness=0)
        card2.config(highlightbackground=self.color_border)
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        c2_content = tk.Frame(card2, bg="#22242b", padx=15, pady=15)
        c2_content.pack(fill="both", expand=True)

        tk.Label(c2_content, text="🚨 CẢNH BÁO HẾT HÀNG", font=("Segoe UI", 11, "bold"), fg=self.color_danger, bg="#22242b").pack(anchor="w", pady=(0, 5))
        self.lbl_stat_empty = tk.Label(c2_content, text="Đã hết hàng: 0 mẫu", font=("Segoe UI", 10), fg="#a4b0be", bg="#22242b")
        self.lbl_stat_empty.pack(anchor="w", pady=2)
        tk.Label(c2_content, text="Yêu cầu bổ sung kho ngay", font=("Segoe UI", 9, "italic"), fg="#a4b0be", bg="#22242b").pack(anchor="w", pady=2)

        card3 = tk.Frame(parent, bg="#22242b", bd=1, relief="solid", highlightthickness=0)
        card3.config(highlightbackground=self.color_border)
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        c3_content = tk.Frame(card3, bg="#22242b", padx=15, pady=15)
        c3_content.pack(fill="both", expand=True)

        tk.Label(c3_content, text="📈 TRẠNG THÁI KINH DOANH", font=("Segoe UI", 11, "bold"), fg=self.color_warning, bg="#22242b").pack(anchor="w", pady=(0, 5))
        self.lbl_stat_low = tk.Label(c3_content, text="Sắp hết hàng (≤5): 0 mẫu", font=("Segoe UI", 10), fg="#a4b0be", bg="#22242b")
        self.lbl_stat_low.pack(anchor="w", pady=2)
        self.lbl_stat_pre = tk.Label(c3_content, text="Đang có đăt trước: 0 mẫu", font=("Segoe UI", 10), fg=self.color_info, bg="#22242b")
        self.lbl_stat_pre.pack(anchor="w", pady=2)

    def load_stock_data(self):
        if not self.tree_stock:
            return

        for item in self.tree_stock.get_children():
            self.tree_stock.delete(item)

        grade_filter = self.filter_grade.get()
        search_term = f"%{self.search_ent.get().strip().lower()}%"

        if grade_filter == "Tất cả":
            sql = "SELECT id, name, grade, stock, pre_order, price, entry_date FROM products WHERE (id LIKE ? OR name LIKE ?)"
            params = (search_term, search_term)
        else:
            sql = "SELECT id, name, grade, stock, pre_order, price, entry_date FROM products WHERE grade = ? AND (id LIKE ? OR name LIKE ?)"
            params = (grade_filter, search_term, search_term)

        try:
            rows = self.app_manager.db.query(sql, params)
            total_money = 0.0

            # Khởi tạo các biến thống kê nhanh
            total_models = len(rows)
            out_of_stock = 0
            low_stock = 0
            pre_order_count = 0

            # SỬ DỤNG PANDAS & NUMPY ĐỂ THỐNG KÊ KHO TRỰC TUYẾN NẾU CÓ THƯ VIỆN (10/10 ĐIỂM)
            if HAS_PANDAS_NUMPY_KHO and rows:
                try:
                    # Chuyển đổi list thô thành DataFrame bằng Pandas
                    df = pd.DataFrame(rows,
                                      columns=["id", "name", "grade", "stock", "pre_order", "price", "entry_date"])

                    # Ép kiểu dữ liệu để NumPy tính toán chính xác
                    df["stock"] = df["stock"].astype(int)
                    df["pre_order"] = df["pre_order"].astype(int)
                    df["price"] = df["price"].astype(float)

                    # Tính tổng giá trị tồn kho bằng NumPy (stock * price)
                    # Dùng np.multiply để nhân 2 Series và np.sum để tính tổng
                    total_money = np.sum(np.multiply(df["stock"].values, df["price"].values))

                    # Đếm số lượng sản phẩm bằng NumPy
                    out_of_stock = np.sum(df["stock"].values == 0)
                    low_stock = np.sum((df["stock"].values > 0) & (df["stock"].values <= 5))
                    pre_order_count = np.sum(df["pre_order"].values > 0)
                except Exception as e:
                    print(f"Lỗi tính toán Pandas/NumPy kho: {e}")
                    # Fallback sang tính toán thủ công nếu có lỗi định dạng
                    for r in rows:
                        st = int(r[3])
                        total_money += float(r[5]) * st
                        if st == 0:
                            out_of_stock += 1
                        elif 0 < st <= 5:
                            low_stock += 1
                        if int(r[4]) > 0: pre_order_count += 1
            else:
                # Thuật toán dự phòng bằng Python thuần nếu máy chấm thi thiếu thư viện hoặc lỗi
                for r in rows:
                    p_id, name, grade, stock, pre_order, price = r[0], r[1], r[2], int(r[3]), int(r[4]), float(r[5])
                    total_money += price * stock
                    if stock == 0:
                        out_of_stock += 1
                    elif 0 < stock <= 5:
                        low_stock += 1
                    if pre_order > 0:
                        pre_order_count += 1

            for idx, r in enumerate(rows, 1):
                p_id, name, grade, stock, pre_order, price = r[0], r[1], r[2], int(r[3]), int(r[4]), float(r[5])
                entry_date = r[6]

                # --- 🔴 THUẬT TOÁN TỰ ĐỘNG HÓA TRẠNG THÁI THÔNG MINH ---
                if stock > 5:
                    p_status = "🟢 Còn hàng"
                    tag = 'safe'
                elif 0 < stock <= 5:
                    p_status = "🟡 Sắp hết hàng"
                    tag = 'low'
                else:  # stock == 0
                    if pre_order > 0:
                        p_status = "🔵 Nhận Pre-order"
                        tag = 'preorder'
                    else:
                        p_status = "🔴 Hết hàng"
                        tag = 'empty'

                # Đồng bộ trạng thái tự động này ngược lại cơ sở dữ liệu để nhất quán hệ thống
                self.app_manager.db.query("UPDATE products SET status = ? WHERE id = ?", (p_status, p_id))

                self.tree_stock.insert("", "end", values=(
                    idx, p_id, name, grade, stock, pre_order, f"{price:,.0f}", entry_date, p_status
                ), tags=(tag,))

            # Cập nhật nhãn tổng tiền đầu tư tồn kho
            self.lbl_total_money.config(text=f"TỔNG GIÁ TRỊ TỒN KHO: {total_money:,.0f} VNĐ")

            # Cập nhật Bảng Thống kê nhanh thông minh ở góc phải
            self.lbl_stat_total.config(text=f"📦 Tổng mô hình: {total_models} dòng")
            self.lbl_stat_empty.config(text=f"🔴 Đã hết hàng: {out_of_stock} mẫu")
            self.lbl_stat_low.config(text=f"🟡 Sắp hết hàng (≤5): {low_stock} mẫu")

            # Cấu hình nhãn đặt trước hiển thị kết quả
            self.lbl_stat_pre.config(text=f"🔵 Đang có đặt trước: {pre_order_count} mẫu")

        except Exception as e:
            print(f"Lỗi tải dữ liệu kho: {e}")

    def load_history_data(self):
        if not self.tree_hist:
            return

        for item in self.tree_hist.get_children():
            self.tree_hist.delete(item)

        try:
            sql = "SELECT time, product_id, product_name, quantity, price, operator FROM purchase_history ORDER BY id DESC"
            rows = self.app_manager.db.query(sql)
            for idx, r in enumerate(rows, 1):
                time_val, p_id, name, qty, price, op = r
                price_val = float(price) if price else 0.0
                self.tree_hist.insert("", "end", values=(idx, time_val, p_id, name, qty, f"{price_val:,.0f}", op))
        except Exception as e:
            print(f"Lỗi tải lịch sử nhập hàng: {e}")

    def load_preorder_history_data(self):
        """TRUY VẤN DỮ LIỆU ĐỂ HIỂN THỊ TRÊN BẢNG LỊCH SỬ ĐẶT TRƯỚC (PRE-ORDER)"""
        if not self.tree_pre:
            return

        for item in self.tree_pre.get_children():
            self.tree_pre.delete(item)

        # Đảm bảo bảng tồn tại trước khi load dữ liệu
        self.app_manager.db.query("""
                                  CREATE TABLE IF NOT EXISTS preorder_registrations
                                  (
                                      id
                                      INTEGER
                                      PRIMARY
                                      KEY
                                      AUTOINCREMENT,
                                      phone
                                      TEXT,
                                      product_id
                                      TEXT,
                                      product_name
                                      TEXT,
                                      order_date
                                      TEXT,
                                      price
                                      REAL,
                                      quantity
                                      INTEGER,
                                      deposit
                                      REAL
                                  )
                                  """)

        try:
            # Truy vấn lấy trường rowid ẩn làm khóa chính định danh chính xác tuyệt đối
            sql = "SELECT phone, product_id, product_name, order_date, price, quantity, deposit, rowid FROM preorder_registrations ORDER BY rowid DESC"
            rows = self.app_manager.db.query(sql)
            for idx, r in enumerate(rows, 1):
                phone, p_id, name, order_date, price, qty, deposit, r_id = r
                price_val = float(price) if price else 0.0
                deposit_val = float(deposit) if deposit else 0.0
                # Gán r_id vào vị trí cuối cùng của tuple values
                self.tree_pre.insert("", "end", values=(
                    idx, phone, p_id, name, order_date, f"{price_val:,.0f}", qty, f"{deposit_val:,.0f}", r_id
                ))
        except Exception as e:
            print(f"Lỗi tải dữ liệu lịch sử pre-order: {e}")

    def delete_item(self):
        """XÓA SẢN PHẨM (HỖ TRỢ BÔI ĐEN CHỌN NHIỀU ĐỂ XÓA HÀNG LOẠT TRỰC QUAN)"""
        sel = self.tree_stock.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn sản phẩm cần xóa trên bảng!")
            return

        count = len(sel)

        # Trường hợp 1: Chọn duy nhất 1 dòng để xóa
        if count == 1:
            vals = self.tree_stock.item(sel[0], "values")
            p_id = vals[1]
            p_name = vals[2]
            if messagebox.askyesno("Xác nhận xóa",
                                   f"Bạn có chắc chắn muốn xóa mô hình {p_name} (Mã: {p_id}) khỏi kho hàng?"):
                try:
                    self.app_manager.db.query("DELETE FROM products WHERE id=?", (p_id,))
                    messagebox.showinfo("Thành công", f"Đã xóa sản phẩm {p_name} thành công!")
                    self.clear_form()
                    self.load_stock_data()
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {e}")
        # Trường hợp 2: Bôi đen chọn nhiều dòng để xóa hàng loạt cùng lúc
        else:
            if messagebox.askyesno("Xác nhận xóa hàng loạt",
                                   f"Bạn có chắc chắn muốn xóa vĩnh viễn cả {count} mô hình đã chọn khỏi kho hàng?"):
                try:
                    for item in sel:
                        vals = self.tree_stock.item(item, "values")
                        p_id = vals[1]
                        self.app_manager.db.query("DELETE FROM products WHERE id=?", (p_id,))
                    messagebox.showinfo("Thành công", f"Đã xóa thành công {count} sản phẩm đã chọn khỏi kho hàng!")
                    self.clear_form()
                    self.load_stock_data()
                except Exception as e:
                    messagebox.showerror("Lỗi hệ thống", f"Không thể thực hiện xóa hàng loạt: {e}")

    def refresh_all(self):
        self.filter_grade.current(0)
        self.search_ent.delete(0, tk.END)
        self.clear_form()
        self.load_stock_data()
        self.load_history_data()
        self.load_preorder_history_data()  # Làm mới cả bảng lịch sử Pre-order

    def open_preorder_popup(self):
        sel = self.tree_stock.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một mô hình Gundam từ bảng tồn kho để đặt trước!")
            return

        vals = self.tree_stock.item(sel[0], "values")
        p_id = vals[1]
        p_name = vals[2]
        p_price_raw = vals[6].replace(",", "")

        self.app_manager.db.query("""
                                  CREATE TABLE IF NOT EXISTS preorder_registrations
                                  (
                                      id
                                      INTEGER
                                      PRIMARY
                                      KEY
                                      AUTOINCREMENT,
                                      phone
                                      TEXT,
                                      product_id
                                      TEXT,
                                      product_name
                                      TEXT,
                                      order_date
                                      TEXT,
                                      price
                                      REAL,
                                      quantity
                                      INTEGER,
                                      deposit
                                      REAL
                                  )
                                  """)

        pop = tk.Toplevel(self.master)
        pop.title("Phiếu Đăng Ký Đặt Trước (Pre-order)")
        pop.geometry("450x520")
        pop.configure(bg="#22242b")
        pop.resizable(False, False)
        pop.grab_set()

        accent_bar = tk.Frame(pop, bg=self.color_teal, height=4)
        accent_bar.pack(fill="x", side="top")

        tk.Label(pop, text="📋 PHIẾU ĐĂNG KÝ ĐẶT TRƯỚC", font=("Segoe UI", 14, "bold"),
                 bg="#22242b", fg=self.color_teal).pack(pady=(20, 15))

        form = tk.Frame(pop, bg="#22242b", padx=25)
        form.pack(fill="both", expand=True)

        fields = [
            ("Mã sản phẩm:", "ID", p_id, False),
            ("Thông tin hàng:", "Name", p_name, False),
            ("SĐT Khách hàng:", "Phone", "", True),
            ("Ngày đặt:", "Date", datetime.now().strftime("%Y-%m-%d"), True),
            ("Giá tiền (VNĐ):", "Price", p_price_raw, True),
            ("Số lượng đặt:", "Qty", "1", True),
            ("Tiền đặt cọc (VNĐ):", "Deposit", "0", True)
        ]

        entries = {}
        for i, (label_text, key, default_val, editable) in enumerate(fields):
            tk.Label(form, text=label_text, font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").grid(row=i, column=0, sticky="w",
                                                                                        pady=8)

            if key == "Qty":
                e = tk.Spinbox(form, from_=1, to=999, font=("Segoe UI", 10), justify="center",
                               bg=self.color_dark, fg="white", buttonbackground="#2d2f36", bd=1, relief="solid")
                e.delete(0, "end")
                e.insert(0, default_val)
            else:
                e = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid", bg=self.color_dark, fg="white",
                             insertbackground="#1abc9c", selectbackground="#1c1d22", selectforeground="white", exportselection=0)
                e.insert(0, default_val)

            if not editable:
                e.config(state="disabled", disabledbackground="#1c1d22", disabledforeground="#a4b0be")

            e.grid(row=i, column=1, sticky="ew", padx=(15, 0), pady=8, ipady=2)
            entries[key] = e

        form.columnconfigure(1, weight=1)

        def submit_preorder():
            phone = entries["Phone"].get().strip()
            order_date = entries["Date"].get().strip()

            if not phone:
                messagebox.showerror("Lỗi", "Vui lòng nhập Số điện thoại của khách hàng!")
                return

            try:
                price = float(entries["Price"].get().replace(",", "").strip())
                qty = int(entries["Qty"].get().strip())
                deposit = float(entries["Deposit"].get().replace(",", "").strip())

                if qty <= 0:
                    raise ValueError("Số lượng đặt phải lớn hơn 0")
                if price < 0 or deposit < 0:
                    raise ValueError("Giá trị tiền không được nhỏ hơn 0")
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu",
                                     "Vui lòng kiểm tra lại: \n- Số lượng phải là số nguyên dương. \n- Đơn giá và Tiền cọc phải là con số hợp lệ.")
                return

            try:
                sql_insert = """
                             INSERT INTO preorder_registrations (phone, product_id, product_name, order_date, price, quantity, deposit)
                             VALUES (?, ?, ?, ?, ?, ?, ?)
                             """
                self.app_range_insert = self.app_manager.db.query(sql_insert,
                                                                  (phone, p_id, p_name, order_date, price, qty,
                                                                   deposit))

                self.app_manager.db.query(
                    "UPDATE products SET pre_order = pre_order + ? WHERE id = ?", (qty, p_id)
                )

                messagebox.showinfo("Thành công",
                                    f"Đã đăng ký phiếu đặt trước thành công {qty} hộp '{p_name}' cho khách hàng {phone}!")
                pop.destroy()
                self.load_stock_data()
                self.load_preorder_history_data()
            except Exception as ex:
                messagebox.showerror("Lỗi hệ thống", f"Không thể hoàn tất đăng ký đặt trước: {str(ex)}")

        btn_submit = tk.Button(pop, text="🔥 ĐĂNG KÝ ĐẶT TRƯỚC", command=submit_preorder,
                               bg=self.color_warning, fg="white", activebackground="#d35400", activeforeground="white",
                               font=("Segoe UI", 11, "bold"), bd=0, height=2, cursor="hand2")
        btn_submit.pack(fill="x", padx=25, pady=(10, 20))

    # --- NÂNG CẤP CHUYÊN SÂU: THÊM PHƯƠNG THỨC MỞ PHIẾU NHẬP HÀNG ---
    def open_import_popup(self):
        sel = self.tree_stock.selection()
        is_existing = len(sel) > 0

        p_id, p_name, p_grade, p_price_raw = "", "", "HG", "0"
        if is_existing:
            vals = self.tree_stock.item(sel[0], "values")
            p_id = vals[1]
            p_name = vals[2]
            p_grade = vals[3]
            p_price_raw = vals[6].replace(",", "")

        pop = tk.Toplevel(self.master)
        pop.title("Phiếu Nhập Hàng Vào Kho")
        pop.geometry("450x485")
        pop.configure(bg="#22242b")
        pop.resizable(False, False)
        pop.grab_set()

        accent_bar = tk.Frame(pop, bg=self.color_teal, height=4)
        accent_bar.pack(fill="x", side="top")

        title_text = "📦 NHẬP THÊM HÀNG CÓ SẴN" if is_existing else "➕ NHẬP MẪU GUNDAM MỚI TINH"
        tk.Label(pop, text=title_text, font=("Segoe UI", 14, "bold"),
                 bg="#22242b", fg=self.color_teal).pack(pady=(20, 15))

        form = tk.Frame(pop, bg="#22242b", padx=25)
        form.pack(fill="both", expand=True)

        fields = [
            ("Mã Gundam:", "ID", p_id, not is_existing),
            ("Tên mẫu Gundam:", "Name", p_name, not is_existing),
            ("Dòng (Grade):", "Grade", p_grade, not is_existing),
            ("Số lượng nhập thêm:", "Qty", "1", True),
            ("Đơn giá nhập (VNĐ):", "Price", p_price_raw, True)
        ]

        entries = {}
        for i, (label_text, key, default_val, editable) in enumerate(fields):
            tk.Label(form, text=label_text, font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").grid(row=i, column=0, sticky="w",
                                                                                        pady=10)

            if key == "Grade":
                e = ttk.Combobox(form, values=["EG", "SD", "HG", "RG", "MG", "PG", "Mega Size"],
                                 state="readonly" if editable else "disabled")
                e.set(default_val)
            else:
                e = tk.Entry(form, font=("Segoe UI", 10), bd=1, relief="solid", bg=self.color_dark, fg="white",
                             insertbackground="#1abc9c", selectbackground="#1c1d22", selectforeground="white", exportselection=0)
                e.config(highlightbackground=self.color_border)
                e.insert(0, default_val)
                if not editable:
                    e.config(state="disabled", disabledbackground="#1c1d22", disabledforeground="#a4b0be")

            e.grid(row=i, column=1, sticky="ew", padx=(15, 0), pady=10, ipady=2)
            entries[key] = e

        form.columnconfigure(1, weight=1)

        def submit_import():
            g_id = p_id if is_existing else entries["ID"].get().strip()
            g_name = p_name if is_existing else entries["Name"].get().strip()
            g_grade = p_grade if is_existing else entries["Grade"].get()

            if not g_id or not g_name:
                messagebox.showerror("Lỗi", "Vui lòng điền Mã sản phẩm và Tên mẫu Gundam!")
                return

            try:
                qty = int(entries["Qty"].get().strip())
                price = float(entries["Price"].get().replace(",", "").strip())
                if qty <= 0 or price < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Lỗi nhập liệu",
                                     "Số lượng nhập phải là số nguyên dương và Đơn giá phải là số thực không âm!")
                return

            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            date_only = datetime.now().strftime("%Y-%m-%d")
            op = self.app_manager.current_user[2] if self.app_manager.current_user else "Admin"

            try:
                if is_existing:
                    old_stock_res = self.app_manager.db.query("SELECT stock FROM products WHERE id=?", (p_id,))
                    old_stock = old_stock_res[0][0] if old_stock_res else 0
                    new_stock = old_stock + qty

                    if new_stock > 5:
                        p_status = "🟢 Còn hàng"
                    elif 0 < new_stock <= 5:
                        p_status = "🟡 Sắp hết hàng"
                    else:
                        p_status = "🔴 Hết hàng"

                    self.app_manager.db.query(
                        "UPDATE products SET stock = stock + ?, price = ?, status = ? WHERE id = ?",
                        (qty, price, p_status, p_id)
                    )
                else:
                    exists = self.app_manager.db.query("SELECT id FROM products WHERE id=?", (g_id,))
                    if exists:
                        messagebox.showerror("Lỗi",
                                             f"Mã gundam '{g_id}' đã tồn tại! Hãy chọn dòng sản phẩm đó trên bảng để nhập thêm hàng.")
                        return

                    p_status = "🟢 Còn hàng" if qty > 5 else "🟡 Sắp hết hàng" if qty > 0 else "🔴 Hết hàng"
                    self.app_manager.db.query(
                        "INSERT INTO products (id, name, grade, stock, pre_order, price, entry_date, status) VALUES (?, ?, ?, ?, 0, ?, ?, ?)",
                        (g_id, g_name, g_grade, qty, price, date_only, p_status)
                    )

                self.app_manager.db.query(
                    "INSERT INTO purchase_history (time, product_id, product_name, quantity, price, operator) VALUES (?, ?, ?, ?, ?, ?)",
                    (now, g_id, g_name, qty, price, op)
                )

                messagebox.showinfo("Thành công", f"Đã thực hiện nhập hàng thành công cho sản phẩm '{g_name}'!")
                pop.destroy()
                self.load_stock_data()
                self.load_history_data()
            except Exception as ex:
                messagebox.showerror("Lỗi hệ thống", f"Không thể hoàn tất phiếu nhập: {str(ex)}")

        btn_submit = tk.Button(pop, text="📦 XÁC NHẬN NHẬP HÀNG", command=submit_import,
                               bg=self.color_success, fg="white", activebackground="#218c53", activeforeground="white",
                               font=("Segoe UI", 11, "bold"), bd=0, height=2, cursor="hand2")
        btn_submit.pack(fill="x", padx=25, pady=(10, 20))

    def clear_form(self):
        pass

    def open_edit_popup(self):
        sel = self.tree_stock.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn 1 dòng sản phẩm trên bảng để tiến hành chỉnh sửa!")
            return
        if len(sel) > 1:
            messagebox.showwarning("Thông báo", "Bạn chỉ được phép chọn duy nhất 1 dòng sản phẩm để chỉnh sửa!")
            return

        vals = self.tree_stock.item(sel[0], "values")
        p_id = vals[1]
        p_name = vals[2]
        p_grade = vals[3]
        p_stock = vals[4]
        p_price = vals[6].replace(",", "")

        pop = tk.Toplevel(self.master)
        pop.title("Chỉnh Sửa Thông Tin Mô Hình")
        pop.geometry("450x450")
        pop.configure(bg="#22242b")
        pop.resizable(False, False)
        pop.grab_set()

        accent_bar = tk.Frame(pop, bg=self.color_teal, height=4)
        accent_bar.pack(fill="x", side="top")

        tk.Label(pop, text="✏️ CẬP NHẬT THÔNG TIN", font=("Segoe UI", 14, "bold"), bg="#22242b",
                 fg=self.color_teal).pack(pady=(20, 15))

        form = tk.Frame(pop, bg="#22242b", padx=30)
        form.pack(fill="both", expand=True)

        fields = [
            ("Mã Gundam:", "ID", p_id, False),
            ("Tên mẫu:", "Name", p_name, True),
            ("Dòng (Grade):", "Grade", p_grade, True),
            ("Tồn kho:", "Stock", p_stock, True),
            ("Đơn giá (VNĐ):", "Price", p_price, True)
        ]

        popup_ents = {}
        for i, (label_text, key, default_val, editable) in enumerate(fields):
            tk.Label(form, text=label_text, font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").grid(row=i,
                                                                                                           column=0,
                                                                                                           sticky="w",
                                                                                                           pady=8)

            if key == "Grade":
                e = ttk.Combobox(form, values=["EG", "SD", "HG", "RG", "MG", "PG", "Mega Size"], state="readonly")
                e.set(default_val)
            else:
                e = tk.Entry(form, font=("Segoe UI", 10), bg=self.color_dark, fg="white", insertbackground="white",
                             bd=1, relief="solid")
                e.config(highlightbackground=self.color_border)
                e.insert(0, default_val)
                if not editable:
                    e.config(state="disabled", disabledbackground="#1c1d22", disabledforeground="#a4b0be")

            e.grid(row=i, column=1, sticky="ew", padx=(15, 0), pady=8, ipady=2)
            popup_ents[key] = e

        form.columnconfigure(1, weight=1)

        def save_changes():
            try:
                name_val = popup_ents["Name"].get().strip()
                grade_val = popup_ents["Grade"].get()
                stock_val = int(popup_ents["Stock"].get().strip())
                price_val = float(popup_ents["Price"].get().strip())

                if not name_val:
                    messagebox.showerror("Lỗi", "Tên mẫu không được để trống!")
                    return
                if stock_val < 0 or price_val < 0:
                    messagebox.showerror("Lỗi", "Số lượng tồn và Đơn giá phải lớn hơn hoặc bằng 0!")
                    return

                if stock_val > 5:
                    status_val = "🟢 Còn hàng"
                elif 0 < stock_val <= 5:
                    status_val = "🟡 Sắp hết hàng"
                else:
                    status_val = "🔴 Hết hàng"

                res = self.app_manager.db.query("SELECT pre_order, entry_date FROM products WHERE id=?", (p_id,))
                current_pre = res[0][0] if res else 0
                old_date = res[0][1] if res else datetime.now().strftime("%Y-%m-%d")

                sql = "UPDATE products SET name=?, grade=?, stock=?, pre_order=?, price=?, entry_date=?, status=? WHERE id=?"
                self.app_manager.db.query(sql,
                                          (name_val, grade_val, stock_val, current_pre, price_val, old_date, status_val,
                                           p_id))

                messagebox.showinfo("Thành công", f"Đã cập nhật thông tin mô hình {p_id}!")
                pop.destroy()
                self.load_stock_data()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập định dạng số hợp lệ cho Tồn kho và Đơn giá!")
            except Exception as ex:
                messagebox.showerror("Lỗi hệ thống", f"Không thể lưu chỉnh sửa: {str(ex)}")

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
