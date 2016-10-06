import telebot
import constants
import pymorphy2
import re
import os
import random
import urllib.request as urllib2

bot = telebot.TeleBot(constants.token);


# Функция, выводящая в консоль о действиях в чате
def log(message, answer):
    from datetime import datetime
    print("\n-------------------------")
    print(datetime.now())
    print("The message from {0} {1}. id= {2} \n Text is: {3}".format(message.from_user.first_name,
                                                                     message.from_user.last_name,
                                                                     str(message.from_user.id),
                                                                     message.text))
    print(answer)


# Декораторы управления командами бота

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False) #объект, хранящий разметку кастомной клавиатуры
    user_markup.row('/start', '/stop')                           #параметры - авто-размер кнопки,
    user_markup.row('photo', 'doc', 'video')
    user_markup.row('sticker', 'audio', 'location')
    bot.send_message(message.from_user.id, 'Welcome!', reply_markup=user_markup)


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardHide()
    bot.send_message(message.from_user.id, '..', reply_markup=hide_markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "a":
        answer = 'https://www.youtube.com/watch?v=ERIhesm8mCw'  # We can store  literal variables in a separate file
        log(message, answer)
        bot.send_message(message.chat.id, answer)
    elif message.text == 'b':
        answer = 'c'
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    elif message.text == "photo":
        bot.send_message(message.from_user.id, "That's a photo from my collection")
        directory = "D:/Dima/Camus/Images"
        files = os.listdir(directory)
        #for file in files:
        random_file = random.choice(files)
        img_path = directory+'/' + random_file
        img = open(img_path, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img)
        img.close()
        answer = 'Photo was sent'
        log(message, answer)
    elif message.text == "photo_url":
        url = "https://upload.wikimedia.org/wikipedia/commons/0/08/Albert_Camus%2C_gagnant_de_prix_Nobel%2C_portrait_en_buste%2C_pos%C3%A9_au_bureau%2C_faisant_face_%C3%A0_gauche%2C_cigarette_de_tabagisme.jpg"
        urllib2.urlretrieve(url)
        image = open(url, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img)
        img.close()
        answer = 'Photo was sent'
        log(message, answer)
    elif message.text == "audio":
        bot.send_message(message.from_user.id, "That's some music one from my collection")
        directory = "D:/Dima/Camus/Audio"
        a_path = directory + '/' + 'the_cure_-_killing_an_arab.mp3'
        audio = open(a_path, 'rb')
        #bot.send_chat_action(message.from_user.id, 'upload_audio')
        bot.send_audio(message.from_user.id, audio)
        audio.close()
        answer = 'Audio was sent'
        log(message, answer)
    elif message.text == "doc":
        bot.send_message(message.from_user.id, "That's some essays")
        dir2 = "D:/Dima/Camus"
        docs = os.listdir(dir2)
        r_doc = random.choice(docs)
        doc = open(dir2 + '/' + r_doc, 'rb')
        #doc = open('D:/Dima/Camus/Absurd.odt', 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_document')
        bot.send_document(message.from_user.id, doc)
        doc.close()
        answer = r_doc
        log(message, answer)
    #elif message.text == "sticker":
        #bot.send_message(message.from_user.id, constant.template_sticker_id)
    elif message.text == "location":
        bot.send_message(message.from_user.id, "That's where I'm")
        bot.send_location(message.from_user.id, 36.791749, 3.061897)
    elif message.text == "video":
        bot.send_message(message.from_user.id, "About me")
        bot.send_chat_action(message.from_user.id, 'upload_video')
        bot.send_video(message.from_user.id, "https://www.youtube.com/watch?time_continue=333&v=ERIhesm8mCw")
    else:
        # answer = 'Hey you'
        morph = pymorphy2.MorphAnalyzer()
        res = ''
        delete = re.compile(u'\W+?', re.UNICODE)
        words = message.text.split(' ')
        for i in words:
            p = morph.parse(i)[0]
            res += delete.sub('', p.normal_form) + ' '

        answer = res
        bot.send_message(message.chat.id, answer)
        log(message, answer)

bot.polling(none_stop=True)
