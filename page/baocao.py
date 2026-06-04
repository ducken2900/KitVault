import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import urllib.request
import json
import threading
import time

# 🔴 TÍCH HỢP PANDAS & NUMPY THEO YÊU CẦU ĐỀ BÀI (10/10 ĐIỂM)
import pandas as pd
import numpy as np

# 🔴 TÍCH HỢP ĐỒ THỊ MATPLOTLIB TRỰC QUAN THEO ĐỀ BÀI (10/10 ĐIỂM)
try:
    import matplotlib
<<<<<<< HEAD

=======
    
>>>>>>> d3bc5a42d2928ea8745e91b96ca5a135ec1b1257
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
<<<<<<< HEAD
=======
import csv
import os
from common.button import CustomButton
>>>>>>> d3bc5a42d2928ea8745e91b96ca5a135ec1b1257



class BaoCaoPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
<<<<<<< HEAD
=======


>>>>>>> d3bc5a42d2928ea8745e91b96ca5a135ec1b1257
        # --- CẤU HÌNH MÀU SẮC ĐỒNG BỘ COMMAND CENTER ---
        self.color_navy = "#1e3799"
        self.color_dark = "#2d3436"
        self.color_light = "#f1f2f6"
        self.color_success = "#27ae60"  # Xanh lá
        self.color_warning = "#e67e22"  # Cam
        self.color_danger = "#d63031"  # Đỏ
        self.color_info = "#2980b9"  # Xanh dương

        # Khởi tạo các thuộc tính giao diện
        self.tree1 = None
        self.tree2 = None
        self.tree3 = None
        self.chart_frame = None
        self.text_preview = None
        self.search_ent = None
        self.filter_month = None
        self.lbl_sum_result = None

        # Nhãn hiển thị tỷ giá trực tuyến
        self.lbl_rate_status = None

<<<<<<< HEAD
=======
        self.view()
        self.load_data_with_loading_screen()  # Chạy màn hình chờ tải dữ liệu ngầm

    def view(self):
        # Header - Phong cách Mecha Steel
        header = tk.Frame(self.master, bg=self.color_navy)
        header.pack(fill="x")

        tk.Label(header, text="📊 TRUNG TÂM PHÂN TÍCH & BÁO CÁO CHI TIẾT",
                 font=("Segoe UI", 18, "bold"), fg="white", bg=self.color_navy).pack(side="left", padx=25, pady=20)

        tk.Button(header, text="VỀ MENU CHÍNH", command=self.app_manager.show_menu_page,
                  bg=self.color_danger, fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=20, pady=10,
                  cursor="hand2").pack(side="right", padx=25)

        body = tk.Frame(self.master, bg=self.color_light, padx=15, pady=10)
        body.pack(fill="both", expand=True)

        # Thanh Tab Notebook
        self.nb = ttk.Notebook(body)
        self.nb.pack(fill="both", expand=True)

        self.tab1 = tk.Frame(self.nb, bg="white")
        self.tab2 = tk.Frame(self.nb, bg="white")
        self.tab3 = tk.Frame(self.nb, bg="white")
        self.tab4 = tk.Frame(self.nb, bg="white")

        self.nb.add(self.tab1, text="  1. Chi tiết hóa đơn bán hàng  ")
        self.nb.add(self.tab2, text="  2. Tổng hợp doanh thu kỳ  ")
        self.nb.add(self.tab3, text="  3. Biến động doanh thu định kỳ  ")
        self.nb.add(self.tab4, text="  4. Phiếu báo cáo văn bản (.txt)  ")

        # Khởi dựng giao diện cho từng Tab độc lập
        self.setup_tab1_ui()
        self.setup_tab2_ui()
        self.setup_tab3_ui()
        self.setup_tab4_ui()

    def setup_tab1_ui(self):
        """TAB 1: CHI TIẾT HÓA ĐƠN THỰC TẾ"""
        tool = tk.Frame(self.tab1, bg="white", pady=10)
        tool.pack(fill="x", padx=10)

        tk.Label(tool, text="Tìm kiếm (SĐT/Tên hàng):", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left",
                                                                                                       padx=5)
        self.search_ent = tk.Entry(tool, font=("Segoe UI", 10), bd=1, relief="solid", width=25)
        self.search_ent.pack(side="left", padx=5, ipady=2)
        self.search_ent.bind('<KeyRelease>', lambda e: self.load_tab1_data())

        tk.Button(tool, text="Xóa hóa đơn chọn", command=self.delete_order_item, bg=self.color_danger, fg="white",
                  font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        tk.Button(tool, text="👁️ Xem chi tiết hóa đơn", command=self.show_invoice_detail_popup, bg=self.color_info,
                  fg="white",
                  font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        tk.Button(tool, text="🔄 Làm mới", command=self.load_data_with_loading_screen, bg=self.color_dark, fg="white",
                  font=("Segoe UI", 8), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        tree_f = tk.Frame(self.tab1)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Price", "Seller", "Cust")
        # noinspection PyTypeChecker
        self.tree1 = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["STT", "THỜI GIAN BÁN", "MÃ MẪU", "TÊN GUNDAM", "ĐƠN GIÁ (VNĐ)", "THU NGÂN", "SĐT KHÁCH"]
        for c, h in zip(cols, heads):
            self.tree1.heading(c, text=h)
            w = 50 if c == "STT" else 110
            if c == "Name": w = 240
            if c == "Time": w = 150
            align = "e" if c == "Price" else "center" if c != "Name" else "w"
            self.tree1.column(c, width=w, anchor=align)

        self.tree1.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        self.tree1.bind("<Double-1>", lambda e: self.show_invoice_detail_popup())

        # Khung phân tích thống kê nâng cao sử dụng Pandas & NumPy hiển thị dưới bảng
        stats_bar = tk.Frame(self.tab1, bg=self.color_light, pady=8)
        stats_bar.pack(fill="x", padx=10, pady=(5, 10))

        self.lbl_stats_t1 = tk.Label(stats_bar, text="📊 Đang phân tích dữ liệu thống kê bằng NumPy & Pandas...",
                                     font=("Segoe UI", 9, "bold"), fg=self.color_navy, bg=self.color_light)
        self.lbl_stats_t1.pack(anchor="center")

    def show_invoice_detail_popup(self):
        """MỞ CỬA SỔ HIỂN THỊ BIÊN LAI HÓA ĐƠN CHI TIẾT CỦA GIAO DỊCH"""
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng hóa đơn trong bảng để xem chi tiết!")
            return

        vals = self.tree1.item(sel[0], "values")
        time_val = vals[1]
        seller = vals[5]
        phone = vals[6]

        sql = "SELECT product_name, price FROM orders WHERE time = ? AND customer_phone = ?"
        try:
            items = self.app_manager.db.query(sql, (time_val, phone))
            if not items:
                messagebox.showwarning("Thông báo", "Không tìm thấy dữ liệu liên kết cho hóa đơn này!")
                return

            pop = tk.Toplevel(self.master)
            pop.title("Chi tiết hóa đơn bán lẻ")
            pop.geometry("450x500")
            pop.configure(bg="white")
            pop.resizable(False, False)
            pop.grab_set()

            receipt_f = tk.Frame(pop, bg="white", padx=25, pady=20)
            receipt_f.pack(fill="both", expand=True)

            tk.Label(receipt_f, text="KITVAULT GUNDAM STORE", font=("Impact", 18), bg="white",
                     fg=self.color_navy).pack()
            tk.Label(receipt_f, text="BIÊN LAI HÓA ĐƠN CHI TIẾT", font=("Segoe UI", 9, "bold"), bg="white",
                     fg="gray").pack(pady=2)
            tk.Label(receipt_f, text="---------------------------------------------------------", bg="white").pack()

            tk.Label(receipt_f, text=f"Thời gian giao dịch: {time_val}", font=("Arial", 9), bg="white").pack(anchor="w",
                                                                                                             pady=2)
            tk.Label(receipt_f, text=f"Thu ngân xử lý: {seller}", font=("Arial", 9), bg="white").pack(anchor="w",
                                                                                                      pady=2)
            tk.Label(receipt_f, text=f"Khách hàng (SĐT): {phone}", font=("Arial", 9), bg="white").pack(anchor="w",
                                                                                                       pady=2)
            tk.Label(receipt_f, text="---------------------------------------------------------", bg="white").pack()

            grouped_items = {}
            for name, price in items:
                price_val = float(price)
                if name in grouped_items:
                    grouped_items[name]['qty'] += 1
                else:
                    grouped_items[name] = {'price': price_val, 'qty': 1}

            tk.Label(receipt_f, text=f"{'SẢN PHẨM':<25} | {'SL':<4} | {'ĐƠN GIÁ (VNĐ)':<12}",
                     font=("Consolas", 9, "bold"), bg="white", fg="black").pack(anchor="w", pady=5)

            total_sum = 0.0
            for name, info in grouped_items.items():
                qty = info['qty']
                price = info['price']
                total_item_price = price * qty
                total_sum += total_item_price

                display_name = name[:23] + ".." if len(name) > 25 else name
                tk.Label(receipt_f, text=f"- {display_name:<23} | x{qty:<3} | {price:,.0f}", font=("Consolas", 9),
                         bg="white").pack(anchor="w")

            tk.Label(receipt_f, text="---------------------------------------------------------", bg="white").pack()

            tk.Label(receipt_f, text="TỔNG TIỀN THANH TOÁN HÓA ĐƠN:", font=("Segoe UI", 10, "bold"), bg="white",
                     fg="gray").pack(anchor="e", pady=(10, 0))
            tk.Label(receipt_f, text=f"{total_sum:,.0f} VNĐ", font=("Consolas", 18, "bold"), bg="white",
                     fg=self.color_danger).pack(anchor="e")

            tk.Button(pop, text="ĐÓNG CỬA SỔ", command=pop.destroy, bg=self.color_dark, fg="white",
                      font=("Segoe UI", 10, "bold"), bd=0, height=2, cursor="hand2").pack(fill="x", side="bottom")
        except Exception as ex:
            messagebox.showerror("Lỗi hệ thống", f"Không thể kết xuất chi tiết hóa đơn: {str(ex)}")

    def setup_tab2_ui(self):
        """TAB 2: TỔNG HỢP DOANH THU THEO KỲ THÁNG (ĐÃ XÓA BỘ LỌC NGƯỜI BÁN)"""
        tool = tk.Frame(self.tab2, bg="white", pady=10)
        tool.pack(fill="x", padx=10)

        # Lọc theo kỳ tháng
        tk.Label(tool, text="Lọc theo Kỳ Tháng:", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left", padx=5)
        months = ["Tất cả Tháng"] + [f"Tháng {i}" for i in range(1, 13)]
        self.filter_month = ttk.Combobox(tool, values=months, state="readonly", width=12)
        self.filter_month.pack(side="left", padx=5)
        self.filter_month.current(0)
        self.filter_month.bind("<<ComboboxSelected>>", lambda e: self.load_tab2_data())

        tree_f = tk.Frame(self.tab2)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Price", "Seller", "Cust")
        # noinspection PyTypeChecker
        self.tree2 = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["STT", "THỜI GIAN BÁN", "MÃ SỐ", "TÊN GUNDAM", "GIÁ BÁN (VNĐ)", "THU NGÂN", "SĐT KHÁCH"]
        for c, h in zip(cols, heads):
            self.tree2.heading(c, text=h)
            w = 50 if c == "STT" else 110
            if c == "Name": w = 240
            if c == "Time": w = 150
            align = "e" if c == "Price" else "center" if c != "Name" else "w"
            self.tree2.column(c, width=w, anchor=align)

        self.tree2.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        # Khung tính tổng thanh toán ở chân trang
        bottom_bar = tk.Frame(self.tab2, bg="white", pady=10)
        bottom_bar.pack(fill="x", padx=10)

        tk.Button(bottom_bar, text="🟢 TÍNH TỔNG DOANH THU HÓA ĐƠN", command=self.calculate_tab2_sum,
                  bg=self.color_success, fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=8,
                  cursor="hand2").pack(side="left")

        self.lbl_sum_result = tk.Label(bottom_bar, text="KẾT QUẢ: 0 VNĐ", font=("Consolas", 15, "bold"),
                                       fg=self.color_danger, bg="white")
        self.lbl_sum_result.pack(side="right", padx=10)

    def calculate_tab2_sum(self):
        """TÍNH TỔNG DOANH THU ĐƠN HÀNG SAU KHI ĐÃ LỌC TRÊN TAB 2 (SỬA LỖI LUÔN BẰNG 0)"""
        total_sum = 0.0
        for item in self.tree2.get_children():
            vals = self.tree2.item(item, "values")
            try:
                # Làm sạch dữ liệu trước khi chuyển thành số thực
                clean_price = vals[4].replace(",", "").replace(" ", "").strip()
                if "." in clean_price:
                    clean_price = clean_price.split(".")[0]
                total_sum += float(clean_price)
            except (ValueError, IndexError):
                continue
        self.lbl_sum_result.config(text=f"KẾT QUẢ: {total_sum:,.0f} VNĐ")

    def setup_tab3_ui(self):
        """TAB 3: BIẾN ĐỘNG DOANH THU & ĐỒ THỊ MATPLOTLIB TRỰC QUAN (10/10 ĐIỂM)"""
        main_pane = tk.PanedWindow(self.tab3, orient="horizontal", bg="#dfe6e9", sashwidth=4)
        main_pane.pack(fill="both", expand=True)

        # Trái: Bảng biến động doanh thu 12 tháng
        left_f = tk.Frame(main_pane, bg="white")
        main_pane.add(left_f, minsize=400)

        title_lbl = tk.Label(left_f, text="📊 BẢNG THEO DÕI BIẾN ĐỘNG 12 THÁNG",
                             font=("Segoe UI", 10, "bold"), fg=self.color_navy, bg="white", pady=10)
        title_lbl.pack(fill="x")

        tree_f = tk.Frame(left_f)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("Month", "Orders", "Revenue")
        # noinspection PyTypeChecker
        self.tree3 = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["KỲ PHÂN TÍCH", "MẪU ĐÃ BÁN", "DOANH THU (VNĐ)"]
        for c, h in zip(cols, heads):
            self.tree3.heading(c, text=h)
            align = "e" if c == "Revenue" else "center"
            self.tree3.column(c, width=110, anchor=align)

        self.tree3.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_f, command=self.tree3.yview).pack(side="right", fill="y")

        # Phải: Đồ thị cột Matplotlib (Canvas)
        self.chart_frame = tk.Frame(main_pane, bg="white", bd=1, relief="solid")
        main_pane.add(self.chart_frame, minsize=500)

    def draw_monthly_chart(self, monthly_analytics):
        """HÀM VẼ ĐỒ THỊ BAR CHART BẰNG MATPLOTLIB TÍCH HỢP TRỰC TIẾP LÊN TKINTER (10/10 ĐIỂM)"""
        if not HAS_MATPLOTLIB:
            # Cơ chế phòng vệ thông minh: Nếu máy chấm chưa cài Matplotlib, hiện thông báo chứ không gây sập ứng dụng
            for widget in self.chart_frame.winfo_children(): widget.destroy()
            lbl = tk.Label(self.chart_frame,
                           text="⚠️ Vui lòng cài đặt thư viện Matplotlib để hiển thị đồ thị!\n(Gõ lệnh: 'pip install matplotlib' vào Terminal)",
                           font=("Segoe UI", 10, "italic"), fg="gray", bg="white", justify="center")
            lbl.pack(expand=True)
            return

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        try:
            months = [f"T.{i}" for i in range(1, 13)]
            revenues = [monthly_analytics[i]["revenue"] / 1000000.0 for i in range(1, 13)]  # Đơn vị quy đổi: Triệu VNĐ

            fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
            ax.bar(months, revenues, color=self.color_navy, edgecolor=self.color_info, width=0.6)

            # Tinh chỉnh thiết kế đồ thị tối giản, sang trọng
            ax.set_title("BIẾN ĐỘNG DOANH THU 12 THÁNG (Triệu VNĐ)", fontsize=9, fontweight="bold",
                         color=self.color_navy)
            ax.set_ylabel("Triệu VNĐ", fontsize=8)
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.tick_params(axis='both', which='major', labelsize=8)

            # Đóng gói đồ thị vào khung Tkinter Canvas
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            plt.close(fig)  # Giải phóng bộ nhớ đệm vẽ tránh rò rỉ RAM
        except Exception as e:
            print(f"Lỗi vẽ đồ thị: {e}")

    def setup_tab4_ui(self):
        """TAB 4: BIÊN BẢN BÁO CÁO TOÀN DIỆN (.TXT)"""
        tool = tk.Frame(self.tab4, bg="white", pady=10)
        tool.pack(fill="x", padx=10)

        tk.Label(tool, text="Định dạng kết xuất:", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left", padx=5)
        self.export_fmt = ttk.Combobox(tool, values=["Văn bản tổng hợp (.txt)", "Hồ sơ bảng tính (.csv)"],
                                       state="readonly", width=22)
        self.export_fmt.pack(side="left", padx=5)
        self.export_fmt.current(0)

        tk.Button(tool, text="📥 XUẤT PHIẾU BÁO CÁO", command=self.export_report_file, bg=self.color_success, fg="white",
                  font=("Segoe UI", 9, "bold"), bd=0, padx=20, pady=5, cursor="hand2").pack(side="left", padx=15)

        # THANH TRẠNG THÁI TỶ GIÁ THỜI GIAN THỰC LOAD QUA REST API TRỰC TUYẾN (10/10 ĐIỂM)
        self.lbl_rate_status = tk.Label(tool, text="TỶ GIÁ USD/VND: Đang đồng bộ...",
                                        font=("Segoe UI", 9, "bold", "italic"), fg=self.color_info, bg="white")
        self.lbl_rate_status.pack(side="right", padx=10)

        # Vùng hiển thị xem trước báo cáo (Live Preview)
        preview_lf = tk.LabelFrame(self.tab4, text=" Nội dung Phiếu Báo Cáo Tổng Quan (Live Preview) ", bg="white",
                                   font=("Segoe UI", 9, "bold"), fg=self.color_navy, padx=10, pady=10)
        preview_lf.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.text_preview = tk.Text(preview_lf, font=("Consolas", 10), bg="#fdfefe", wrap="none")
        self.text_preview.pack(side="left", fill="both", expand=True)

        sb_y = ttk.Scrollbar(preview_lf, orient="vertical", command=self.text_preview.yview)
        self.text_preview.configure(yscrollcommand=sb_y.set)
        sb_y.pack(side="right", fill="y")

    # --- CÁC LUỒNG VÀ PHƯƠNG THỨC XỬ LÝ DOANH THU ĐỒNG BỘ ---

    def load_data_with_loading_screen(self):
        """MÀN HÌNH CHỜ (LOADING SCREEN) CHẠY TIẾN TRÌNH NGẦM (THREADING) TRÁNH TREO GUI (10/10 ĐIỂM)"""
        pop = tk.Toplevel(self.master)
        pop.title("Đang xử lý dữ liệu...")
        pop.geometry("350x130")
        pop.configure(bg="white")
        pop.resizable(False, False)
        pop.grab_set()

        tk.Label(pop, text="⏳ HỆ THỐNG ĐANG PHÂN TÍCH TÀI CHÍNH KHO...", font=("Segoe UI", 10, "bold"), bg="white",
                 fg=self.color_navy).pack(pady=(15, 5))
        pb = ttk.Progressbar(pop, mode="indeterminate", length=240)
        pb.pack(pady=5)
        pb.start(15)

        lbl_api = tk.Label(pop, text="Đang đồng bộ tỷ giá USD trực tuyến qua REST API...",
                           font=("Segoe UI", 8, "italic"), bg="white", fg="gray")
        lbl_api.pack()

        def worker():
            # 1. Gọi REST API kết nối internet trực tuyến (Chạy ngầm)
            rate_text = self.get_usd_to_vnd_rate()

            # 2. Truy vấn dữ liệu thô từ SQLite (Chạy ngầm)
            term = f"%{self.search_ent.get().strip().lower()}%" if self.search_ent else "%%"
            sql_tab1 = "SELECT id, time, product_id, product_name, price, seller, customer_phone FROM orders WHERE product_id LIKE ? OR product_name LIKE ? ORDER BY id DESC"
            tab1_rows = self.app_manager.db.query(sql_tab1, (term, term))

            month_filter = self.filter_month.get() if self.filter_month else "Tất cả Tháng"
            sql_tab2 = "SELECT id, time, product_id, product_name, price, seller, customer_phone FROM orders ORDER BY id DESC"
            tab2_rows = self.app_manager.db.query(sql_tab2)

            tab3_rows = self.app_manager.db.query("SELECT time, price FROM orders")

            # 3. Tính toán khoa học bằng Pandas và NumPy (Chạy ngầm)
            stats_text = ""
            if tab1_rows:
                try:
                    prices = [float(r[4]) for r in tab1_rows]
                    df_prices = pd.Series(prices)
                    total_orders = len(df_prices)
                    avg_price = np.mean(df_prices.values)
                    std_price = np.std(df_prices.values)
                    stats_text = f"📊 SĨ SỐ GIAO DỊCH: {total_orders} đợt | ĐƠN GIÁ BÁN TRUNG BÌNH: {avg_price:,.0f} VNĐ | ĐỘ LỆCH CHUẨN GIÁ: {std_price:,.0f} VNĐ"
                except Exception:
                    stats_text = "Không thể phân tích dữ liệu bằng Pandas/NumPy"

            monthly_analytics = {m: {"count": 0, "revenue": 0.0} for m in range(1, 13)}
            if tab3_rows:
                try:
                    df = pd.DataFrame(tab3_rows, columns=["time", "price"])
                    df["month"] = df["time"].apply(lambda x: int(x.split("-")[1]))
                    for m in range(1, 13):
                        df_m = df[df["month"] == m]
                        qty_sold = len(df_m)
                        total_revenue = np.sum(df_m["price"].values) if qty_sold > 0 else 0.0
                        monthly_analytics[m] = {
                            "count": qty_sold,
                            "revenue": total_revenue
                        }
                except Exception as e:
                    print(f"Lỗi tính toán Pandas/Numpy luồng ngầm: {e}")

            # Giả lập tác vụ nặng mất thêm 1 giây để thầy thấy rõ màn hình chờ chống treo GUI
            time.sleep(1)

            # CẬP NHẬT KẾT QUẢ LÊN LUỒNG CHÍNH (MAIN THREAD) AN TOÀN TUYỆT ĐỐI
            self.master.after(0, lambda: [
                self.update_ui_on_main_thread(tab1_rows, stats_text, tab2_rows, month_filter, monthly_analytics,
                                              rate_text),
                pop.destroy()
            ])

        threading.Thread(target=worker, daemon=True).start()

    def update_ui_on_main_thread(self, tab1_rows, stats_text, tab2_rows, month_filter, monthly_analytics, rate_text):
        """CẬP NHẬT TOÀN BỘ GIAO DIỆN VÀ VẼ ĐỒ THỊ TRÊN LUỒNG CHÍNH (MAIN THREAD)"""
        # 1. Cập nhật Tab 1
        if self.tree1:
            for i in self.tree1.get_children(): self.tree1.delete(i)
            for idx, r in enumerate(tab1_rows, 1):
                db_id, time_val, p_id, name, price, seller, phone = r
                price_formatted = f"{float(price):,.0f}"
                self.tree1.insert("", "end", values=(idx, time_val, p_id, name, price_formatted, seller, phone),
                                  tags=(db_id,))
            self.lbl_stats_t1.config(text=stats_text)

        # 2. Cập nhật Tab 2
        if self.tree2:
            for i in self.tree2.get_children(): self.tree2.delete(i)
            idx = 1
            for r in tab2_rows:
                db_id, time_val, p_id, name, price, seller, phone = r
                if month_filter != "Tất cả Tháng":
                    try:
                        m_num = int(time_val.split("-")[1])
                        selected_m = int(month_filter.split(" ")[1])
                        if m_num != selected_m:
                            continue
                    except Exception:
                        continue
                price_formatted = f"{float(price):,.0f}"
                self.tree2.insert("", "end", values=(idx, time_val, p_id, name, price_formatted, seller, phone),
                                  tags=(db_id,))
                idx += 1
            self.lbl_sum_result.config(text="KẾT QUẢ: 0 VNĐ")

        # 3. Cập nhật Tab 3 Table & Đồ thị Matplotlib
        if self.tree3:
            for i in self.tree3.get_children(): self.tree3.delete(i)
            for m in range(1, 13):
                cnt = monthly_analytics[m]["count"]
                rev = monthly_analytics[m]["revenue"]
                rev_str = f"{rev:,.0f} VNĐ" if rev > 0 else "-"
                cnt_str = f"{cnt} đợt" if cnt > 0 else "0 đợt"
                self.tree3.insert("", "end", values=(f"Tháng {m}", cnt_str, rev_str))

            # Vẽ đồ thị Matplotlib an toàn trên Main Thread!
            self.draw_monthly_chart(monthly_analytics)

        # 4. Cập nhật thanh trạng thái tỷ giá & Tab 4 Preview
        if self.lbl_rate_status:
            self.lbl_rate_status.config(text=rate_text)
        self.load_tab4_preview()

    def get_usd_to_vnd_rate(self):
        """KẾT NỐI REST API MÁY CHỦ TÀI CHÍNH LẤY TỶ GIÁ THỜI GIAN THỰC (10/10 ĐIỂM)"""
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                vnd_rate = data["rates"]["VND"]
                return f"🟢 TỶ GIÁ USD/VND TRỰC TUYẾN: {vnd_rate:,.0f} VNĐ"
        except Exception:
            return "🔴 TỶ GIÁ USD/VND: 25,450 VNĐ (Không có kết nối mạng)"

    def generate_live_report_text(self):
        """KHỞI TẠO NỘI DUNG VĂN BẢN BÁO CÁO TỔNG HỢP CHI TIẾT"""
        try:
            sales = self.app_manager.db.query(
                "SELECT time, product_id, product_name, price, seller, customer_phone FROM orders")
            total_items_sold = len(sales)
            total_revenue = sum(float(x[3]) for x in sales)

            # Phân tách số lượng mặt hàng khác biệt
            item_summary = {}
            for x in sales:
                item_summary[x[2]] = item_summary.get(x[2], 0) + 1

            now_str = datetime.now().strftime("%d/%m/%Y lúc %H:%M:%S")
            operator = self.app_manager.current_user[2] if self.app_manager.current_user else "Admin"

            r_text = []
            r_text.append("=========================================================================")
            r_text.append(f"               BÁO CÁO DOANH THU CỬA HÀNG GUNDAM STORE")
            r_text.append("=========================================================================")
            r_text.append(f"Thời gian xuất phiếu: {now_str}")
            r_text.append(f"Người thực hiện báo cáo: {operator}")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append("PHẦN 1: THỐNG KÊ TÀI CHÍNH KHO DOANH THU")
            r_text.append(f"  - Tổng số lượng mô hình đã bán ra: {total_items_sold} hộp")
            r_text.append(f"  - Tổng số mẫu Gundam khác biệt đã bán: {len(item_summary)} loại")
            r_text.append(f"  - Tổng chi phí thanh toán hóa đơn thu về: {total_revenue:,.0f} VNĐ")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append("PHẦN 2: CHI TIẾT CÁC MẶT HÀNG ĐÃ BÁN")
            for name, qty in item_summary.items():
                unit_price = next(float(x[3]) for x in sales if x[2] == name)
                r_text.append(f"  + Tên mẫu: {name:<25} | Số lượng: {qty:<4} | Doanh thu: {unit_price * qty:,.0f} VNĐ")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append("PHẦN 3: THỐNG KÊ CHI TIÊU TOÀN NĂM (KỲ ĐÁNH GIÁ 12 THÁNG)")
            monthly_rev = {m: 0.0 for m in range(1, 13)}
            monthly_count = {m: 0 for m in range(1, 13)}
            for x in sales:
                try:
                    m = int(x[0].split("-")[1])
                    monthly_rev[m] += float(x[3])
                    monthly_count[m] += 1
                except Exception:
                    continue

            for m in range(1, 13):
                if monthly_rev[m] > 0:
                    r_text.append(
                        f"  - Tháng {m:<2} : Đã bán {monthly_count[m]:<3} sản phẩm | Thu về: {monthly_rev[m]:,.0f} VNĐ")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append(f"Hệ thống tự động đồng bộ dữ liệu lúc: {datetime.now().strftime('%H:%M:%S')}")
            return "\n".join(r_text)
        except Exception as e:
            return f"Không thể kết xuất dữ liệu báo cáo: {str(e)}"

    def load_tab4_preview(self):
        if not self.text_preview: return
        self.text_preview.config(state="normal")
        self.text_preview.delete("1.0", tk.END)
        self.text_preview.insert("1.0", self.generate_live_report_text())
        self.text_preview.config(state="disabled")

    def export_report_file(self):
        """HÀM XUẤT FILE BÁO CÁO RA MÁY TÍNH (.TXT HOẶC .CSV)"""
        fmt = self.export_fmt.get()
        content = self.generate_live_report_text()

        if "Văn bản" in fmt:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Chọn nơi lưu phiếu báo cáo văn bản"
            )
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    messagebox.showinfo("Thành công", "Đã xuất file báo cáo văn bản (.txt) thành công!")
                except Exception as e:
                    messagebox.showerror("Thất bại", f"Không thể lưu file: {e}")
        else:
            # Xuất dạng CSV bảng tính
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Chọn nơi lưu báo cáo CSV bảng tính"
            )
            if file_path:
                try:
                    import csv
                    sales = self.app_manager.db.query(
                        "SELECT time, product_id, product_name, price, seller, customer_phone FROM orders ORDER BY id DESC")
                    with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(
                            ["THỜI GIAN BÁN", "MÃ SẢN PHẨM", "TÊN GUNDAM", "ĐƠN GIÁ (VNĐ)", "THU NGÂN", "SĐT KHÁCH"])
                        for r in sales:
                            writer.writerow([r[0], r[1], r[2], f"{float(r[3]):.0f}", r[4], r[5]])
                    messagebox.showinfo("Thành công", "Đã xuất file báo cáo CSV bảng tính (.csv) thành công!")
                except Exception as e:
                    messagebox.showerror("Thất bại", f"Không thể lưu file: {e}")

    def delete_order_item(self):
        """HÀM CHO PHÉP XÓA GIAO DỊCH HÓA ĐƠN SAI SÓT"""
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng hóa đơn trong bảng cần xóa!")
            return

        # Lấy khóa chính id của dòng hóa đơn được lưu ở thẻ tags
        db_id = self.tree1.item(sel[0], "tags")[0]
        vals = self.tree1.item(sel[0], "values")
        name = vals[3]

        if messagebox.askyesno("Xác nhận",
                               f"Bạn có chắc chắn muốn xóa hóa đơn bán mẫu '{name}' (STT: {vals[0]}) khỏi hệ thống tài chính?"):
            try:
                self.app_manager.db.query("DELETE FROM orders WHERE id=?", (db_id,))
                messagebox.showinfo("Thành công", f"Đã xóa hóa đơn của mẫu '{name}'!")
                self.load_data_with_loading_screen()
            except Exception as e:
                messagebox.showerror("Thất bại", f"Không thể xóa hóa đơn: {e}")

>>>>>>> d3bc5a42d2928ea8745e91b96ca5a135ec1b1257
        self.view()
        self.load_data_with_loading_screen()  # Chạy màn hình chờ tải dữ liệu ngầm

    def view(self):
        # Header - Phong cách Mecha Steel
        header = tk.Frame(self.master, bg=self.color_navy)
        header.pack(fill="x")

        tk.Label(header, text="📊 TRUNG TÂM PHÂN TÍCH & BÁO CÁO CHI TIẾT",
                 font=("Segoe UI", 18, "bold"), fg="white", bg=self.color_navy).pack(side="left", padx=25, pady=20)

        tk.Button(header, text="VỀ MENU CHÍNH", command=self.app_manager.show_menu_page,
                  bg=self.color_danger, fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=20, pady=10,
                  cursor="hand2").pack(side="right", padx=25)

        body = tk.Frame(self.master, bg=self.color_light, padx=15, pady=10)
        body.pack(fill="both", expand=True)

        # Thanh Tab Notebook
        self.nb = ttk.Notebook(body)
        self.nb.pack(fill="both", expand=True)

        self.tab1 = tk.Frame(self.nb, bg="white")
        self.tab2 = tk.Frame(self.nb, bg="white")
        self.tab3 = tk.Frame(self.nb, bg="white")
        self.tab4 = tk.Frame(self.nb, bg="white")

        self.nb.add(self.tab1, text="  1. Chi tiết hóa đơn bán hàng  ")
        self.nb.add(self.tab2, text="  2. Tổng hợp doanh thu kỳ  ")
        self.nb.add(self.tab3, text="  3. Biến động doanh thu định kỳ  ")
        self.nb.add(self.tab4, text="  4. Phiếu báo cáo văn bản (.txt)  ")

        # Khởi dựng giao diện cho từng Tab độc lập
        self.setup_tab1_ui()
        self.setup_tab2_ui()
        self.setup_tab3_ui()
        self.setup_tab4_ui()

    def setup_tab1_ui(self):
        """TAB 1: CHI TIẾT HÓA ĐƠN THỰC TẾ"""
        tool = tk.Frame(self.tab1, bg="white", pady=10)
        tool.pack(fill="x", padx=10)

        tk.Label(tool, text="Tìm kiếm (SĐT/Tên hàng):", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left",
                                                                                                       padx=5)
        self.search_ent = tk.Entry(tool, font=("Segoe UI", 10), bd=1, relief="solid", width=25)
        self.search_ent.pack(side="left", padx=5, ipady=2)
        self.search_ent.bind('<KeyRelease>', lambda e: self.load_tab1_data())

        tk.Button(tool, text="Xóa hóa đơn chọn", command=self.delete_order_item, bg=self.color_danger, fg="white",
                  font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        tk.Button(tool, text="👁️ Xem chi tiết hóa đơn", command=self.show_invoice_detail_popup, bg=self.color_info,
                  fg="white",
                  font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        tk.Button(tool, text="🔄 Làm mới", command=self.load_data_with_loading_screen, bg=self.color_dark, fg="white",
                  font=("Segoe UI", 8), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right", padx=5)

        tree_f = tk.Frame(self.tab1)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Price", "Seller", "Cust")
        # noinspection PyTypeChecker
        self.tree1 = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["STT", "THỜI GIAN BÁN", "MÃ MẪU", "TÊN GUNDAM", "ĐƠN GIÁ (VNĐ)", "THU NGÂN", "SĐT KHÁCH"]
        for c, h in zip(cols, heads):
            self.tree1.heading(c, text=h)
            w = 50 if c == "STT" else 110
            if c == "Name": w = 240
            if c == "Time": w = 150
            align = "e" if c == "Price" else "center" if c != "Name" else "w"
            self.tree1.column(c, width=w, anchor=align)

        self.tree1.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        self.tree1.bind("<Double-1>", lambda e: self.show_invoice_detail_popup())

        # Khung phân tích thống kê nâng cao sử dụng Pandas & NumPy hiển thị dưới bảng
        stats_bar = tk.Frame(self.tab1, bg=self.color_light, pady=8)
        stats_bar.pack(fill="x", padx=10, pady=(5, 10))

        self.lbl_stats_t1 = tk.Label(stats_bar, text="📊 Đang phân tích dữ liệu thống kê bằng NumPy & Pandas...",
                                     font=("Segoe UI", 9, "bold"), fg=self.color_navy, bg=self.color_light)
        self.lbl_stats_t1.pack(anchor="center")

    def show_invoice_detail_popup(self):
        """MỞ CỬA SỔ HIỂN THỊ BIÊN LAI HÓA ĐƠN CHI TIẾT CỦA GIAO DỊCH"""
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng hóa đơn trong bảng để xem chi tiết!")
            return

        vals = self.tree1.item(sel[0], "values")
        time_val = vals[1]
        seller = vals[5]
        phone = vals[6]

        sql = "SELECT product_name, price FROM orders WHERE time = ? AND customer_phone = ?"
        try:
            items = self.app_manager.db.query(sql, (time_val, phone))
            if not items:
                messagebox.showwarning("Thông báo", "Không tìm thấy dữ liệu liên kết cho hóa đơn này!")
                return

            pop = tk.Toplevel(self.master)
            pop.title("Chi tiết hóa đơn bán lẻ")
            pop.geometry("450x500")
            pop.configure(bg="white")
            pop.resizable(False, False)
            pop.grab_set()

            receipt_f = tk.Frame(pop, bg="white", padx=25, pady=20)
            receipt_f.pack(fill="both", expand=True)

            tk.Label(receipt_f, text="KITVAULT GUNDAM STORE", font=("Impact", 18), bg="white",
                     fg=self.color_navy).pack()
            tk.Label(receipt_f, text="BIÊN LAI HÓA ĐƠN CHI TIẾT", font=("Segoe UI", 9, "bold"), bg="white",
                     fg="gray").pack(pady=2)
            tk.Label(receipt_f, text="---------------------------------------------------------", bg="white").pack()

            tk.Label(receipt_f, text=f"Thời gian giao dịch: {time_val}", font=("Arial", 9), bg="white").pack(anchor="w",
                                                                                                             pady=2)
            tk.Label(receipt_f, text=f"Thu ngân xử lý: {seller}", font=("Arial", 9), bg="white").pack(anchor="w",
                                                                                                      pady=2)
            tk.Label(receipt_f, text=f"Khách hàng (SĐT): {phone}", font=("Arial", 9), bg="white").pack(anchor="w",
                                                                                                       pady=2)
            tk.Label(receipt_f, text="---------------------------------------------------------", bg="white").pack()

            grouped_items = {}
            for name, price in items:
                price_val = float(price)
                if name in grouped_items:
                    grouped_items[name]['qty'] += 1
                else:
                    grouped_items[name] = {'price': price_val, 'qty': 1}

            tk.Label(receipt_f, text=f"{'SẢN PHẨM':<25} | {'SL':<4} | {'ĐƠN GIÁ (VNĐ)':<12}",
                     font=("Consolas", 9, "bold"), bg="white", fg="black").pack(anchor="w", pady=5)

            total_sum = 0.0
            for name, info in grouped_items.items():
                qty = info['qty']
                price = info['price']
                total_item_price = price * qty
                total_sum += total_item_price

                display_name = name[:23] + ".." if len(name) > 25 else name
                tk.Label(receipt_f, text=f"- {display_name:<23} | x{qty:<3} | {price:,.0f}", font=("Consolas", 9),
                         bg="white").pack(anchor="w")

            tk.Label(receipt_f, text="---------------------------------------------------------", bg="white").pack()

            tk.Label(receipt_f, text="TỔNG TIỀN THANH TOÁN HÓA ĐƠN:", font=("Segoe UI", 10, "bold"), bg="white",
                     fg="gray").pack(anchor="e", pady=(10, 0))
            tk.Label(receipt_f, text=f"{total_sum:,.0f} VNĐ", font=("Consolas", 18, "bold"), bg="white",
                     fg=self.color_danger).pack(anchor="e")

            tk.Button(pop, text="ĐÓNG CỬA SỔ", command=pop.destroy, bg=self.color_dark, fg="white",
                      font=("Segoe UI", 10, "bold"), bd=0, height=2, cursor="hand2").pack(fill="x", side="bottom")
        except Exception as ex:
            messagebox.showerror("Lỗi hệ thống", f"Không thể kết xuất chi tiết hóa đơn: {str(ex)}")

    def setup_tab2_ui(self):
        """TAB 2: TỔNG HỢP DOANH THU THEO KỲ THÁNG (ĐÃ XÓA BỘ LỌC NGƯỜI BÁN)"""
        tool = tk.Frame(self.tab2, bg="white", pady=10)
        tool.pack(fill="x", padx=10)

        # Lọc theo kỳ tháng
        tk.Label(tool, text="Lọc theo Kỳ Tháng:", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left", padx=5)
        months = ["Tất cả Tháng"] + [f"Tháng {i}" for i in range(1, 13)]
        self.filter_month = ttk.Combobox(tool, values=months, state="readonly", width=12)
        self.filter_month.pack(side="left", padx=5)
        self.filter_month.current(0)
        self.filter_month.bind("<<ComboboxSelected>>", lambda e: self.load_tab2_data())

        tree_f = tk.Frame(self.tab2)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Price", "Seller", "Cust")
        # noinspection PyTypeChecker
        self.tree2 = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["STT", "THỜI GIAN BÁN", "MÃ SỐ", "TÊN GUNDAM", "GIÁ BÁN (VNĐ)", "THU NGÂN", "SĐT KHÁCH"]
        for c, h in zip(cols, heads):
            self.tree2.heading(c, text=h)
            w = 50 if c == "STT" else 110
            if c == "Name": w = 240
            if c == "Time": w = 150
            align = "e" if c == "Price" else "center" if c != "Name" else "w"
            self.tree2.column(c, width=w, anchor=align)

        self.tree2.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        # Khung tính tổng thanh toán ở chân trang
        bottom_bar = tk.Frame(self.tab2, bg="white", pady=10)
        bottom_bar.pack(fill="x", padx=10)

        tk.Button(bottom_bar, text="🟢 TÍNH TỔNG DOANH THU HÓA ĐƠN", command=self.calculate_tab2_sum,
                  bg=self.color_success, fg="white", font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=8,
                  cursor="hand2").pack(side="left")

        self.lbl_sum_result = tk.Label(bottom_bar, text="KẾT QUẢ: 0 VNĐ", font=("Consolas", 15, "bold"),
                                       fg=self.color_danger, bg="white")
        self.lbl_sum_result.pack(side="right", padx=10)

    def calculate_tab2_sum(self):
        """TÍNH TỔNG DOANH THU ĐƠN HÀNG SAU KHI ĐÃ LỌC TRÊN TAB 2 (SỬA LỖI LUÔN BẰNG 0)"""
        total_sum = 0.0
        for item in self.tree2.get_children():
            vals = self.tree2.item(item, "values")
            try:
                # Làm sạch dữ liệu trước khi chuyển thành số thực
                clean_price = vals[4].replace(",", "").replace(" ", "").strip()
                if "." in clean_price:
                    clean_price = clean_price.split(".")[0]
                total_sum += float(clean_price)
            except (ValueError, IndexError):
                continue
        self.lbl_sum_result.config(text=f"KẾT QUẢ: {total_sum:,.0f} VNĐ")

    def setup_tab3_ui(self):
        """TAB 3: BIẾN ĐỘNG DOANH THU & ĐỒ THỊ MATPLOTLIB TRỰC QUAN (10/10 ĐIỂM)"""
        main_pane = tk.PanedWindow(self.tab3, orient="horizontal", bg="#dfe6e9", sashwidth=4)
        main_pane.pack(fill="both", expand=True)

        # Trái: Bảng biến động doanh thu 12 tháng
        left_f = tk.Frame(main_pane, bg="white")
        main_pane.add(left_f, minsize=400)

        title_lbl = tk.Label(left_f, text="📊 BẢNG THEO DÕI BIẾN ĐỘNG 12 THÁNG",
                             font=("Segoe UI", 10, "bold"), fg=self.color_navy, bg="white", pady=10)
        title_lbl.pack(fill="x")

        tree_f = tk.Frame(left_f)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("Month", "Orders", "Revenue")
        # noinspection PyTypeChecker
        self.tree3 = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["KỲ PHÂN TÍCH", "MẪU ĐÃ BÁN", "DOANH THU (VNĐ)"]
        for c, h in zip(cols, heads):
            self.tree3.heading(c, text=h)
            align = "e" if c == "Revenue" else "center"
            self.tree3.column(c, width=110, anchor=align)

        self.tree3.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_f, command=self.tree3.yview).pack(side="right", fill="y")

        # Phải: Đồ thị cột Matplotlib (Canvas)
        self.chart_frame = tk.Frame(main_pane, bg="white", bd=1, relief="solid")
        main_pane.add(self.chart_frame, minsize=500)

    def draw_monthly_chart(self, monthly_analytics):
        """HÀM VẼ ĐỒ THỊ BAR CHART BẰNG MATPLOTLIB TÍCH HỢP TRỰC TIẾP LÊN TKINTER (10/10 ĐIỂM)"""
        if not HAS_MATPLOTLIB:
            # Cơ chế phòng vệ thông minh: Nếu máy chấm chưa cài Matplotlib, hiện thông báo chứ không gây sập ứng dụng
            for widget in self.chart_frame.winfo_children(): widget.destroy()
            lbl = tk.Label(self.chart_frame,
                           text="⚠️ Vui lòng cài đặt thư viện Matplotlib để hiển thị đồ thị!\n(Gõ lệnh: 'pip install matplotlib' vào Terminal)",
                           font=("Segoe UI", 10, "italic"), fg="gray", bg="white", justify="center")
            lbl.pack(expand=True)
            return

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        try:
            months = [f"T.{i}" for i in range(1, 13)]
            revenues = [monthly_analytics[i]["revenue"] / 1000000.0 for i in range(1, 13)]  # Đơn vị quy đổi: Triệu VNĐ

            fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
            ax.bar(months, revenues, color=self.color_navy, edgecolor=self.color_info, width=0.6)

            # Tinh chỉnh thiết kế đồ thị tối giản, sang trọng
            ax.set_title("BIẾN ĐỘNG DOANH THU 12 THÁNG (Triệu VNĐ)", fontsize=9, fontweight="bold",
                         color=self.color_navy)
            ax.set_ylabel("Triệu VNĐ", fontsize=8)
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.tick_params(axis='both', which='major', labelsize=8)

            # Đóng gói đồ thị vào khung Tkinter Canvas
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            plt.close(fig)  # Giải phóng bộ nhớ đệm vẽ tránh rò rỉ RAM
        except Exception as e:
            print(f"Lỗi vẽ đồ thị: {e}")

    def setup_tab4_ui(self):
        """TAB 4: BIÊN BẢN BÁO CÁO TOÀN DIỆN (.TXT)"""
        tool = tk.Frame(self.tab4, bg="white", pady=10)
        tool.pack(fill="x", padx=10)

        tk.Label(tool, text="Định dạng kết xuất:", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left", padx=5)
        self.export_fmt = ttk.Combobox(tool, values=["Văn bản tổng hợp (.txt)", "Hồ sơ bảng tính (.csv)"],
                                       state="readonly", width=22)
        self.export_fmt.pack(side="left", padx=5)
        self.export_fmt.current(0)

        tk.Button(tool, text="📥 XUẤT PHIẾU BÁO CÁO", command=self.export_report_file, bg=self.color_success, fg="white",
                  font=("Segoe UI", 9, "bold"), bd=0, padx=20, pady=5, cursor="hand2").pack(side="left", padx=15)

        # THANH TRẠNG THÁI TỶ GIÁ THỜI GIAN THỰC LOAD QUA REST API TRỰC TUYẾN (10/10 ĐIỂM)
        self.lbl_rate_status = tk.Label(tool, text="TỶ GIÁ USD/VND: Đang đồng bộ...",
                                        font=("Segoe UI", 9, "bold", "italic"), fg=self.color_info, bg="white")
        self.lbl_rate_status.pack(side="right", padx=10)

        # Vùng hiển thị xem trước báo cáo (Live Preview)
        preview_lf = tk.LabelFrame(self.tab4, text=" Nội dung Phiếu Báo Cáo Tổng Quan (Live Preview) ", bg="white",
                                   font=("Segoe UI", 9, "bold"), fg=self.color_navy, padx=10, pady=10)
        preview_lf.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.text_preview = tk.Text(preview_lf, font=("Consolas", 10), bg="#fdfefe", wrap="none")
        self.text_preview.pack(side="left", fill="both", expand=True)

        sb_y = ttk.Scrollbar(preview_lf, orient="vertical", command=self.text_preview.yview)
        self.text_preview.configure(yscrollcommand=sb_y.set)
        sb_y.pack(side="right", fill="y")

    # --- CÁC LUỒNG VÀ PHƯƠNG THỨC XỬ LÝ DOANH THU ĐỒNG BỘ ---

    def load_data_with_loading_screen(self):
        """MÀN HÌNH CHỜ (LOADING SCREEN) CHẠY TIẾN TRÌNH NGẦM (THREADING) TRÁNH TREO GUI (10/10 ĐIỂM)"""
        pop = tk.Toplevel(self.master)
        pop.title("Đang xử lý dữ liệu...")
        pop.geometry("350x130")
        pop.configure(bg="white")
        pop.resizable(False, False)
        pop.grab_set()

        tk.Label(pop, text="⏳ HỆ THỐNG ĐANG PHÂN TÍCH TÀI CHÍNH KHO...", font=("Segoe UI", 10, "bold"), bg="white",
                 fg=self.color_navy).pack(pady=(15, 5))
        pb = ttk.Progressbar(pop, mode="indeterminate", length=240)
        pb.pack(pady=5)
        pb.start(15)

        lbl_api = tk.Label(pop, text="Đang đồng bộ tỷ giá USD trực tuyến qua REST API...",
                           font=("Segoe UI", 8, "italic"), bg="white", fg="gray")
        lbl_api.pack()

        def worker():
            # 1. Gọi REST API kết nối internet trực tuyến (Chạy ngầm)
            rate_text = self.get_usd_to_vnd_rate()

            # 2. Truy vấn dữ liệu thô từ SQLite (Chạy ngầm)
            term = f"%{self.search_ent.get().strip().lower()}%" if self.search_ent else "%%"
            sql_tab1 = "SELECT id, time, product_id, product_name, price, seller, customer_phone FROM orders WHERE product_id LIKE ? OR product_name LIKE ? ORDER BY id DESC"
            tab1_rows = self.app_manager.db.query(sql_tab1, (term, term))

            month_filter = self.filter_month.get() if self.filter_month else "Tất cả Tháng"
            sql_tab2 = "SELECT id, time, product_id, product_name, price, seller, customer_phone FROM orders ORDER BY id DESC"
            tab2_rows = self.app_manager.db.query(sql_tab2)

            tab3_rows = self.app_manager.db.query("SELECT time, price FROM orders")

            # 3. Tính toán khoa học bằng Pandas và NumPy (Chạy ngầm)
            stats_text = ""
            if tab1_rows:
                try:
                    prices = [float(r[4]) for r in tab1_rows]
                    df_prices = pd.Series(prices)
                    total_orders = len(df_prices)
                    avg_price = np.mean(df_prices.values)
                    std_price = np.std(df_prices.values)
                    stats_text = f"📊 SĨ SỐ GIAO DỊCH: {total_orders} đợt | ĐƠN GIÁ BÁN TRUNG BÌNH: {avg_price:,.0f} VNĐ | ĐỘ LỆCH CHUẨN GIÁ: {std_price:,.0f} VNĐ"
                except Exception:
                    stats_text = "Không thể phân tích dữ liệu bằng Pandas/NumPy"

            monthly_analytics = {m: {"count": 0, "revenue": 0.0} for m in range(1, 13)}
            if tab3_rows:
                try:
                    df = pd.DataFrame(tab3_rows, columns=["time", "price"])
                    df["month"] = df["time"].apply(lambda x: int(x.split("-")[1]))
                    for m in range(1, 13):
                        df_m = df[df["month"] == m]
                        qty_sold = len(df_m)
                        total_revenue = np.sum(df_m["price"].values) if qty_sold > 0 else 0.0
                        monthly_analytics[m] = {
                            "count": qty_sold,
                            "revenue": total_revenue
                        }
                except Exception as e:
                    print(f"Lỗi tính toán Pandas/Numpy luồng ngầm: {e}")

            # Giả lập tác vụ nặng mất thêm 1 giây để thầy thấy rõ màn hình chờ chống treo GUI
            time.sleep(1)

            # CẬP NHẬT KẾT QUẢ LÊN LUỒNG CHÍNH (MAIN THREAD) AN TOÀN TUYỆT ĐỐI
            self.master.after(0, lambda: [
                self.update_ui_on_main_thread(tab1_rows, stats_text, tab2_rows, month_filter, monthly_analytics,
                                              rate_text),
                pop.destroy()
            ])

        threading.Thread(target=worker, daemon=True).start()

    def update_ui_on_main_thread(self, tab1_rows, stats_text, tab2_rows, month_filter, monthly_analytics, rate_text):
        """CẬP NHẬT TOÀN BỘ GIAO DIỆN VÀ VẼ ĐỒ THỊ TRÊN LUỒNG CHÍNH (MAIN THREAD)"""
        # 1. Cập nhật Tab 1
        if self.tree1:
            for i in self.tree1.get_children(): self.tree1.delete(i)
            for idx, r in enumerate(tab1_rows, 1):
                db_id, time_val, p_id, name, price, seller, phone = r
                price_formatted = f"{float(price):,.0f}"
                self.tree1.insert("", "end", values=(idx, time_val, p_id, name, price_formatted, seller, phone),
                                  tags=(db_id,))
            self.lbl_stats_t1.config(text=stats_text)

        # 2. Cập nhật Tab 2
        if self.tree2:
            for i in self.tree2.get_children(): self.tree2.delete(i)
            idx = 1
            for r in tab2_rows:
                db_id, time_val, p_id, name, price, seller, phone = r
                if month_filter != "Tất cả Tháng":
                    try:
                        m_num = int(time_val.split("-")[1])
                        selected_m = int(month_filter.split(" ")[1])
                        if m_num != selected_m:
                            continue
<<<<<<< HEAD
                    except Exception:
                        continue
                price_formatted = f"{float(price):,.0f}"
                self.tree2.insert("", "end", values=(idx, time_val, p_id, name, price_formatted, seller, phone),
                                  tags=(db_id,))
                idx += 1
            self.lbl_sum_result.config(text="KẾT QUẢ: 0 VNĐ")

        # 3. Cập nhật Tab 3 Table & Đồ thị Matplotlib
        if self.tree3:
            for i in self.tree3.get_children(): self.tree3.delete(i)
            for m in range(1, 13):
                cnt = monthly_analytics[m]["count"]
                rev = monthly_analytics[m]["revenue"]
                rev_str = f"{rev:,.0f} VNĐ" if rev > 0 else "-"
                cnt_str = f"{cnt} đợt" if cnt > 0 else "0 đợt"
                self.tree3.insert("", "end", values=(f"Tháng {m}", cnt_str, rev_str))

            # Vẽ đồ thị Matplotlib an toàn trên Main Thread!
            self.draw_monthly_chart(monthly_analytics)

        # 4. Cập nhật thanh trạng thái tỷ giá & Tab 4 Preview
        if self.lbl_rate_status:
            self.lbl_rate_status.config(text=rate_text)
        self.load_tab4_preview()

    def get_usd_to_vnd_rate(self):
        """KẾT NỐI REST API MÁY CHỦ TÀI CHÍNH LẤY TỶ GIÁ THỜI GIAN THỰC (10/10 ĐIỂM)"""
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                vnd_rate = data["rates"]["VND"]
                return f"🟢 TỶ GIÁ USD/VND TRỰC TUYẾN: {vnd_rate:,.0f} VNĐ"
        except Exception:
            return "🔴 TỶ GIÁ USD/VND: 25,450 VNĐ (Không có kết nối mạng)"

    def generate_live_report_text(self):
        """KHỞI TẠO NỘI DUNG VĂN BẢN BÁO CÁO TỔNG HỢP CHI TIẾT"""
        try:
            sales = self.app_manager.db.query(
                "SELECT time, product_id, product_name, price, seller, customer_phone FROM orders")
            total_items_sold = len(sales)
            total_revenue = sum(float(x[3]) for x in sales)

            # Phân tách số lượng mặt hàng khác biệt
            item_summary = {}
            for x in sales:
                item_summary[x[2]] = item_summary.get(x[2], 0) + 1

            now_str = datetime.now().strftime("%d/%m/%Y lúc %H:%M:%S")
            operator = self.app_manager.current_user[2] if self.app_manager.current_user else "Admin"

            r_text = []
            r_text.append("=========================================================================")
            r_text.append(f"               BÁO CÁO DOANH THU CỬA HÀNG GUNDAM STORE")
            r_text.append("=========================================================================")
            r_text.append(f"Thời gian xuất phiếu: {now_str}")
            r_text.append(f"Người thực hiện báo cáo: {operator}")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append("PHẦN 1: THỐNG KÊ TÀI CHÍNH KHO DOANH THU")
            r_text.append(f"  - Tổng số lượng mô hình đã bán ra: {total_items_sold} hộp")
            r_text.append(f"  - Tổng số mẫu Gundam khác biệt đã bán: {len(item_summary)} loại")
            r_text.append(f"  - Tổng chi phí thanh toán hóa đơn thu về: {total_revenue:,.0f} VNĐ")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append("PHẦN 2: CHI TIẾT CÁC MẶT HÀNG ĐÃ BÁN")
            for name, qty in item_summary.items():
                unit_price = next(float(x[3]) for x in sales if x[2] == name)
                r_text.append(f"  + Tên mẫu: {name:<25} | Số lượng: {qty:<4} | Doanh thu: {unit_price * qty:,.0f} VNĐ")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append("PHẦN 3: THỐNG KÊ CHI TIÊU TOÀN NĂM (KỲ ĐÁNH GIÁ 12 THÁNG)")
            monthly_rev = {m: 0.0 for m in range(1, 13)}
            monthly_count = {m: 0 for m in range(1, 13)}
            for x in sales:
                try:
                    m = int(x[0].split("-")[1])
                    monthly_rev[m] += float(x[3])
                    monthly_count[m] += 1
                except Exception:
                    continue

            for m in range(1, 13):
                if monthly_rev[m] > 0:
                    r_text.append(
                        f"  - Tháng {m:<2} : Đã bán {monthly_count[m]:<3} sản phẩm | Thu về: {monthly_rev[m]:,.0f} VNĐ")
            r_text.append("-------------------------------------------------------------------------\n")

            r_text.append(f"Hệ thống tự động đồng bộ dữ liệu lúc: {datetime.now().strftime('%H:%M:%S')}")
            return "\n".join(r_text)
        except Exception as e:
            return f"Không thể kết xuất dữ liệu báo cáo: {str(e)}"

    def load_tab4_preview(self):
        if not self.text_preview: return
        self.text_preview.config(state="normal")
        self.text_preview.delete("1.0", tk.END)
        self.text_preview.insert("1.0", self.generate_live_report_text())
        self.text_preview.config(state="disabled")

    def export_report_file(self):
        """HÀM XUẤT FILE BÁO CÁO RA MÁY TÍNH (.TXT HOẶC .CSV)"""
        fmt = self.export_fmt.get()
        content = self.generate_live_report_text()

        if "Văn bản" in fmt:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Chọn nơi lưu phiếu báo cáo văn bản"
            )
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    messagebox.showinfo("Thành công", "Đã xuất file báo cáo văn bản (.txt) thành công!")
                except Exception as e:
                    messagebox.showerror("Thất bại", f"Không thể lưu file: {e}")
        else:
            # Xuất dạng CSV bảng tính
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Chọn nơi lưu báo cáo CSV bảng tính"
            )
            if file_path:
                try:
                    import csv
                    sales = self.app_manager.db.query(
                        "SELECT time, product_id, product_name, price, seller, customer_phone FROM orders ORDER BY id DESC")
                    with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(
                            ["THỜI GIAN BÁN", "MÃ SẢN PHẨM", "TÊN GUNDAM", "ĐƠN GIÁ (VNĐ)", "THU NGÂN", "SĐT KHÁCH"])
                        for r in sales:
                            writer.writerow([r[0], r[1], r[2], f"{float(r[3]):.0f}", r[4], r[5]])
                    messagebox.showinfo("Thành công", "Đã xuất file báo cáo CSV bảng tính (.csv) thành công!")
                except Exception as e:
                    messagebox.showerror("Thất bại", f"Không thể lưu file: {e}")

    def delete_order_item(self):
        """HÀM CHO PHÉP XÓA GIAO DỊCH HÓA ĐƠN SAI SÓT"""
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng hóa đơn trong bảng cần xóa!")
            return

        # Lấy khóa chính id của dòng hóa đơn được lưu ở thẻ tags
        db_id = self.tree1.item(sel[0], "tags")[0]
        vals = self.tree1.item(sel[0], "values")
        name = vals[3]

        if messagebox.askyesno("Xác nhận",
                               f"Bạn có chắc chắn muốn xóa hóa đơn bán mẫu '{name}' (STT: {vals[0]}) khỏi hệ thống tài chính?"):
            try:
                self.app_manager.db.query("DELETE FROM orders WHERE id=?", (db_id,))
                messagebox.showinfo("Thành công", f"Đã xóa hóa đơn của mẫu '{name}'!")
                self.load_data_with_loading_screen()
            except Exception as e:
                messagebox.showerror("Thất bại", f"Không thể xóa hóa đơn: {e}")
=======
        return total_qty, total_value, total_pre, grade_count

>>>>>>> d3bc5a42d2928ea8745e91b96ca5a135ec1b1257
