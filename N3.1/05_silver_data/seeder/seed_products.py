
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
    df = read_csv("products.csv")
    df = clean_strings(df)
    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce").astype("Int64")
    for c in ["price", "cogs"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[["product_id", "product_name", "category", "segment", "size", "color", "price", "cogs"]]
    df = df.dropna(subset=["product_id"]).drop_duplicates()
    df["product_id"] = df["product_id"].astype(int)
    assert_unique(df, ["product_id"], "Products")
    save(df, "Products.csv")

if __name__ == "__main__":
    main()
