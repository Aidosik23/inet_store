import psycopg2

# установка соединения с базой данных
postgres = psycopg2.connect(
    host="localhost",
    database="internet_store",
    user="postgres",
    password="qwerty123",
    port = 5432
)

cursor = postgres.cursor()

def get_all_product():
    query = ''' SELECT * FROM product;
    '''
    cursor.execute(query=query)
    all_product = cursor.fetchall()
    return all_product

def product_categories():
    query = '''SELECT * FROM category; 
    '''
    cursor.execute(query=query)
    all_categories = cursor.fetchall()
    return all_categories

def product_brand():
    query = '''SELECT * FROM brand; 
    '''
    cursor.execute(query=query)
    all_brand = cursor.fetchall()
    return all_brand
#---------------------------------------------------------------------
def names_brand():
    query = '''SELECT * FROM brand;'''
    cursor.execute(query=query)
    all_brands = cursor.fetchall()
    return all_brands

def get_brand_info(brand_id):
    try:
        query = '''SELECT * FROM product 
                WHERE brand = {}; 
        '''
        cursor.execute(query=query.format(brand_id))
        brand_info = cursor.fetchone()
        return brand_info
    except psycopg2.errors.UndefinedColumn:
        print("Ошибка нет такой ID")
#---------------------------------------------------------------------------------

def names_category():
    query = '''SELECT * FROM category; 
    '''
    cursor.execute(query=query)
    all_category = cursor.fetchall()
    return all_category
    # for category in all_category:
    #      print(f"{category[0]}. {category[1]}")
def get_category_info(category_name):  
    query_a = ''' SELECT p.name, p.price, c.name as category, b.product_name as brand
FROM product p 
JOIN brand b on p.brand = b.product_id
JOIN category c on p.category = c.product_id
WHERE c.name = %s;
        '''
    cursor.execute(query_a, (category_name,))
    category_phones = cursor.fetchall()
    mess = ''
    for i in category_phones:
        mess += str(i) + '\n'
    return mess

#------------------------------------------------------------------------------------------

def delete_products():
    query = '''SELECT * FROM product;'''
    cursor.execute(query=query)
    all_product = cursor.fetchall()
    return all_product

def get_delete_prod(delete_id):
    query = '''DELETE FROM product WHERE product_id = %s;'''
    cursor.execute(query, (delete_id,))
    postgres.commit()
    if cursor.rowcount == 0:
        return None
    else:
        return "Продукт с ID {} был успешно удален".format(delete_id)

#----------------------------------------------------------------------------------        
def add_product():
    query = '''SELECT * FROM product;'''
    cursor.execute(query=query)
    all_product = cursor.fetchall()
    return all_product


def get_add_product(add_id):
    query = "INSERT INTO product (name, price, desk, created, category, brand) VALUES (%s, %s, %s, %s, %s, %s)"
    # values = (name, price, desk, created, category_id, brand_id)
    cursor.execute(query, (add_id,))
    postgres.commit()
    if cursor.rowcount == 0:
        return None
    else:
        return "Продукт успешно добавлен!"
#------------------------------------------------------------------------------------------------------------------------

def update_product():
    print("Список всех продуктов:")
    query = '''SELECT * FROM product;'''
    cursor.execute(query)
    all_products = cursor.fetchall()
    for product in all_products:
        print(product)
    product_id = input("Введите ID продукта для изменения: ")
    query = '''SELECT * FROM product WHERE product_id = %s;'''
    cursor.execute(query, (product_id,))
    product_info = cursor.fetchone()
    if product_info:
        print(f"Название продукта: {product_info[1]}")
        new_name = input("Введите новое название продукта (оставьте пустым, если не хотите изменять): ")
        if new_name:
            product_info[1] = new_name
        print(f"Цена продукта: {product_info[2]} сом.")
        new_price = input("Введите новую цену продукта (оставьте пустым, если не хотите изменять): ")
        if new_price:
            product_info[2] = new_price
        print(f"Описание продукта {product_info[3]}")    
        new_desk = input("Введите новое описание продукт(Оставьте пустым, если не хотите его изменять): ")    
        if new_desk:
            product_info[3] = new_desk
        print(f"Дата создания {product_info[4]}")    
        new_created = input("Введите новую дату создания(Оставьте пустым, если не хотите изменять): ")
        if new_created:
            product_info[4] = new_created
        query = '''UPDATE product SET name = %s, price = %s, desk = %s, created =%s WHERE product_id = %s;'''
        cursor.execute(query, (product_info[1], product_info[2], product_info[3], product_info[4], product_id))
        postgres.commit()
        print("Запись успешно обновлена!")
    else:
        print("Продукт с таким ID не найден.")

def search_product():
    search_prod = input("Введите слово (название или описание): ")
    query = '''SELECT * FROM product WHERE name ILIKE %s OR desk ILIKE %s;
    '''
    values = ('%' + search_prod + '%', '%' + search_prod + '%')
    cursor.execute(query, values)
    search_info = cursor.fetchall()
    if search_info:
        for prod in search_info:
            print(prod)
    else:
        print("Увы, но ничего не найдено!")
    search_prod_two = input("Введите (Дату создания, ID, цену, категорию или бренд: ")
    query_one = '''SELECT * FROM product WHERE product_id = %s OR price = %s OR created = %s OR category = %s OR brand = %s;
    '''
    values_one = (search_prod_two, search_prod_two, search_prod_two, search_prod_two, search_prod_two)    
    cursor.execute(query_one, values_one)
    search_info_two = cursor.fetchall()
    if search_info_two:
        for prod_two in search_info_two:
            print(prod_two)
    else:
        print("Увы, но ничего не найдено!")
         
def user_commands():
    print("Выберите команду: ")
    print("1: Показать все продукты")
    print("2: Показать все категории")
    print("3: Показать все Бренды")
    print("4: Выбрать Бренд")
    print("5: Выбрать категорию")
    print("6: Удалить запись по ID")
    print("7: Добавить запись")
    print("8: Обновить запись")
    print("9: Найти запись по ключевому слову")
    command = input("Введите команду: ")
    if command == '1':
        all_product = get_all_product()
        for prod in all_product:
            print(prod)
    elif command == '2':
        all_categories = product_categories()
        for i in all_categories:
            print(i)
    elif command == '3':
        all_brand = product_brand()
        for i in all_brand:
            print(i)
    elif command == '4':
        names_brand()
        print(get_brand_info())
    elif command == '5':    
        name_category = names_category()
        for i in name_category:
            print(i)
    elif command == '6':
        delete_products()     
    elif command == '7':
        add_product()     
    elif command == '8':
        update_product()
    elif command == '9':
        search_product()        
    else:
        print("Не верная команда!")    
