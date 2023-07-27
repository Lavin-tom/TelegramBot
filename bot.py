import telebot
import random
import json
from telebot import types
from fuzzywuzzy import fuzz

TOKEN = open('api-key.txt').readline()
bot = telebot.TeleBot(TOKEN)
print("Bot is online")

hideBoard = types.ReplyKeyboardRemove()  # hide the keyboard

#load ragas json file    
with open('res/raga.json', 'r', encoding='utf-8') as raga:
    ragadata = json.load(raga)

#load swaras json file    
with open('res/swaras.json', 'r', encoding='utf-8') as swara:
    swarasdata = json.load(swara)

#load western notes json file    
with open('res/western_notes.json', 'r', encoding='utf-8') as western:
    westerndata = json.load(western)    

hey_msg = ['Hi','Hello','Hey']
user_name = ['Musician','Composer']
bot_name = ['Musician','Composer']
knownUsers = []
userStep = {}

carnatic_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
carnatic_select.add('Carnatic-Ragas','Carnatic-Swaras')
western_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
western_select.add('Scales','Chords')
suggestions_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)

commands = {
			'start':'Restart bot',
			'carnatic':'Search Carnatic ragas and swaras',
            'western':'still under development',
            'source':'Source code of me',
            'help':'Help',
			'all':'List all commands',
            'about':'About me',
			}

#other functions
def copy_dictionary(original_dict, key):
    new_dict = {}
    if key in original_dict:
        new_dict[key] = original_dict[key]
    return new_dict

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected")
        return 0
    
#console output
def listener(messages):
	for m in messages:
		if m.content_type == 'text':
			print(m.from_user.first_name +'['+ str(m.chat.id) + "] : " + m.text)

bot.set_update_listener(listener)

#---------------------main commands-----------------
#show all available commands
@bot.message_handler(commands=['all'])
def command_all(m):
    #print('commands')
    text = "All available commands :\n"
    for key in commands:
        text += "🔸 /" + key + " : "
        text += commands[key] + "\n\n"
    bot.send_message(m.chat.id,text)
@bot.message_handler(commands=['about'])
def handle_start_help(m):
    print('about')
    bot.send_chat_action(m.chat.id,'typing')
    note = "Rhythm is a chatbot designed to assist users in finding Carnatic ragas easily."
    note += "It was created out of a love and passion for both music and coding." 
    note += "If you encounter any issues or have suggestions for improvements,"
    note += "please type /source for navigate to source code in github.\n"
    note += "This project is inspired from https://github.com/lpadukana/karnatic-music"
    bot.send_message(m.chat.id,note)

@bot.message_handler(commands=['source'])
def handle_start_help(m):
        print('source')
        bot.send_chat_action(m.chat.id,'typing')
        link = "https://github.com/Lavin-tom/TelegramBot"
        formatted_message = f"[Click here]({link}) to visit the GitHub repository."
        bot.reply_to(m, formatted_message, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def handle_start_help(m):
        print('help')
        bot.send_chat_action(m.chat.id,'typing')
        text = random.choice(hey_msg)
        text += ' '
        if m.chat.type == "private":
            text += m.chat.first_name
        else:
            text += random.choice(user_name)
        text += ' , I am a '+ random.choice(bot_name) + " Bot"
        text += '\n\nI can do following things :'
        text += '\n 🔸 Provide Carnatic Ragas and Swaras'
        text += '\n 🔸 Provide Western Music note (comming soon)'
        text += "\n\nSee all commands at  /all  :)"
        text += "\n\n\nContact Developer 👨‍💻: @love_in_tom"
        bot.reply_to(m,text)

@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if cid not in knownUsers:
		knownUsers.append(cid)
		userStep[cid] = 0
	handle_start_help(m)
        
#search carnatic 
@bot.message_handler(commands=['carnatic'])
def command_searchRaga(m):
    cid = m.chat.id
    bot.send_message(cid, "what do you want ?",reply_markup=carnatic_select)
    userStep[cid] = 'carnatic'

#search carnatic swaras
@bot.message_handler(commands=['western'])
def command_searchSwaras(m):
    cid = m.chat.id
    bot.send_message(cid, "what do you want ?",reply_markup=western_select)
    userStep[cid] = 'western'
    
    #text = "Still under development..."
    #bot.reply_to(m,text)

#--------------------------------------Western Notes-------------------------------#
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'western')
def msg_cpp_select(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_chat_action(cid, 'typing')
    userQuery = m.text.lower()
    if userQuery == 'scales':
        tsearch = 'Enter which scales u want to know' 
        #userQuery= 'mohanam'
        bot.send_message(m.chat.id,tsearch,reply_markup=hideBoard)
        userStep[cid] = 'western_scale_search'

    elif userQuery == 'chords':
        tsearch = 'Enter which chords u want to search' 
        bot.send_message(m.chat.id,tsearch,reply_markup=hideBoard)
        userStep[cid] = 'western_chord_search'
    else:
        bot.send_message(cid,"Invalid Commmands")

#[value == western_scale_search]    
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'western_scale_search')
def handle_user_scale_query(m):
    try:
        userQuery = m.text.upper()
        print(userQuery)
        new_dict = copy_dictionary(westerndata, userQuery)
        text = ""

        if "major_scale" in new_dict[userQuery]:
            text += "Major Scale : "
            text += new_dict[userQuery]['major_scale'] + "\n"
        if "minor_scale_natural" in new_dict[userQuery]:
            text += "Natural Minor Scale : "
            text += str(new_dict[userQuery]['minor_scale_natural']) + "\n"
            text += "Melodic Minor Scale : \n"        
        if "minor_scale_melodic_ascending" in new_dict[userQuery]:
            text += "Ascending : "
            text += str(new_dict[userQuery]['minor_scale_melodic_ascending']) + "\n"      
        if "minor_scale_harmonic" in new_dict[userQuery]:
            text += "Harmonic : "
            text += str(new_dict[userQuery]['minor_scale_harmonic']) + "\n"      

        bot.send_message(m.chat.id,text)
	    
    except Exception as e:
        bot.send_message(m.chat.id, "Search error!! Try again\n Now you are in Western scale mode if you want to switch to chord click here /western and select chords")
        # Calculate the similarity score between the user input and each word in the JSON data
        similarity_scores = [(word, fuzz.ratio(userQuery, word)) for word in westerndata]

        # Sort the similarity scores descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Get the top N suggestions based on the highest similarity scores
        top_suggestions = [score[0] for score in similarity_scores[:3]]
        print("Did you mean:")
        bot.reply_to(m,"Did you mean: ")

        choice_msg = "Select any one"
        bot.send_message(m.chat.id,choice_msg)
        cid = m.chat.id
        suggestions_select=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for suggestion in top_suggestions:
            suggestions_select.add(suggestion)
            #bot.send_message(m.chat.id,suggestion)
        bot.send_message(cid, "what do you want ?",reply_markup=suggestions_select)

#[value == western_chords_search]    
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'western_chord_search')
def handle_user_scale_query(m):
    try:
        userQuery = m.text.upper()
        print(userQuery)
        new_dict = copy_dictionary(westerndata, userQuery)
        text = ""

        if "major_chord" in new_dict[userQuery]:
            text += "Major Chord : "
            text += new_dict[userQuery]['major_chord'] + "\n"
        if "minor_chord" in new_dict[userQuery]:
            text += "Minor Chord : "
            text += str(new_dict[userQuery]['minor_chord']) + "\n"        

        bot.send_message(m.chat.id,text)
	    
    except Exception as e:
        bot.send_message(m.chat.id, "Search error!! Try again\nNow you are in Western Scale mode if you want to switch to chords click here /western and select scales")
        # Calculate the similarity score between the user input and each word in the JSON data
        similarity_scores = [(word, fuzz.ratio(userQuery, word)) for word in westerndata]

        # Sort the similarity scores descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Get the top N suggestions based on the highest similarity scores
        top_suggestions = [score[0] for score in similarity_scores[:3]]
        print("Did you mean:")
        bot.reply_to(m,"Did you mean: ")

        choice_msg = "Select any one"
        bot.send_message(m.chat.id,choice_msg)
        cid = m.chat.id
        suggestions_select=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for suggestion in top_suggestions:
            suggestions_select.add(suggestion)
            #bot.send_message(m.chat.id,suggestion)
        bot.send_message(cid, "what do you want ?",reply_markup=suggestions_select)

#-------------------Custom keyboard functions-------------------
#---------------------------carnatic raga-----------------------------
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'carnatic')
def msg_cpp_select(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_chat_action(cid, 'typing')
    userQuery = m.text.lower()
    if userQuery == 'carnatic-ragas':
        tsearch = 'Enter which raga u want to search' 
        #userQuery= 'mohanam'
        bot.send_message(m.chat.id,tsearch,reply_markup=hideBoard)
        userStep[cid] = 'carnatic_ragas_search'

    elif userQuery == 'carnatic-swaras':
        tsearch = 'Enter which swaras u want to search' 
        bot.send_message(m.chat.id,tsearch,reply_markup=hideBoard)
        userStep[cid] = 'carnatic_swaras_search'
    else:
        bot.send_message(cid,"Invalid Commmands")

#[value == carnatic_raga_search]    
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'carnatic_ragas_search')
def handle_user_ragas_query(m):
    try:
        userQuery = m.text.lower()
        #print(userQuery)
        new_dict = copy_dictionary(ragadata, userQuery)
        text = ""

        if "name" in new_dict[userQuery]:
            text += "Name : "
            text += new_dict[userQuery]['name'] + "\n"
        if "janya" in new_dict[userQuery]:
            text += "Janya: "
            text += str(new_dict[userQuery]['janya']) + "\n"        
        if "melakarta" in new_dict[userQuery]:
            text += "Melakarta: "
            text += new_dict[userQuery]['melakarta'] + "\n"  
        if "derived_from" in new_dict[userQuery]:
            text += "Derived from: "
            text += new_dict[userQuery]['derived_from'] + "\n" 
        if "scales" in new_dict[userQuery]:
            text += "Scale: \n"
            text += "Arohanam: "
            text += new_dict[userQuery]['scales'][0]['arohanam'] + "\n" 
            text += "Avarohanam: "
            text += new_dict[userQuery]['scales'][0]['avarohanam'] + "\n" 

        bot.send_message(m.chat.id,text)
	    
    except Exception as e:
        bot.send_message(m.chat.id, "Search error!! Try again\n Now you are in Raga mode if you want to switch to swara  click here /carnatic and select carnatic-swara")
        # Calculate the similarity score between the user input and each word in the JSON data
        similarity_scores = [(word, fuzz.ratio(userQuery, word)) for word in ragadata]

        # Sort the similarity scores descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Get the top N suggestions based on the highest similarity scores
        top_suggestions = [score[0] for score in similarity_scores[:3]]
        print("Did you mean:")
        bot.reply_to(m,"Did you mean: ")

        choice_msg = "Select any one"
        bot.send_message(m.chat.id,choice_msg)
        cid = m.chat.id
        suggestions_select=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for suggestion in top_suggestions:
            suggestions_select.add(suggestion)
            #bot.send_message(m.chat.id,suggestion)
        bot.send_message(cid, "what do you want ?",reply_markup=suggestions_select)

#[value == carnatic_swara_search]    
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'carnatic_swaras_search')
def handle_user_swara_query(m):
    try:
        userQuery = m.text.upper()
        print(userQuery)
        new_dict = copy_dictionary(swarasdata, userQuery)
        text = ""

        if "name" in new_dict[userQuery]:
            text += "Name : "
            text += new_dict[userQuery]['name'] + "\n"
        if "sanskrit_name" in new_dict[userQuery]:
            text += "Sanskrit name: "
            text += new_dict[userQuery]['sanskrit_name']+ "\n"
        if "short_name" in new_dict[userQuery]:
            text += "Shortname: "
            text += new_dict[userQuery]['shortname']+ "\n"
        if "key" in new_dict[userQuery]:
            text += "Key: "
            text += new_dict[userQuery]['key']+ "\n"
        if "note" in new_dict[userQuery]:
            text += "Note: "
            text += new_dict[userQuery]['note']+ "\n"
        if "halfsteps" in new_dict[userQuery]:
            text += "Halfsteps: "
            text += str(new_dict[userQuery]['halfsteps'])+ "\n"

        bot.send_message(m.chat.id,text)
	    
    except Exception as e:
        bot.send_message(m.chat.id, "Search error!! Try again")
        # Calculate the similarity score between the user input and each word in the JSON data
        similarity_scores = [(word, fuzz.ratio(userQuery, word)) for word in swarasdata]

        # Sort the similarity scores descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Get the top N suggestions based on the highest similarity scores
        top_suggestions = [score[0] for score in similarity_scores[:3]]
        print("Did you mean:")
        bot.reply_to(m,"Did you mean: ")
        choice_msg = "Select any one"
        bot.send_message(m.chat.id,choice_msg)
        cid = m.chat.id
        suggestions_select=types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for suggestion in top_suggestions:
            suggestions_select.add(suggestion)
            #bot.send_message(m.chat.id,suggestion)
        bot.send_message(cid, "what do you want ?",reply_markup=suggestions_select)

#welcome code
@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_welcome(m):
		lower_text = m.text.lower()
		if lower_text == 'hello' or lower_text == 'hi' or lower_text == 'hai':
			text = random.choice(hey_msg)
			text += " "
			text += m.from_user.first_name
			bot.reply_to(m,text)
                        
bot.infinity_polling()