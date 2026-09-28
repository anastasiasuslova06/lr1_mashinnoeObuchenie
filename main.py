"""Точка входа: лабораторная работа №1, задания 1-5.

Запуск:
    python main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from src.config import DATA_DIR, OUTPUT_DIR, SEED, set_seeds, timestamped_filename
from src.io_utils import read_table, write_table, save_figure
from src.data_loader import check_data_quality, show_table


def section(title: str) -> None:
    """Печатает заголовок раздела."""
    line = "=" * 70
    print(f"\n{line}\n{title}\n{line}")


def main() -> int:
    # Фиксируем seed для воспроизводимости
    set_seeds(SEED)
    print(f"Seed зафиксирован: {SEED}")

    # ------------------------------------------------------------------
    # Задание 1. Чтение данных
    # ------------------------------------------------------------------
    section("Задание 1. Чтение данных")
    dataset_path = Path(DATA_DIR) / "dataset.xlsx"

    if not dataset_path.exists():
        print(f"[!] Файл не найден: {dataset_path}")
        print("    Положите dataset.xlsx в папку data/ и перезапустите.")
        return 1

    df = read_table(str(dataset_path))
    print(f"Загружено: {df.shape[0]} строк, {df.shape[1]} столбцов")

    # ------------------------------------------------------------------
    # Задание 5. Вывод таблицы
    # ------------------------------------------------------------------
    section("Задание 5. Вывод таблицы")
    show_table(df, n=10)

    # ------------------------------------------------------------------
    # Задание 4. Проверка качества данных
    # ------------------------------------------------------------------
    section("Задание 4. Проверка качества данных")
    report = check_data_quality(df)

    missing = {k: v for k, v in report["missing"].items() if v}
    if missing:
        print("Пропуски в столбцах:")
        for col, cnt in missing.items():
            print(f"  {col:<25} {cnt}")
    else:
        print("Пропусков нет.")

    print("\nТипы столбцов:")
    for col, dtype in report["dtypes"].items():
        print(f"  {col:<25} {dtype}")

    if report["non_numeric"]:
        print("\nНекорректные значения (первые примеры):")
        for col, vals in report["non_numeric"].items():
            print(f"  {col}: {vals}")
    else:
        print("\nНекорректных значений не найдено.")

    # ------------------------------------------------------------------
    # Задание 2. Запись данных во все форматы
    # ------------------------------------------------------------------
    section("Задание 2. Запись данных")
    paths = write_table(df, "dataset_copy")
    for fmt, p in paths.items():
        print(f"  {fmt:<5} -> {p}")

    # ------------------------------------------------------------------
    # Задание 3. Сохранение изображения (пример графика)
    # ------------------------------------------------------------------
    section("Задание 3. Сохранение изображения")
    import matplotlib
    matplotlib.use("Agg")  # без GUI, чтобы работало в консоли
    import matplotlib.pyplot as plt

    # Берём первые две числовые колонки для графика
    num_cols = df.select_dtypes(include="number").columns.tolist()
    fig, ax = plt.subplots(figsize=(8, 5))
    if len(num_cols) >= 2:
        ax.scatter(df[num_cols[0]], df[num_cols[1]], s=10, alpha=0.6)
        ax.set_xlabel(num_cols[0])
        ax.set_ylabel(num_cols[1])
        ax.set_title(f"{num_cols[0]} vs {num_cols[1]}")
    else:
        ax.text(0.5, 0.5, "Недостаточно числовых столбцов",
                ha="center", va="center")
        ax.set_title("Пример графика")

    fig_path = save_figure(fig, "scatter_example")
    plt.close(fig)
    print(f"График сохранён: {fig_path}")

    # ------------------------------------------------------------------
    section("Готово")
    print(f"Результаты в папке: {Path(OUTPUT_DIR).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())