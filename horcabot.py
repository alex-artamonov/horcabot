import telebot
from telegram.constants import ParseMode
from telebot import types
import hangman as hm
import os

secrets = 'secrets.txt'
# with open(secrets) as file:
#     TOKEN = file.readline().strip()
TOKEN = os.environ["HORCABOT"]

bot = telebot.TeleBot(TOKEN)
commands = [
    "start",
    "restart",
    "stop",
]

game_dict = {}


def create_command_buttons():
    # commands_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    commands_markup = types.ReplyKeyboardMarkup(is_persistent=True)
    for command in commands:
        commands_markup.add(types.KeyboardButton("/" + command))
    return commands_markup


def game_init(cid, message, output):
    game = hm.Hangman(cid)
    game_dict[cid] = game
    print(game.word)
    bot.send_message(message.chat.id, output, parse_mode=ParseMode.HTML)
    bot.send_message(message.chat.id, "- - - -", parse_mode=ParseMode.HTML)


@bot.message_handler(commands=commands)
def greet(message):
    name = message.chat.first_name
    cid = message.chat.id
    print(message.text, name, cid)

    if message.text == "/start":
        output = f"¡Hola, {name}! Empieza el juego del ahorcado."
        output += f"\nTu objetivo es adivinar una palabra de 4 letras. Pulsa una letra."
        game_init(cid, message, output)
    elif message.text == "/restart":
        output = f"\nTu objetivo es adivinar una palabra de 4 letras. Pulsa una letra."
        game_init(cid, message, output)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "¡Hasta luego!", parse_mode=ParseMode.HTML)
        game_dict[cid] = None


@bot.message_handler(content_types=["text"])
def get_input(message: telebot.types.Message):
    parajugar = "Para jugar al ahorcado pulsa /start o /restart"
    game = game_dict.get(message.chat.id)
    if not game:
        bot.send_message(
            message.chat.id,
            parajugar,
            reply_markup=create_command_buttons(),
        )
        return
    letter = message.text
    try:
        response = game.get_response(letter)
        output = "<pre><code>" + response + "</code></pre>"
        bot.send_message(
            game.id,
            output,
            parse_mode=ParseMode.HTML,
        )
        if game.finished:
            link = (
                f"https://www.wordreference.com/es/en/translation.asp?spen={game.word}"
            )
            bot.send_message(message.chat.id, link)
            bot.send_message(message.chat.id, parajugar)
    except ValueError as e:
        bot.send_message(game.id, e, parse_mode=ParseMode.HTML)

def start_bot():
    create_command_buttons()
    print(bot.get_me())
    bot.polling(non_stop=True)
