#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import os
import pytest
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from src.data_manager import add_person, filter_by_month, delete_by_column, load_data

@pytest.fixture
def clean_data_file():
    test_file = "people.parquet"
    if os.path.exists(test_file):
        os.remove(test_file)
    yield test_file
    if os.path.exists(test_file):
        os.remove(test_file)

def test_add_person(clean_data_file):
    file_path = clean_data_file
    add_person("Иванов", "Иван", "123456", "01.01.2000", file_path)
    df = load_data(file_path)
    assert len(df) == 1
    assert df.iloc[0]["Фамилия"] == "Иванов"

def test_filter_by_month(clean_data_file):
    file_path = clean_data_file
    add_person("Петров", "Петр", "654321", "15.02.1990", file_path)
    results = filter_by_month(2, file_path)
    assert not results.empty
    assert results.iloc[0]["Имя"] == "Петр"

def test_delete_by_column(clean_data_file):
    file_path = clean_data_file
    add_person("Сидоров", "Сидор", "111222", "10.03.1985", file_path)
    delete_by_column("Фамилия", "Сидоров", file_path)
    df = load_data(file_path)
    assert df.empty
