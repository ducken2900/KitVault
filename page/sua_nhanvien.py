import tkinter as tk
from tkinter import messagebox


class SuaNhanVienPage:
    def __init__(self, master, app_manager, data):
        self.master = master
        self.app_manager = app_manager
        # data chứa thông tin nhân viên được truyền từ bảng: [User, Pass, Name, Phone, Role]
        self.data = data
        self.old_username = data[0]  # Lưu giữ Tên đăng nhập gốc để làm điều kiện WHERE trong SQL
        self.ents = {}

        self.view()

    def view(self):
        # Header - Phong cách Mecha Dark
        header = tk.Frame(self.master, bg="#2d3436")
        header.pack(fill="x")
        tk.Label(header, text="⚙️ PHÂN CÔNG NHÂN SỰ", font=("Segoe UI", 18, "bold"),
                 fg="#00a8ff", bg="#2d3436").pack(pady=20)

        # Khung chứa Form nhập liệu
        form = tk.Frame(self.master, padx=40)
        form.pack(pady=20, fill="both")

        # Danh sách nhãn và tương ứng trường dữ liệu nhập
        labels = ["User:", "Pass:", "Tên:", "SĐT:", "Quyền:"]

        # Vòng lặp dựng các ô nhập liệu dạng lưới
        for i, txt in enumerate(labels):
            tk.Label(form, text=txt, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=10)

            # Đổ dữ liệu cũ của nhân sự được chọn vào các trường nhập tương ứng
            old_val = self.data[i] if i < len(self.data) else ""

            e = tk.Entry(form, font=("Arial", 11), bd=0, highlightthickness=1, highlightbackground="#dfe6e9")
            e.grid(row=i, column=1, sticky="ew", padx=10, ipady=5)
            e.insert(0, old_val)

            # KHÓA TÊN ĐĂNG NHẬP: Không cho phép sửa Username để bảo toàn tính toàn vẹn cơ sở dữ liệu
            if txt == "User:":
                e.config(state="disabled", disabledbackground="#dfe6e9")

            self.ents[txt] = e

        form.grid_columnconfigure(1, weight=1)

        # Nút xác nhận lưu cập nhật thông tin nhân viên
        btn_update = tk.Button(self.master, text="CẬP NHẬT NHÂN SỰ", command=self.update,
                               bg="#ffa500", fg="black", font=("Segoe UI", 10, "bold"),
                               bd=0, height=2, cursor="hand2")
        btn_update.pack(pady=20, fill="x", padx=100)

        # Nút Hủy bỏ quay lại giao diện quản trị nhân viên
        tk.Button(self.master, text="HỦY BỎ", command=self.app_manager.show_quanly_taikhoan_page,
                  bg="white", fg="#636e72", font=("Segoe UI", 9), bd=0, cursor="hand2").pack()

    def update(self):
        """XỬ LÝ GHI ĐÈ THÔNG TIN NHÂN SỰ MỚI VÀO CƠ SỞ DỮ LIỆU SQL"""
        u = self.old_username
        p = self.ents["Pass:"].get().strip()
        n = self.ents["Tên:"].get().strip()
        s = self.ents["SĐT:"].get().strip()
        r = self.ents["Quyền:"].get().strip()  # Quyền tự do nhập (ví dụ: Thu ngân, Quản trị viên, Tư vấn...)

        if not p or not n:
            messagebox.showerror("Error", "Mật khẩu và Họ tên nhân viên không được để trống!")
            return

        # Thực thi câu lệnh UPDATE chỉnh sửa thông tin tài khoản nhân sự
        sql = "UPDATE users SET password=?, fullname=?, phone=?, role=? WHERE username=?"
        try:
            self.app_manager.db.query(sql, (p, n, s, r, u))
            messagebox.showinfo("Success", f"Đã phân công nhiệm vụ mới cho {n}!")
            self.app_manager.show_quanly_taikhoan_page()
        except Exception as e:
            messagebox.showerror("System Error", f"Lỗi cập nhật: {str(e)}")