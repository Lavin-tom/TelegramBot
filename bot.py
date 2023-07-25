import telebot
import random
import json
from telebot import types

TOKEN = open('api-key.txt').readline()
bot = telebot.TeleBot(TOKEN)
print("Bot is online")

hideBoard = types.ReplyKeyboardRemove()  # hide the keyboard
    
raga_data = json.load(open('res/raga.json'))

hey_msg = ['Hi','Hello','Hey']
user_name = ['Musician','Composer']
userStep = {}
commands = {
			'/start':'Restart bot',
			'/help':'Help',
			'/all':'List all commands',
			'/search_carnatic_ragas':'Search Carnatic ragas',
			}

@bot.message_handler(commands=['help'])
def handle_start_help(m):
		print('help')
		bot.send_chat_action(m.chat.id,'typing')
		text = random.choice(hey_msg)
		if m.chat.type == "private":
				text += m.chat.first_name
		else:
				text += random.choice(user_name)
		text += "helping"
		bot.reply_to(m,text)

#show all available commands
@bot.message_handler(commands=['all'])
def command_all(m):
		print('commands')
		text = "All available commands :\n"
		for key in commands:
			text += " "+key+": "
			text += commands[key] + "\n"
		bot.send_message(m.chat.id,text)

#show all available commands
@bot.message_handler(commands=['search_carnatic_ragas'])
def command_searchRaga(m):
	try:
		userStep[m.chat.id] = 0
		print('searching-carnatic-ragas')
		tsearch = 'enter which raga u want to search' 
		bot.send_message(m.chat.id,tsearch,reply_markup=hideBoard)

	except Exception as e:
		bot.send_message(m.chat.id,"Some error")

@bot.message_handler(func=lambda message: True)
def handle_user_query(m):
    try:
        userQuery = m.text
        print(userQuery)
        # Assuming you have a JSON string stored in userQuery
        #json_data = json.loads(userQuery)  # Convert JSON string to a Python dictionary
        
        # Access the JSON data as needed
        #value = raga_data[userQuery]

        # Do something with the value
        #print(value)
        # bot.send_message(m.chat.id, response)

    except Exception as e:
        bot.send_message(m.chat.id, "Search error")

#welcome code
@bot.message_handler(func=lambda message: True)
def send_welcome(m):
		lower_text = m.text.lower()
		if lower_text == 'hello' or lower_text == 'hi' or lower_text == 'hai':
			text = random.choice(hey_msg)
			text += " "
			text += m.from_user.first_name
			bot.reply_to(m,text)

bot.infinity_polling()