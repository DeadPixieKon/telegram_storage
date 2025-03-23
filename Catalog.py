from sqlite import DBWork


class Sostoyanie:
    WAIT_FOR_START_COMMAND: int = -1
    WAIT_FOR_INPUT: int = 0
    DOWNLOADING_FILE: int = 1
    SENDING_FILE: int = 2
    CREATING_NEW_FOLDER: int = 3
    TEXT_PROCESSING: int = 4


class Catalog: # Catalog
    # 1-ая статическая переменная / реализация
    db = DBWork()
    path = db.get_working_path()
    @staticmethod
    def get_path() -> str:
        return Catalog.path
    @staticmethod
    def set_path(path:str) -> None:
        Catalog.path = path

    # 2-ая статическая переменная / реализация
    sostoyanie = 0
    @staticmethod
    def get_sostoyanie() -> int:
        return Catalog.sostoyanie
    @staticmethod
    def set_sostoyanie(sostoyanie: int) -> None:
        Catalog.sostoyanie = sostoyanie


    @staticmethod
    def parse_path(path: str) -> list:
        return Catalog.db.parse_path(Catalog.path)

    @staticmethod
    def check_existane(path: str, file_name:str="") -> bool:
        return Catalog.db.chеck_existane(path, file_name)


    # обертка гэттеров на DBWork
    @staticmethod
    def get_folders_list() -> list:
        return [i[1] for i in Catalog.db.get_folders_list(Catalog.db.get_folder_id(Catalog.path))]
    @staticmethod
    def get_files_list() -> list:
        return [i[1] for i in Catalog.db.get_files_list(Catalog.db.get_folder_id(Catalog.path))]


    # перемещение
    @staticmethod
    def move_to_folder(folder_name: str) -> bool:
        if folder_name[-1] != '/': folder_name = folder_name + '/'
        if not Catalog.db.chеck_existane(Catalog.path + folder_name):
            return False
        path = Catalog.path
        path = path + folder_name
        Catalog.path = path
        return True

    @staticmethod
    def exit_folder():
        path = Catalog.path
        if path.strip('/') == "storage":
            return
        else:
            a = path[:-1].rindex('/')
            path = path[:a + 1]
        Catalog.path = path


    # Создание
    @staticmethod
    def create_new_folder(new_folder_name:str) -> bool:
        if new_folder_name.count('/') > 0:
            return False
        try:
            Catalog.db.create_new_folder(Catalog.db.get_folder_id(Catalog.path), new_folder_name)
        except Exception:
            return False # похоже такая папка уже существует
        return True # все ок

    @staticmethod
    def insert_new_file(file_name:str, system_file_path: str) -> bool:
        if file_name.count('/') > 0:
            return False
        folder_id: int = Catalog.db.get_folder_id(Catalog.get_path())
        Catalog.db.insert_file(file_name=file_name, file_path=system_file_path, folder_id=folder_id)
        return True


    # Удаление
    @staticmethod
    def delete_folder(path: str) -> bool:
        try:
            Catalog.db.delete_folder(Catalog.db.get_folder_id(path))
            return True
        except Exception:
            return False
    @staticmethod
    def delete_file(path: str, delete_file_name: str) -> bool:
        try:
            Catalog.db.delete_file(Catalog.db.get_file_id(path, delete_file_name))
            return True
        except Exception:
            return False

    @staticmethod
    def get_tree() -> str:
        return Catalog.db.get_tree()


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