#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

from src.data_manager import add_person, delete_by_column, filter_by_month


def run_gui():
    def create_empty_parquet(filepath):
        empty_df = pd.DataFrame(columns=["Фамилия", "Имя", "Телефон", "Дата рождения"])
        empty_df.to_parquet(filepath, index=False)

    def ask_file():
        file_path = filedialog.askopenfilename(
            title="Выберите parquet-файл",
            filetypes=[("Parquet files", "*.parquet")],
            defaultextension=".parquet",
        )
        if not file_path:
            file_path = filedialog.asksaveasfilename(
                title="Создать новый parquet-файл",
                filetypes=[("Parquet files", "*.parquet")],
                defaultextension=".parquet",
            )
            if file_path:
                create_empty_parquet(file_path)
                messagebox.showinfo("Информация", f"Создан новый файл: {file_path}")
            else:
                messagebox.showerror("Ошибка", "Файл не выбран.")
                return None
        return file_path

    file_path = ask_file()
    if not file_path:
        return

    def on_add():
        try:
            add_person(
                last_name_var.get(),
                first_name_var.get(),
                phone_var.get(),
                birthdate_var.get(),
                file_path,
            )
            messagebox.showinfo("Успех", "Запись добавлена!")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def on_filter():
        try:
            month = int(month_var.get())
            results = filter_by_month(month, file_path)
            result_text.delete("1.0", tk.END)
            if results.empty:
                result_text.insert(tk.END, "Нет людей с днем рождения в этом месяце.")
            else:
                result_text.insert(tk.END, results.to_string(index=False))
        except ValueError:
            messagebox.showerror("Ошибка", "Месяц должен быть числом от 1 до 12")

    def on_delete():
        try:
            delete_by_column(delete_column_var.get(), delete_value_var.get(), file_path)
            messagebox.showinfo("Готово", "Удаление завершено")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    root = tk.Tk()
    root.title("Учет данных о людях")
    root.geometry("600x550")

    tk.Label(root, text="Фамилия").pack()
    last_name_var = tk.StringVar()
    tk.Entry(root, textvariable=last_name_var).pack()

    tk.Label(root, text="Имя").pack()
    first_name_var = tk.StringVar()
    tk.Entry(root, textvariable=first_name_var).pack()

    tk.Label(root, text="Телефон").pack()
    phone_var = tk.StringVar()
    tk.Entry(root, textvariable=phone_var).pack()

    tk.Label(root, text="Дата рождения (ДД.ММ.ГГГГ)").pack()
    birthdate_var = tk.StringVar()
    tk.Entry(root, textvariable=birthdate_var).pack()

    tk.Button(root, text="Добавить", command=on_add).pack(pady=5)

    tk.Label(root, text="Фильтр по месяцу рождения (1-12)").pack()
    month_var = tk.StringVar()
    tk.Entry(root, textvariable=month_var).pack()
    tk.Button(root, text="Показать", command=on_filter).pack(pady=5)

    result_text = tk.Text(root, height=10, width=70)
    result_text.pack()

    tk.Label(root, text="Удалить записи по колонке").pack()
    delete_column_var = tk.StringVar()
    delete_column_menu = ttk.Combobox(root, textvariable=delete_column_var)
    delete_column_menu["values"] = ["Фамилия", "Имя", "Телефон"]
    delete_column_menu.pack()

    delete_value_var = tk.StringVar()
    tk.Entry(root, textvariable=delete_value_var).pack()
    tk.Button(root, text="Удалить", command=on_delete).pack(pady=5)

    root.mainloop()
