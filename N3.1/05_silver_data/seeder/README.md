# Pandas Seeder - từng bảng

Mỗi bảng có một file `.py` riêng. Các script đọc dữ liệu gốc trong thư mục `student_data/`,
chuẩn hóa dữ liệu theo mô hình 3NF và xuất CSV vào `seeder/output/`.

## Cấu trúc

student_data/
├── customers.csv
├── geography.csv
├── inventory.csv
├── order_items.csv
├── payments.csv
├── products.csv
├── promotions.csv
├── returns.csv
├── reviews.csv
├── web_traffic.csv
├── shipments_realistic.csv
└── orders_enriched.csv

seeder/
├── seed_geography.py
├── seed_customers.py
├── seed_products.py
├── seed_promotions.py
├── seed_sales_employees.py
├── seed_orders.py
├── seed_order_items.py
├── seed_payments.py
├── seed_shippers.py
├── seed_shipping_locations.py
├── seed_shipments.py
├── seed_returns.py
├── seed_reviews.py
├── seed_inventory.py
├── seed_web_traffic.py
└── run_all_seeders.py

## Cài đặt

pip install pandas

## Chạy một bảng

python seed_customers.py

## Chạy toàn bộ

python run_all_seeders.py

## Lưu ý quan trọng

- `order_items.csv` có trường hợp trùng `(order_id, product_id)`, vì vậy `OrderItems` dùng `order_item_id`.
- `promo_id` và `promo_id_2` được chuyển thành bảng liên kết `OrderItemPromotions`.
- Thông tin nhân viên bán hàng nằm trong `orders_enriched.csv` nên `SalesEmployees` được tách từ đó.
- Thông tin shipper và địa điểm giao hàng nằm trong `shipments_realistic.csv` nên được tách thành `Shippers` và `ShippingLocations`.
- Các thuộc tính mô tả sản phẩm trong `inventory.csv` không được lặp lại ở bảng Inventory; bảng Products là nơi quản lý chúng.
