import telebot
from telebot import types
from context import *
from secret import *

bot = telebot.TeleBot(telebotssss, parse_mode=None)

def is_admin(username):
    return username == "Alone_200_5" 

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bnt1 = types.KeyboardButton("/menu")
    markup.add(bnt1)

    setup_database()
    username = message.from_user.username
    chat_id = message.chat.id

    if username:
        add_user(username, chat_id)
        bot.reply_to(message, "Welcome! You are now a user.", reply_markup=markup)
    else:
        bot.reply_to(message, "Please enter your username.", reply_markup=markup)

@bot.message_handler(commands=['menu'])
def admin_menu_command(message):
    username = message.from_user.username
    if username:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            "Add Trip", 
            "Delete Trip", 
            "View Trips", 
            "Add Companion Request", 
            "Delete Companion Request", 
            "View Companion Requests", 
            "Find Companion",
            "Update Trip",
            "Update Companion Request"
        ]
        for button_text in buttons:
            markup.add(types.KeyboardButton(button_text))
        bot.send_message(message.chat.id, "Admin Menu:", reply_markup=markup)
    else:
        bot.reply_to(message, "You do not have access. Please provide your username.")

@bot.message_handler(commands=['find_passenger'])
def find_passenger_command(message):
    username = message.from_user.username
    if username:
        bot.reply_to(message, "Введите информацию для поиска попутчика:")
        bot.register_next_step_handler(message, add_find_passenger_info)
    else:
        bot.reply_to(message, "You do not have access.")

def add_find_passenger_info(message):
    passenger_info = message.text
    user_id = message.from_user.id
    add_books(user_id, "", "", "", passenger_info)
    bot.reply_to(message, "Запрос успешно добавлен.")

@bot.message_handler()
def admin_buttons(message):
    username = message.from_user.username
    if username:
        if message.text == "Add Trip":
            add_book(message)
        elif message.text == "Delete Trip":
            delete_trip(message)
        elif message.text == "View Trips":
            view_trips_step(message)
        elif message.text == "Add Companion Request":
            add_books(message)
        elif message.text == "Delete Companion Request":
            delete_companion_request(message)
        elif message.text == "View Companion Requests":
            view_companion_requests(message)
        elif message.text == "Find Companion":
            find_passenger_command(message)
        elif message.text == "Update Trip":
            save_updated_trip(message)
        elif message.text == "Update Companion Request":
            save_updated_companion_request(message)


book_dict = {}
def add_book(message):
    book_dict[message.chat.id] = {
        'user_id': '',
        'start_location': '',
        'end_location': '',
        'prodaction_date': '',
        'trip_date': '',
        'seats_available': '',
        'description': ''
    }
    bot.send_message(message.chat.id,"start_location: ")
    bot.register_next_step_handler(message,name)
    
def name(message):
    book_dict[message.chat.id]['start_location'] = message.text
    bot.send_message(message.chat.id,"end_location: ")
    bot.register_next_step_handler(message,janre_ids)
    
def janre_ids(message):
    book_dict[message.chat.id]['end_location'] = message.text
    bot.send_message(message.chat.id,"prodaction_date: ")
    bot.register_next_step_handler(message,author_ids)
    
def author_ids(message):
    book_dict[message.chat.id]['prodaction_date'] = message.text
    bot.send_message(message.chat.id,"trip_date: ")
    bot.register_next_step_handler(message,prodaction_dates)
    
def prodaction_dates(message):
    book_dict[message.chat.id]['trip_date'] = message.text
    bot.send_message(message.chat.id,"seats_available: ")
    bot.register_next_step_handler(message,pagess)
    
def pagess(message):
    book_dict[message.chat.id]['seats_available'] = message.text
    bot.send_message(message.chat.id,"description: ")
    bot.register_next_step_handler(message,pricec)
    
def pricec(message):
    book_dict[message.chat.id]['description'] = message.text
    conn = connection_database()
    cur = conn.cursor()
    cur.execute(f"""
     INSERT INTO trips (start_location, end_location, trip_date, seats_available, description) 
     VALUES ('{book_dict[message.chat.id]['start_location']}',  '{book_dict[message.chat.id]['end_location']}', '{book_dict[message.chat.id]['trip_date']}', '{book_dict[message.chat.id]['seats_available']}', '{book_dict[message.chat.id]['description']}')
                """)
    conn.commit()
    bot.send_message(message.chat.id,"korishumo angom shud: ")
    close_con(conn,cur)
    


book_dicts = {}
def add_books(message):
    book_dicts[message.chat.id] = {
        'start_location': '',
        'end_location': '',
        'prodaction_date': '',
        'trip_date': '',
        'description': ''
    }
    bot.send_message(message.chat.id,"start_location: ")
    bot.register_next_step_handler(message,names)
    
def names(message):
    book_dicts[message.chat.id]['start_location'] = message.text
    bot.send_message(message.chat.id,"end_location: ")
    bot.register_next_step_handler(message,janre_idss)
    
def janre_idss(message):
    book_dicts[message.chat.id]['end_location'] = message.text
    bot.send_message(message.chat.id,"prodaction_date: ")
    bot.register_next_step_handler(message,author_idss)
    
def author_idss(message):
    book_dicts[message.chat.id]['prodaction_date'] = message.text
    bot.send_message(message.chat.id,"trip_date: ")
    bot.register_next_step_handler(message,prodaction_datess)
    
def prodaction_datess(message):
    book_dicts[message.chat.id]['trip_date'] = message.text
    bot.send_message(message.chat.id,"description: ")
    bot.register_next_step_handler(message,pricecs)
    
def pricecs(message):
    book_dicts[message.chat.id]['description'] = message.text
    conn = connection_database()
    cur = conn.cursor()
    cur.execute(f"""
     INSERT INTO trips( start_location, end_location, trip_date,description) 
     VALUES ('{book_dicts[message.chat.id]['start_location']}',  '{book_dicts[message.chat.id]['end_location']}', '{book_dicts[message.chat.id]['trip_date']}',  '{book_dicts[message.chat.id]['description']}')""")
    conn.commit()
    bot.send_message(message.chat.id,"korishumo angom shud: ")
    close_con(conn,cur)


def delete_trip_step(message):
    bot.reply_to(message, "Enter the trip ID to delete:")
    bot.register_next_step_handler(message, delete_trip_info)

def delete_trip_info(message):
    trip_id = message.text
    delete_trip(trip_id)
    bot.reply_to(message, "Trip deleted!")

def view_trips_step(message):
    trips = get_trips()
    if trips:
        response = [f"ID: {trip[0]}, Start: {trip[2]}, End: {trip[3]}, Date: {trip[4]}, Seats: {trip[5]}\n" for trip in trips]
    else:
        response = "No available trips."
    bot.reply_to(message, response)



def delete_companion_request_step(message):
        bot.reply_to(message, "Enter the request ID to delete:")
        bot.register_next_step_handler(message, delete_companion_request_info)

def delete_companion_request_info(message):
    request_id = message.text
    if request_id:
        delete_companion_request(request_id)
        bot.reply_to(message, "Companion request deleted!")
    else:
        bot.send_message(message.chat.id,"Shumo id nadored")

def view_companion_requests_step(message):
    requests = get_companion_requests()
    if requests:
        response = [f"Request ID: {request[0]}, User ID: {request[1]}, Start: {request[2]}, End: {request[3]}\n" for request in requests]
    else:
        response = "No companion requests available."
    bot.reply_to(message, response)
    
    
def update_trip_info(message):
    trip_id = message.text
    bot.reply_to(message, "Enter new start location:")
    bot.register_next_step_handler(message, update_trip_start, trip_id)

def update_trip_start(message, trip_id):
    start_location = message.text
    bot.reply_to(message, "Enter new end location:")
    bot.register_next_step_handler(message, update_trip_end, trip_id, start_location)

def update_trip_end(message, trip_id, start_location):
    end_location = message.text
    bot.reply_to(message, "Enter new trip date (YYYY-MM-DD HH:MM:SS):")
    bot.register_next_step_handler(message, update_trip_date, trip_id, start_location, end_location)

def update_trip_date(message, trip_id, start_location, end_location):
    trip_date = message.text
    bot.reply_to(message, "Enter new seats available:")
    bot.register_next_step_handler(message, update_trip_seats, trip_id, start_location, end_location, trip_date)

def update_trip_seats(message, trip_id, start_location, end_location, trip_date):
    seats_available = message.text
    bot.reply_to(message, "Enter new description:")
    bot.register_next_step_handler(message, save_updated_trip, trip_id, start_location, end_location, trip_date, seats_available)

def save_updated_trip(message, trip_id, start_location, end_location, trip_date, seats_available):
    description = message.text
    update_trip(trip_id, start_location, end_location, trip_date, seats_available, description)
    bot.reply_to(message, "Trip successfully updated!")

def update_companion_request_step(message):
    bot.reply_to(message, "Enter the companion request ID to update:")
    bot.register_next_step_handler(message, update_companion_request_info)

def update_companion_request_info(message):
    request_id = message.text
    bot.reply_to(message, "Enter new start location:")
    bot.register_next_step_handler(message, update_companion_request_start, request_id)

def update_companion_request_start(message, request_id):
    start_location = message.text
    bot.reply_to(message, "Enter new end location:")
    bot.register_next_step_handler(message, update_companion_request_end, request_id, start_location)

def update_companion_request_end(message, request_id, start_location):
    end_location = message.text
    bot.reply_to(message, "Enter new trip date (YYYY-MM-DD HH:MM:SS):")
    bot.register_next_step_handler(message, update_companion_request_date, request_id, start_location, end_location)

def update_companion_request_date(message, request_id, start_location, end_location):
    trip_date = message.text
    bot.reply_to(message, "Enter new description:")
    bot.register_next_step_handler(message, save_updated_companion_request, request_id, start_location, end_location, trip_date)

def save_updated_companion_request(message, request_id, start_location, end_location, trip_date):
    description = message.text
    update_companion_request(request_id, start_location, end_location, trip_date, description)
    bot.reply_to(message, "Companion request successfully updated!")

bot.infinity_polling()
