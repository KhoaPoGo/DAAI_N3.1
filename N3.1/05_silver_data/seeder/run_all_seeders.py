
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent / "student_data"

def read_csv(name, **kwargs):
    path = BASE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {path}")
    return pd.read_csv(path, **kwargs)

def clean_strings(df):
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string").str.strip()
    return df

def save(df, name):
    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / name
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"Đã tạo: {out}")
    print(f"Số dòng: {len(df):,}")
    print(f"Số cột: {len(df.columns)}")
    return out

def assert_unique(df, cols, table_name):
    dup = df[df.duplicated(cols, keep=False)]
    if not dup.empty:
        raise ValueError(f"{table_name}: khóa {cols} bị trùng {len(dup):,} dòng.")

def assert_not_null(df, cols, table_name):
    bad = [c for c in cols if c in df.columns and df[c].isna().any()]
    if bad:
        raise ValueError(f"{table_name}: khóa bắt buộc bị NULL: {bad}")

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SEEDERS = [
    "seed_geography.py",
    "seed_customers.py",
    "seed_products.py",
    "seed_promotions.py",
    "seed_sales_employees.py",
    "seed_orders.py",
    "seed_order_items.py",
    "seed_payments.py",
    "seed_shippers.py",
    "seed_shipping_locations.py",
    "seed_shipments.py",
    "seed_returns.py",
    "seed_reviews.py",
    "seed_inventory.py",
    "seed_web_traffic.py",
]

for script in SEEDERS:
    print("\n" + "=" * 70)
    print(f"RUN: {script}")
    print("=" * 70)
    subprocess.run([sys.executable, str(HERE / script)], check=True)

print("\nHoàn tất toàn bộ Seeder Pandas.")
