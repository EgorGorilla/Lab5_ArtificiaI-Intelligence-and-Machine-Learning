#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame(columns=["Фамилия", "Имя", "Телефон", "Дата рождения"])


def save_data(df, file_path):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)


def add_person(last, first, phone, bdate_str, file_path):
    try:
        date = datetime.strptime(bdate_str, "%d.%m.%Y")
        birth_list = [date.day, date.month, date.year]
    except ValueError as e:
        raise ValueError("Дата должна быть в формате ДД.ММ.ГГГГ") from e

    df = load_data(file_path)
    new_row = {
        "Фамилия": last,
        "Имя": first,
        "Телефон": phone,
        "Дата рождения": birth_list,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df = df.sort_values(by=["Фамилия", "Имя"])
    save_data(df, file_path)


def filter_by_month(month: int, file_path):
    df = load_data(file_path)
    return df[df["Дата рождения"].apply(lambda d: d[1] == month)]


def delete_by_column(col, val, file_path):
    df = load_data(file_path)
    if col not in df.columns:
        raise ValueError(f"Колонка '{col}' не найдена.")
    df = df[df[col] != val]
    save_data(df, file_path)
    return df
