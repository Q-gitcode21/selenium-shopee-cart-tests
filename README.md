 Tự động kiểm thử giỏ hàng Shopee (Python + Selenium)

Dự án kiểm thử tự động các chức năng giỏ hàng Shopee, được viết bằng Python + Selenium + Pytest.
Bao gồm các trường hợp kiểm thử thêm, sửa, xóa và xác minh sản phẩm trong giỏ hàng.

 --- Chức năng kiểm thử

Thêm sản phẩm có / không có phân loại

Xử lý khi chưa chọn phân loại hoặc hết hàng

Kiểm tra giới hạn số lượng theo tồn kho

Tăng / giảm / nhập số lượng trong giỏ hàng

Sửa phân loại sản phẩm

Xóa từng sản phẩm hoặc toàn bộ giỏ hàng

Kiểm tra nút “Mua ngay” hoạt động đúng

--- Công nghệ sử dụng

Ngôn ngữ: Python 3.11+

Thư viện: Selenium, Pytest

Trình duyệt: Chrome (dùng profile đã đăng nhập Shopee)

Mẫu thiết kế: Fixture + hàm kiểm thử

--- Cách chạy

1. Cài thư viện

pip install selenium pytest


2. Mở file test_cart.py, chỉnh lại đường dẫn profile Chrome:

options.add_argument(r"--user-data-dir=C:\Users\<Tên_user>\AppData\Local\Google\Chrome\User Data")
options.add_argument(r"--profile-directory=Profile 2")


3.Chạy test

pytest -v test_cart.py
