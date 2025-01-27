import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
                   id INTEGER PRIMARY KEY,
                   title TEXT NOT NULL,
                   description TEXT,
                   price INTEGER NOT NULL
                   )'''
                   )
    connection.commit()


def new_product(title, description, price):
    check_product = cursor.execute('SELECT * FROM Products WHERE title=?', (title,))
    if check_product.fetchone() is None:
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)', (title, description, price))
        connection.commit()


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()


if __name__ == '__main__':
    initiate_db()
    new_product('Витамин А', 'Комплекс для ежедневного использования', 100)
    new_product('Витамин B', 'Комплекс для легких нагрузок', 200)
    new_product('Витамин C', 'Комплекс для нормальных нагрузок', 300)
    new_product('Витамин D', 'Комплекс для тяжелых нагрузок', 400)

    connection.close()
