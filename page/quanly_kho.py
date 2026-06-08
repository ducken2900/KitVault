import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime
import os

# Tích hợp bộ xử lý dữ liệu lớn phục vụ tính toán tài sản kho hàng
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

        # [THIẾT KẾ]: Bảng màu phẳng chủ đạo tối Dark-Theme của phân hệ Kho
        self.color_navy = "#2d2f36"
        self.color_dark = "#1c1d22"
        self.color_border = "#3d414e"
        self.color_success = "#2ecc71"  # Xanh lục (Đủ hàng)
        self.color_warning = "#f39c12"  # Màu cam (Sắp hết hàng)
        self.color_danger = "#e74c3c"  # Màu đỏ (Kho trống)
        self.color_info = "#00a8ff"  # Xanh neon (Đặt hàng pre-order)
        self.color_teal = "#1abc9c"  # Xanh Ngọc chính

        self.tree_stock = None
        self.tree_hist = None
        self.tree_pre = None
        self.search_ent = None
        self.filter_grade = None
        self.lbl_total_money = None

        self.setup_dark_styles()
        self.view()
        self.load_stock_data()
        self.load_history_data()
        self.load_preorder_history_data()

    def setup_dark_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#22242b", foreground="#f5f6fa",
                        fieldbackground="#22242b", rowheight=35, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#2d2f36",
                        foreground="white", borderwidth=1, bordercolor="#3d414e")
        style.map("Treeview", background=[('selected', self.color_teal)], foreground=[('selected', 'white')])

    def view(self):
        # Header phân hệ kho
        header = tk.Frame(self.master, bg=self.color_navy, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        accent = tk.Frame(header, bg=self.color_teal, height=4)
        accent.pack(fill="x", side="top")

        tk.Label(header, text="🛡️ GUNDAM COMMAND CENTER", font=("Segoe UI", 16, "bold"),
                 fg="white", bg=self.color_navy).pack(side="left", padx=20)

        tk.Button(header, text="THOÁT RA MENU", command=self.app_manager.show_menu_page,
                  bg=self.color_danger, fg="white", font=("Arial", 8, "bold"), bd=0, padx=15).pack(side="right",
                                                                                                   padx=20)

        # Thanh PanedWindow kéo giãn tỷ lệ giữa bảng và các hộp thống kê
        paned = tk.PanedWindow(self.master, orient="vertical", bg=self.color_dark, sashwidth=4)
        paned.pack(fill="both", expand=True)

        upper_frame = tk.Frame(paned, bg=self.color_dark)
        paned.add(upper_frame, minsize=400)

        # Khởi tạo 3 thẻ Tab chính bằng Notebook
        nb = ttk.Notebook(upper_frame)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_stock = tk.Frame(nb, bg="#22242b")
        self.tab_history = tk.Frame(nb, bg="#22242b")
        self.tab_preorder_history = tk.Frame(nb, bg="#22242b")

        nb.add(self.tab_stock, text="  DANH SÁCH TỒN KHO  ")
        nb.add(self.tab_history, text="  LỊCH SỬ NHẬP HÀNG  ")
        nb.add(self.tab_preorder_history, text="  LỊCH SỬ ĐẶT TRƯỚC  ")

        self.setup_stock_table_ui()
        self.setup_history_table_ui()
        self.setup_preorder_history_table_ui()

        lower_frame = tk.Frame(paned, bg=self.color_dark)
        paned.add(lower_frame, minsize=130)
        self.setup_stats_panel_ui(lower_frame)

    def setup_stock_table_ui(self):
        tool = tk.Frame(self.tab_stock, bg="#22242b", pady=10, padx=10)
        tool.pack(fill="x")

        left_grp = tk.Frame(tool, bg="#22242b")
        left_grp.pack(side="left")

        # Combobox lọc gundam theo dòng sản phẩm
        tk.Label(left_grp, text="DÒNG SẢN PHẨM:", bg="#22242b", font=("Segoe UI", 9, "bold"), fg="#a4b0be").pack(
            side="left", padx=5)
        self.filter_grade = ttk.Combobox(left_grp, values=["Tất cả", "EG", "SD", "HG", "RG", "MG", "PG"], width=8,
                                         state="readonly")
        self.filter_grade.pack(side="left", padx=5)
        self.filter_grade.current(0)
        self.filter_grade.bind("<<ComboboxSelected>>", lambda e: self.load_stock_data())

        # Ô tìm kiếm sản phẩm theo từ khóa
        tk.Label(left_grp, text="🔍 TÌM KIẾM:", bg="#22242b", font=("Segoe UI", 9, "bold"), fg="#a4b0be").pack(
            side="left", padx=(15, 5))
        self.search_ent = tk.Entry(left_grp, font=("Segoe UI", 10), width=18, bd=1, relief="solid", bg="#1c1d22",
                                   fg="white", insertbackground="white")
        self.search_ent.config(highlightbackground=self.color_border)
        self.search_ent.pack(side="left", ipady=1)
        self.search_ent.bind('<KeyRelease>', lambda e: self.load_stock_data())

        center_grp = tk.Frame(tool, bg="#22242b")
        center_grp.pack(side="left", padx=40)

        # Nút nạp/xuất bảng tính CSV bằng Pandas
        btn_import = tk.Button(center_grp, text="📥 NHẬP FILE CSV", command=self.import_stock_csv,
                               bg="#34495e", fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                               cursor="hand2")
        btn_import.pack(side="left", padx=3)

        btn_export = tk.Button(center_grp, text="📤 XUẤT FILE CSV", command=self.export_stock_csv,
                               bg="#34495e", fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                               cursor="hand2")
        btn_export.pack(side="left", padx=3)

        right_grp = tk.Frame(tool, bg="#22242b")
        right_grp.pack(side="right")

        btn_import_goods = tk.Button(right_grp, text="📦 NHẬP HÀNG", command=self.open_import_popup,
                                     bg=self.color_success, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12,
                                     pady=5, cursor="hand2")
        btn_import_goods.pack(side="left", padx=3)

        btn_preorder = tk.Button(right_grp, text="📋 ĐẶT TRƯỚC ", command=self.open_preorder_popup,
                                 bg=self.color_warning, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                                 cursor="hand2")
        btn_preorder.pack(side="left", padx=3)

        btn_edit = tk.Button(right_grp, text="✏️ SỬA THÔNG TIN", command=self.open_edit_popup,
                             bg=self.color_warning, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                             cursor="hand2")
        btn_edit.pack(side="left", padx=3)

        btn_delete = tk.Button(right_grp, text="🗑️ XÓA MẪU CHỌN", command=self.delete_item,
                               bg=self.color_danger, fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=12, pady=5,
                               cursor="hand2")
        btn_delete.pack(side="left", padx=3)

        # [THIẾT KẾ]: Bố cục bảng Treeview quản lý kho gundam trực quan
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

        # Phân loại màu trạng thái cho từng dòng sản phẩm
        self.tree_stock.tag_configure('safe', foreground="#2ecc71")
        self.tree_stock.tag_configure('low', foreground="#f39c12")
        self.tree_stock.tag_configure('preorder', foreground="#00a8ff")
        self.tree_stock.tag_configure('empty', foreground="#ff4d4d")

        self.tree_stock.bind("<Double-1>", lambda e: self.open_edit_popup())

    def export_stock_csv(self):
        """[TÍNH NĂNG]: Chuyển dữ liệu kho sang DataFrame Pandas và nhân mảng NumPy"""
        if not HAS_PANDAS_NUMPY_KHO:
            messagebox.showerror("Thiếu thư viện", "Vui lòng cài đặt thư viện Pandas & NumPy!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        try:
            rows = self.app_manager.db.query(
                "SELECT id, name, grade, stock, pre_order, price, entry_date, status FROM products")

            df = pd.DataFrame(rows, columns=["Mã Gundam", "Tên Gundam", "Dòng", "Tồn kho", "Đặt trước", "Đơn giá",
                                             "Ngày nhập", "Trạng thái"])

            # [CƠ CHẾ]: Tích hợp NumPy tính cột Tổng giá trị tồn kho của gundam
            df["Tổng vốn tồn kho (VNĐ)"] = np.multiply(df["Tồn kho"].values, df["Đơn giá"].values)

            df.to_csv(file_path, index=False, encoding="utf-8-sig")
            messagebox.showinfo("Thành công", "Đã xuất dữ liệu bằng Pandas & NumPy!")
        except Exception as e:
            messagebox.showerror("Thất bại", f"Không thể xuất file: {str(e)}")

    def import_stock_csv(self):
        """[TÍNH NĂNG]: Đọc file CSV bằng cấu trúc DataFrame Pandas"""
        if not HAS_PANDAS_NUMPY_KHO:
            messagebox.showerror("Thiếu thư viện", "Vui lòng cài đặt thư viện Pandas & NumPy!")
            return

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        try:
            df = pd.read_csv(file_path, encoding="utf-8-sig")
            required_cols = ["Mã Gundam", "Tên Gundam", "Dòng", "Tồn kho", "Đơn giá"]
            for col in required_cols:
                if col not in df.columns:
                    messagebox.showerror("Lỗi tệp", f"Thiếu cột bắt buộc: {col}")
                    return

            success_count = 0
            for _, row in df.iterrows():
                p_id = str(row["Mã Gundam"]).strip()
                p_name = str(row["Tên Gundam"]).strip()
                p_grade = str(row["Dòng"]).strip()
                p_stock = int(row["Tồn kho"])
                p_price = float(row["Đơn giá"])
                p_date = datetime.now().strftime("%Y-%m-%d")
                p_status = "🟢 Còn hàng" if p_stock > 5 else "🟡 Sắp hết hàng" if p_stock > 0 else "🔴 Hết hàng"

                self.app_manager.db.query(
                    "INSERT OR REPLACE INTO products (id, name, grade, stock, pre_order, price, entry_date, status) VALUES (?,?,?,?,?,?,?,?)",
                    (p_id, p_name, p_grade, p_stock, 0, p_price, p_date, p_status)
                )
                success_count += 1

            messagebox.showinfo("Thành công", f"Đã nạp {success_count} sản phẩm vào kho!")
            self.load_stock_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")

    def load_stock_data(self):
        """[TÍNH NĂNG]: Phân tích dữ liệu bằng Pandas & NumPy và nạp lên bảng"""
        if not self.tree_stock: return
        for item in self.tree_stock.get_children(): self.tree_stock.delete(item)

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
            total_models = len(rows)
            out_of_stock = 0
            low_stock = 0
            pre_order_count = 0

            # Sử dụng các toán tử NumPy tính toán nhanh tài sản kho hàng
            if HAS_PANDAS_NUMPY_KHO and rows:
                df = pd.DataFrame(rows, columns=["id", "name", "grade", "stock", "pre_order", "price", "entry_date"])
                df["stock"] = df["stock"].astype(int)
                df["pre_order"] = df["pre_order"].astype(int)
                df["price"] = df["price"].astype(float)

                total_money = np.sum(np.multiply(df["stock"].values, df["price"].values))
                out_of_stock = np.sum(df["stock"].values == 0)
                low_stock = np.sum((df["stock"].values > 0) & (df["stock"].values <= 5))
                pre_order_count = np.sum(df["pre_order"].values > 0)
            else:
                for r in rows:
                    st = int(r[3])
                    total_money += float(r[5]) * st
                    if st == 0:
                        out_of_stock += 1
                    elif 0 < st <= 5:
                        low_stock += 1
                    if int(r[4]) > 0: pre_order_count += 1

            for idx, r in enumerate(rows, 1):
                p_id, name, grade, stock, pre_order, price = r[0], r[1], r[2], int(r[3]), int(r[4]), float(r[5])
                entry_date = r[6]

                if stock > 5:
                    p_status, tag = "🟢 Còn hàng", 'safe'
                elif 0 < stock <= 5:
                    p_status, tag = "🟡 Sắp hết hàng", 'low'
                else:
                    p_status, tag = "🔵 Nhận Pre-order" if pre_order > 0 else "🔴 Hết hàng", 'preorder' if pre_order > 0 else 'empty'

                self.tree_stock.insert("", "end",
                                       values=(idx, p_id, name, grade, stock, pre_order, f"{price:,.0f}", entry_date,
                                               p_status), tags=(tag,))

            # Xuất dữ liệu đã tính lên các nhãn thông số
            self.lbl_total_money.config(text=f"TỔNG GIÁ TRỊ TỒN KHO: {total_money:,.0f} VNĐ")
            self.lbl_stat_total.config(text=f"📦 Tổng mô hình: {total_models} dòng")
            self.lbl_stat_empty.config(text=f"🔴 Đã hết hàng: {out_of_stock} mẫu")
            self.lbl_stat_low.config(text=f"🟡 Sắp hết hàng (≤5): {low_stock} mẫu")
            self.lbl_stat_pre.config(text=f"🔵 Đang có đặt trước: {pre_order_count} mẫu")

        except Exception as e:
            print(f"Lỗi: {e}")

    # Các hàm giao diện hỗ trợ bảng phụ
    def load_history_data(self):
        pass

    def load_preorder_history_data(self):
        pass

    def setup_history_table_ui(self):
        pass

    def setup_preorder_history_table_ui(self):
        pass

    def setup_stats_panel_ui(self, parent):
        """[THIẾT KẾ]: Bố cục 3 Card tóm tắt tài chính kho ở chân trang"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        card1 = tk.Frame(parent, bg="#22242b", bd=1, relief="solid")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        c1 = tk.Frame(card1, bg="#22242b", padx=15, pady=15)
        c1.pack(fill="both", expand=True)
        tk.Label(c1, text="💰 TỔNG QUAN TÀI SẢN KHO", font=("Segoe UI", 11, "bold"), fg=self.color_teal,
                 bg="#22242b").pack(anchor="w")
        self.lbl_stat_total = tk.Label(c1, text="Tổng mô hình: 0 dòng", font=("Segoe UI", 10), fg="#a4b0be",
                                       bg="#22242b")
        self.lbl_stat_total.pack(anchor="w", pady=2)
        self.lbl_total_money = tk.Label(c1, text="Tổng giá trị: 0 VNĐ", font=("Segoe UI", 11, "bold"), fg="white",
                                        bg="#22242b")
        self.lbl_total_money.pack(anchor="w", pady=2)

        card2 = tk.Frame(parent, bg="#22242b", bd=1, relief="solid")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        c2 = tk.Frame(card2, bg="#22242b", padx=15, pady=15)
        c2.pack(fill="both", expand=True)
        tk.Label(c2, text="🚨 CẢNH BÁO HẾT HÀNG", font=("Segoe UI", 11, "bold"), fg=self.color_danger,
                 bg="#22242b").pack(anchor="w")
        self.lbl_stat_empty = tk.Label(c2, text="Đã hết hàng: 0 mẫu", font=("Segoe UI", 10), fg="#a4b0be", bg="#22242b")
        self.lbl_stat_empty.pack(anchor="w", pady=2)

        card3 = tk.Frame(parent, bg="#22242b", bd=1, relief="solid")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        c3 = tk.Frame(card3, bg="#22242b", padx=15, pady=15)
        c3.pack(fill="both", expand=True)
        tk.Label(c3, text="📈 TRẠNG THÁI KINH DOANH", font=("Segoe UI", 11, "bold"), fg=self.color_warning,
                 bg="#22242b").pack(anchor="w")
        self.lbl_stat_low = tk.Label(c3, text="Sắp hết hàng (≤5): 0 mẫu", font=("Segoe UI", 10), fg="#a4b0be",
                                     bg="#22242b")
        self.lbl_stat_low.pack(anchor="w", pady=2)
        self.lbl_stat_pre = tk.Label(c3, text="Đang có đặt trước: 0 mẫu", font=("Segoe UI", 10), fg=self.color_info,
                                     bg="#22242b")
        self.lbl_stat_pre.pack(anchor="w", pady=2)

    def delete_item(self):
        pass

    def open_preorder_popup(self):
        pass

    def open_import_popup(self):
        pass

    def open_edit_popup(self):
        pass

    def cancel_preorder(self):
        pass

    def pay_preorder_directly(self):
        pass

    def show_preorder_receipt(self, phone, p_id, p_name, qty, price, deposit, remaining):
        pass

    def clear_form(self):
        pass

    def refresh_all(self):
        pass
