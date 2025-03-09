from telebot import types

from Catalog import Catalog


class Data:
    CHANGE_FOLDER: str = '1'
    SEND_FILE: str = '2'
    DELETE_FOLDER: str = '3'
    DELETE_FILE: str = "4"
    BASE_DELETE: str = '5'
    class Status:
        EXIT: str = '(exit)'
        CREATE: str = '(create)'
        FOLDER: str = '1'
        FILE: str = '2'


class InnerBottonsMarkup:
    @staticmethod
    def change_folder() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="cd ..", callback_data='|'.join(
            [Data.CHANGE_FOLDER, Catalog.get_path(), Data.Status.EXIT]))
        markup.add(btn)
        btn = types.InlineKeyboardButton(text="create", callback_data='|'.join(
            [Data.CHANGE_FOLDER, Catalog.get_path(), Data.Status.CREATE]))
        markup.add(btn)
        for i in Catalog.get_folders_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.CHANGE_FOLDER, Catalog.get_path(), i]))
            markup.add(btn)
        return markup

    @staticmethod
    def send_file() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for i in Catalog.get_files_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.SEND_FILE, Catalog.get_path(), i]))
            markup.add(btn)
        return markup

    @staticmethod
    def delete_folders() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for i in Catalog.get_folders_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.DELETE_FOLDER, Catalog.get_path(), i]))
            markup.add(btn)
        return markup
    @staticmethod
    def delete_files() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for i in Catalog.get_files_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.DELETE_FILE, Catalog.get_path(), i]))
            markup.add(btn)
        return markup
    @staticmethod
    def base_delete() -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="folder", callback_data='|'.join(
            [Data.BASE_DELETE, Catalog.get_path(), Data.Status.FOLDER]))
        markup.add(btn)
        btn = types.InlineKeyboardButton(text="file", callback_data='|'.join(
            [Data.BASE_DELETE, Catalog.get_path(), Data.Status.FILE]))
        markup.add(btn)
        return markup

    @staticmethod
    def base_keyboard() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("изменить папку")
        markup.add(btn1)
        btn2 = types.KeyboardButton("показать файлы")
        markup.add(btn2)
        return markup