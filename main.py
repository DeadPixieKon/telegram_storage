import configparser

import telebot
from telebot import types

from CodeExecuter import CodeExecuter
from Catalog import Sostoyanie
from Catalog import Catalog
from InnerBottonsMarkup import InnerBottonsMarkup
from InnerBottonsMarkup import Data

import re

# с ним бот желательно не должен напрямую взаимодействовать
# class CodeExecuter:
#     @staticmethod
#     def execute(command:str) -> str:
#         try:
#             return subprocess.check_output(command, shell=True).decode().strip()
#         except Exception:
#             return ''
#
#     @staticmethod
#     def check_how_many(path: str) -> int:
#         command = "ls \"" + path + "\" | wc -l"
#         return int(subprocess.check_output(command, shell=True).decode().strip())
#
#     @staticmethod
#     def chеck_existane(path: str, file_name:str="") -> bool:
#         reply: int = 1
#         if file_name == "":
#             if path.strip().__contains__(' '):
#                 path = '"' + path + '"'
#             command = "[ -d " + path + " ] && echo $? || echo $?"
#             reply = int(subprocess.check_output(command, shell=True).decode().strip())
#             # print(str(reply) + "|" + command)
#         else:
#             full: str = path + file_name
#             if full.strip().__contains__(' '):
#                 full = '"' + full + '"'
#             command = "[ -f " + full + " ] && echo $? || echo $?"
#             reply = int(subprocess.check_output(command, shell=True).decode().strip())
#         return reply == 0
#
#     ## Гэттеры
#     @staticmethod
#     def get_folders_list(dir:str='') -> list:
#         command = 'ls -F "' + dir + '" | grep /'
#         try:
#             return subprocess.check_output(command, shell=True).decode().strip().split('\n')
#         except Exception: # значит что нет подобного
#             return list()
#     @staticmethod
#     def get_files_list(dir:str='') -> list:
#         command =  'ls -F "' + dir + '" | grep -v /'
#         try:
#             return subprocess.check_output(command, shell=True).decode().strip().split('\n')
#         except Exception: # значит что нет подобного
#             return list()
#
#     @staticmethod
#     def get_working_path() -> str:
#         return 'storage/'
#     @staticmethod
#     def get_working_fullpath() -> str:
#         command = 'echo $PWD'
#         return subprocess.check_output(command, shell=True).decode().strip() + '/'
#
#
#     ## Создание
#     @staticmethod
#     def create_new_folder(path:str, new_folder_name:str) -> None:
#         command = 'mkdir "' + path + new_folder_name + '"'
#         subprocess.check_output(command, shell=True)
#
#
#     ## потом в конце проверить
#     ## Удаление
#     @staticmethod
#     def delete_file(path: str, delete_ffile_name: str) -> None:
#         command = 'rm "' + path + delete_ffile_name + "'"
#         subprocess.check_output(command, shell=True)
#     @staticmethod
#     def delete_folder(path: str, delete_folder_name: str) -> bool:
#         if (CodeExecuter.check_how_many(path + delete_folder_name) != 0):
#             return False
#         command = 'rm -r "' + path + delete_folder_name + "'"
#         subprocess.check_output(command, shell=True)
#         return True


print("now")
# class Sostoyanie:
#     WAIT_FOR_START_COMMAND: int = -1
#     WAIT_FOR_INPUT: int = 0
#     DOWNLOADING_FILE: int = 1
#     SENDING_FILE: int = 2
#     CREATING_NEW_FOLDER: int = 3
#     TEXT_PROCESSING: int = 4


# class Catalog: # Catalog
#     # 1-ая статическая переменная / реализация
#     path = CodeExecuter.get_working_path()
#     @staticmethod
#     def get_path() -> str:
#         return Catalog.path
#     @staticmethod
#     def set_path(path:str) -> None:
#         Catalog.path = path
#
#     # 2-ая статическая переменная / реализация
#     sostoyanie = 0
#     @staticmethod
#     def get_sostoyanie() -> int:
#         return Catalog.sostoyanie
#     @staticmethod
#     def set_sostoyanie(sostoyanie: int) -> None:
#         Catalog.sostoyanie = sostoyanie
#
#     # обертка гэттеров на CodeExecuter
#     @staticmethod
#     def get_folders_list() -> list:
#         return CodeExecuter.get_folders_list(Catalog.path)
#     @staticmethod
#     def get_files_list() -> list:
#         return CodeExecuter.get_files_list(Catalog.path)
#
#     @staticmethod
#     def get_fullpath() -> str:
#         return CodeExecuter.get_working_fullpath() + Catalog.path
#
#     # перемещение
#     @staticmethod
#     def move_to_folder(dir: str) -> bool:
#         if not CodeExecuter.chеck_existane(Catalog.path + dir):
#             return False
#         path = Catalog.path
#         path = path + dir
#         Catalog.path = path
#         return True
#
#     @staticmethod
#     def exitFolder():
#         path = Catalog.path
#         if (len(path) == 0):
#             return
#         if path.count('/') == 1:
#             path = ""
#         else:
#             a = path[:-1].rindex('/')
#             path = path[:a + 1]
#         Catalog.path = path
#
#     # Создание
#     @staticmethod
#     def create_new_folder(new_folder_name:str) -> bool:
#         try:
#             CodeExecuter.create_new_folder(Catalog.path, new_folder_name)
#         except Exception:
#             return False # похоже такая папка уже существует
#         return True # все ок


print("now")
# class InnerBottonsMarkup:
#     @staticmethod
#     def get_change_folder_markup() -> types.InlineKeyboardMarkup:
#         markup = types.InlineKeyboardMarkup()
#         btn = types.InlineKeyboardButton(text="cd ..",
#                                          callback_data="change_folder|" + Catalog.get_path() + "|" + "(exit)")
#         markup.add(btn)
#         btn = types.InlineKeyboardButton(text="create",
#                                          callback_data="change_folder|" + Catalog.get_path() + "|" + "(create)")
#         markup.add(btn)
#         for i in Catalog.get_folders_list():
#             btn = types.InlineKeyboardButton(text=i, callback_data="change_folder|" + Catalog.get_path() + "|" + i)
#             markup.add(btn)
#         return markup
# 
#     @staticmethod
#     def get_change_files_markup() -> types.InlineKeyboardMarkup:
#         markup = types.InlineKeyboardMarkup()
#         for i in Catalog.get_files_list():
#             btn = types.InlineKeyboardButton(text=i, callback_data="files_list|" + Catalog.get_path() + "|" + i)
#             markup.add(btn)
#         return markup
# 
#     @staticmethod
#     def get_delete_folders_markup() -> types.InlineKeyboardMarkup:
#         markup = types.InlineKeyboardMarkup()
#         for i in Catalog.get_folders_list():
#             btn = types.InlineKeyboardButton(text=i, callback_data="delete_folders_list|" + Catalog.get_path() + "|" + i)
#             markup.add(btn)
#         return markup
#     @staticmethod
#     def get_delete_files_markup() -> types.InlineKeyboardMarkup:
#         markup = types.InlineKeyboardMarkup()
#         for i in Catalog.get_files_list():
#             btn = types.InlineKeyboardButton(text=i, callback_data="delete_files_list|" + Catalog.get_path() + "|" + i)
#             markup.add(btn)
#         return markup
#     @staticmethod
#     def get_delete_markup() -> types.InlineKeyboardMarkup:
#         markup = types.InlineKeyboardMarkup()
#         btn = types.InlineKeyboardButton(text="folder", callback_data="delete|" + Catalog.get_path() + "|folder")
#         markup.add(btn)
#         btn = types.InlineKeyboardButton(text="file", callback_data="delete|" + Catalog.get_path() + "|file")
#         markup.add(btn)
#         return markup
# 
#     @staticmethod
#     def get_base_keyboard_markup() -> types.ReplyKeyboardMarkup:
#         markup = types.ReplyKeyboardMarkup()
#         btn1 = types.KeyboardButton("изменить папку")
#         markup.add(btn1)
#         btn2 = types.KeyboardButton("показать файлы")
#         markup.add(btn2)
#         return markup


class BotConfig:
    last_markup_message_id: int = None

    @staticmethod
    def read_config(file='config.ini'):
        config = configparser.ConfigParser()
        config.read(file)
        return config

    @staticmethod
    def read_last_id(config_file='config.ini'):
        config = configparser.ConfigParser()
        config.read(config_file)
        last_id = config.get('Settings', 'last_id')
        return int(last_id)

    @staticmethod
    def update_last_id(new_id, config_file='config.ini'):
        config = configparser.ConfigParser()
        config.read(config_file)

        # Обновляем значение last_id
        config.set('Settings', 'last_id', str(new_id))

        # Записываем изменения обратно в файл
        with open(config_file, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def get_file_id_counter():
        n = BotConfig.read_last_id()

        def inner():
            nonlocal n
            n += 1
            BotConfig.update_last_id(n)
            return n

        return inner

    
    @staticmethod
    def is_valid_folder_name(name: str) -> bool:
        # Проверяем, что имя не пустое
        if not name:
            return False
    
        # Проверяем наличие недопустимых символов
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F]()'  # Недопустимые символы для Windows
        if re.search(invalid_chars, name):
            return False
    
        # Проверяем, что имя не зарезервировано системой
        reserved_names = [
            "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
            "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
            "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        ]
        if name.upper() in reserved_names:
            return False
    
        # Проверяем длину имени (обычно ограничение 255 символов)
        if len(name) > 255:
            return False
    
        # Если все проверки пройдены, имя считается допустимым
        return True


bot = telebot.TeleBot(BotConfig.read_config()['Telegram']['token'])


@bot.message_handler(commands=['dir'])
def send_welcome(message:types.Message):
    bot.send_message(message.from_user.id, Catalog.get_path())

@bot.message_handler(commands=['tree'])
def send_welcome(message: types.Message):
    bot.send_message(message.from_user.id, CodeExecuter.execute("tree -F " + CodeExecuter.get_working_path()))

@bot.message_handler(commands=['delete'])
def send_welcome(message:types.Message):
    BotConfig.last_markup_message_id = (
        bot.send_message(message.from_user.id, "what you like to delete",
                     reply_markup=InnerBottonsMarkup.base_delete())).id

@bot.message_handler(commands=['enter_info'])
def send_welcome(message:types.Message):
    bot.send_message(message.from_user.id, 'login: ???\npass: ???')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message:types.Message):
    BotConfig.last_markup_message_id = None
    bot.send_message(message.from_user.id, "Choose action",
                     reply_markup=InnerBottonsMarkup.base_keyboard())


@bot.message_handler(content_types=['text'])
def text_processor(message:types.Message):
    # Создание папки
    if Catalog.get_sostoyanie() == Sostoyanie.CREATING_NEW_FOLDER:
        if not BotConfig.is_valid_folder_name(message.text): # проверка на корректность
            return
        Catalog.create_new_folder(message.text)
        bot.send_message(message.from_user.id, "new folder created")
        Catalog.set_sostoyanie(Sostoyanie.WAIT_FOR_INPUT)
        return

    if Catalog.get_sostoyanie() != Sostoyanie.WAIT_FOR_INPUT:
        return
    # обработка кнопок
    Catalog.set_sostoyanie(Sostoyanie.TEXT_PROCESSING)
    if message.text == "изменить папку":
        BotConfig.last_markup_message_id = (
            bot.send_message(message.from_user.id, "Folders list",
                         reply_markup=InnerBottonsMarkup.change_folder())).id
    elif message.text == "показать файлы":
        if len(Catalog.get_files_list()) == 0:
            BotConfig.last_markup_message_id = (
                bot.send_message(message.from_user.id, "there is no files in this folder",
                             reply_markup=InnerBottonsMarkup.send_file())).id
        else:
            BotConfig.last_markup_message_id = (
                bot.send_message(message.from_user.id, "Files list",
                             reply_markup=InnerBottonsMarkup.send_file())).id
    Catalog.set_sostoyanie(Sostoyanie.WAIT_FOR_INPUT)

@bot.callback_query_handler(func=lambda call: True)
def answer(call:types.CallbackQuery):
    usr_id = call.from_user.id
    msg = call.message
    bot.edit_message_text(text=call.data, chat_id=usr_id, message_id=msg.message_id)
    s = call.data.split('|')
    print(s)
    if BotConfig.last_markup_message_id is not None and (
            BotConfig.last_markup_message_id != call.message.id or s[1] != Catalog.get_path()
    ):
        bot.edit_message_text(text="Not valid message!", chat_id=usr_id, message_id=msg.message_id)
        return None

    match s[0]:
        case Data.CHANGE_FOLDER:
            match s[2]:
                case Data.Status.EXIT:
                    if len(Catalog.get_path().split('/')) <= 2:
                        bot.edit_message_text(text="Can't quit root folder!", chat_id=usr_id, message_id=msg.message_id)
                        return None
                    Catalog.exitFolder()
                    bot.edit_message_text(text="exited folder\n" + Catalog.get_path(), chat_id=usr_id,
                                          message_id=msg.message_id)
                case Data.Status.CREATE:
                    bot.edit_message_text(text="type folder name", chat_id=usr_id, message_id=msg.message_id)
                    Catalog.set_sostoyanie(Sostoyanie.CREATING_NEW_FOLDER)
                case _:
                    if Catalog.move_to_folder(s[2]):
                        bot.edit_message_text(text="moved to\n" + Catalog.get_path(), chat_id=usr_id,
                                              message_id=msg.message_id)
                    else:
                        bot.edit_message_text(text="there is no such folder", chat_id=usr_id,
                                              message_id=msg.message_id)
        case Data.SEND_FILE: # Отправить файл
            bot.edit_message_text(text="Trying to send", chat_id=usr_id, message_id=msg.message_id)
            with open(Catalog.get_path() + s[2], "rb") as file:
                bot.send_document(call.from_user.id, document=file)
            bot.edit_message_text(text="File \"" + s[2] + "\" sended", chat_id=usr_id, message_id=msg.message_id)
        case Data.BASE_DELETE:
            match s[2]:
                case Data.Status.FILE:
                    if (len(Catalog.get_files_list()) == 0):
                        bot.edit_message_text(text="there is no files here", chat_id=usr_id, message_id=msg.message_id)
                    else:
                        BotConfig.last_markup_message_id = (
                            bot.edit_message_text(text="choose file to delete", chat_id=usr_id,
                                                  message_id=msg.message_id,
                                                  reply_markup=InnerBottonsMarkup.delete_files())).id
                case Data.Status.FOLDER:
                    if (len(Catalog.get_folders_list()) == 0):
                        BotConfig.last_markup_message_id = (
                            bot.edit_message_text(text="there is no folders here", chat_id=usr_id,
                                                  message_id=msg.message_id)).id
                    else:
                        BotConfig.last_markup_message_id = (
                            bot.edit_message_text(text="choose file to delete", chat_id=usr_id,
                                                  message_id=msg.message_id,
                                                  reply_markup=InnerBottonsMarkup.delete_folders())).id
        case Data.DELETE_FILE:
            # так же надо реализовать отправку удаляемого файла
            # s[1] - путь s[2] - имя файла
            bot.edit_message_text(text="Trying to send", chat_id=usr_id, message_id=msg.message_id)
            with open(Catalog.get_path() + s[2], "rb") as file:
                bot.send_document(call.from_user.id, document=file)
            CodeExecuter.delete_file(Catalog.get_path(), s[2])
            bot.edit_message_text(text="file deleted\n" + s[1] + s[2], chat_id=usr_id, message_id=msg.message_id)
        case Data.DELETE_FOLDER:
            # так же надо реализовать отправку удаляемого файла
            # s[1] - путь s[2] - имя папки
            if not CodeExecuter.delete_folder(Catalog.get_path(), s[2]):
                bot.edit_message_text(text="Папка не пустая перед удалением почистите", chat_id=usr_id, message_id=msg.message_id)
            else:
                bot.edit_message_text(text="file deleted\n" + s[1] + s[2], chat_id=usr_id, message_id=msg.message_id)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = Catalog.get_path() + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as exc:
        bot.reply_to(message, exc)






bot.polling(non_stop=True, interval=0)