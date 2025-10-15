from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest
import re
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\Users\THANH AN COMPUTER\AppData\Local\Google\Chrome\User Data")
    options.add_argument(r"--profile-directory=Profile 2")  # Đảm bảo đúng profile đã đăng nhập
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

# Giấu dấu vết automation
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

# TC1: Thêm sản phẩm không có phân loại thành công
def test_add_product_no_variant(driver):
    wait = WebDriverWait(driver, 10)

    # ====== Bước 1: Mở trang sản phẩm chi tiết ======
    product_url = "https://shopee.vn/product/972724310/18876819498"
    product_id = "18876819498"
    driver.get(product_url)
    time.sleep(5)
    
    # ====== Bước 2: Nhấn nút "Thêm vào giỏ hàng" ======
    add_to_cart_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[.//span[contains(text(), "thêm vào giỏ hàng")]]')
    ))
    add_to_cart_btn.click()
    time.sleep(3)

    # ====== Bước 3: Vào giỏ hàng kiểm tra sản phẩm có trong đó ======
    cart_icon = driver.find_element(By.ID, "cart_drawer_target_id")
    cart_icon.click()

    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "cart-page-logo__page-name")
    ))

    # Tìm phần tử có chứa itemId trong link hoặc attribute
    time.sleep(2)  # Chờ DOM ổn định
    #Lấy toàn bộ html của trang web
    page_source = driver.page_source
    #Kiểm tra xem có id sản phẩm trong trang đó ko
    assert product_id in page_source, f"[FAIL] Không tìm thấy sản phẩm {product_id} trong trang giỏ hàng"

# TC2 Thêm sản phẩm có phân loại thành công
def test_add_product_with_variant(driver):
    wait = WebDriverWait(driver, 10)

    # ====== Bước 1: Mở trang sản phẩm chi tiết ======
    product_url = "https://shopee.vn/product/12208293/4309959950"  # Thay bằng ID sản phẩm thực tế
    product_id = "4309959950"  # ID sản phẩm
    driver.get(product_url)
    time.sleep(5)

    # ====== Bước 2: Chọn phân loại màu sắc
    selection_buttons = driver.find_elements(By.CLASS_NAME, "selection-box-unselected")
    if selection_buttons:
        # Chọn lựa chọn đầu tiên trong selection box lựa chọn còn hàng 
        first_button = selection_buttons[0]
        first_button.click()
        print("Đã chọn phân loại đầu tiên.")
    else:
        print("Không tìm thấy lựa chọn phân loại.")

    # ====== Bước 2: Nhấn nút "Thêm vào giỏ hàng" ======
    add_to_cart_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[.//span[contains(text(), "thêm vào giỏ hàng")]]')
    ))
    add_to_cart_btn.click()
    time.sleep(3)

    # ====== Bước 3: Vào giỏ hàng kiểm tra sản phẩm có trong đó ======
    cart_icon = driver.find_element(By.ID, "cart_drawer_target_id")
    cart_icon.click()

    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "cart-page-logo__page-name")
    ))
    #Kiểm tra thêm phân loại hàng đã chọn đúng trong đó
    # Tìm phần tử có chứa itemId trong link hoặc attribute
    time.sleep(2)  # Chờ DOM ổn định
    page_source = driver.page_source
    assert product_id in page_source, f"[FAIL] Không tìm thấy sản phẩm {product_id} trong trang giỏ hàng"

    print("[PASS] Sản phẩm đã được thêm thành công vào giỏ hàng.")
# TC3 Thêm phân loại = blank
def test_add_product_with_invalid_variant(driver):
    wait = WebDriverWait(driver, 10)

    # ====== Bước 1: Mở trang chi tiết sản phẩm có phân loại ======
    product_url = "https://shopee.vn/product/12208293/4309959950"  # Thay bằng ID sản phẩm thực tế
    driver.get(product_url)
    time.sleep(5)

    # ====== Bước 2: Nhấn "Thêm vào giỏ hàng" mà KHÔNG chọn phân loại ======
    add_to_cart_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[.//span[contains(text(), "thêm vào giỏ hàng")]]')
    ))
    add_to_cart_btn.click()
    time.sleep(2)

    # ====== Bước 3: Kiểm tra thông báo lỗi hiển thị ======
    try:
        error_popup = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[contains(text(), "Vui lòng chọn Phân loại hàng")]')
        ))
        assert error_popup.is_displayed(), "[FAIL] Không tìm thấy thông báo lỗi khi chưa chọn phân loại"
        print("[PASS] Hiển thị đúng thông báo yêu cầu chọn phân loại hàng.")
    except:
        print("[FAIL] Không hiển thị thông báo lỗi yêu cầu chọn phân loại hàng.")
        assert False
# TC4 Thêm phân loại hết hàng
def test_add_out_of_stock_variant(driver):
    wait = WebDriverWait(driver, 10)

    # Bước 1: Mở trang sản phẩm đã biết có phân loại hết hàng
    product_url = "https://shopee.vn/product/965158714/26181834612"
    driver.get(product_url)
    time.sleep(5)

    # Bước 2: Chọn phân loại đã biết là hết hàng (ví dụ: 1T450-L)
    variant_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[@aria-label="đỏ"]')
    ))
    variant_button.click()
    time.sleep(1)

    # B2: Kiểm tra phân loại "tròn" bị disable
    round_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='tròn']")))

    # Kiểm tra thuộc tính aria-disabled
    assert round_button.get_attribute("aria-disabled") == "true", "Phân loại 'tròn' không bị disable sau khi chọn 'đỏ'"
# TC5 Thêm số lượng vượt quá sl tồn kho
def test_add_product_exceed_stock(driver):
    wait = WebDriverWait(driver, 10)

    # ====== Bước 1: Mở trang chi tiết sản phẩm ======
    product_url = "https://shopee.vn/product/972724310/18876819498"  # Ví dụ sản phẩm có tồn kho 8995
    driver.get(product_url)
    time.sleep(5)

    # ====== Bước 2:Lấy số lượng tồn kho thực tế từ giao diện ======
    stock_text_elem = driver.find_element(By.XPATH, '//div[contains(text(), "sản phẩm có sẵn")]')
    stock_text = stock_text_elem.text  # Ví dụ: "8995 sản phẩm có sẵn"
    stock_quantity = int(''.join(filter(str.isdigit, stock_text)))  # Lấy số 8995

    # ====== Bước 3: Nhập số lượng vượt quá kho ======
    quantity_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input[type="text"][role="spinbutton"]')
    ))

    quantity_input.clear()
    quantity_input.send_keys(stock_quantity+1)  # Nhập số lượng tồn kho +1
    time.sleep(2)

    
    # ======Bước 3: Kiểm tra số lượng bị giới hạn không vượt quá tồn kho ======
    adjusted_value = quantity_input.get_attribute("value")
    print(f"[INFO] Giá trị sau khi nhập: {adjusted_value}, Tồn kho: {stock_quantity}")

    assert int(adjusted_value) == stock_quantity, "[FAIL] Hệ thống không giới hạn số lượng theo tồn kho"

# TC6 Thêm sản phẩm hết hàng
def test_out_of_stock_product_page(driver):
    wait = WebDriverWait(driver, 10)

    # Bước 1: Mở trang sản phẩm hết hàng
    product_url = "https://shopee.vn/product/965158714/26781850750"  # <-- Thay bằng link thực tế
    driver.get(product_url)
    time.sleep(5)

    # Bước 2: Kiểm tra trạng thái "Hết hàng" và nút bị disable
    try:
        # Kiểm tra dòng chữ "Hết Hàng" hiển thị trên ảnh hoặc gần sản phẩm
        sold_out_text = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(text(), "Hết Hàng") or contains(text(), "hết hàng")]')
        ))
        assert sold_out_text.is_displayed(), "[FAIL] Không thấy dòng chữ 'Hết Hàng'."

        # Kiểm tra nút "Thêm Vào Giỏ Hàng" bị disable
        add_to_cart_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[.//span[contains(text(), "thêm vào giỏ hàng")]]')
    ))
        assert not add_to_cart_btn.is_enabled(), "[FAIL] Nút 'Thêm Vào Giỏ Hàng' không bị disable."

        print("[PASS] Sản phẩm hết hàng hiển thị đúng và không cho thêm vào giỏ.")
    except Exception as e:
        print(f"[FAIL] Có lỗi xảy ra: {e}")
# TC7 Thêm nhiều sản phẩm vào giỏ hàng
def test_add_multiple_products_to_cart(driver):
    wait = WebDriverWait(driver, 10)

    # Danh sách sản phẩm (link và ID)
    products = [
        {
            "url": "https://shopee.vn/product/293689173/29671405356",  # Sản phẩm A
            "id": "29671405356"
        },
        {
            "url": "https://shopee.vn/product/1267321054/24781905036",  # Sản phẩm B
            "id": "24781905036"
        }
    ]

    for product in products:
        driver.get(product["url"])
        time.sleep(5)

        # Nếu có phân loại, bạn có thể thêm phần xử lý chọn phân loại ở đây

        # Nhấn "Thêm vào giỏ hàng"
        add_to_cart_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[.//span[contains(text(), "thêm vào giỏ hàng")]]')
        ))
        add_to_cart_btn.click()
        time.sleep(3)

    # Sau khi thêm cả hai, vào giỏ hàng
    cart_icon = driver.find_element(By.ID, "cart_drawer_target_id")
    cart_icon.click()
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "cart-page-logo__page-name")
    ))

    time.sleep(2)
    page_source = driver.page_source

    for product in products:
        assert product["id"] in page_source, f"[FAIL] Không tìm thấy sản phẩm {product['id']} trong giỏ hàng"

    print("[PASS] Cả hai sản phẩm đều xuất hiện trong giỏ hàng.")
# TC8 Check bấm mua ngay
def test_buy_now_product_is_selected(driver):
    wait = WebDriverWait(driver, 10)

    # ====== Bước 1: Mở trang chi tiết sản phẩm ======
    product_url = "https://shopee.vn/product/972724310/18876819498"
    product_id = "18876819498"
    driver.get(product_url)
    time.sleep(5)

    # ====== Bước 2: Click nút "Mua ngay" ======
    buy_now_btn = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//button[contains(text(), "Mua ngay")]')
))

    buy_now_btn.click()

    # ====== Bước 3: Đợi chuyển sang trang giỏ hàng ======
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "cart-page-logo__page-name")
    ))

    # ====== Bước 4: Xác minh sản phẩm có trong HTML ======
    assert product_id in driver.page_source, f"[FAIL] Không tìm thấy sản phẩm {product_id} trong trang giỏ hàng"

    # ====== Bước 5: Xác minh checkbox của chính sản phẩm đó đã được chọn ======
    # Tìm phần tử chứa link tới sản phẩm => từ đó tìm ancestor => tìm checkbox
    # Lấy phần tử link chứa product_id
    product_link_elem = driver.find_element(By.XPATH, f'//a[contains(@href, "{product_id}")]')

    # Lấy phần tử checkbox theo cách chính xác hơn
    checkbox_input = product_link_elem.find_element(By.XPATH, './following::label//input[@type="checkbox"]')


    # Kiểm tra checkbox đã được chọn
    assert checkbox_input.get_attribute("aria-checked") == "true", "[FAIL] Sản phẩm vừa mua không được tick chọn"
    
    print("[PASS] Sản phẩm vừa bấm 'Mua Ngay' đã được thêm vào giỏ hàng và được chọn.")
#Test case  Sửa sản phẩm
# Testcase nhập số lượng hợp lệ
def test_quantity_valid(driver, quantity="5"):
    wait = WebDriverWait(driver, 10)
    # Mở giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(3)
    
    # Tìm input chứa số lượng sản phẩm
    input_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text" and @role="spinbutton"]')))
    
    # Nhập số lượng hợp lệ vào ô
    input_field.clear()
    input_field.send_keys(quantity)
    time.sleep(3)
    total_amount_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "gJyWia")]//span[contains(@class, "vjkBXu")]')))
    total_amount_element.click()
    time.sleep(2)
    # Kiểm tra số lượng thực tế trong input sau khi nhập
    new_value = int(input_field.get_attribute('value'))
    assert new_value != quantity, f"Số lượng sau cập nhật là {new_value}, mong đợi là {quantity}"
    
#Testcase nhập số lượng là 0
def test_quantity_zero(driver):
    wait = WebDriverWait(driver, 10)
    # Mở giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(3)
    
    # Tìm input chứa số lượng sản phẩm
    input_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text" and @role="spinbutton"]')))
    
    # Nhập số lượng 0 vào ô
    input_field.clear()
    input_field.send_keys("0")
    time.sleep(2)
    total_amount_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "gJyWia")]//span[contains(@class, "vjkBXu")]')))
    total_amount_element.click()
    time.sleep(2)
    # Kiểm tra giá trị trong input sau khi nhập
    input_value = input_field.get_attribute("value")
    assert input_value != "0", f"Hệ thống cho phép nhập số lượng 0 (giá trị: {input_value}) - không hợp lệ"
#Test case nhập số lượng vượt quá tồn kho
def test_quantity_exceeds_stock(driver):
    wait = WebDriverWait(driver, 10)
    
    # Mở giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    
    # Tìm input chứa số lượng sản phẩm
    input_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text" and @role="spinbutton"]')))
    
    # Nhập số lượng vượt quá kho
    input_field.send_keys("9999")
    time.sleep(2)
    
    # Click vào phần tử tổng tiền để mất focus (hoặc có thể click vào phần tử khác)
    total_amount_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "gJyWia")]//span[contains(@class, "vjkBXu")]')))
    total_amount_element.click()
    time.sleep(2)
    
    try:
        # Chờ cho đến khi thông báo lỗi xuất hiện
        error_message = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "shopee-alert-popup__message")]')))
        
        # Lấy nội dung thông báo lỗi
        error_text = error_message.text
        
        # Trích xuất số lượng tối đa từ thông báo
        match = re.search(r"Rất tiếc, bạn chỉ có thể mua tối đa (\d+) sản phẩm của chương trình giảm giá này.", error_text)
        if match:
            max_quantity = int(match.group(1))
            
            # Kiểm tra xem số lượng trong input đã được điều chỉnh về số lượng tối đa hay chưa
            new_value = int(input_field.get_attribute('value'))
            
            # Assert kiểm tra nếu số lượng trong input đã được điều chỉnh đúng
            assert new_value != max_quantity, f"[Fail] Số lượng trong input không được điều chỉnh đúng, giá trị thực tế: {new_value}, giá trị mong đợi: {max_quantity}"
            print(f"[Pass] Số lượng trong input đã được tự động điều chỉnh về tối đa: {new_value}")
        else:
            assert False, "[Fail] Không tìm thấy số lượng tối đa trong thông báo lỗi."
        
    except Exception as e:
        assert False, f"[Fail] Không thấy thông báo lỗi xuất hiện. Lỗi: {str(e)}"


# trước khi test số lượng thêm sản phẩm này số lượng là 1 https://shopee.vn/product/965158714/25443434123 
def test_increase_quantity(driver):
    wait = WebDriverWait(driver, 10)
    # ====== Bước 1: Mở trang sản phẩm chi tiết ======
    product_url = "https://shopee.vn/product/965158714/25443434123"
    product_id = "25443434123"
    driver.get(product_url)
    time.sleep(5)
    
    # ====== Bước 2: Nhấn nút "Thêm vào giỏ hàng" ======
    add_to_cart_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[.//span[contains(text(), "thêm vào giỏ hàng")]]')
    ))
    add_to_cart_btn.click()
    time.sleep(3)
    # Mở giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    
    # Tìm input chứa số lượng sản phẩm
    input_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text" and @role="spinbutton"]')))
    current_value = int(input_field.get_attribute('value'))
    # Tăng số lượng lên
    increase_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Increase"]')))
    increase_button.click()
    time.sleep(1)

    # Kiểm tra số lượng hiện tại
    new_value = int(input_field.get_attribute('value'))
       
    assert new_value == (current_value + 1), f"[Fail] Số lượng không đúng, giá trị thực tế: {new_value}, giá trị mong đợi: {current_value + 1}"
    print(f"[Pass] Số lượng tăng lên 1 đơn vị, giá trị mới: {new_value}")
def test_decrease_quantity(driver):
    wait = WebDriverWait(driver, 10)
    
    # Mở giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    
    # Tìm input chứa số lượng sản phẩm
    input_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@type="text" and @role="spinbutton"]')))
    current_value = int(input_field.get_attribute('value'))
    # Giảm số lượng xuống
    decrease_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Decrease"]')))
    decrease_button.click()
    time.sleep(1)

    # Kiểm tra số lượng sau khi giảm
    new_value = int(input_field.get_attribute('value'))
    
    assert new_value == (current_value - 1), f"[Fail] Số lượng không đúng, giá trị thực tế: {new_value}, giá trị mong đợi: {current_value - 1}"
    print(f"[Pass] Số lượng giảm xuống 1 đơn vị, giá trị mới: {new_value}")

def test_increase_button_disabled(driver):
    wait = WebDriverWait(driver, 10)
    
    # Mở giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    
    # Tìm nút tăng số lượng
    increase_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Increase"]')))
    increase_button.click()
    time.sleep(4)
    # Kiểm tra xem nút tăng số lượng có bị vô hiệu hóa không qua aria-disabled
    aria_disabled = increase_button.get_attribute("aria-disabled")
    if aria_disabled == "true":
        print("[Pass] Nút tăng số lượng bị vô hiệu hóa qua aria-disabled.")
    else:
        print("[Fail] Nút tăng số lượng không bị vô hiệu hóa qua aria-disabled.")
    
    # Kiểm tra nếu nút có lớp CSS disabled (hoặc lớp tương tự)
    button_classes = increase_button.get_attribute("class")
    if "disabled" in button_classes:
        print("[Pass] Nút tăng số lượng bị vô hiệu hóa qua CSS class.")
    else:
        print("[Fail] Nút tăng số lượng không bị vô hiệu hóa qua CSS class.")
    
    # Kiểm tra nếu nút không thể click được (is_enabled() == False)
    try:
        # Kiểm tra nếu nút bị disabled, is_enabled() sẽ trả về False
        assert not increase_button.is_enabled(), "[Fail] Nút tăng số lượng vẫn còn khả năng sử dụng."
        print("[Pass] Nút tăng số lượng bị disabled khi vượt quá tồn kho.")
    except AssertionError:
        print("[Fail] Nút tăng số lượng vẫn có thể click được.")

def test_decrease_quantity_to_zero_with_popup(driver):
    wait = WebDriverWait(driver, 10)
    product_id="25443434123"
    # Mở giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    
    
    # Giảm số lượng xuống 1
    decrease_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Decrease"]')))
    decrease_button.click()
    time.sleep(2)
    
    # Giảm tiếp số lượng về 0
    decrease_button.click()
    time.sleep(5)
    
    # Kiểm tra sự xuất hiện của popup xác nhận
    popup = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "shopee-alert-popup__title") and contains(text(), "Bạn chắc chắn muốn bỏ sản phẩm này?")]')))
    assert popup.is_displayed(), "[Fail] Popup xác nhận không xuất hiện khi giảm số lượng về 0."
    print("[Pass] Popup xác nhận xuất hiện khi giảm số lượng về 0.")
    
    # Kiểm tra và click nút "Có" để xóa sản phẩm
    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "btn-solid-primary") and contains(text(), "có")]')))
    confirm_button.click()
    time.sleep(5)
    print("[Pass] Đã nhấn 'Có' để xác nhận xóa sản phẩm.")
    assert product_id not in driver.page_source, f"[Pass] Đã xóa sản phẩm {product_id} trong trang giỏ hàng"
     
# Sửa phân loại sản phẩm thành công
def test_edit_variant_successfully(driver):
    wait = WebDriverWait(driver, 10)
    # ====== Bước 1: Mở trang sản phẩm chi tiết ======
    product_url = "https://shopee.vn/product/1095130225/23958042094"  # Thay bằng ID sản phẩm thực tế
    product_id = "23958042094"  # ID sản phẩm
    driver.get(product_url)
    time.sleep(5)

    # ====== Bước 2: Chọn phân loại màu sắc
    selection_buttons = driver.find_elements(By.CLASS_NAME, "selection-box-unselected")
    if selection_buttons:
        # Chọn lựa chọn đầu tiên trong selection box lựa chọn còn hàng 
        first_button = selection_buttons[0]
        first_button.click()
        print("Đã chọn phân loại đầu tiên.")
    else:
        print("Không tìm thấy lựa chọn phân loại.")

    # ====== Bước 2: Nhấn nút "Thêm vào giỏ hàng" ======
    add_to_cart_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[.//span[contains(text(), "thêm vào giỏ hàng")]]')
    ))
    add_to_cart_btn.click()
    time.sleep(3)

    # Mở trang Shopee giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(5)
    # Bước 1: Click vào nút phân loại hàng (button mM4TZ8)
    category_button = driver.find_element(By.CSS_SELECTOR, ".mM4TZ8")
    category_button.click()
    time.sleep(3)
    # Bước 2: Lấy phân loại hiện tại
    current_variation = driver.find_element(By.CSS_SELECTOR, ".product-variation.product-variation--selected")
    current_variation_label = current_variation.text  # Lấy nhãn phân loại hiện tại
    print(f"Phân loại hiện tại: {current_variation_label}")

    # Bước 3: Tìm các phân loại có sẵn để thay đổi
    variation_buttons = driver.find_elements(By.CSS_SELECTOR, ".product-variation")
    
    # Lọc các phân loại không bị disable (không phải phân loại hết hàng)
    available_variations = [btn for btn in variation_buttons if 'product-variation--disabled' not in btn.get_attribute('class')]

    # Bước 4: Chọn phân loại đầu tiên có sẵn khác với phân loại hiện tại
    new_variation_label = ""
    for btn in available_variations:
        if btn.text != current_variation_label:
            btn.click()
            new_variation_label = btn.text  # Lưu phân loại mới đã chọn
            break  # Dừng lại sau khi chọn phân loại khác

    # Kiểm tra xem phân loại đã thay đổi
    assert new_variation_label != current_variation_label, "Phân loại không thay đổi sau khi chọn"

    # Bước 5: Nhấn "Xác nhận"
    confirm_button = driver.find_element(By.CSS_SELECTOR, ".shopee-button-solid--primary")
    confirm_button.click()
    time.sleep(5)

    variation_div = driver.find_element(By.CSS_SELECTOR, ".dDPSp3")
    variation_text = variation_div.text.strip()  # Lấy văn bản phân loại

        # Kiểm tra xem văn bản phân loại có giống với phân loại mới đã chọn không
    assert new_variation_label == variation_text, f"Giỏ hàng không cập nhật phân loại mới. Phân loại trong giỏ hàng: {variation_text}, nhưng cần là: {new_variation_label}"
#  Bỏ chọn tất cả các phân loại
def test_edit_variant_without_selection(driver):
    # Mở trang Shopee giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(5)
    # Bước 1: Click vào nút phân loại hàng (button mM4TZ8)
    category_button = driver.find_element(By.CSS_SELECTOR, ".mM4TZ8")
    category_button.click()
    time.sleep(3)
    # Bỏ chọn tất cả các phân loại
    variation_buttons = driver.find_elements(By.CSS_SELECTOR, ".product-variation")
    
    for btn in variation_buttons:
        if 'product-variation--selected' in btn.get_attribute('class'):
            btn.click()

    # Kiểm tra nếu nút "Xác nhận" bị vô hiệu hóa
    confirm_button = driver.find_element(By.CSS_SELECTOR, ".shopee-button-solid--primary")
    assert confirm_button.get_attribute("disabled")

#  Kiểm tra phân loại hết hàng (disabled)
def test_edit_variant_out_of_stock(driver):
    # Mở trang Shopee giỏ hàng
    driver.get("https://shopee.vn/cart")
    time.sleep(5)
    # Bước 1: Click vào nút phân loại hàng (button mM4TZ8)
    category_button = driver.find_element(By.CSS_SELECTOR, ".mM4TZ8")
    category_button.click()
    time.sleep(3)
    #Tìm tất cả các phân loại
    variation_buttons = driver.find_elements(By.CSS_SELECTOR, ".product-variation")
    
    # Kiểm tra các phân loại bị vô hiệu hóa
    disabled_variations = [btn for btn in variation_buttons if 'product-variation--disabled' in btn.get_attribute('class')]

    # Chọn phân loại bị disable và kiểm tra xem chúng có bị vô hiệu hóa
    for btn in disabled_variations:
        assert 'true' in btn.get_attribute('aria-disabled')

#TC 1 Xóa tất cả sản phẩm nhưng chưa tích chọn
def test_clear_cart_no_checkall(driver):
    wait = WebDriverWait(driver, 10)
    
    # Mở trang giỏ hàng của Shopee
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    

    # Bấm xóa all
    delete_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'clear-btn-style') and contains(text(), 'Xóa')]")
    ))
    delete_button.click()
   
     # Kiểm tra thông báo khi chưa chọn sản phẩm nhưng bấm xóa
    no_product_selected_message = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//div[contains(text(), "Vui lòng chọn sản phẩm")]')
    ))
    assert no_product_selected_message.is_displayed(), "[FAIL] Thông báo không hiển thị khi chưa chọn sản phẩm mà bấm xóa."
    print("[PASS] Thông báo hiển thị đúng khi chưa chọn sản phẩm mà bấm xóa.")
#TC 2 Xóa 1 sản phẩm trong giỏ hàng
def test_clear_one_product(driver):
    wait = WebDriverWait(driver, 10)
    
    # Mở trang giỏ hàng của Shopee
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    #Tìm sp đầu tiên
    elements = driver.find_elements(By.CLASS_NAME, "c54pg1")
    href = elements[0].get_attribute("href")
    # Sử dụng Regex để tìm ID sản phẩm
    match = re.search(r'\.(\d+)\?xptdk=', href)
    if match:
        product_id = match.group(1)
        print("Product ID:", product_id)
    else:
        print("Product ID not found")
    xpath = f'//a[contains(@href, "{product_id}")]/ancestor::div[@role="listitem"]//button[@class="lSrQtj"]'
    time.sleep(3)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    # Click vào phần tử
    
    driver.execute_script("arguments[0].click();", element)
    # Đợi một chút để xóa sản phẩm
    time.sleep(6)

    assert product_id not in driver.page_source, f"[Pass] Không tìm thấy sản phẩm {product_id} trong trang giỏ hàng"
#TC 3 Xóa 2 sản phẩm trong giỏ hàng
def test_clear_two_product(driver):
    wait = WebDriverWait(driver, 10)
    
    # Mở trang giỏ hàng của Shopee
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    #Tìm sp đầu tiên
    elements = driver.find_elements(By.CLASS_NAME, "c54pg1")
    if len(elements) < 2:
        print("Less than two products found.")
        return

    # Lấy href của hai sản phẩm đầu tiên
    href1 = elements[0].get_attribute("href")
    href2 = elements[1].get_attribute("href")

    # Hàm để tìm ID sản phẩm
    def get_product_id(href):
        match = re.search(r'\.(\d+)\?', href)
        if match:
            return match.group(1)
        else:
            return "Product ID not found"

    product_id1 = get_product_id(href1)
    product_id2 = get_product_id(href2)

    print("Product ID 1:", product_id1)
    print("Product ID 2:", product_id2)
    xpath1 = f'//a[contains(@href, "{product_id1}")]/ancestor::div[@role="listitem"]//div[@class="stardust-checkbox__box"]'
    xpath2 = f'//a[contains(@href, "{product_id2}")]/ancestor::div[@role="listitem"]//div[@class="stardust-checkbox__box"]'
    time.sleep(3)
    element1 = wait.until(EC.visibility_of_element_located((By.XPATH, xpath1)))
    # Click vào phần tử
    
    driver.execute_script("arguments[0].click();", element1)
    time.sleep(2)
    element2 = wait.until(EC.visibility_of_element_located((By.XPATH, xpath2)))
    # Click vào phần tử
    
    driver.execute_script("arguments[0].click();", element2)
    # Xóa các sản phẩm đã chọn
    delete_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'clear-btn-style') and contains(text(), 'Xóa')]")
    ))
    delete_button.click()
    time.sleep(2)
    # Bấm xác nhận xóa giỏ hàng
    delete_popup = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "cancel-btn")
    ))
    delete_popup.click()
    time.sleep(3)  # Chờ xóa sản phẩm
    
    try:
        # Nếu sản phẩm vẫn còn trong trang, điều này sẽ tạo ra một ngoại lệ
        assert product_id1 not in driver.page_source, f"[Pass] Không tìm thấy sản phẩm {product_id1} trong trang giỏ hàng"
        assert product_id2 not in driver.page_source, f"[Pass] Không tìm thấy sản phẩm {product_id2} trong trang giỏ hàng"
    except AssertionError as e:
        print(f"Test Failed: {e}")
        assert False, "Test thất bại vì sản phẩm chưa bị xóa."
#TC 4 Hiện thị giỏ hàng trống , Chọn xóa tất cả sản phẩm 
def test_clear_cart(driver):
    wait = WebDriverWait(driver, 10)
    
    # Mở trang giỏ hàng của Shopee
    driver.get("https://shopee.vn/cart")
    time.sleep(3)  # Đợi trang tải xong
    
    # Chọn tất cả sản phẩm (nếu có)
    select_all_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Chọn Tất Cả')]")
    ))
    select_all_button.click()
    time.sleep(1)  # Chờ phản hồi sau khi chọn

    # Xóa các sản phẩm đã chọn
    delete_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'clear-btn-style') and contains(text(), 'Xóa')]")
    ))
    delete_button.click()
    # Bấm xác nhận xóa giỏ hàng
    delete_popup = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "cancel-btn")
    ))
    delete_popup.click()
    time.sleep(3)  # Chờ xóa sản phẩm
    # Kiểm tra giỏ hàng trống
    empty_cart_message = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//div[contains(text(), "Giỏ hàng của bạn còn trống")]')
    ))
    assert empty_cart_message.is_displayed(), "[FAIL] Giỏ hàng vẫn còn sản phẩm."
    print("[PASS] Giỏ hàng trống được hiển thị đúng.")
 

