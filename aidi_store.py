import telebot
import psycopg2
import internet_st

bot = telebot.TeleBot('5653681639:AAG0UP6P8PlLudgYlY4gOlAjf2p-JLXlp3c')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Выберите команду:\n1: Показать все продукты\n2: Показать все категории\n3: Показать все Бренды\n4: Выбрать Бренд\n5: Выбрать категорию\n6: Удалить запись\n7: Добавить продукт")
#--------------------------------------------------------------------------------------
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Список доступных команд:\n/start - начало работы\n/help - помощь")
#-------------------------------------------------------------------------------------
@bot.message_handler(commands=["choose_brand"])
def process_brand(message):
    brand = internet_st.get_brand_info(brand_id=message.text)
    msg = bot.send_message(message.chat.id, str(brand))
#------------------------------------------------------------------------------------   
@bot.message_handler(commands=["choose_category"])
def process_category(message):
    category = internet_st.get_category_info(category_name=message.text)
    msg = bot.send_message(message.chat.id, str(category))

#------------------------------------------------------------------------------------
@bot.message_handler(commands=["choose_delete_prod"])
def delete_prod_new(message):
    delete_prod = internet_st.get_delete_prod(delete_id=message.text)
    # msg = bot.send_message(message.chat.id, str(delete_prod))
    if delete_prod:
        bot.reply_to(message, f"Товар с ID {message.text} успешно удален.")
    else:
        bot.reply_to(message, f"Товар с ID {message.text} не найден.")
#------------------------------------------------------------------------------------    
@bot.message_handler(commands=["choose_add_prod"])
def add_new_prod(message):
    add_pod = internet_st.get_add_product(add_id=message.text)
    if add_pod:
        bot.reply_to(message, f"Товар успешно добавлен.")
    else:
        bot.reply_to(message, f"Товар не добавлен. Видимо ошибка")    



#------------------------------------------------------------------------------------    
@bot.message_handler(func=lambda message: True)
def user_commands(message):
    if message.text == '1':
        all_product = internet_st.get_all_product()
        mess = ''
        for prod in all_product:
            mess += str(prod) +'\n'+'\n'
        bot.reply_to(message, str(mess))
    
    elif message.text == '2':
        all_categories = internet_st.product_categories()
        mess = ''
        for i in all_categories:
            mess += str(i) + '\n' + '\n'
        bot.reply_to(message, str(mess))
    
    elif message.text == '3':
        all_brand = internet_st.product_brand()
        mess = ''
        for i in all_brand:
            mess += str(i) + '\n' + '\n'
        bot.reply_to(message, str(mess))
    
    elif message.text == '4':
        all_brands = internet_st.names_brand()
        mess = ''
        for brand in all_brands:
            mess += str(brand) + '\n'
        bot.reply_to(message, str(mess))
        msg = bot.send_message(message.chat.id, "Введите ID бренда: ")
        bot.register_next_step_handler(msg, process_brand)
    
    elif message.text == '5':
        all_category = internet_st.names_category()
        mess = ''
        for category in all_category:
            mess += str(category) + '\n'
        bot.reply_to(message, str(mess))
        msg = bot.send_message(message.chat.id, "Введите категорию (например: 'Phones'): ")    
        bot.register_next_step_handler(msg, process_category)
    
    elif message.text == '6':
        all_delete = internet_st.delete_products()
        mess = ''
        for i in all_delete:
            mess += str(i) + '\n'+'\n'
        bot.reply_to(message, str(mess))
        msg = bot.send_message(message.chat.id, "Введите ID Товара для удаления: ")
        bot.register_next_step_handler(msg, delete_prod_new) 
    
    elif message.text == '7':
        add_products = internet_st.add_product()
        mess = ''
        for i in add_products:
            mess += str(i)+'\n'+'\n'
        bot.reply_to(message, str(mess))
        msg= bot.send_message(message.chat.id, "Введите название продукта: ")
        msg= bot.send_message(message.chat.id, "Введите цену продукта : ")
        msg= bot.send_message(message.chat.id, "Введите характеристики : ")
        msg= bot.send_message(message.chat.id, "Введите дату создания : ")
        msg= bot.send_message(message.chat.id, "Введите ID категории продукта (1-Phones, 2-Laptop, 3-Tablet): ")
        msg= bot.send_message(message.chat.id, "Введите ID бренда продукта: 1-Xiaomi, 2-APPlE, 3-Samsung, 4-Lenovo, 5-Asus, 6-HP, 7-iPAD, 8- GalaxyTab, 9-Xiaomi-Pad: ")
        bot.register_next_step_handler(msg, add_new_prod)

        

    else:
        bot.reply_to(message, "Не верная команда!")  


# bot.polling(none_stop=True)
if __name__ == '__main__':
    print('Start bot...')
    bot.infinity_polling()
