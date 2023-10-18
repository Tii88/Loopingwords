import telebot
import json
from keep_alive import keep_alive
from telebot import types

keep_alive()
bot = telebot.TeleBot("6675748109:AAE5qpmjAjiOnnt-nZWQgdcPCtny99uzY7U")

users_file = "users.txt"
admin = 5915380319


def load_users():
  with open(users_file, "a+") as f:
    f.seek(0)
    users = set(line.strip() for line in f)
  return users


def save_users(users):
  with open(users_file, "w") as f:
    for user_id in users:
      f.write(f"{user_id}\n")


users = load_users()


@bot.message_handler(commands=['broadcast'])
def send_broadcast(message):
  if message.from_user.id != admin:
    bot.send_message(admin, "Unauthorized!")
    return

  msg_text = message.text.split(
      '/broadcast ',
      1)[1] if len(message.text.split('/broadcast ', 1)) > 1 else ""

  for user_id in users:
    try:
      bot.send_message(int(user_id),
                       f"<b>Message By Admin</b>\n\n{msg_text}",
                       parse_mode="html")
    except Exception as e:
      print(f"Failed to send message to {user_id}. Error: {e}")

  bot.send_message(
      admin,
      "<b>Broadcast Task Completed ☁️\nYour msg has been sent to all</b>",
      parse_mode="html")


#save data user and keyboard
users = load_users()

DATA_FILE = 'user_data.json'


def load_data():
  try:
    with open(DATA_FILE, 'r') as file:
      return json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
    return {}


def save_data(data):
  with open(DATA_FILE, 'w') as file:
    json.dump(data, file)


def get_user_data(user_id, key):
  data = load_data()
  return data.get(str(user_id), {}).get(key, None)


2


def save_user_data(user_id, key, value):
  data = load_data()
  if str(user_id) not in data:
    data[str(user_id)] = {}
  data[str(user_id)][key] = value
  save_data(data)

@bot.message_handler(commands=['forward'])
def forward_message_to_all_users(message):
    if message.from_user.id != admin:
        bot.send_message(admin, "Unauthorized!")
        return

    if not message.reply_to_message:
        bot.send_message(admin, "Please reply to the message you want to forward and then use /forward.")
        return

    for user_id in users:
        try:
            bot.forward_message(int(user_id), message.chat.id, message.reply_to_message.message_id)
        except Exception as e:
            print(f"Failed to forward message to {user_id}. Error: {e}")


@bot.message_handler(commands=['start'])
def handle_start(message):
  user_id = str(message.from_user.id)
  if user_id not in users:
    users.add(user_id)
    save_users(users)
  user_id = message.from_user.id
  start_data = get_user_data(user_id, "start_data")
  if start_data is None:
    msg = f"<b>🎉 New User Joined Bot:\n\nID:</b> <code>{message.chat.id}</code>\n<b>User:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n<b>Username:</b> @{message.chat.username}"
    bot.send_message(chat_id=admin, text=msg, parse_mode="html")
    save_user_data(user_id, "num", 0)
    save_user_data(user_id, "start_data", 1)
    video = "https://t.me/pgdudeu/11"
    bot.send_video(message.chat.id, video=video, caption="សូមមេីលវីដេអូ")
    bot.send_message(message.chat.id, "បញ្ជាក់មិនដំណេីរការលេីសពី400ទេ!")
    menu(message)
  else:
    user_id = str(message.from_user.id)
    if user_id not in users:
      users.add(user_id)
      save_users(users)
    save_user_data(user_id, "num", 0)
    video = "https://t.me/pgdudeu/11"
    bot.send_video(message.chat.id, video=video, caption="សូមមេីលវីដេអូ")
    bot.send_message(message.chat.id, "បញ្ជាក់មិនដំណេីរការលេីសពី400ទេ!")
    menu(message)


def menu(message):
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.row("ɴᴜᴍʙᴇʀ ɪɴ ꜰʀᴏɴᴛ", "ɴᴜᴍʙᴇʀ ᴀᴛ ᴛʜᴇ ᴇɴᴅ")
  keyboard.row("ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ", "ɴᴏ ɴᴜᴍʙᴇʀ")
  bot.send_message(message.chat.id, text="Menu", reply_markup=keyboard)


#number in front


@bot.message_handler(func=lambda message: message.text == "ɴᴜᴍʙᴇʀ ɪɴ ꜰʀᴏɴᴛ")
def number1(message):
  user_id = message.from_user.id
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.row("🔙 Back")
  bot.send_message(message.chat.id,
                   "-> កំណត់ ɴᴜᴍʙᴇʀ ɪɴ ꜰʀᴏɴᴛ",
                   reply_markup=keyboard)
  save_user_data(user_id, "num", 1)


#number the end


@bot.message_handler(func=lambda message: message.text == "ɴᴜᴍʙᴇʀ ᴀᴛ ᴛʜᴇ ᴇɴᴅ")
def number2(message):
  user_id = message.from_user.id
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.row("🔙 Back")
  bot.send_message(message.chat.id,
                   "-> កំណត់ ɴᴜᴍʙᴇʀ ᴀᴛ ᴛʜᴇ ᴇɴᴅ",
                   reply_markup=keyboard)
  save_user_data(user_id, "num", 2)


#number with %


@bot.message_handler(
    func=lambda message: message.text == "ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ")
def number3(message):
  user_id = message.from_user.id
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.row("🔙 Back")
  bot.send_message(message.chat.id,
                   "-> កំណត់ ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ",
                   reply_markup=keyboard)
  save_user_data(user_id, "num", 3)


#no number


@bot.message_handler(func=lambda message: message.text == "ɴᴏ ɴᴜᴍʙᴇʀ")
def number4(message):
  user_id = message.from_user.id
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.row("🔙 Back")
  bot.send_message(message.chat.id,
                   "-> កំណត់ ɴᴏ ɴᴜᴍʙᴇʀ",
                   reply_markup=keyboard)
  save_user_data(user_id, "num", 4)


@bot.message_handler(func=lambda message: message.text == "🔙 Back")
def back(message):
  user_id = message.from_user.id
  save_user_data(user_id, "num", 0)
  menu(message)

CHANNEL_ID = '@imrothbots'
@bot.message_handler(func=lambda message: True)
def content_types(message):
  try:
    status = bot.get_chat_member(CHANNEL_ID, message.from_user.id).status
    if status in ["member", "administrator", "creator"]:
      user_id = message.from_user.id
      num = get_user_data(user_id, "num")
      if num == 0:
        bot.send_message(message.chat.id, "ជ្រេីសរេីសមុីនុយ | Chose the Menu")
      if num == 1:
        try:
          test = message.text
          post = test.split("#")
          int_num = int(post[0])
          string_word = post[1]
          if int_num > 400:
            bot.send_message(message.chat.id, "Only 400 Number")
            return
          output = "\n".join(
            [f"{i}. {string_word}" for i in range(1, int_num + 1)])
          bot.send_message(message.chat.id, output)
        except:
          bot.send_message(message.chat.id,
                         "<b>Erorr</b>\nឧទាហរណ៏ <code>10#Roth</code>",
                         parse_mode="HTML")
      if num == 2:
        try:
          test = message.text
          post = test.split("#")
          int_num = int(post[0])
          string_word = post[1]
          if int_num > 400:
            bot.send_message(message.chat.id, "Only 400 Number")
            return
          output = "\n".join([f"{string_word} {i}" for i in range(1, int_num + 1)])
          bot.send_message(message.chat.id, output)
        except:
          bot.send_message(message.chat.id,
                         "<b>Erorr</b>\nឧទាហរណ៏ <code>10#Roth</code>",
                         parse_mode="HTML")
      if num == 3:
        try:
          test = message.text
          post = test.split("#")
          int_num = int(post[0])
          string_word = post[1]
          if int_num > 400:
            bot.send_message(message.chat.id, "Only 400 Number")
            return
          output = "\n".join(
            [f"{i}% {string_word}" for i in range(1, int_num + 1)])
          bot.send_message(message.chat.id, output)
        except:
          bot.send_message(message.chat.id,
                         "<b>Erorr</b>\nឧទាហរណ៏ <code>10#Roth</code>",
                         parse_mode="HTML")
      if num == 4:
        try:
          test = message.text
          post = test.split("#")
          int_num = int(post[0])
          string_word = post[1]
          if int_num > 400:
            bot.send_message(message.chat.id, "Only 400 Number")
            return
          output = "\n".join([f"{string_word}" for i in range(1, int_num + 1)])
          bot.send_message(message.chat.id, output)
        except:
          bot.send_message(message.chat.id,
                         "<b>Erorr</b>\nឧទាហរណ៏ <code>10#Roth</code>",
                         parse_mode="HTML")
    else:
      bot.send_message(message.chat.id, "please join my channel @imrothbots")
  except Exception as e:
    bot.send_message(message.chat.id,
                       "An error occurred. Please try again later.")
    
            


if __name__ == "__main__":
  try:
    bot.polling(none_stop=True)
  finally:
    save_users(users)  # Save on exit just to be sure.
