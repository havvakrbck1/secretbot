import telebot
import random
import string
import json
import os

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'gizli_mesajlar.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def mesajlari_yukle():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def mesajlari_kaydet(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def gizli_kod_uret(uzunluk=6):
    karakterler = string.ascii_uppercase + string.digits
    return ''.join(random.choice(karakterler) for _ in range(uzunluk))

@bot.message_handler(commands=['start'])
def start_mesaji(message):
    bot.send_message(message.chat.id, 
        "🤫 Hoş geldin! Gizli bir mesaj oluşturmak için /gizlimesaj yaz.\n"
        "Bir kodla gizli mesajı çözmek için /coz yaz!")

@bot.message_handler(commands=['gizlimesaj'])
def gizli_mesaj_al(message):
    bot.send_message(message.chat.id, "📜 Göndermek istediğin gizli mesajı yaz:")
    bot.register_next_step_handler(message, mesaj_kaydet)

def mesaj_kaydet(message):
    gizli_mesaj = message.text
    kod = gizli_kod_uret()
    data = mesajlari_yukle()
    data[kod] = gizli_mesaj
    mesajlari_kaydet(data)
    bot.send_message(message.chat.id, f"🔒 Mesaj kaydedildi!\nGizli kodun: `{kod}`\nBu kodu istediğin kişiye gönder!", parse_mode='Markdown')

@bot.message_handler(commands=['coz'])
def gizli_kod_al(message):
    bot.send_message(message.chat.id, "🔎 Lütfen çözmek istediğin gizli kodu yaz:")
    bot.register_next_step_handler(message, mesaj_coz)

def mesaj_coz(message):
    kod = message.text.strip().upper()
    data = mesajlari_yukle()
    if kod in data:
        gizli_mesaj = data[kod]
        bot.send_message(message.chat.id, f"📜 Gizli Mesaj:\n\n{gizli_mesaj}\n\n💥 Bu mesaj artık silindi.", parse_mode='Markdown')
        del data[kod]  
        mesajlari_kaydet(data)
    else:
        bot.send_message(message.chat.id, "❌ Bu kodla eşleşen bir mesaj bulunamadı.")

bot.polling(none_stop=True)
