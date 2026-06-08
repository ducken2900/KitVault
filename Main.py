# =========================================================================
# FILE: Main.py
# NGUỒN KHỞI CHẠY CHÍNH CỦA HỆ THỐNG
# =========================================================================
from app_manager import AppManager
def main():
    # [GIAO DIỆN]: Hiển thị dòng trạng thái chào mừng dưới màn hình Terminal/Console.
    # [CÁCH DÙNG]: Chạy file này bằng lệnh 'python Main.py' để bắt đầu toàn bộ ứng dụng.
    print("------------------------------")
    print("HỆ THỐNG GUNDAM KITVAULT PRO")
    print("Trạng thái: Đang khởi chạy...")
    print("------------------------------")

    # [SỬA TẠI ĐÂY]: Khởi tạo bộ quản lý ứng dụng điều hướng (AppManager).
    app = AppManager()
    app.run()


if __name__ == "__main__":
    main()