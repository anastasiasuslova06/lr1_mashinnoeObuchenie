import pandas as pd


def check_data_quality(df: pd.DataFrame) -> dict:
    """Проверяет пустые ячейки, некорректные данные, типы."""
    report = {
        "missing": df.isna().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "non_numeric": {},
    }
    for col in df.columns:
        if df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors="coerce")
            bad = df[col][converted.isna() & df[col].notna()]
            if not bad.empty:
                report["non_numeric"][col] = bad.tolist()[:10]
    return report


def show_table(df: pd.DataFrame, n: int = 10) -> None:
    """Печатает первые n строк, форму и типы."""
    print(df.head(n))
    print(f"\nShape: {df.shape}")
    print(f"Dtypes:\n{df.dtypes}")