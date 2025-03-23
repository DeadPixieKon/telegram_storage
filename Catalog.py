from sqlite import DBWork


class Sostoyanie:
    WAIT_FOR_START_COMMAND: int = -1
    WAIT_FOR_INPUT: int = 0
    DOWNLOADING_FILE: int = 1
    SENDING_FILE: int = 2
    CREATING_NEW_FOLDER: int = 3
    TEXT_PROCESSING: int = 4


class Catalog:
    def __init__(self):
        self.__db = DBWork()
        self.__path = self.__db.get_working_path()
        self.__sostoyanie = 0

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path:str) -> None:
        self.__path = path

    @property
    def db(self):
        return self.__db

    @property
    def sostoyanie(self) -> int:
        return self.__sostoyanie

    @sostoyanie.setter
    def sostoyanie(self, sostoyanie: int) -> None:
        self.__sostoyanie = sostoyanie


    @staticmethod
    def parse_path(path: str) -> list:
        return DBWork.parse_path(path)

    def check_existane(self, path: str, file_name:str="") -> bool:
        return self.__db.chеck_existane(path, file_name)

    # обертка гэттеров на DBWork
    def get_folders_list(self) -> list:
        return [i[1] for i in self.__db.get_folders_list(self.__db.get_folder_id(self.__path))]

    def get_files_list(self) -> list:
        return [i[1] for i in self.__db.get_files_list(self.__db.get_folder_id(self.__path))]


    # перемещение
    def move_to_folder(self, folder_name: str) -> bool:
        if folder_name[-1] != '/': folder_name = folder_name + '/'
        if not self.__db.chеck_existane(self.__path + folder_name):
            return False
        path = self.__path
        path = path + folder_name
        self.__path = path
        return True

    def exit_folder(self):
        path = self.__path
        if path.strip('/') == "storage":
            return
        else:
            a = path[:-1].rindex('/')
            path = path[:a + 1]
        self.__path = path


    # Создание
    def create_new_folder(self, new_folder_name:str) -> bool:
        if new_folder_name.count('/') > 0:
            return False
        try:
            self.__db.create_new_folder(self.__db.get_folder_id(self.__path), new_folder_name)
        except Exception:
            return False # похоже такая папка уже существует
        return True # все ок

    def insert_new_file(self, file_name:str, system_file_path: str) -> bool:
        if file_name.count('/') > 0:
            return False
        folder_id: int = self.__db.get_folder_id(self.__path)
        self.__db.insert_file(file_name=file_name, file_path=system_file_path, folder_id=folder_id)
        return True

    def retrieve_system_file_path(self, path: str, file_name: str):
        return self.__db.retrieve_file(self.__db.get_file_id(path, file_name))


    # Удаление
    def delete_folder(self, path: str) -> bool:
        try:
            self.__db.delete_folder(self.__db.get_folder_id(path))
            return True
        except Exception:
            return False

    def delete_file(self, path: str, delete_file_name: str) -> bool:
        try:
            self.__db.delete_file(self.__db.get_file_id(path, delete_file_name))
            return True
        except Exception:
            return False

    def get_tree(self) -> str:
        return self.__db.get_tree()


# ctlg = Catalog()
# print(ctlg.chеck_existane("storage/", "lol.txt"))
# print(ctlg.get_folders_list())
# ctlg.move_to_folder("USA")
# print("path:", ctlg.get_path())
# ctlg.exitFolder()
# print("path:", ctlg.get_path())
# print(ctlg.get_files_list())
# ctlg.create_new_folder("jaba")
# ctlg.delete_folder("storage/jaba")
# ctlg.insert_new_file("lol.txt", "storage/file2")
# ctlg.delete_file(ctlg.get_path(), "lol.txt")
# print(ctlg.get_tree())