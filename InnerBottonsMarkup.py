from telebot import types

from Catalog import Catalog as Kat


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
    def __init__(self, ctlg: Kat):
        self.__ctlg: Kat = ctlg

    def change_folder(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="cd ..", callback_data='|'.join(
            [Data.CHANGE_FOLDER, self.__ctlg.path, Data.Status.EXIT]))
        markup.add(btn)
        btn = types.InlineKeyboardButton(text="create", callback_data='|'.join(
            [Data.CHANGE_FOLDER, self.__ctlg.path, Data.Status.CREATE]))
        markup.add(btn)
        for i in self.__ctlg.get_folders_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.CHANGE_FOLDER, self.__ctlg.path, i]))
            markup.add(btn)
        return markup

    def send_file(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for i in self.__ctlg.get_files_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.SEND_FILE, self.__ctlg.path, i]))
            markup.add(btn)
        return markup

    def delete_folders(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for i in self.__ctlg.get_folders_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.DELETE_FOLDER, self.__ctlg.path, i]))
            markup.add(btn)
        return markup

    def delete_files(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for i in self.__ctlg.get_files_list():
            btn = types.InlineKeyboardButton(text=i, callback_data='|'.join(
            [Data.DELETE_FILE, self.__ctlg.path, i]))
            markup.add(btn)
        return markup

    def base_delete(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="folder", callback_data='|'.join(
            [Data.BASE_DELETE, self.__ctlg.path, Data.Status.FOLDER]))
        markup.add(btn)
        btn = types.InlineKeyboardButton(text="file", callback_data='|'.join(
            [Data.BASE_DELETE, self.__ctlg.path, Data.Status.FILE]))
        markup.add(btn)
        return markup

    @staticmethod
    def base_keyboard(self) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("изменить папку")
        markup.add(btn1)
        btn2 = types.KeyboardButton("показать файлы")
        markup.add(btn2)
        return markup