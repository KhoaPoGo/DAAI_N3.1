
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

def main():
    src = read_csv("orders_enriched.csv")
    src = clean_strings(src)
    src["order_id"] = pd.to_numeric(src["order_id"], errors="coerce").astype("Int64")
    src["customer_id"] = pd.to_numeric(src["customer_id"], errors="coerce").astype("Int64")
    src["zip"] = pd.to_numeric(src["zip"], errors="coerce").astype("Int64")
    src["order_date"] = pd.to_datetime(src["order_date"], errors="coerce")

    # 3NF: geography fields, payment_method and employee descriptive fields
    # are not copied into Orders because they belong to their own entities.
    df = src[[
        "order_id", "order_date", "customer_id", "zip",
        "order_status", "device_type", "order_source", "sales_employee_id", "comment"
    ]].drop_duplicates(subset=["order_id"])

    df = df.dropna(subset=["order_id"])
    df["order_id"] = df["order_id"].astype(int)
    assert_unique(df, ["order_id"], "Orders")
    save(df, "Orders.csv")

if __name__ == "__main__":
    main()
