import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
from datetime import datetime


class MenuPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # =========================================================================
        # [MÀU SẮC]: BẢNG MÀU CHỦ ĐẠO (Đổi mã màu tại đây sẽ đổi màu toàn màn hình)
        # =========================================================================
        self.colors = {
            "bg_main": "#1c1d22",  # Màu nền tối Obsidian của cửa sổ chính
            "bg_card": "#2d2f36",  # Màu nền xám tối Slate của các khung chứa
            "border": "#3d414e",  # Màu xám mờ của các đường viền

            "btn_idle_bg": "#22242b",  # Màu nền mặc định khi chưa di chuột vào nút
            "text_gray": "#a4b0be",  # Màu chữ phụ (Mô tả, ghi chú)

            # Màu đặc trưng cho từng phân hệ (Liên kết trực tiếp tới hàm create_minimal_card ở dưới)
            "kho": "#3498db",  # Xanh dương - Kho hàng Gundam
            "pos": "#2ecc71",  # Xanh lá Mint - Trạm bán lẻ POS
            "staff": "#95a5a6",  # Xám thép - Quản lý nhân sự
            "report": "#9b59b6",  # Tím - Báo cáo & Phân tích doanh thu
            "teal": "#1abc9c",  # Xanh ngọc - Viền trang trí & Giới thiệu
            "warning": "#e67e22",  # Cam - Nút mở hướng dẫn PDF
            "danger": "#e74c3c",  # Đỏ - Nút Đăng xuất mặc định

            # Màu khi di chuột vào (Hover State) của từng nút bấm tương ứng
            "btn_kho_hover_bg": "#3498db",  # Rà chuột vào nút Kho -> Đổi sang nền Xanh dương
            "btn_pos_hover_bg": "#2ecc71",  # Rà chuột vào nút POS -> Đổi sang nền Xanh lá
            "btn_staff_hover_bg": "#95a5a6",  # Rà chuột vào nút Nhân sự -> Đổi sang nền Xám
            "btn_report_hover_bg": "#9b59b6",  # Rà chuột vào nút Báo cáo -> Đổi sang nền Tím
            "btn_about_hover_bg": "#1abc9c",  # Rà chuột vào nút Giới thiệu -> Đổi sang nền Xanh ngọc
            "btn_pdf_hover_bg": "#e67e22",  # Rà chuột vào nút Hướng dẫn -> Đổi sang nền Cam
            "btn_logout_hover_bg": "#c0392b"  # Rà chuột vào nút Đăng xuất -> Đổi sang nền Đỏ sẫm
        }

        self.view()

    def view(self):
        # [MÀU SẮC]: Gán màu nền tối Obsidian cho toàn bộ cửa sổ gốc
        self.master.configure(bg=self.colors["bg_main"])

        # ---------------- 1. HEADER (TIÊU ĐỀ ĐỈNH TRANG) ----------------
        # [MÀU SẮC]: bg=self.colors["bg_card"] gán nền màu xám Slate cho thanh Header
        header_f = tk.Frame(self.master, bg=self.colors["bg_card"])
        header_f.pack(fill="x", side="top")

        # [KÍCH THƯỚC]: height=4 tạo một đường viền ngang trang trí mỏng màu xanh ngọc ở đỉnh trang
        accent = tk.Frame(header_f, bg=self.colors["teal"], height=4)
        accent.pack(fill="x")

        # [THIẾT KẾ & KÍCH THƯỚC]: Tiêu đề sảnh chính.
        # font=("Segoe UI", 16, "bold"): Sửa phông chữ và cỡ chữ tiêu đề tại đây.
        # pady=15, padx=25: Khoảng đệm chữ cách viền xung quanh (Doc x Ngang)
        tk.Label(header_f, text="🛡️ BÀN ĐIỀU KHIỂN TRUNG TÂM",
                 font=("Segoe UI", 16, "bold"), fg="white", bg=self.colors["bg_card"]).pack(pady=15, side="left",
                                                                                            padx=25)

        tk.Label(header_f, text="TRẠNG THÁI: HOẠT ĐỘNG & BẢO MẬT",
                 font=("Segoe UI", 9, "bold"), fg=self.colors["teal"], bg=self.colors["bg_card"]).pack(side="right",
                                                                                                       padx=25, pady=15)

        # ---------------- 2. KHUNG PHÂN CHIA BỐ CỤC CHÍNH ----------------
        main_container = tk.Frame(self.master, bg=self.colors["bg_main"])
        main_container.pack(fill="both", expand=True, padx=25, pady=15)

        # [KÍCH THƯỚC & BỐ CỤC]: grid_columnconfigure phân chia tỷ lệ bề rộng của 2 cột:
        # column=0 (Sidebar trái) có weight=1 (Chiếm 25% độ rộng cửa sổ)
        # column=1 (Hệ thống thẻ phải) có weight=3 (Chiếm 75% độ rộng cửa sổ)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)

        # ---------------- 3. CỘT TRÁI: SIDEBAR GIÁM SÁT TRẠNG THÁI NHÂN VIÊN ----------------
        # [MÀU SẮC & KÍCH THƯỚC]: bd=1, relief="solid" vẽ viền mỏng quanh khung giám sát
        # config(highlightbackground=...) gán màu xám mờ cho đường viền này
        sidebar = tk.LabelFrame(main_container, text=" PHÂN HỆ GIÁM SÁT ", font=("Segoe UI", 9, "bold"),
                                fg=self.colors["text_gray"], bg=self.colors["bg_card"], bd=1, relief="solid", padx=20,
                                pady=20)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        sidebar.config(highlightbackground=self.colors["border"])

        # [KÍCH THƯỚC]: font=("Segoe UI", 42) điều chỉnh độ to nhỏ của biểu tượng Khiên Bảo Mật
        avatar_lbl = tk.Label(sidebar, text="\U0001F6E1", font=("Segoe UI", 42), fg=self.colors["teal"],
                              bg=self.colors["bg_card"], anchor="center")
        avatar_lbl.pack(pady=(15, 10), anchor="center")

        # [LIÊN KẾT]: Nạp thông tin tài khoản đang đăng nhập từ app_manager.py
        user = self.app_manager.current_user
        name, role = user[2], user[4]  # user[2] là họ tên, user[4] là quyền hạn (Admin/Nhân viên)
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        tk.Label(sidebar, text=name.upper(), font=("Segoe UI", 12, "bold"), fg="white", bg=self.colors["bg_card"]).pack(
            pady=2)
        tk.Label(sidebar, text=f"QUYỀN: {role.upper()}", font=("Segoe UI", 9, "bold"), fg=self.colors["teal"],
                 bg=self.colors["bg_card"]).pack(pady=(0, 15))
        tk.Label(sidebar, text=f"Thời gian vào: {now_str}", font=("Segoe UI", 8, "italic"), fg=self.colors["text_gray"],
                 bg=self.colors["bg_card"]).pack(pady=5)

        # Đường cắt ngang trang trí mỏng (height=1)
        sep = tk.Frame(sidebar, bg=self.colors["border"], height=1)
        sep.pack(fill="x", pady=15)

        # --- NÚT BẤM 1: GIỚI THIỆU PHẦN MỀM ---
        # [LIÊN KẾT]: command=self.show_about_popup dẫn tới hàm mở cửa sổ popup giới thiệu ở dưới
        btn_about = tk.Button(sidebar, text="ℹ️ GIỚI THIỆU PHẦN MỀM", command=self.show_about_popup,
                              bg=self.colors["bg_card"], fg=self.colors["text_gray"], font=("Segoe UI", 9, "bold"),
                              bd=1, relief="solid", height=2, cursor="hand2", highlightthickness=0)
        btn_about.config(highlightbackground=self.colors["border"])
        btn_about.pack(fill="x", pady=5)
        # [MÀU SẮC - LIÊN KẾT HOVER]: Rà chuột đổi sang màu xanh ngọc (btn_about_hover_bg), rời đi về màu xám Slate
        btn_about.bind("<Enter>", lambda e: btn_about.config(bg=self.colors["btn_about_hover_bg"], fg="white"))
        btn_about.bind("<Leave>", lambda e: btn_about.config(bg=self.colors["bg_card"], fg=self.colors["text_gray"]))

        # --- NÚT BẤM 2: TÀI LIỆU HƯỚNG DẪN PDF ---
        # [LIÊN KẾT]: command=self.open_pdf_manual dẫn tới hàm kích hoạt mở file PDF hướng dẫn sử dụng
        btn_pdf = tk.Button(sidebar, text="📕 HƯỚNG DẪN (PDF)", command=self.open_pdf_manual,
                            bg=self.colors["bg_card"], fg=self.colors["text_gray"], font=("Segoe UI", 9, "bold"),
                            bd=1, relief="solid", height=2, cursor="hand2", highlightthickness=0)
        btn_pdf.config(highlightbackground=self.colors["border"])
        btn_pdf.pack(fill="x", pady=5)
        # [MÀU SẮC - LIÊN KẾT HOVER]: Rà chuột đổi sang màu Cam (btn_pdf_hover_bg), rời đi về màu xám Slate
        btn_pdf.bind("<Enter>", lambda e: btn_pdf.config(bg=self.colors["btn_pdf_hover_bg"], fg="white"))
        btn_pdf.bind("<Leave>", lambda e: btn_pdf.config(bg=self.colors["bg_card"], fg=self.colors["text_gray"]))

        # --- NÚT BẤM 3: ĐĂNG XUẤT HỆ THỐNG ---
        # [LIÊN KẾT]: command=self.app_manager.show_login_page thoát phiên và trả về màn hình đăng nhập ban đầu
        btn_logout = tk.Button(sidebar, text="🚪 ĐĂNG XUẤT", bg=self.colors["danger"], fg="white",
                               font=("Segoe UI", 10, "bold"), bd=0, height=2, cursor="hand2")
        btn_logout.pack(fill="x", side="bottom", pady=10)
        # [MÀU SẮC - LIÊN KẾT HOVER]: Rà chuột đổi sang đỏ sẫm (btn_logout_hover_bg), rời đi về đỏ tươi mặc định
        btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg=self.colors["btn_logout_hover_bg"]))
        btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=self.colors["danger"]))

        # ---------------- 4. CỘT PHẢI: HỆ THỐNG KHỐI PHÂN HỆ LỆNH TRUNG TÂM ----------------
        workspace = tk.LabelFrame(main_container, text=" HỆ THỐNG PHÂN HỆ LỆNH TRUNG TÂM ",
                                  font=("Segoe UI", 9, "bold"), fg=self.colors["text_gray"], bg=self.colors["bg_card"],
                                  bd=1, relief="solid", padx=20, pady=20)
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.config(highlightbackground=self.colors["border"])

        # [KÍCH THƯỚC & BỐ CỤC]: Chia cột phải thành lưới 2x2 cân bằng (mỗi cột/dòng chiếm 50% diện tích)
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=1)
        workspace.grid_rowconfigure(0, weight=1)
        workspace.grid_rowconfigure(1, weight=1)

        # PHÂN HỆ 1: Quản lý kho hàng Gundam (Đặt ở dòng 0, cột 0)
        # [LIÊN KẾT]: command=self.app_manager.show_quanly_kho_page mở giao diện Kho
        # normal_color=self.colors["kho"] gán màu xanh dương cho Tiêu đề & chữ trên nút bấm
        # hover_color=self.colors["btn_kho_hover_bg"] định nghĩa màu nền sáng lên khi rà chuột
        self.create_minimal_card(
            parent=workspace, title="📦 QUẢN LÝ KHO HÀNG GUNDAM",
            desc="Nhập thêm hàng hóa mới, điều chỉnh thông tin mô hình,\ntheo dõi lịch sử nhập hàng và quản lý đặt trước (pre-order).",
            command=self.app_manager.show_quanly_kho_page,
            normal_color=self.colors["kho"],
            hover_color=self.colors["btn_kho_hover_bg"],
            row=0, col=0
        )

        # PHÂN HỆ 2: Trạm POS bán hàng (Đặt ở dòng 0, cột 1)
        # [LIÊN KẾT]: command=self.app_manager.show_quanly_donhang_page mở giao diện Bán hàng
        # normal_color=self.colors["pos"] gán màu xanh lá Mint cho Tiêu đề & chữ trên nút bấm
        # hover_color=self.colors["btn_pos_hover_bg"] định nghĩa màu nền sáng lên khi rà chuột
        self.create_minimal_card(
            parent=workspace, title="🛒 TRẠM GIAO DỊCH BÁN HÀNG",
            desc="Quầy bán lẻ trực tiếp tại cửa hàng, tính tiền thừa\nthối cho khách và kết xuất in biên lai hóa đơn nhanh.",
            command=self.app_manager.show_quanly_donhang_page,
            normal_color=self.colors["pos"],
            hover_color=self.colors["btn_pos_hover_bg"],
            row=0, col=1
        )

        # [LIÊN KẾT - PHÂN QUYỀN]: Kiểm tra nếu tài khoản đang đăng nhập là Admin:
        # Nếu đúng -> Máy tính mới chạy hàm vẽ Phân hệ 3 và Phân hệ 4 lên màn hình.
        # Nếu sai -> Hai phân hệ này bị ẩn hoàn toàn, nhân viên thông thường không thể nhìn thấy.
        if role == "Admin" or user[0].lower() == "admin":
            # PHÂN HỆ 3: Quản trị tài khoản nhân viên (Đặt ở dòng 1, cột 0)
            # [LIÊN KẾT]: command=self.app_manager.show_quanly_taikhoan_page mở giao diện Nhân sự
            self.create_minimal_card(
                parent=workspace, title="👥 QUẢN LÝ NHÂN SỰ TÀI KHOẢN",
                desc="Quản trị phân bổ nhân viên, cấp tài khoản bảo mật mới,\nchỉnh sửa mật khẩu hoặc thu hồi quyền truy cập hệ thống.",
                command=self.app_manager.show_quanly_taikhoan_page,
                normal_color=self.colors["staff"],
                hover_color=self.colors["btn_staff_hover_bg"],
                row=1, col=0
            )

            # PHÂN HỆ 4: Trung tâm phân tích báo cáo doanh thu (Đặt ở dòng 1, cột 1)
            # [LIÊN KẾT]: command=self.app_manager.show_baocao_page mở giao diện Kế toán
            self.create_minimal_card(
                parent=workspace, title="📊 BÁO CÁO DOANH THU CHI TIẾT",
                desc="Thống kê phân tích số liệu Pandas & NumPy học thuật,\ntự động kết xuất biên bản văn bản và vẽ đồ thị Matplotlib.",
                command=self.app_manager.show_baocao_page,
                normal_color=self.colors["report"],
                hover_color=self.colors["btn_report_hover_bg"],
                row=1, col=1
            )

    # =========================================================================
    # 5. KHUÔN MẪU DỰNG KHỐI HỘP FLAT-UI (CREATE MINIMAL CARD)
    # [LIÊN KẾT]: Hàm này nhận các tham số tiêu đề, mô tả, màu sắc động từ bước 4
    #             để tiến hành vẽ khối hộp chức năng hoàn chỉnh lên màn hình.
    # =========================================================================
    def create_minimal_card(self, parent, title, desc, command, normal_color, hover_color, row, col):
        # Khung hộp lớn bao ngoài.
        # [KÍCH THƯỚC]: padx=12, pady=12 tạo khoảng cách hở ra giữa các hộp để không bị dính vào nhau.
        card_f = tk.Frame(parent, bg="#22242b", bd=1, relief="solid", highlightthickness=0)
        card_f.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        card_f.config(highlightbackground=self.colors["border"])

        # Khung lót đệm bên trong.
        # [KÍCH THƯỚC]: padx=20, pady=20 đẩy chữ lùi sâu vào trong hộp để bố cục thoáng mắt.
        content = tk.Frame(card_f, bg="#22242b", padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # ---------------- THÀNH PHẦN 1: CHỮ TIÊU ĐỀ ----------------
        # [LIÊN KẾT & MÀU SẮC]: fg=normal_color nhận giá trị màu truyền vào để đổi màu chữ tiêu đề tương ứng.
        title_lbl = tk.Label(content, text=title, font=("Segoe UI", 11, "bold"), fg=normal_color, bg="#22242b")
        title_lbl.pack(anchor="center", pady=(5, 10))

        # ---------------- THÀNH PHẦN 2: ĐOẠN VĂN MÔ TẢ ----------------
        # [KÍCH THƯỚC]: font=("Segoe UI", 9) điều chỉnh chữ mô tả nhỏ hơn tiêu đề.
        # wraplength=320 bắt buộc đoạn văn tự động xuống dòng khi độ dài vượt quá 320 pixel.
        desc_lbl = tk.Label(content, text=desc, font=("Segoe UI", 9), fg=self.colors["text_gray"], bg="#22242b",
                            justify="center", wraplength=320)
        desc_lbl.pack(fill="both", expand=True, pady=(0, 20))

        # ---------------- THÀNH PHẦN 3: NÚT BẤM "TRUY CẬP" ----------------
        # [LIÊN KẾT]: command=command liên kết hành động click chuột vào nút với trang tương ứng.
        # fg=normal_color gán màu chữ nút bấm mặc định trùng màu với màu tiêu đề phân hệ.
        btn = tk.Button(content, text="TRUY CẬP", command=command, bg=self.colors["btn_idle_bg"], fg=normal_color,
                        font=("Segoe UI", 9, "bold"), bd=1, relief="solid", cursor="hand2", highlightthickness=0)
        btn.config(highlightbackground=self.colors["border"])
        btn.pack(fill="x", side="bottom", ipady=4)

        # [LIÊN KẾT HOVER ĐỔI MÀU NÚT]:
        # Khi chuột rà vào (<Enter>): Đổi màu nền nút 'bg' thành hover_color cụ thể của phân hệ đó, chữ chuyển trắng.
        # Khi chuột rời đi (<Leave>): Trả màu nền nút 'bg' về màu tối mặc định (btn_idle_bg), chữ chuyển lại màu normal_color.
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color, fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.colors["btn_idle_bg"], fg=normal_color))

    # =========================================================================
    # 6. CÁC HÀM TIỆN ÍCH PHỤ TRỢ (POPUP GIỚI THIỆU & PDF HƯỚNG DẪN)
    # =========================================================================
    def show_about_popup(self):
        """[TÍNH NĂNG]: Hàm tạo cửa sổ popup nhỏ đè lên trên để hiển thị thông tin sinh viên"""
        pop = tk.Toplevel(self.master)
        pop.title("Giới thiệu")
        # [KÍCH THƯỚC]: geometry("400x320") giới hạn kích thước cửa sổ popup cố định
        pop.geometry("400x320")
        pop.configure(bg="#2d2f36")
        pop.resizable(False, False)  # Khóa không cho kéo giãn kích thước popup
        pop.grab_set()

        tk.Label(pop, text="ℹ️ THÔNG TIN PHẦN MỀM", font=("Segoe UI", 12, "bold"), bg="#2d2f36",
                 fg=self.colors["teal"]).pack(pady=(15, 10))

        details = [
            ("• Phần mềm:", "GUNDAM KITVAULT PRO"),
            ("• Phiên bản:", "1.0.0"),
            ("• Sinh viên thực hiện:", "Nguyễn Minh Đức"),
            ("• Giảng viên hướng dẫn:", "ThS. Vũ Duy Sơn"),
            ("• Đơn vị:", "Trường Đại học Hạ Long (UHL)"),
            ("• Ngày phát hành:", "06/06/2026")
        ]

        # Vòng lặp tự động vẽ danh sách thông tin sinh viên lên cửa sổ popup
        for label, val in details:
            lbl_f = tk.Frame(pop, bg="#2d2f36")
            lbl_f.pack(fill="x", padx=40, pady=2)
            tk.Label(lbl_f, text=label, font=("Segoe UI", 9, "bold"), bg="#2d2f36", fg=self.colors["text_gray"]).pack(
                side="left")
            tk.Label(lbl_f, text=f" {val}", font=("Segoe UI", 9), bg="#2d2f36", fg="white").pack(side="left")

        desc_lbl = tk.Label(pop,
                            text="Hệ thống hỗ trợ quản lý kho hàng mô hình Gundam,\ngiao dịch bán lẻ tại quầy và báo cáo doanh thu tài chính tự động.",
                            font=("Segoe UI", 9, "italic"), bg="#2d2f36", fg="#bdc5cb", justify="center")
        desc_lbl.pack(pady=15)

        btn_close = tk.Button(pop, text="Xác nhận", command=pop.destroy, bg=self.colors["teal"], fg="white",
                              font=("Segoe UI", 9, "bold"), width=12, height=1, bd=0, cursor="hand2")
        btn_close.pack(pady=(0, 10))
        btn_close.bind("<Enter>", lambda e: btn_close.config(bg="#16a085"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(bg=self.colors["teal"]))

    def open_pdf_manual(self):
        pdf_path = "documents/huong_dan_su_dung.pdf"
        if not os.path.exists(pdf_path):
            messagebox.showerror("Lỗi mở file", "Không tìm thấy file tài liệu hướng dẫn thật!\nVui lòng đảm bảo file 'huong_dan_su_dung.pdf' đã được đặt chính xác trong thư mục 'documents'.\n\n*Lưu ý: Hãy kiểm tra tránh đặt trùng tên dạng 'huong_dan_su_dung.pdf.pdf' trên Windows.")
            return

        try:
            webbrowser.open(os.path.abspath(pdf_path))
        except Exception as e:
            messagebox.showerror("Lỗi mở file", f"Không thể mở file PDF hướng dẫn: {str(e)}")
