
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
    src = read_csv("shipments_realistic.csv", usecols=["shipper_id", "city", "region", "district"])
    src = clean_strings(src)
    # Location belongs to the shipment destination in this source; it is separated
    # from Shipments to avoid repeating city/region/district on every shipment row.
    df = src[["city", "region", "district"]].drop_duplicates().reset_index(drop=True)
    df.insert(0, "shipping_location_id", range(1, len(df) + 1))
    assert_unique(df, ["shipping_location_id"], "ShippingLocations")
    save(df, "ShippingLocations.csv")

if __name__ == "__main__":
    main()
