import configparser

import telebot
from telebot import types

from Catalog import Sostoyanie
from Catalog import Catalog
from InnerBottonsMarkup import InnerBottonsMarkup 
from InnerBottonsMarkup import Data

import re


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
ctlg: Catalog = Catalog()
inner_button_murkup: InnerBottonsMarkup = InnerBottonsMarkup(ctlg)

@bot.message_handler(commands=['dir'])
def send_welcome(message:types.Message):
    bot.send_message(message.from_user.id, ctlg.path)

@bot.message_handler(commands=['tree'])
def send_welcome(message: types.Message):
    # bot.send_message(message.from_user.id, CodeExecuter.execute("tree -F " + CodeExecuter.get_working_path()))
    bot.send_message(message.from_user.id, ctlg.get_tree())

@bot.message_handler(commands=['delete'])
def send_welcome(message:types.Message):
    BotConfig.last_markup_message_id = (
        bot.send_message(message.from_user.id, "what you like to delete",
                     reply_markup=inner_button_murkup.base_delete())).id

@bot.message_handler(commands=['enter_info'])
def send_welcome(message:types.Message):
    bot.send_message(message.from_user.id, 'login: ???\npass: ???')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message:types.Message):
    BotConfig.last_markup_message_id = None
    bot.send_message(message.from_user.id, "Choose action",
                     reply_markup=inner_button_murkup.base_keyboard())


@bot.message_handler(content_types=['text'])
def text_processor(message:types.Message):
    # Создание папки
    if ctlg.sostoyanie == Sostoyanie.CREATING_NEW_FOLDER:
        if not BotConfig.is_valid_folder_name(message.text): # проверка на корректность
            return
        ctlg.create_new_folder(message.text)
        bot.send_message(message.from_user.id, "new folder created")
        ctlg.sostoyanie = Sostoyanie.WAIT_FOR_INPUT
        return

    if ctlg.sostoyanie != Sostoyanie.WAIT_FOR_INPUT:
        return
    # обработка кнопок
    ctlg.sostoyanie = Sostoyanie.TEXT_PROCESSING
    if message.text == "изменить папку":
        BotConfig.last_markup_message_id = (
            bot.send_message(message.from_user.id, "Folders list",
                         reply_markup=inner_button_murkup.change_folder())).id
    elif message.text == "показать файлы":
        if len(ctlg.get_files_list()) == 0:
            BotConfig.last_markup_message_id = (
                bot.send_message(message.from_user.id, "there is no files in this folder",
                             reply_markup=inner_button_murkup.send_file())).id
        else:
            BotConfig.last_markup_message_id = (
                bot.send_message(message.from_user.id, "Files list",
                             reply_markup=inner_button_murkup.send_file())).id
    ctlg.sostoyanie = Sostoyanie.WAIT_FOR_INPUT

@bot.callback_query_handler(func=lambda call: True)
def answer(call:types.CallbackQuery):
    usr_id = call.from_user.id
    msg = call.message
    bot.edit_message_text(text=call.data, chat_id=usr_id, message_id=msg.message_id)
    s = call.data.split('|')
    print(s)
    if BotConfig.last_markup_message_id is not None and (
            BotConfig.last_markup_message_id != call.message.id or s[1] != ctlg.path
    ):
        bot.edit_message_text(text="Not valid message!", chat_id=usr_id, message_id=msg.message_id)
        return None

    match s[0]:
        case Data.CHANGE_FOLDER:
            match s[2]:
                case Data.Status.EXIT:
                    if len(Catalog.parse_path(ctlg.path)) <= 2:
                        bot.edit_message_text(text="Can't quit root folder!", chat_id=usr_id, message_id=msg.message_id)
                        return None
                    ctlg.exit_folder()
                    bot.edit_message_text(text="exited folder\n" + ctlg.path, chat_id=usr_id,
                                          message_id=msg.message_id)
                case Data.Status.CREATE:
                    bot.edit_message_text(text="type folder name", chat_id=usr_id, message_id=msg.message_id)
                    ctlg.sostoyanie = Sostoyanie.CREATING_NEW_FOLDER
                case _:
                    if ctlg.move_to_folder(s[2]):
                        bot.edit_message_text(text="moved to\n" + ctlg.path, chat_id=usr_id,
                                              message_id=msg.message_id)
                    else:
                        bot.edit_message_text(text="there is no such folder", chat_id=usr_id,
                                              message_id=msg.message_id)
        case Data.SEND_FILE: # Отправить файл
            bot.edit_message_text(text="Trying to send", chat_id=usr_id, message_id=msg.message_id)
            system_file_path: str = ctlg.retrieve_system_file_path(ctlg.path, s[2])
            with open(system_file_path, "rb") as file:
                bot.send_document(call.from_user.id, document=file)
            bot.edit_message_text(text="File \"" + s[2] + "\" sended", chat_id=usr_id, message_id=msg.message_id)
        case Data.BASE_DELETE:
            match s[2]:
                case Data.Status.FILE:
                    if (len(ctlg.get_files_list()) == 0):
                        bot.edit_message_text(text="there is no files here", chat_id=usr_id, message_id=msg.message_id)
                    else:
                        BotConfig.last_markup_message_id = (
                            bot.edit_message_text(text="choose file to delete", chat_id=usr_id,
                                                  message_id=msg.message_id,
                                                  reply_markup=inner_button_murkup.delete_files())).id
                case Data.Status.FOLDER:
                    if (len(ctlg.get_folders_list()) == 0):
                        BotConfig.last_markup_message_id = (
                            bot.edit_message_text(text="there is no folders here", chat_id=usr_id,
                                                  message_id=msg.message_id)).id
                    else:
                        BotConfig.last_markup_message_id = (
                            bot.edit_message_text(text="choose file to delete", chat_id=usr_id,
                                                  message_id=msg.message_id,
                                                  reply_markup=inner_button_murkup.delete_folders())).id
        case Data.DELETE_FILE:
            # так же надо реализовать отправку удаляемого файла
            # s[1] - путь s[2] - имя файла
            bot.edit_message_text(text="Trying to send", chat_id=usr_id, message_id=msg.message_id)
            system_file_path: str = ctlg.retrieve_system_file_path(ctlg.path, s[2])
            with open(system_file_path, "rb") as file:
                bot.send_document(call.from_user.id, document=file)
            ctlg.delete_file(ctlg.path, s[2])
            bot.edit_message_text(text="file deleted\n" + s[1] + s[2], chat_id=usr_id, message_id=msg.message_id)
        case Data.DELETE_FOLDER:
            # так же надо реализовать отправку удаляемого файла
            # s[1] - путь s[2] - имя папки
            if not ctlg.delete_folder(ctlg.path + s[2]):
                bot.edit_message_text(text="Папка не пустая перед удалением почистите", chat_id=usr_id, 
                                      message_id=msg.message_id)
            else:
                bot.edit_message_text(text="file deleted\n" + s[1] + s[2], chat_id=usr_id, message_id=msg.message_id)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = ctlg.path + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as exc:
        bot.reply_to(message, exc)





print(ctlg.get_tree())
bot.polling(non_stop=True, interval=0)