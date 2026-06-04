import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


class QuanLyDonHangPage:
    def __init__(self, master, app_manager, prefill_phone=None):
        self.master = master
        self.app_manager = app_manager
        self.prefill_phone = prefill_phone  # Nhận tham số liên kết để tương thích hệ thống

        # Khởi tạo các thuộc tính để dọn sạch lỗi PyCharm
        self.cart = []
        self.total_bill = 0.0
        self.bill_items = []
        self.tree_s = None
        self.tree_c = None
        self.tree_h = None  # Bảng lịch sử thanh toán
        self.lbl_t = None
        self.lbl_final = None
        self.filter_grade = None
        self.search_ent = None
        self.search_hist_ent = None
        self.spin_qty = None

        # Tiền khách đưa và Tiền thừa trả khách
        self.ent_cash = None
        self.lbl_change = None

        self.view()
        self.load_stock()
        self.load_payment_history()  # Nạp dữ liệu lịch sử thanh toán

        # Tự động quét và thông báo hàng đặt trước đã về kho sau khi giao diện tải xong 1 giây
        self.master.after(1000, self.check_pending_preorders_notification)

    def view(self):
        # Header - Phong cách Mecha Dark Cao cấp
<<<<<<< HEAD
        header = tk.Frame(self.master, bg="#1e3799")
        header.pack(fill="x")

        tk.Label(header, text="🛒 TRẠM GIAO DỊCH BÁN HÀNG POS", font=("Segoe UI", 20, "bold"),
                 fg="white", bg="#1e3799").pack(side="left", padx=20, pady=15)
=======
        header = tk.Frame(self.master, bg="#2c3e50")
        header.pack(fill="x")

        tk.Label(header, text="🛒 TRẠM GIAO DỊCH BÁN HÀNG POS", font=("Segoe UI", 20, "bold"),
                 fg="#1abc9c", bg="#2c3e50").pack(side="left", padx=20, pady=15)
>>>>>>> d3bc5a42d2928ea8745e91b96ca5a135ec1b1257

        tk.Button(header, text="QUAY LẠI MENU", command=self.app_manager.show_menu_page,
                  bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=20, cursor="hand2").pack(
            side="right", padx=20)

        main = tk.Frame(self.master, bg="#f1f2f6", padx=10, pady=10)
        main.pack(fill="both", expand=True)

        # Sử dụng Notebook để phân tách tab Bán hàng và tab Xem lịch sử thanh toán hóa đơn
        nb = ttk.Notebook(main)
        nb.pack(fill="both", expand=True)

        self.tab_pos = tk.Frame(nb, bg="#f1f2f6")
        self.tab_history = tk.Frame(nb, bg="white")

        nb.add(self.tab_pos, text="  🛒 QUẦY BÁN HÀNG  ")
        nb.add(self.tab_history, text="  📜 LỊCH SỬ THANH TOÁN  ")

        # --- TAB 1: QUẦY BÁN HÀNG ---
        left = tk.LabelFrame(self.tab_pos, text=" CHỌN MÔ HÌNH TRONG KHO ", bg="white", font=("Segoe UI", 10, "bold"),
                             fg="#2c3e50", padx=10,
                             pady=10)
        left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Thanh tìm kiếm và tích hợp bộ lọc Dòng (Grade) mới tinh gọn
        search_f = tk.Frame(left, bg="white")
        search_f.pack(fill="x", pady=(0, 10))

        tk.Label(search_f, text="DÒNG (GRADE):", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left",
                                                                                                padx=(0, 5))
        self.filter_grade = ttk.Combobox(search_f, values=["Tất cả", "EG", "SD", "HG", "RG", "MG", "PG", "Mega Size"],
                                         width=10, state="readonly")
        self.filter_grade.pack(side="left", padx=5)
        self.filter_grade.current(0)
        self.filter_grade.bind("<<ComboboxSelected>>", lambda e: self.load_stock())

        tk.Label(search_f, text="🔍 TÌM KIẾM:", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left", padx=(15, 5))
        self.search_ent = tk.Entry(search_f, font=("Segoe UI", 10), bd=1, relief="solid")
        self.search_ent.pack(side="left", fill="x", expand=True, padx=5, ipady=2)
        self.search_ent.bind('<KeyRelease>', lambda e: self.load_stock())

        # Bảng sản phẩm (Đã bổ sung thêm cột Dòng/Grade)
        # noinspection PyTypeChecker
        self.tree_s = ttk.Treeview(left, columns=("ID", "Name", "Grade", "Price", "Stock", "Date"), show="headings",
                                   height=15)
        heads = ["MÃ GUNDAM", "TÊN MÔ HÌNH", "DÒNG (GRADE)", "GIÁ BÁN (VNĐ)", "TỒN KHO", "NGÀY NHẬP"]
        for c, h in zip(self.tree_s["columns"], heads):
            self.tree_s.heading(c, text=h)
            w = 90 if c in ["ID", "Stock", "Grade"] else 110
            if c == "Name": w = 200
            align = "e" if c == "Price" else "center" if c != "Name" else "w"
            self.tree_s.column(c, width=w, anchor=align)
        self.tree_s.pack(fill="both", expand=True)

        # BIND SỰ KIỆN DOUBLE-CLICK ĐỂ THÊM NHANH 1 SẢN PHẨM VÀO GIỎ
        self.tree_s.bind("<Double-1>", lambda e: self.add_to_cart_double_click())

        # Nhóm công cụ bên trái
        action_left_f = tk.Frame(left, bg="white", pady=10)
        action_left_f.pack(fill="x")

        tk.Label(action_left_f, text="Số lượng mua:", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left")
        self.spin_qty = tk.Spinbox(action_left_f, from_=1, to=99, width=5, justify="center", font=("Segoe UI", 10))
        self.spin_qty.pack(side="left", padx=5)

        tk.Button(action_left_f, text="⬇ THÊM VÀO GIỎ HÀNG", bg="#1e3799", fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=20, cursor="hand2",
                  command=self.add_to_cart).pack(side="left", padx=5)

        # Khung hóa đơn bên phải
        right = tk.LabelFrame(self.tab_pos, text=" CHI TIẾT HÓA ĐƠN THANH TOÁN ", bg="white",
                              font=("Segoe UI", 10, "bold"), fg="#2c3e50", padx=10,
                              pady=10, width=480)
        right.pack(side="right", fill="both", padx=5, pady=5)
        right.pack_propagate(False)

        # noinspection PyTypeChecker
        self.tree_c = ttk.Treeview(right, columns=("N", "Q", "S"), show="headings")
        self.tree_c.heading("N", text="SẢN PHẨM")
        self.tree_c.heading("Q", text="SL")
        self.tree_c.heading("S", text="THÀNH TIỀN (VNĐ)")
        for c in self.tree_c["columns"]:
            align = "e" if c == "S" else "center" if c == "Q" else "w"
            self.tree_c.column(c, width=100 if c != "N" else 220, anchor=align)
        self.tree_c.pack(fill="both", expand=True)

        tk.Button(right, text="🗑 Xóa món đã chọn", command=self.remove_from_cart, fg="#e74c3c",
                  font=("Segoe UI", 9, "underline"), bg="white", bd=0,
                  cursor="hand2").pack(anchor="e", pady=3)

        self.lbl_t = tk.Label(right, text="Tạm tính: 0 VNĐ", font=("Segoe UI", 10, "bold"), fg="#7f8c8d", bg="white")
        self.lbl_t.pack(pady=(10, 0), anchor="e")

        self.lbl_final = tk.Label(right, text="TỔNG: 0 VNĐ",
                                  font=("Consolas", 15, "bold"), fg="#e74c3c", bg="white", justify="right")
        self.lbl_final.pack(pady=5, anchor="e")

        # Khung tính tiền thối cho khách trực tiếp
        calc_f = tk.Frame(right, bg="white", pady=5)
        calc_f.pack(fill="x", pady=5)

        tk.Label(calc_f, text="TIỀN KHÁCH ĐƯA (VNĐ):", bg="white", font=("Segoe UI", 9, "bold")).grid(row=0, column=0,
                                                                                                      sticky="w")
        self.ent_cash = tk.Entry(calc_f, width=18, font=("Segoe UI", 10, "bold"), bd=1, relief="solid", justify="right")
        self.ent_cash.grid(row=0, column=1, padx=5, sticky="ew")
        self.ent_cash.bind('<KeyRelease>', lambda e: self.calculate_change())

        tk.Label(calc_f, text="TIỀN THỪA TRẢ KHÁCH:", bg="white", font=("Segoe UI", 9, "bold")).grid(row=1, column=0,
                                                                                                     sticky="w", pady=5)
        self.lbl_change = tk.Label(calc_f, text="0 VNĐ", bg="white", fg="#2980b9", font=("Segoe UI", 11, "bold"))
        self.lbl_change.grid(row=1, column=1, padx=5, sticky="e", pady=5)

        calc_f.columnconfigure(1, weight=1)

        tk.Button(right, text="💳 XUẤT HÓA ĐƠN & THANH TOÁN", bg="#2ecc71", fg="white",
                  font=("Segoe UI", 11, "bold"), height=2, bd=0, cursor="hand2", command=self.checkout).pack(fill="x")

        # --- TAB 2: KHỞI DỰNG GIAO DIỆN LỊCH SỬ THANH TOÁN ---
        self.setup_payment_history_ui()

    def setup_payment_history_ui(self):
        """THIẾT KẾ PHẦN TRA CỨU LỊCH SỬ THANH TOÁN HÓA ĐƠN"""
        tool = tk.Frame(self.tab_history, bg="white", pady=10)
        tool.pack(fill="x", padx=10)

        tk.Label(tool, text="🔍 Tìm kiếm (SĐT/Tên hàng):", font=("Segoe UI", 9, "bold"), bg="white").pack(side="left")
        self.search_hist_ent = tk.Entry(tool, font=("Segoe UI", 10), bd=1, relief="solid", width=25)
        self.search_hist_ent.pack(side="left", padx=5, ipady=2)
        self.search_hist_ent.bind('<KeyRelease>', lambda e: self.load_payment_history())

        tk.Button(tool, text="🔄 Làm mới danh sách", command=self.load_payment_history, bg="#34495e", fg="white",
                  font=("Segoe UI", 8, "bold"), bd=0, padx=15, pady=5, cursor="hand2").pack(side="right")

        # Bảng hiển thị thông tin hóa đơn đã bán ra
        tree_f = tk.Frame(self.tab_history)
        tree_f.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("STT", "Time", "ID", "Name", "Price", "Seller", "Cust")
        # noinspection PyTypeChecker
        self.tree_h = ttk.Treeview(tree_f, columns=cols, show="headings", height=15)
        heads = ["STT", "THỜI GIAN", "MÃ SẢN PHẨM", "TÊN GUNDAM", "ĐƠN GIÁ (VNĐ)", "THU NGÂN", "SĐT KHÁCH"]
        for c, h in zip(cols, heads):
            self.tree_h.heading(c, text=h)
            w = 50 if c == "STT" else 120
            if c == "Name": w = 240
            if c == "Time": w = 150
            align = "e" if c == "Price" else "center" if c != "Name" else "w"
            self.tree_h.column(c, width=w, anchor=align)

        self.tree_h.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_f, orient="vertical", command=self.tree_h.yview)
        self.tree_h.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

    def load_payment_history(self):
        """TRUY VẤN LỊCH SỬ BÁN HÀNG TỪ DATABASE ĐỒNG BỘ"""
        if not self.tree_h:
            return
        for i in self.tree_h.get_children():
            self.tree_h.delete(i)

        term = f"%{self.search_hist_ent.get().strip().lower()}%"
        sql = """
              SELECT time, product_id, product_name, price, seller, customer_phone
              FROM orders
              WHERE (customer_phone LIKE ? OR product_name LIKE ? OR product_id LIKE ?)
              ORDER BY id DESC \
              """
        try:
            rows = self.app_manager.db.query(sql, (term, term, term))
            for idx, r in enumerate(rows, 1):
                time_val, p_id, name, price, seller, phone = r
                price_formatted = f"{float(price):,.0f}"
                self.tree_h.insert("", "end", values=(idx, time_val, p_id, name, price_formatted, seller, phone))
        except Exception as e:
            print(f"Lỗi tải lịch sử thanh toán: {e}")

    def check_pending_preorders_notification(self):
        """QUÉT DATABASE TỰ ĐỘNG THÔNG BÁO VÀ THANH TOÁN KHI HÀNG ĐẶT TRƯỚC ĐÃ VỀ KHO VÀ ĐỦ SL GIAO"""
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

        # Quét sử dụng rowid để tương thích 100% mọi cơ sở dữ liệu cũ/mới của bạn
        sql = """
              SELECT p.rowid, \
                     p.phone, \
                     p.product_id, \
                     p.product_name, \
                     p.price, \
                     p.quantity, \
                     p.deposit, \
                     pr.stock
              FROM preorder_registrations p
                       JOIN products pr ON p.product_id = pr.id
              WHERE pr.stock >= p.quantity \
              """
        try:
            ready_preorders = self.app_manager.db.query(sql)
            if not ready_preorders:
                return

            for preorder in ready_preorders:
                r_id, phone, pid, name, price, qty, deposit, stock = preorder

                total_price = price * qty
                remaining = total_price - deposit

                msg = (f"🔔 THÔNG BÁO: HÀNG ĐẶT TRƯỚC ĐÃ VỀ KHO VÀ ĐỦ HÀNG GIAO!\n"
                       f"-----------------------------------------\n"
                       f"• Khách hàng (SĐT): {phone}\n"
                       f"• Sản phẩm đặt: {name} (Mã: {pid})\n"
                       f"• Số lượng: {qty} hộp (Tồn kho hiện có: {stock})\n"
                       f"• Tiền cọc đã đóng: {deposit:,.0f} VNĐ\n"
                       f"• Số tiền cần thu nốt: {remaining:,.0f} VNĐ\n"
                       f"-----------------------------------------\n"
                       f"Bạn có muốn hệ thống tự động xử lý thanh toán khấu trừ và xuất hóa đơn giao hàng ngay bây giờ?")

                if messagebox.askyesno("Giao hàng đặt trước tự động", msg):
                    now_order = datetime.now().strftime("%Y-%m-%d %H:%M")
                    operator = self.app_manager.current_user[0] if self.app_manager.current_user else "admin"

                    # 1. Trừ tồn kho vật lý của sản phẩm
                    self.app_manager.db.query(
                        "UPDATE products SET stock = stock - ? WHERE id = ?", (qty, pid)
                    )

                    # 2. Khấu trừ số lượng pre_order trong kho của sản phẩm chính
                    self.app_manager.db.query(
                        "UPDATE products SET pre_order = CASE WHEN pre_order >= ? THEN pre_order - ? ELSE 0 END WHERE id = ?",
                        (qty, qty, pid)
                    )

                    # 3. Xóa bỏ phiếu đặt trước đã hoàn thành bằng rowid
                    self.app_manager.db.query(
                        "DELETE FROM preorder_registrations WHERE rowid = ?", (r_id,)
                    )

                    # 4. Ghi nhận doanh thu bán lẻ vào danh sách hóa đơn chính
                    for _ in range(qty):
                        self.app_manager.db.query(
                            "INSERT INTO orders (time, product_id, product_name, price, seller, customer_phone) VALUES (?, ?, ?, ?, ?, ?)",
                            (now_order, pid, name, price, operator, phone)
                        )

                    # 5. Xuất trực tiếp biên lai thu nốt tiền cọc hoàn tất giao dịch
                    self.show_receipt(
                        bill_data=[{'name': name, 'qty': qty, 'price': total_price}],
                        total=remaining,
                        phone=phone,
                        rank="ĐẶT TRƯỚC",
                        total_deposit=deposit
                    )

                    self.load_stock()
                    self.load_payment_history()  # Đồng bộ danh sách lịch sử sau khi bán
                    break  # Xử lý lần lượt từng thông báo
        except Exception as e:
            print(f"Lỗi quét thông báo đặt trước: {e}")

    def calculate_change(self):
        """TÍNH TIỀN THỐI LẠI CHO KHÁCH TRỰC TIẾP"""
        try:
            cash_str = self.ent_cash.get().strip().replace(",", "")
            if not cash_str:
                self.lbl_change.config(text="0 VNĐ", fg="#2980b9")
                return
            cash_val = float(cash_str)
            change = cash_val - self.total_bill
            if change >= 0:
                self.lbl_change.config(text=f"{change:,.0f} VNĐ", fg="#27ae60")
            else:
                self.lbl_change.config(text="Khách đưa chưa đủ tiền!", fg="#e74c3c")
        except ValueError:
            self.lbl_change.config(text="Nhập số tiền hợp lệ!", fg="#e74c3c")

    def show_receipt(self, bill_data, total, phone, rank, total_deposit=0.0, cash_received=0.0, change_returned=0.0):
        """XUẤT BIÊN LAI IN HÓA ĐƠN TRỰC QUAN KHẤU TRỪ CỌC & TIỀN THỪA TRẢ KHÁCH"""
        res_win = tk.Toplevel(self.master)
        res_win.title("HÓA ĐƠN BÁN HÀNG")
        res_win.geometry("400x600")
        res_win.configure(bg="white")

        receipt_f = tk.Frame(res_win, bg="white", padx=20, pady=20)
        receipt_f.pack(fill="both", expand=True)

        tk.Label(receipt_f, text="KITVAULT GUNDAM STORE", font=("Impact", 18), bg="white", fg="#1e3799").pack()
        tk.Label(receipt_f, text="------------------------------------------------", bg="white").pack()
        tk.Label(receipt_f, text=f"Ngày bán: {datetime.now().strftime('%d/%m/%Y %H:%M')}", bg="white").pack(anchor="w")
        tk.Label(receipt_f,
                 text=f"Thu ngân: {self.app_manager.current_user[2] if self.app_manager.current_user else 'Admin'}",
                 bg="white").pack(anchor="w")
        tk.Label(receipt_f, text=f"Khách hàng: {phone} ({rank})", bg="white").pack(anchor="w")
        tk.Label(receipt_f, text="------------------------------------------------", bg="white").pack()

        for item in bill_data:
            tk.Label(receipt_f, text=f"{item['name']}", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
            tk.Label(receipt_f, text=f"   x{item['qty']} : {item['price']:,.0f} VNĐ", bg="white").pack(anchor="w")

        tk.Label(receipt_f, text="------------------------------------------------", bg="white").pack()

        # Kiểm tra nếu hóa đơn có tiền cọc đặt trước
        if total_deposit > 0:
            tk.Label(receipt_f, text=f"Tổng tiền hàng sau giảm giá: {(total + total_deposit):,.0f} VNĐ",
                     font=("Arial", 9), bg="white").pack(anchor="e")
            tk.Label(receipt_f, text=f"Đã trừ tiền đặt cọc trước: -{total_deposit:,.0f} VNĐ",
                     font=("Arial", 9, "italic"), bg="white", fg="blue").pack(anchor="e")
            tk.Label(receipt_f, text="TIỀN CẦN THU THÊM:", font=("Arial", 10, "bold"), bg="white").pack(anchor="e")
        else:
            tk.Label(receipt_f, text="TỔNG CỘNG THANH TOÁN:", font=("Arial", 10), bg="white").pack(anchor="e")

        tk.Label(receipt_f, text=f"{total:,.0f} VNĐ", font=("Arial", 16, "bold"), bg="white", fg="#d63031").pack(
            anchor="e")

        # In thêm thông tin Tiền thối cho khách trực quan trên hóa đơn
        if cash_received > 0:
            tk.Label(receipt_f, text=f"Tiền khách đưa: {cash_received:,.0f} VNĐ", font=("Arial", 9), bg="white").pack(
                anchor="e")
            tk.Label(receipt_f, text=f"Tiền thừa trả khách: {change_returned:,.0f} VNĐ", font=("Arial", 9, "bold"),
                     bg="white", fg="green").pack(anchor="e")

        tk.Label(receipt_f, text="CẢM ƠN QUÝ KHÁCH - SEE YOU AGAIN!", font=("Arial", 9, "italic"), bg="white",
                 fg="gray").pack(pady=15)

        tk.Button(res_win, text="ĐÓNG & IN HÓA ĐƠN", command=res_win.destroy, bg="#1e3799", fg="white",
                  font=("Arial", 10, "bold"), height=2, bd=0).pack(fill="x", side="bottom")

    def load_stock(self):
        if not self.tree_s: return
        for i in self.tree_s.get_children(): self.tree_s.delete(i)

        # Nhận diện Dòng và Ô tìm kiếm đồng bộ
        grade_filter = self.filter_grade.get() if self.filter_grade else "Tất cả"
        term = f"%{self.search_ent.get().lower()}%"

        if grade_filter == "Tất cả":
            sql = "SELECT id, name, grade, price, stock, entry_date FROM products WHERE id LIKE ? OR name LIKE ?"
            params = (term, term)
        else:
            sql = "SELECT id, name, grade, price, stock, entry_date FROM products WHERE grade = ? AND (id LIKE ? OR name LIKE ?)"
            params = (grade_filter, term, term)

        try:
            rows = self.app_manager.db.query(sql, params)
            for r in rows:
                # Định dạng tiền tệ VNĐ sạch không bị số thực lẻ .0
                price_formatted = f"{float(r[3]):,.0f}"
                self.tree_s.insert("", "end", values=(r[0], r[1], r[2], price_formatted, r[4], r[5]))
        except Exception as e:
            print(f"Lỗi tải danh mục kho: {e}")

    def add_to_cart(self):
        sel = self.tree_s.selection()
        if not sel: return
        v = self.tree_s.item(sel[0], "values")
        qty = int(self.spin_qty.get())
        if int(v[4]) < qty:  # Cột tồn kho hiện tại nằm ở vị trí index 4
            messagebox.showerror("!", "Không đủ hàng trong kho!")
            return

        # Bóc tách dấu phẩy tiền tệ ra để lấy số thực tính toán (Cột giá hiện tại nằm ở index 3)
        price_val = float(v[3].replace(",", ""))
        for _ in range(qty):
            self.cart.append({"id": v[0], "name": v[1], "price": price_val})
        self.update_cart_view()

    def add_to_cart_double_click(self):
        """KÍCH ĐÚP CHUỘT ĐỂ THÊM NHANH 1 SẢN PHẨM VÀO GIỎ HÀNG (DÙNG CHO BÁN LẺ TRỰC TIẾP)"""
        sel = self.tree_s.selection()
        if not sel: return
        v = self.tree_s.item(sel[0], "values")
        qty = 1
        if int(v[4]) < qty:  # Tồn kho ở index 4
            messagebox.showerror("!", "Không đủ hàng trong kho!")
            return

        # Bóc tách tiền tệ (Giá ở index 3)
        price_val = float(v[3].replace(",", ""))
        self.cart.append({"id": v[0], "name": v[1], "price": price_val})
        self.update_cart_view()

    def remove_from_cart(self):
        sel = self.tree_c.selection()
        if sel:
            name = self.tree_c.item(sel[0], "values")[0]
            self.cart = [x for x in self.cart if x['name'] != name]
            self.update_cart_view()

    def update_cart_view(self):
        if not self.tree_c: return
        for i in self.tree_c.get_children(): self.tree_c.delete(i)
        temp_total = 0
        summary = {}
        self.bill_items = []
        for item in self.cart:
            summary[item['name']] = summary.get(item['name'], 0) + 1
            temp_total += item['price']

        for name, qty in summary.items():
            p = next(x['price'] for x in self.cart if x['name'] == name)
            self.tree_c.insert("", "end", values=(name, qty, f"{p * qty:,.0f}"))
            self.bill_items.append({'name': name, 'qty': qty, 'price': p * qty})

        self.lbl_t.config(text=f"Tạm tính: {temp_total:,.0f} VNĐ")
        self.lbl_final.config(text=f"TỔNG: {temp_total:,.0f} VNĐ", fg="#d63031")

        self.total_bill = temp_total

        # Đồng bộ tính lại Tiền thừa ngay lập tức
        self.calculate_change()

    def checkout(self):
        if not self.cart: return
        if messagebox.askyesno("Thanh toán", "Xác nhận giao dịch?"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            phone = "Khách lẻ"  # Cố định đối tượng bán lẻ trực tiếp tại quầy

            sold = {}
            for item in self.cart:
                sold[item['id']] = sold.get(item['id'], 0) + 1
                # Ghi nhận lịch sử đơn hàng
                self.app_manager.db.query(
                    "INSERT INTO orders (time, product_id, product_name, price, seller, customer_phone) VALUES (?,?,?,?,?,?)",
                    (now, item['id'], item['name'], item['price'], self.app_manager.current_user[0], phone))

            # Giảm trừ tồn kho thực tế
            for pid, q in sold.items():
                self.app_manager.db.query("UPDATE products SET stock = stock - ? WHERE id = ?", (q, pid))

            # Đọc thông số tiền khách đưa và tiền thối
            cash_str = self.ent_cash.get().strip().replace(",", "")
            cash_received = float(cash_str) if cash_str else 0.0
            change_returned = max(0.0, cash_received - self.total_bill) if cash_received > 0 else 0.0

            self.show_receipt(self.bill_items, self.total_bill, phone, "BÁN LẺ TRỰC TIẾP", cash_received,
                              change_returned)

            # Reset trạng thái
            self.cart = []
            self.ent_cash.delete(0, tk.END)
            self.load_stock()
            self.load_payment_history()  # Đồng bộ hóa danh sách lịch sử sau khi bán
            self.update_cart_view()