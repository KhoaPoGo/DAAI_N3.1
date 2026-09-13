
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
    df = src[[
        "shipper_id", "shipper_company", "shipper_vehicle",
        "shipper_experience_years", "shipper_rating",
        "delivery_success_rate", "average_delivery_time",
        "working_shift", "join_date", "shipper_name", "shipper_phone",
        "shipper_gender", "shipper_age", "shipper_marital_status", "shipper_education"
    ]].copy()

    df["shipper_id"] = df["shipper_id"].astype("string").str.strip()
    df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")
    for c in ["shipper_experience_years", "shipper_age"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["shipper_rating", "delivery_success_rate", "average_delivery_time"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["shipper_id"]).drop_duplicates(subset=["shipper_id"])
    assert_unique(df, ["shipper_id"], "Shippers")
    save(df, "Shippers.csv")

if __name__ == "__main__":
    main()
