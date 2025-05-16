import os
from datetime import datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

FILE = "people.parquet"

def load_data():
    if os.path.exists(FILE):
        return pd.read_parquet(FILE)
    return pd.DataFrame(columns=["Фамилия", "Имя", "Телефон", "Дата рождения"])

def save_data(df):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, FILE)

def add_person(last, first, phone, bdate_str):
    try:
        date = datetime.strptime(bdate_str, "%d.%m.%Y")
        birth_list = [date.day, date.month, date.year]
    except ValueError:
        raise ValueError("Дата в формате ДД.ММ.ГГГГ")
    df = load_data()
    new_row = {"Фамилия": last, "Имя": first, "Телефон": phone, "Дата рождения": birth_list}
    df = pd.concat([df, pd.DataFrame([new_row])])
    df = df.sort_values(by=["Фамилия", "Имя"])
    save_data(df)

def filter_by_month(month: int):
    df = load_data()
    return df[df["Дата рождения"].apply(lambda d: d[1] == month)]

def delete_by_column(col, val):
    df = load_data()
    if col not in df.columns:
        raise ValueError(f"Колонка '{col}' не найдена.")
    df = df[df[col] != val]
    save_data(df)
    return df
