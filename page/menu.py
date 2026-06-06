import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
from datetime import datetime


class MenuPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # --- CẤU HÌNH MÀU SẮC ĐỒNG BỘ DARK TECH ---
        self.color_bg = "#1c1d22"  # Đen nhám Obsidian
        self.color_card = "#2d2f36"  # Xám tối Slate
        self.color_border = "#3d414e"  # Viền xám mờ
        self.color_navy = "#1e3799"  # Xanh Navy chính
        self.color_teal = "#1abc9c"  # Xanh Ngọc
        self.color_danger = "#e74c3c"  # Đỏ
        self.color_warning = "#e67e22"  # Cam

        # --- CẤU HÌNH MÀU SẮC RIÊNG CHO TỪNG PHÂN HỆ ĐỂ DỄ PHÂN BIỆT ---
        self.color_kho = "#3498db"  # Xanh dương (Phân hệ Kho hàng)
        self.color_pos = "#2ecc71"  # Xanh lá Mint (Phân hệ POS bán lẻ)
        self.color_staff = "#95a5a6"  # Xám thép (Phân hệ Nhân sự)
        self.color_report = "#9b59b6"  # Tím (Phân hệ Báo cáo)

        self.view()

    def view(self):
        # Màu nền tối giản cho toàn bộ khung cửa sổ Menu
        self.master.configure(bg=self.color_bg)

        # 1. Header phẳng màu tối với dải xanh ngọc công nghệ phía trên cùng
        header_f = tk.Frame(self.master, bg=self.color_card)
        header_f.pack(fill="x", side="top")

        accent = tk.Frame(header_f, bg=self.color_teal, height=4)
        accent.pack(fill="x")

        tk.Label(header_f, text="🛡️ BÀN ĐIỀU KHIỂN TRUNG TÂM",
                 font=("Segoe UI", 16, "bold"), fg="white", bg=self.color_card).pack(pady=15, side="left", padx=25)

        tk.Label(header_f, text="TRẠNG THÁI: HOẠT ĐỘNG & BẢO MẬT",
                 font=("Segoe UI", 9, "bold"), fg=self.color_teal, bg=self.color_card).pack(side="right", padx=25,
                                                                                            pady=15)

        # Khung làm việc chính chia dạng Đa cột thích ứng màn hình lớn
        main_container = tk.Frame(self.master, bg=self.color_bg)
        main_container.pack(fill="both", expand=True, padx=25, pady=15)

        main_container.grid_columnconfigure(0, weight=1)  # Cột trái (Sidebar) chiếm 30%
        main_container.grid_columnconfigure(1, weight=3)  # Cột phải (Lưới lệnh) chiếm 70%
        main_container.grid_rowconfigure(0, weight=1)

        # ---------------- 2. CỘT TRÁI: SIDEBAR GIÁM SÁT PHIÊN LÀM VIỆC ----------------
        sidebar = tk.LabelFrame(main_container, text=" PHÂN HỆ GIÁM SÁT ", font=("Segoe UI", 9, "bold"),
                                fg="#a4b0be", bg=self.color_card, bd=1, relief="solid", padx=20, pady=20)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        sidebar.config(highlightbackground=self.color_border)

        # 🔴 KHẮC PHỤC LỖI LỆCH KHIÊN: Sử dụng mã ký tự khiên đơn thuần khiết (không chứa byte ẩn gây lệch lề)
        avatar_lbl = tk.Label(sidebar, text="\U0001F6E1", font=("Segoe UI", 42), fg=self.color_teal, bg=self.color_card,
                              anchor="center")
        avatar_lbl.pack(pady=(15, 10), anchor="center")

        # Thông tin tài khoản hoạt động
        user = self.app_manager.current_user
        name, role = user[2], user[4]
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        tk.Label(sidebar, text=name.upper(), font=("Segoe UI", 12, "bold"), fg="white", bg=self.color_card).pack(pady=2)
        tk.Label(sidebar, text=f"QUYỀN: {role.upper()}", font=("Segoe UI", 9, "bold"), fg=self.color_teal,
                 bg=self.color_card).pack(pady=(0, 15))

        tk.Label(sidebar, text=f"Thời gian vào: {now_str}", font=("Segoe UI", 8, "italic"), fg="#a4b0be",
                 bg=self.color_card).pack(pady=5)

        # Đường phân cách mỏng phẳng
        sep = tk.Frame(sidebar, bg=self.color_border, height=1)
        sep.pack(fill="x", pady=15)

        # Các nút tiện ích thiết kế dạng Outline phẳng tối giản
        btn_about = tk.Button(sidebar, text="ℹ️ GIỚI THIỆU PHẦN MỀM", command=self.show_about_popup,
                              bg=self.color_card, fg="#a4b0be", font=("Segoe UI", 9, "bold"),
                              bd=1, relief="solid", height=2, cursor="hand2", highlightthickness=0)
        btn_about.config(highlightbackground=self.color_border)
        btn_about.pack(fill="x", pady=5)
        btn_about.bind("<Enter>", lambda e: btn_about.config(bg=self.color_teal, fg="white"))
        btn_about.bind("<Leave>", lambda e: btn_about.config(bg=self.color_card, fg="#a4b0be"))

        btn_pdf = tk.Button(sidebar, text="📕 HƯỚNG DẪN (PDF)", command=self.open_pdf_manual,
                            bg=self.color_card, fg="#a4b0be", font=("Segoe UI", 9, "bold"),
                            bd=1, relief="solid", height=2, cursor="hand2", highlightthickness=0)
        btn_pdf.config(highlightbackground=self.color_border)
        btn_pdf.pack(fill="x", pady=5)
        btn_pdf.bind("<Enter>", lambda e: btn_pdf.config(bg=self.color_warning, fg="white"))
        btn_pdf.bind("<Leave>", lambda e: btn_pdf.config(bg=self.color_card, fg="#a4b0be"))

        # Nút đăng xuất phẳng đỏ
        btn_logout = tk.Button(sidebar, text="🚪 ĐĂNG XUẤT", bg=self.color_danger, fg="white",
                               font=("Segoe UI", 10, "bold"), bd=0, height=2, cursor="hand2",
                               command=self.app_manager.show_login_page)
        btn_logout.pack(fill="x", side="bottom", pady=10)
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#c0392b"))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=self.color_danger))

        # ---------------- 3. CỘT PHẢI: LƯỚI THẺ LỆNH CHỈ HUY TỐI GIẢN (OUTLINE CARDS) ----------------
        workspace = tk.LabelFrame(main_container, text=" HỆ THỐNG PHÂN HỆ LỆNH TRUNG TÂM ",
                                  font=("Segoe UI", 9, "bold"),
                                  fg="#a4b0be", bg=self.color_card, bd=1, relief="solid", padx=20, pady=20)
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.config(highlightbackground=self.color_border)

        # Cấu hình lưới 2x2 cho các thẻ phân hệ
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=1)
        workspace.grid_rowconfigure(0, weight=1)
        workspace.grid_rowconfigure(1, weight=1)

        # Phân hệ 1: Quản lý kho hàng Gundam (Màu xanh dương)
        self.create_minimal_card(
            parent=workspace, title="📦 QUẢN LÝ KHO HÀNG GUNDAM",
            desc="Nhập thêm hàng hóa mới, điều chỉnh thông tin mô hình,\ntheo dõi lịch sử nhập hàng và quản lý đặt trước (pre-order).",
            command=self.app_manager.show_quanly_kho_page,
            accent_color=self.color_kho, row=0, col=0
        )

        # Phân hệ 2: Trạm POS Giao dịch bán hàng (Màu xanh lá Mint)
        self.create_minimal_card(
            parent=workspace, title="🛒 TRẠM GIAO DỊCH BÁN HÀNG",
            desc="Quầy bán lẻ trực tiếp tại cửa hàng, tính tiền thừa\nthối cho khách và kết xuất in biên lai hóa đơn nhanh.",
            command=self.app_manager.show_quanly_donhang_page,
            accent_color=self.color_pos, row=0, col=1
        )

        # Nếu là quản trị viên tối cao: Hiển thị thêm các phân hệ bảo mật và báo cáo doanh thu tài chính
        if role == "Admin" or user[0].lower() == "admin":
            # Phân hệ 3: Quản trị tài khoản nhân viên (Màu xám thép)
            self.create_minimal_card(
                parent=workspace, title="👥 QUẢN LÝ NHÂN SỰ TÀI KHOẢN",
                desc="Quản trị phân bổ nhân viên, cấp tài khoản bảo mật mới,\nchỉnh sửa mật khẩu hoặc thu hồi quyền truy cập hệ thống.",
                command=self.app_manager.show_quanly_taikhoan_page,
                accent_color=self.color_staff, row=1, col=0
            )

            # Phân hệ 4: Trung tâm phân tích doanh thu (Màu tím)
            self.create_minimal_card(
                parent=workspace, title="📊 BÁO CÁO DOANH THU CHI TIẾT",
                desc="Thống kê phân tích số liệu Pandas & NumPy học thuật,\ntự động kết xuất biên bản văn bản và vẽ đồ thị Matplotlib.",
                command=self.app_manager.show_baocao_page,
                accent_color=self.color_report, row=1, col=1
            )

    def create_minimal_card(self, parent, title, desc, command, accent_color, row, col):
        card_f = tk.Frame(parent, bg="#22242b", bd=1, relief="solid", highlightthickness=0)
        card_f.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        card_f.config(highlightbackground=self.color_border)

        content = tk.Frame(card_f, bg="#22242b", padx=20, pady=20)
        content.pack(fill="both", expand=True)

        title_lbl = tk.Label(content, text=title, font=("Segoe UI", 11, "bold"), fg=accent_color, bg="#22242b")
        title_lbl.pack(anchor="center", pady=(5, 10))

        desc_lbl = tk.Label(content, text=desc, font=("Segoe UI", 9), fg="#a4b0be", bg="#22242b", justify="center",
                            wraplength=320)
        desc_lbl.pack(fill="both", expand=True, pady=(0, 20))

        btn = tk.Button(content, text="TRUY CẬP", command=command, bg="#22242b", fg=accent_color,
                        font=("Segoe UI", 9, "bold"), bd=1, relief="solid", cursor="hand2", highlightthickness=0)
        btn.config(highlightbackground=self.color_border)
        btn.pack(fill="x", side="bottom", ipady=4)

        btn.bind("<Enter>", lambda e: btn.config(bg=accent_color, fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#22242b", fg=accent_color))

    def show_about_popup(self):
        pop = tk.Toplevel(self.master)
        pop.title("Giới thiệu")
        pop.geometry("400x320")
        pop.configure(bg="#2d2f36")
        pop.resizable(False, False)
        pop.grab_set()

        tk.Label(pop, text="ℹ️ THÔNG TIN PHẦN MỀM", font=("Segoe UI", 12, "bold"), bg="#2d2f36",
                 fg=self.color_teal).pack(pady=(15, 10))

        details = [
            ("• Phần mềm:", "GUNDAM KITVAULT PRO"),
            ("• Phiên bản:", "1.0.0"),
            ("• Sinh viên thực hiện:", "Nguyễn Minh Đức"),
            ("• Giảng viên hướng dẫn:", "ThS. Vũ Duy Sơn"),
            ("• Đơn vị:", "Trường Đại học Hạ Long (UHL)"),
            ("• Ngày phát hành:", "06/06/2026")
        ]

        for label, val in details:
            lbl_f = tk.Frame(pop, bg="#2d2f36")
            lbl_f.pack(fill="x", padx=40, pady=2)
            tk.Label(lbl_f, text=label, font=("Segoe UI", 9, "bold"), bg="#2d2f36", fg="#a4b0be").pack(side="left")
            tk.Label(lbl_f, text=f" {val}", font=("Segoe UI", 9), bg="#2d2f36", fg="white").pack(side="left")

        desc_lbl = tk.Label(pop,
                            text="Hệ thống hỗ trợ quản lý kho hàng mô hình Gundam,\ngiao dịch bán lẻ tại quầy và báo cáo doanh thu tài chính tự động.",
                            font=("Segoe UI", 9, "italic"), bg="#2d2f36", fg="#bdc5cb", justify="center")
        desc_lbl.pack(pady=15)

        btn_close = tk.Button(pop, text="Xác nhận", command=pop.destroy, bg=self.color_teal, fg="white",
                              font=("Segoe UI", 9, "bold"), width=12, height=1, bd=0, cursor="hand2")
        btn_close.pack(pady=(0, 10))
        btn_close.bind("<Enter>", lambda e: btn_close.config(bg="#16a085"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(bg=self.color_teal))

    def open_pdf_manual(self):
        """MỞ FILE PDF HƯỚNG DẪN SỬ DỤNG PHẦN MỀM"""
        os.makedirs("documents", exist_ok=True)
        pdf_path = "documents/huong_dan_su_dung.pdf"

        # Tạo file giả lập tránh crash nếu máy chưa có sẵn tệp thực tế
        if not os.path.exists(pdf_path):
            try:
                with open(pdf_path, "w", encoding="utf-8") as f:
                    f.write("%PDF-1.4 ... Gia lap file Huong dan su dung phan mem Gundam Store ...")
            except Exception:
                pass

        try:
            webbrowser.open(os.path.abspath(pdf_path))
        except Exception as e:
            messagebox.showerror("Lỗi mở file", f"Không thể mở file PDF hướng dẫn: {str(e)}")
