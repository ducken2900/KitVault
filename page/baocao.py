import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import urllib.request
import json
import threading
import time

import pandas as pd
import numpy as np

try:
    import matplotlib

    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class BaoCaoPage:
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
        self.tree3 = None
        self.chart_frame = None
        self.text_preview = None
        self.search_ent = None
        self.filter_month = None
        self.lbl_sum_result = None
        self.lbl_rate_status = None

        self.setup_dark_styles()
        self.view()
        self.load_data_with_loading_screen()

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

        tk.Label(header, text="📊 TRUNG TÂM PHÂN TÍCH & BÁO CÁO CHI TIẾT",
                 font=("Segoe UI", 16, "bold"), fg="white", bg=self.color_navy).pack(side="left", padx=20, pady=(5, 0))

        btn_back = tk.Button(header, text="QUAY LẠI MENU", command=self.app_manager.show_menu_page,
                             bg=self.color_danger, fg="white", font=("Arial", 8, "bold"), bd=0, padx=15)
        btn_back.pack(side="right", padx=20, pady=(5, 0))
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#c0392b"))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg=self.color_danger))

        body = tk.Frame(self.master, bg=self.color_dark, padx=15, pady=10)
        body.pack(fill="both", expand=True)

        self.nb = ttk.Notebook(body)
        self.nb.pack(fill="both", expand=True)

        self.tab1 = tk.Frame(self.nb, bg="#22242b")
        self.tab2 = tk.Frame(self.nb, bg="#22242b")
        self.tab3 = tk.Frame(self.nb, bg="#22242b")
        self.tab4 = tk.Frame(self.nb, bg="#22242b")

        self.nb.add(self.tab1, text="  1. Chi tiết hóa đơn bán hàng  ")
        self.nb.add(self.tab2, text="  2. Tổng hợp doanh thu kỳ  ")
        self.nb.add(self.tab3, text="  3. Biến động doanh thu định kỳ  ")
        self.nb.add(self.tab4, text="  4. Phiếu báo cáo văn bản (.txt)  ")

        self.setup_tab1_ui()
        self.setup_tab2_ui()
        self.setup_tab3_ui()
        self.setup_tab4_ui()

    def setup_tab1_ui(self):
        tool = tk.Frame(self.tab1, bg="#22242b", pady=10, padx=10)
        tool.pack(fill="x")

        tk.Label(tool, text="Tìm kiếm (SĐT/Tên hàng):", font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").pack(side="left", padx=5)
        self.search_ent = tk.Entry(tool, font=("Segoe UI", 10), bg=self.color_dark, fg="white", insertbackground="white", bd=1, relief="solid")
        self.search_ent.config(highlightbackground=self.color_border)
        self.search_ent.pack(side="left", padx=5, ipady=2)
        self.search_ent.bind('<KeyRelease>', lambda e: self.load_tab1_data())

        btn_delete = tk.Button(tool, text="Xóa hóa đơn chọn", command=self.delete_order_item, bg=self.color_danger, fg="white",
                  font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2")
        btn_delete.pack(side="right", padx=5)
        btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#c0392b"))
        btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg=self.color_danger))

        btn_detail = tk.Button(tool, text="👁️ Xem chi tiết hóa đơn", command=self.show_invoice_detail_popup, bg=self.color_info,
                  fg="white", font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2")
        btn_detail.pack(side="right", padx=5)
        btn_detail.bind("<Enter>", lambda e: btn_detail.config(bg="#0097e6"))
        btn_detail.bind("<Leave>", lambda e: btn_detail.config(bg=self.color_info))

        btn_refresh = tk.Button(tool, text="🔄 Làm mới", command=self.load_data_with_loading_screen, bg="#34495e", fg="white",
                  font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2")
        btn_refresh.pack(side="right", padx=5)
        btn_refresh.bind("<Enter>", lambda e: btn_refresh.config(bg="#2c3e50"))
        btn_refresh.bind("<Leave>", lambda e: btn_refresh.config(bg="#34495e"))

        tree_f = tk.Frame(self.tab1, bg="#22242b")
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Price", "Seller", "Cust")
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
        sb1 = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=sb1.set)
        sb1.pack(side="right", fill="y")

        self.tree1.bind("<Double-1>", lambda e: self.show_invoice_detail_popup())

        stats_bar = tk.Frame(self.tab1, bg=self.color_card, pady=8)
        stats_bar.pack(fill="x", padx=10, pady=(5, 10))
        stats_bar.config(highlightbackground=self.color_border)

        self.lbl_stats_t1 = tk.Label(stats_bar, text="📊 Đang phân tích dữ liệu thống kê bằng NumPy & Pandas...",
                                     font=("Segoe UI", 9, "bold"), fg=self.color_teal, bg=self.color_card)
        self.lbl_stats_t1.pack(anchor="center")

    def show_invoice_detail_popup(self):
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
                     fg="#1e3799").pack()
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
                     fg="#e74c3c").pack(anchor="e")

            tk.Button(pop, text="ĐÓNG CỬA SỔ", command=pop.destroy, bg="#2d3436", fg="white",
                      font=("Segoe UI", 10, "bold"), bd=0, height=2, cursor="hand2").pack(fill="x", side="bottom")
        except Exception as ex:
            messagebox.showerror("Lỗi hệ thống", f"Không thể kết xuất chi tiết hóa đơn: {str(ex)}")

    def setup_tab2_ui(self):
        tool = tk.Frame(self.tab2, bg="#22242b", pady=10, padx=10)
        tool.pack(fill="x")

        tk.Label(tool, text="Lọc theo Kỳ Tháng:", font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").pack(side="left", padx=5)
        months = ["Tất cả Tháng"] + [f"Tháng {i}" for i in range(1, 13)]
        self.filter_month = ttk.Combobox(tool, values=months, state="readonly", width=12)
        self.filter_month.pack(side="left", padx=5)
        self.filter_month.current(0)
        self.filter_month.bind("<<ComboboxSelected>>", lambda e: self.load_tab2_data())

        tree_f = tk.Frame(self.tab2, bg="#22242b")
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Price", "Seller", "Cust")
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
        sb2 = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y")

        bottom_bar = tk.Frame(self.tab2, bg="#22242b", pady=15, padx=10)
        bottom_bar.pack(fill="x")

        self.lbl_sum_result = tk.Label(bottom_bar, text="TỔNG DOANH THU KỲ: 0 VNĐ", font=("Segoe UI", 14, "bold"),
                                       fg=self.color_success, bg="#22242b")
        self.lbl_sum_result.pack(side="right", padx=10)

    def calculate_tab2_sum(self):
        total_sum = 0.0
        for item in self.tree2.get_children():
            vals = self.tree2.item(item, "values")
            try:
                clean_price = vals[4].replace(",", "").replace(" ", "").strip()
                if "." in clean_price:
                    clean_price = clean_price.split(".")[0]
                total_sum += float(clean_price)
            except (ValueError, IndexError):
                continue
        self.lbl_sum_result.config(text=f"TỔNG DOANH THU KỲ: {total_sum:,.0f} VNĐ")
    def setup_tab3_ui(self):
        main_pane = tk.PanedWindow(self.tab3, orient="horizontal", bg="#1c1d22", sashwidth=4)
        main_pane.pack(fill="both", expand=True)

        left_f = tk.Frame(main_pane, bg="#22242b")
        main_pane.add(left_f, minsize=400)

        title_lbl = tk.Label(left_f, text="📊 BẢNG THEO DÕI BIẾN ĐỘNG 12 THÁNG",
                             font=("Segoe UI", 10, "bold"), fg=self.color_teal, bg="#22242b", pady=10)
        title_lbl.pack(fill="x")

        tree_f = tk.Frame(left_f, bg="#22242b")
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("Month", "Orders", "Revenue")
        self.tree3 = ttk.Treeview(tree_f, columns=cols, show="headings")
        heads = ["KỲ PHÂN TÍCH", "MẪU ĐÃ BÁN", "DOANH THU (VNĐ)"]
        for c, h in zip(cols, heads):
            self.tree3.heading(c, text=h)
            align = "e" if c == "Revenue" else "center"
            self.tree3.column(c, width=110, anchor=align)

        self.tree3.pack(side="left", fill="both", expand=True)
        sb3 = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree3.yview)
        self.tree3.configure(yscrollcommand=sb3.set)
        sb3.pack(side="right", fill="y")

        self.chart_frame = tk.Frame(main_pane, bg="#22242b", bd=1, relief="solid")
        self.chart_frame.config(highlightbackground=self.color_border)
        main_pane.add(self.chart_frame, minsize=500)

    def draw_monthly_chart(self, monthly_analytics):
        if not HAS_MATPLOTLIB:
            for widget in self.chart_frame.winfo_children(): widget.destroy()
            lbl = tk.Label(self.chart_frame,
                           text="⚠️ Vui lòng cài đặt thư viện Matplotlib để hiển thị đồ thị!\n(Gõ lệnh: 'pip install matplotlib' vào Terminal)",
                           font=("Segoe UI", 10, "italic"), fg="gray", bg="#22242b", justify="center")
            lbl.pack(expand=True)
            return

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        try:
            months = [f"T.{i}" for i in range(1, 13)]
            revenues = [monthly_analytics[i]["revenue"] / 1000000.0 for i in range(1, 13)]

            fig, ax = plt.subplots(figsize=(6, 3), dpi=100, facecolor="#22242b")
            ax.set_facecolor("#22242b")
            ax.bar(months, revenues, color=self.color_teal, edgecolor="#1abc9c", width=0.6)

            ax.set_title("BIÊN ĐỘNG DOANH THU 12 THÁNG (Triệu VNĐ)", fontsize=9, fontweight="bold",
                         color="white")
            ax.set_ylabel("Triệu VNĐ", fontsize=8, color="#a4b0be")
            ax.grid(True, linestyle="--", alpha=0.2, color="#3d414e")
            ax.tick_params(axis='both', which='major', labelsize=8, colors="#a4b0be")

            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)
            ax.spines["left"].set_color("#3d414e")
            ax.spines["bottom"].set_color("#3d414e")

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            plt.close(fig)
        except Exception as e:
            print(f"Lỗi vẽ đồ thị: {e}")

    def setup_tab4_ui(self):
        tool = tk.Frame(self.tab4, bg="#22242b", pady=10, padx=10)
        tool.pack(fill="x")

        tk.Label(tool, text="Định dạng kết xuất:", font=("Segoe UI", 9, "bold"), bg="#22242b", fg="#a4b0be").pack(side="left", padx=5)
        self.export_fmt = ttk.Combobox(tool, values=["Văn bản tổng hợp (.txt)", "Hồ sơ bảng tính (.csv)"],
                                       state="readonly", width=22)
        self.export_fmt.pack(side="left", padx=5)
        self.export_fmt.current(0)

        btn_export = tk.Button(tool, text="📥 XUẤT PHIẾU BÁO CÁO", command=self.export_report_file, bg=self.color_success, fg="white",
                  font=("Segoe UI", 9, "bold"), bd=0, padx=20, pady=5, cursor="hand2")
        btn_export.pack(side="left", padx=15)
        btn_export.bind("<Enter>", lambda e: btn_export.config(bg="#218c53"))
        btn_export.bind("<Leave>", lambda e: btn_export.config(bg=self.color_success))

        self.lbl_rate_status = tk.Label(tool, text="TỶ GIÁ USD/VND: Đang đồng bộ...",
                                        font=("Segoe UI", 9, "bold", "italic"), fg=self.color_info, bg="#22242b")
        self.lbl_rate_status.pack(side="right", padx=10)

        preview_lf = tk.LabelFrame(self.tab4, text=" Nội dung Phiếu Báo Cáo Tổng Quan (Live Preview) ", bg="#22242b",
                                   font=("Segoe UI", 9, "bold"), fg=self.color_teal, padx=10, pady=10)
        preview_lf.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        preview_lf.config(highlightbackground=self.color_border)

        self.text_preview = tk.Text(preview_lf, font=("Consolas", 10), bg="#1c1d22", fg="#f5f6fa", wrap="none", insertbackground="white", bd=1, relief="solid")
        self.text_preview.pack(side="left", fill="both", expand=True)

        sb_y = ttk.Scrollbar(preview_lf, orient="vertical", command=self.text_preview.yview)
        self.text_preview.configure(yscrollcommand=sb_y.set)
        sb_y.pack(side="right", fill="y")

    def load_data_with_loading_screen(self):
        pop = tk.Toplevel(self.master)
        pop.title("Đang xử lý dữ liệu...")
        pop.geometry("350x130")
        pop.configure(bg="white")
        pop.resizable(False, False)
        pop.grab_set()

        tk.Label(pop, text="⏳ HỆ THỐNG ĐANG PHÂN TÍCH TÀI CHÍNH KHO...", font=("Segoe UI", 10, "bold"), bg="white",
                 fg="#1e3799").pack(pady=(15, 5))
        pb = ttk.Progressbar(pop, mode="indeterminate", length=240)
        pb.pack(pady=5)
        pb.start(15)

        lbl_api = tk.Label(pop, text="Đang đồng bộ tỷ giá USD trực tuyến qua REST API...",
                           font=("Segoe UI", 8, "italic"), bg="white", fg="gray")
        lbl_api.pack()

        def worker():
            rate_text = self.get_usd_to_vnd_rate()

            term = f"%{self.search_ent.get().strip().lower()}%" if self.search_ent else "%%"
            sql_tab1 = "SELECT id, time, product_id, product_name, price, seller, customer_phone FROM orders WHERE product_id LIKE ? OR product_name LIKE ? ORDER BY id DESC"
            tab1_rows = self.app_manager.db.query(sql_tab1, (term, term))

            month_filter = self.filter_month.get() if self.filter_month else "Tất cả Tháng"
            sql_tab2 = "SELECT id, time, product_id, product_name, price, seller, customer_phone FROM orders ORDER BY id DESC"
            tab2_rows = self.app_manager.db.query(sql_tab2)

            tab3_rows = self.app_manager.db.query("SELECT time, price FROM orders")

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

            time.sleep(1)

            self.master.after(0, lambda: [
                self.update_ui_on_main_thread(tab1_rows, stats_text, tab2_rows, month_filter, monthly_analytics,
                                              rate_text),
                pop.destroy()
            ])

        threading.Thread(target=worker, daemon=True).start()

    def update_ui_on_main_thread(self, tab1_rows, stats_text, tab2_rows, month_filter, monthly_analytics, rate_text):
        if self.tree1:
            for i in self.tree1.get_children(): self.tree1.delete(i)
            for idx, r in enumerate(tab1_rows, 1):
                db_id, time_val, p_id, name, price, seller, phone = r
                price_formatted = f"{float(price):,.0f}"
                self.tree1.insert("", "end", values=(idx, time_val, p_id, name, price_formatted, seller, phone),
                                  tags=(db_id,))
            self.lbl_stats_t1.config(text=stats_text)

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
            self.calculate_tab2_sum()

        if self.tree3:
            for i in self.tree3.get_children(): self.tree3.delete(i)
            for m in range(1, 13):
                cnt = monthly_analytics[m]["count"]
                rev = monthly_analytics[m]["revenue"]
                rev_str = f"{rev:,.0f} VNĐ" if rev > 0 else "-"
                cnt_str = f"{cnt} đợt" if cnt > 0 else "0 đợt"
                self.tree3.insert("", "end", values=(f"Tháng {m}", cnt_str, rev_str))

            self.draw_monthly_chart(monthly_analytics)

        if self.lbl_rate_status:
            self.lbl_rate_status.config(text=rate_text)
        self.load_tab4_preview()

    def get_usd_to_vnd_rate(self):
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
        try:
            sales = self.app_manager.db.query(
                "SELECT time, product_id, product_name, price, seller, customer_phone FROM orders")
            total_items_sold = len(sales)
            total_revenue = sum(float(x[3]) for x in sales)

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
        sel = self.tree1.selection()
        if not sel:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một dòng hóa đơn trong bảng cần xóa!")
            return

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

    def load_tab1_data(self):
        self.load_data_with_loading_screen()

    def load_tab2_data(self):
        self.load_data_with_loading_screen()