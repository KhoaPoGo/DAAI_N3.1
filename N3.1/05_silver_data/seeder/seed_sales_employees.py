
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
    # Employee attributes are embedded in orders_enriched.csv.
    src = read_csv("orders_enriched.csv", usecols=[
        "sales_employee_id", "sales_employee_name",
        "marital_status", "education_level", "years_experience"
    ])
    src = clean_strings(src)
    src["sales_employee_id"] = src["sales_employee_id"].astype("string").str.strip()
    src["years_experience"] = pd.to_numeric(src["years_experience"], errors="coerce")
    df = src.dropna(subset=["sales_employee_id"]).drop_duplicates(subset=["sales_employee_id"])
    df = df.rename(columns={"sales_employee_name": "employee_name"})
    df = df[["sales_employee_id", "employee_name", "marital_status", "education_level", "years_experience"]]
    assert_unique(df, ["sales_employee_id"], "SalesEmployees")
    save(df, "SalesEmployees.csv")

if __name__ == "__main__":
    main()
