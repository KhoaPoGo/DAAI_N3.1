
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
    src = read_csv("shipments_realistic.csv")
    src = clean_strings(src)
    for c in ["order_id"]:
        src[c] = pd.to_numeric(src[c], errors="coerce").astype("Int64")
    for c in ["ship_date", "delivery_date"]:
        src[c] = pd.to_datetime(src[c], errors="coerce")
    src["shipping_fee"] = pd.to_numeric(src["shipping_fee"], errors="coerce")

    # Create a deterministic location key from the natural location attributes.
    loc = src[["city", "region", "district"]].drop_duplicates().reset_index(drop=True)
    loc.insert(0, "shipping_location_id", range(1, len(loc) + 1))
    src = src.merge(loc, on=["city", "region", "district"], how="left")

    df = src[[
        "order_id", "shipper_id", "shipping_location_id",
        "ship_date", "delivery_date", "shipping_fee"
    ]].copy()
    df = df.dropna(subset=["order_id"]).reset_index(drop=True)
    df.insert(0, "shipment_id", range(1, len(df) + 1))
    df["order_id"] = df["order_id"].astype(int)
    save(df, "Shipments.csv")

if __name__ == "__main__":
    main()
