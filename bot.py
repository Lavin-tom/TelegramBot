import telebot
import random
import json
from telebot import types
from fuzzywuzzy import fuzz

TOKEN = open('api-key.txt').readline()
bot = telebot.TeleBot(TOKEN)
print("Bot is online")

hideBoard = types.ReplyKeyboardRemove()  # hide the keyboard

#load json file    
with open('res/raga.json', 'r', encoding='utf-8') as f:
    ragadata = json.load(f)

hey_msg = ['Hi','Hello','Hey']
user_name = ['Musician','Composer']
userStep = {}
commands = {
			'/start':'Restart bot',
			'/help':'Help',
			'/all':'List all commands',
			'/search_carnatic_ragas':'Search Carnatic ragas',
            '/source':'Source code of me',
            '/about':'About me'
			}

def copy_dictionary(original_dict, key):
    new_dict = {}
    if key in original_dict:
        new_dict[key] = original_dict[key]
    return new_dict

@bot.message_handler(commands=['about'])
def handle_start_help(m):
        print('about')
        bot.send_chat_action(m.chat.id,'typing')
        note = "Rhythm is a chatbot designed to assist users in finding Carnatic ragas easily."
        note += "It was created out of a love and passion for both music and coding." 
        note += "If you encounter any issues or have suggestions for improvements,"
        note += "please type /source for navigate to source code in github.\n"
        note += "This project is inspired from https://github.com/lpadukana/karnatic-music"
        bot.reply_to(m,note)

@bot.message_handler(commands=['source'])
def handle_start_help(m):
        print('source')
        bot.send_chat_action(m.chat.id,'typing')
        link = "https://github.com/Lavin-tom/TelegramBot"
        formatted_message = f"[Click here]({link}) to visit the GitHub repository."
        bot.reply_to(m, formatted_message, parse_mode='Markdown')

@bot.message_handler(commands=['help','start'])
def handle_start_help(m):
        print('help')
        bot.send_chat_action(m.chat.id,'typing')
        text = random.choice(hey_msg)
        text += ' '
        if m.chat.type == "private":
            text += m.chat.first_name
        else:
            text += random.choice(user_name)
        text += " type or choose /all for see all available commands"
        bot.reply_to(m,text)

#show all available commands
@bot.message_handler(commands=['all'])
def command_all(m):
		#print('commands')
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
		bot.send_message(m.chat.id,"Error in searching Ragas..")

@bot.message_handler(func=lambda message: True)
def handle_user_query(m):
    try:
        userQuery = m.text.lower()
        #print(userQuery)
        new_dict = copy_dictionary(ragadata, userQuery)
        text = ""

        if "name" in new_dict[userQuery]:
            #print(new_dict[userQuery]['name'])
            text += "Name : "
            text += new_dict[userQuery]['name'] + "\n"
        if "janya" in new_dict[userQuery]:
            #print(new_dict[userQuery]['janya'])
            text += "Janya: "
            text += str(new_dict[userQuery]['janya']) + "\n"        
        if "melakarta" in new_dict[userQuery]:
            #print(new_dict[userQuery]['melakarta'])
            text += "Melakarta: "
            text += new_dict[userQuery]['melakarta'] + "\n"  
        if "derived_from" in new_dict[userQuery]:
            #print(new_dict[userQuery]['derived_from'])
            text += "Derived from: "
            text += new_dict[userQuery]['derived_from'] + "\n" 
        if "scales" in new_dict[userQuery]:
            #print(new_dict[userQuery]['scales'][0]['arohanam'])
            #print(new_dict[userQuery]['scales'][0]['avarohanam'])
            text += "Scale: \n"
            text += "Arohanam: "
            text += new_dict[userQuery]['scales'][0]['arohanam'] + "\n" 
            text += "Avarohanam: "
            text += new_dict[userQuery]['scales'][0]['avarohanam'] + "\n" 

        bot.send_message(m.chat.id,text)
	    
    except Exception as e:
        bot.send_message(m.chat.id, "Search error!! Try again")
              # Calculate the similarity score between the user input and each word in the JSON data
        similarity_scores = [(word, fuzz.ratio(userQuery, word)) for word in ragadata]

            # Sort the similarity scores descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

            # Get the top N suggestions based on the highest similarity scores
        top_suggestions = [score[0] for score in similarity_scores[:3]]
        print("Did you mean:")
        bot.reply_to(m,"Did you mean: ")
        #i=1
        for suggestion in top_suggestions:
            #print(suggestion)
            #bot.send_message(m.chat.id,f"{i}.{suggestion}")
            bot.send_message(m.chat.id,suggestion)
            #i += 1

        choice_msg = "Searching recommended Raga.."
        bot.send_message(m.chat.id,choice_msg)

        #choice = 1
        #bot.send_message(m.chat.id,choice,reply_markup=hideBoard)
        #print(f"choice{choice}")
        #if choice != 0 or choice < 4:
        m.text = top_suggestions[0]
        print(m.text)
        #handle_user_query(m)

        #print(top_suggestions[0])
        #m.text = top_suggestions[0]
        #handle_user_query(m)


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