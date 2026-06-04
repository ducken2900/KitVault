import tkinter as tk
from tkinter import messagebox
import sqlite3


class RegisterPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # Khai báo thuộc tính lưu trữ các trường nhập liệu
        self.ents = {}

        self.view()

    def view(self):
        # Thiết lập tông màu xanh Navy đặc trưng
        main_navy = "#1e3799"
        self.master.configure(bg="#f1f2f6")

        # Thay đổi tiêu đề động dựa trên việc có phiên đăng nhập của Admin hay không
        is_admin = self.app_manager.current_user is not None
        title = "THÊM NHÂN VIÊN MỚI" if is_admin else "ĐĂNG KÝ TÀI KHOẢN"

        header = tk.Frame(self.master, bg=main_navy)
        header.pack(fill="x")
        tk.Label(header, text=title, font=("Arial", 20, "bold"), fg="white", bg=main_navy).pack(pady=30)

        # Khung chứa Form nhập liệu chính
        form = tk.Frame(self.master, padx=50, bg="#f1f2f6")
        form.pack(fill="x", pady=20)

        fields = ["User:", "Pass:", "Name:", "Phone:"]
        for i, txt in enumerate(fields):
            tk.Label(form, text=txt, font=("Arial", 10, "bold"), bg="#f1f2f6").grid(row=i, column=0, sticky="w",
                                                                                    pady=10)

            # Ẩn ký tự đối với ô nhập mật khẩu
            show_char = "*" if "Pass" in txt else ""
            e = tk.Entry(form, font=("Arial", 11), show=show_char, bd=1, relief="solid")
            e.grid(row=i, column=1, sticky="ew", padx=10, ipady=5)
            self.ents[txt] = e

        form.columnconfigure(1, weight=1)

        # Nút xác nhận đăng ký tài khoản
        tk.Button(self.master, text="XÁC NHẬN", bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), height=2, command=self.save).pack(fill="x", padx=100, pady=25)

        # Nút Quay lại
        tk.Button(self.master, text="QUAY LẠI", command=self.back, bd=0, fg="#1e3799", bg="#f1f2f6",
                  cursor="hand2").pack()

    def back(self):
        """ĐIỀU HƯỚNG QUAY LẠI CHÍNH XÁC DỰA TRÊN ĐĂNG NHẬP"""
        if self.app_manager.current_user:
            # Nếu đang là Admin đăng nhập: Quay lại trang quản lý nhân sự
            self.app_manager.show_quanly_taikhoan_page()
        else:
            # Nếu là khách chưa đăng nhập: Quay về trang login
            self.app_manager.show_login_page()

    def save(self):
        """XỬ LÝ THU THẬP VÀ GHI TÀI KHOẢN MỚI VÀO CƠ SỞ DỮ LIỆU"""
        # Thu thập thông tin từ form
        u = self.ents["User:"].get().strip()
        p = self.ents["Pass:"].get().strip()
        n = self.ents["Name:"].get().strip()
        s = self.ents["Phone:"].get().strip()

        if not u or not p or not n:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đủ thông tin bắt buộc (Tài khoản, Mật khẩu, Họ tên)!")
            return

        try:
            # Thực thi câu lệnh INSERT ghi tài khoản mới vào cơ sở dữ liệu
            sql = "INSERT INTO users (username, password, fullname, phone, role) VALUES (?, ?, ?, ?, ?)"
            self.app_manager.db.query(sql, (u, p, n, s, "Nhân viên"))

            messagebox.showinfo("Thành công", f"Đã đăng ký thành công tài khoản người dùng '{u}'!")
            self.back()

        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi đăng ký", "Tên đăng nhập này đã tồn tại trên hệ thống! Vui lòng chọn tên khác.")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể đăng ký: {str(e)}")