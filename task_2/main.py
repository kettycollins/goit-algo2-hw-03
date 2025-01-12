import os
import csv
import random
from timeit import timeit
from BTrees.OOBTree import OOBTree

def load_data(filename):
    # Формуємо шлях до файлу з поточного каталогу
    filepath = os.path.join(os.getcwd(), filename)
    print(f"Looking for file: {filepath}")  # Додано для виведення шляху до файлу
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist.")
    items = []
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            items.append({
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            })
    return items

# Функція для додавання товару до OOBTree
def add_item_to_tree(tree, item):
    tree[item["ID"]] = item

# Функція для додавання товару до dict
def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = item

# Функція для виконання діапазонного запиту на OOBTree
def range_query_tree(tree, min_price, max_price):
    return [
        value for key, value in tree.items()
        if min_price <= value["Price"] <= max_price
    ]

# Функція для виконання діапазонного запиту на dict
def range_query_dict(dictionary, min_price, max_price):
    return [
        value for key, value in dictionary.items()
        if min_price <= value["Price"] <= max_price
    ]

# Основна програма
def main():
    # Завантажуємо дані
    filename = "generated_items_data.csv"
    items = load_data(filename)

    # Ініціалізуємо структури даних
    tree = OOBTree()
    dictionary = {}

    # Додаємо дані до структур
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Випадкові межі для діапазонних запитів
    random_queries = [
        (random.uniform(10, 100), random.uniform(101, 200))
        for _ in range(100)
    ]

    # Виконуємо вимірювання продуктивності для OOBTree
    tree_time = timeit(
        stmt="for q in random_queries: range_query_tree(tree, q[0], q[1])",
        globals=globals(),
        number=1
    )

    # Виконуємо вимірювання продуктивності для dict
    dict_time = timeit(
        stmt="for q in random_queries: range_query_dict(dictionary, q[0], q[1])",
        globals=globals(),
        number=1
    )

    # Виводимо результати
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main()
