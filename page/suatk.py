import tkinter as tk
from tkinter import messagebox, ttk


class SuaTKPage:
    def __init__(self, master, app_manager, item_data):
        self.master = master
        self.app_manager = app_manager
        # item_data nhận từ bảng kho: [ID, Name, Grade, Stock, PreOrder, Price, Date, Status]
        self.item_data = item_data
        self.old_id = item_data[0]  # Lưu mã cũ để làm điều kiện WHERE trong SQL

        # Khai báo thuộc tính lưu các ô nhập liệu
        self.ents = {}

        self.view()

    def view(self):
        # Header - Màu Cam Cảnh Báo
        header_bg = "#e67e22"
        header = tk.Frame(self.master, bg=header_bg)
        header.pack(fill="x")
        tk.Label(header, text="⚙️ CẬP NHẬT THÔNG TIN MÔ HÌNH", font=("Segoe UI", 18, "bold"),
                 fg="white", bg=header_bg).pack(pady=25)

        # Khung chứa Form nhập liệu chính
        body = tk.Frame(self.master, padx=40, pady=20)
        body.pack(fill="both", expand=True)

        # Danh sách cấu hình lựa chọn
        grades = ["EG", "SD", "HG", "RG", "MG", "PG", "Mega Size"]
        status_list = ["🟢 Còn hàng", "🔴 Hết hàng", "🟡 Sắp hết hàng"]

        # Danh sách các trường dữ liệu hiển thị
        labels = [
            ("Mã Gundam:", "ID"),
            ("Tên mô hình:", "Name"),
            ("Dòng (Grade):", "Grade"),
            ("Số lượng tồn:", "Stock"),
            ("SL Đặt trước:", "PreOrder"),
            ("Giá bán (VNĐ):", "Price"),
            ("Ngày nhập:", "Date"),
            ("Tình trạng:", "Status")
        ]

        # Vòng lặp tự động tạo các nhãn và ô nhập liệu dạng Grid
        for i, (txt, key) in enumerate(labels):
            tk.Label(body, text=txt, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=8)

            current_val = self.item_data[i] if i < len(self.item_data) else ""

            if "Grade" in txt:
                e = ttk.Combobox(body, values=grades, state="readonly", font=("Arial", 10))
                e.grid(row=i, column=1, sticky="ew", padx=10)
                e.set(current_val)
            elif "trạng" in txt:
                e = ttk.Combobox(body, values=status_list, state="readonly", font=("Arial", 10))
                e.grid(row=i, column=1, sticky="ew", padx=10)
                e.set(current_val)
            else:
                e = tk.Entry(body, font=("Arial", 11), bd=1, relief="solid")
                e.grid(row=i, column=1, sticky="ew", padx=10, ipady=3)
                e.insert(0, current_val)

                # Khóa không cho sửa Mã Gundam để tránh lỗi khóa chính cơ sở dữ liệu
                if key == "ID":
                    e.config(state="disabled", disabledbackground="#dfe6e9")

            self.ents[key] = e

        body.columnconfigure(1, weight=1)

        # Cấu hình nhóm nút bấm lưu hoặc hủy bỏ ở chân trang
        btn_f = tk.Frame(self.master, pady=20)
        btn_f.pack(fill="x", padx=100)

        tk.Button(btn_f, text="LƯU THAY ĐỔI", command=self.update,
                  bg="#e67e22", fg="white", font=("Segoe UI", 11, "bold"),
                  bd=0, height=2, cursor="hand2").pack(fill="x", pady=5)

        tk.Button(btn_f, text="HỦY BỎ", command=self.app_manager.show_quanly_kho_page,
                  bg="white", fg="#e67e22", font=("Segoe UI", 9, "underline"),
                  bd=0, cursor="hand2").pack()

    def update(self):
        """XỬ LÝ THU THẬP DỮ LIỆU MỚI VÀ GHI ĐÈ VÀO DATABASE"""
        try:
            # 1. Thu thập dữ liệu và làm sạch dấu phẩy tiền tệ
            p_name = self.ents["Name"].get().strip()
            p_grade = self.ents["Grade"].get()
            p_stock = int(self.ents["Stock"].get().strip())
            p_pre = int(self.ents["PreOrder"].get().strip())
            p_price = float(self.ents["Price"].get().strip().replace(",", ""))
            p_date = self.ents["Date"].get().strip()

            # 2. Tự động hóa đồng bộ trạng thái màu dựa trên lượng tồn kho mới
            if p_stock > 5:
                p_status = "🟢 Còn hàng"
            elif 0 < p_stock <= 5:
                p_status = "🟡 Sắp hết hàng"
            else:
                p_status = "🔴 Hết hàng"

            new_data = (p_name, p_grade, p_stock, p_pre, p_price, p_date, p_status, self.old_id)

        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Số lượng tồn kho phải là số nguyên, đơn giá phải là con số!")
            return

        # 3. Thực thi câu lệnh SQL UPDATE chỉnh sửa mô hình
        sql = """UPDATE products \
                 SET name=?, \
                     grade=?, \
                     stock=?, \
                     pre_order=?, \
                     price=?, \
                     entry_date=?, \
                     status=?
                 WHERE id = ?"""

        try:
            self.app_manager.db.query(sql, new_data)
            messagebox.showinfo("Thành công", f"Đã cập nhật mô hình: {new_data[0]}")
            self.app_manager.show_quanly_kho_page()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể cập nhật thông tin: {str(e)}")