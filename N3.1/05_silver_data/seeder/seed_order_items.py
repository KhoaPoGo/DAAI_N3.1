
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
    src = read_csv("order_items.csv")
    src = clean_strings(src)
    for c in ["order_id", "product_id", "quantity"]:
        src[c] = pd.to_numeric(src[c], errors="coerce").astype("Int64")
    for c in ["unit_price", "discount_amount"]:
        src[c] = pd.to_numeric(src[c], errors="coerce")

    # A surrogate key is required because (order_id, product_id) is not unique
    # in the source data.
    items = src[["order_id", "product_id", "quantity", "unit_price", "discount_amount"]].copy()
    items = items.dropna(subset=["order_id", "product_id"]).reset_index(drop=True)
    items.insert(0, "order_item_id", range(1, len(items) + 1))
    items["order_id"] = items["order_id"].astype(int)
    items["product_id"] = items["product_id"].astype(int)
    save(items, "OrderItems.csv")

    # 1NF/3NF: repeated promo_id and promo_id_2 become rows in a bridge table.
    promos = src[["promo_id", "promo_id_2"]].copy()
    promos.insert(0, "order_item_id", range(1, len(promos) + 1))
    long = promos.melt(
        id_vars=["order_item_id"],
        value_vars=["promo_id", "promo_id_2"],
        var_name="promo_slot",
        value_name="promo_id"
    )
    long["promo_id"] = long["promo_id"].astype("string").str.strip()
    long = long.dropna(subset=["promo_id"])
    long = long[long["promo_id"] != ""].drop_duplicates(["order_item_id", "promo_id"])
    long["sequence_no"] = long["promo_slot"].map({"promo_id": 1, "promo_id_2": 2})
    bridge = long[["order_item_id", "promo_id", "sequence_no"]].sort_values(["order_item_id", "sequence_no"])
    save(bridge, "OrderItemPromotions.csv")

if __name__ == "__main__":
    main()
