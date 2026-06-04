import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


class TaoTKPage:
    def __init__(self, master, app_manager):
        # Khởi tạo tham số và lưu trữ các ô nhập liệu (ents)
        self.master = master
        self.app_manager = app_manager
        self.ents = {}
        self.view()

    def view(self):
        # Tiêu đề chính của giao diện
        tk.Label(self.master, text="📦 NHẬP HÀNG GUNDAM MỚI", font=("Segoe UI", 18, "bold"), fg="#1e3799").pack(pady=20)

        # Định nghĩa danh sách các dòng gundam (Grade) và các trạng thái
        grades = ["EG", "SD", "HG", "RG", "MG", "PG", "Mega Size"]
        status = ["🟢 Còn hàng", "🔴 Hết hàng", "🟡 Sắp hết hàng"]

        # Danh sách cấu trúc các trường nhập liệu
        labels = [
            ("Mã Gundam:", "ID"),
            ("Tên mô hình:", "Name"),
            ("Dòng (Grade):", "Grade"),
            ("Số lượng nhập:", "Stock"),
            ("SL Đặt trước:", "PreOrder"),
            ("Giá nhập (VNĐ):", "Price"),
            ("Ngày nhập:", "Date"),
            ("Tình trạng:", "Status")
        ]

        form = tk.Frame(self.master, padx=40)
        form.pack(fill="x")

        # Vòng lặp tự động dựng các ô nhập liệu dạng lưới (Grid Layout)
        for i, (txt, key) in enumerate(labels):
            tk.Label(form, text=txt, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=8)

            if "Grade" in txt:
                e = ttk.Combobox(form, values=grades, state="readonly", font=("Arial", 10))
                e.grid(row=i, column=1, sticky="ew", padx=10)
                e.current(2)
            elif "trạng" in txt:
                e = ttk.Combobox(form, values=status, state="readonly", font=("Arial", 10))
                e.grid(row=i, column=1, sticky="ew", padx=10)
                e.current(0)
            else:
                e = tk.Entry(form, font=("Arial", 10), bd=1, relief="solid")
                e.grid(row=i, column=1, sticky="ew", padx=10, ipady=3)
                if any(x in txt for x in ["lượng", "Đặt", "Giá"]):
                    e.insert(0, "0")
                if "Ngày" in txt:
                    e.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.ents[key] = e

        form.columnconfigure(1, weight=1)

        # Cấu hình nhóm nút bấm hành động ở chân trang
        btn_f = tk.Frame(self.master)
        btn_f.pack(pady=30)

        tk.Button(btn_f, text="LƯU VÀO KHO", command=self.save, bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), width=18, height=2, bd=0).pack(side="left", padx=10)

        tk.Button(btn_f, text="HỦY BỎ", command=self.app_manager.show_quanly_kho_page,
                  bg="#636e72", fg="white", font=("Arial", 10), width=12, height=2, bd=0).pack(side="left")

    def save(self):
        """XỬ LÝ LƯU THÔNG TIN SẢN PHẨM MỚI VÀ GHI PHIẾU NHẬP"""
        try:
            # 1. Thu thập và làm sạch dữ liệu từ các ô nhập liệu
            p_id = self.ents["ID"].get().strip()
            p_name = self.ents["Name"].get().strip()
            p_grade = self.ents["Grade"].get()
            p_stock = int(self.ents["Stock"].get().strip())
            p_pre = int(self.ents["PreOrder"].get().strip())
            p_price = float(self.ents["Price"].get().strip())
            p_date = self.ents["Date"].get().strip()

            # 2. Tự động hóa trạng thái sản phẩm dựa trên số lượng nhập thực tế
            if p_stock > 5:
                p_status = "🟢 Còn hàng"
            elif 0 < p_stock <= 5:
                p_status = "🟡 Sắp hết hàng"
            else:
                p_status = "🔴 Hết hàng"

            # Xác định người thực hiện nhập hàng
            op_name = self.app_manager.current_user[2] if self.app_manager.current_user else "Admin"

            if not p_id or not p_name:
                messagebox.showerror("Lỗi", "Vui lòng nhập đủ Mã và Tên!")
                return

            # 3. Ghi đè hoặc thêm mới thông tin vào bảng sản phẩm chính (products)
            sql_p = "INSERT OR REPLACE INTO products (id, name, grade, stock, pre_order, price, entry_date, status) VALUES (?,?,?,?,?,?,?,?)"
            self.app_manager.db.query(sql_p, (p_id, p_name, p_grade, p_stock, p_pre, p_price, p_date, p_status))

            # 4. Ghi nhận phiếu nhập hàng mới vào tệp lịch sử nhập hàng (purchase_history)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_h = "INSERT INTO purchase_history (time, product_id, product_name, quantity, price, operator) VALUES (?,?,?,?,?,?)"
            self.app_manager.db.query(sql_h, (now, p_id, p_name, p_stock, p_price, op_name))

            messagebox.showinfo("Thành công", f"Đã nhập {p_name} và lưu lịch sử!")
            self.app_manager.show_quanly_kho_page()

        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng và Giá phải là số!")