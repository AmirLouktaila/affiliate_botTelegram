import telebot
import requests,re
from aliexpress_api import AliexpressApi, models

bot = telebot.TeleBot("your_token_bot")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("اشترك في قناة ", url="https://t.me/NSshoping"))

  # Reply Keyboard Button
  # markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
  # markup.add(telebot.types.KeyboardButton("Reply Keyboard Button"))
  
    markdown = "مرحبا بك في   AliCoinsDz  هنا يمكنك ان تجد افضل العروض والمنتجات المناسبة لك"
    bot.reply_to(message, markdown, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):

    def extract_links(text):
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(url_pattern, text)
        return links

    input_text = message.text
    links = extract_links(input_text)

    aliexpress = AliexpressApi(appkey, secretkey, models.Language.EN, models.Currency.EUR, tracking_id)
    
    for link in links:
        response = requests.get(link, allow_redirects=True)
        print(response.url) 
        def extract_item(text):
            start_index = text.find('item/') + len('item/')
            end_index = text.find('.', start_index)
            
            if start_index != -1 and end_index != -1:
                extracted_text = text[start_index:end_index]
                return extracted_text
            else:
                return None
        
        input_text = response.url
        extracted_item = extract_item(input_text)
        
        urls_send=extracted_item
        try:
            print(urls_send)
            affiliate_links = aliexpress.get_affiliate_links(urls_send)
            
            markup1 = telebot.types.InlineKeyboardMarkup()
            markup1.add(telebot.types.InlineKeyboardButton("شراء منتج", url=affiliate_links[0].promotion_link))
      
            bot.send_message(message.chat.id,f'{affiliate_links[0].promotion_link}',reply_markup=markup1)

        except Exception as e:
            print(link)
            affiliate_links = aliexpress.get_affiliate_links(link)
            
            markup1 = telebot.types.InlineKeyboardMarkup()
            markup1.add(telebot.types.InlineKeyboardButton("شراء منتج", url=affiliate_links[0].promotion_link))
      
            bot.send_message(message.chat.id,f'{affiliate_links[0].promotion_link}',reply_markup=markup1)

             





bot.infinity_polling()