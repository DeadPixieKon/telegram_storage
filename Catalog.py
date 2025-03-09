from CodeExecuter import CodeExecuter


class Sostoyanie:
    WAIT_FOR_START_COMMAND: int = -1
    WAIT_FOR_INPUT: int = 0
    DOWNLOADING_FILE: int = 1
    SENDING_FILE: int = 2
    CREATING_NEW_FOLDER: int = 3
    TEXT_PROCESSING: int = 4


class Catalog: # Catalog
    # 1-ая статическая переменная / реализация
    path = CodeExecuter.get_working_path()
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
    def chеck_existane(path: str, file_name:str="") -> bool:
        return CodeExecuter.chеck_existane(path, file_name)


    # обертка гэттеров на CodeExecuter
    @staticmethod
    def get_folders_list() -> list:
        return CodeExecuter.get_folders_list(Catalog.path)
    @staticmethod
    def get_files_list() -> list:
        return CodeExecuter.get_files_list(Catalog.path)

    @staticmethod
    def get_fullpath() -> str:
        fullpath: str = CodeExecuter.get_working_fullpath()
        if fullpath[-1] != '/': fullpath = fullpath + '/'
        return  fullpath + Catalog.path


    # перемещение
    @staticmethod
    def move_to_folder(dir: str) -> bool:
        # if not bool(dir.strip()):
        #     return False
        if dir[-1] != '/': dir = dir + '/'
        if not CodeExecuter.chеck_existane(Catalog.path + dir):
            return False
        path = Catalog.path
        path = path + dir
        Catalog.path = path
        return True

    @staticmethod
    def exitFolder():
        path = Catalog.path
        if (len(path) == 0):
            return
        if path.count('/') == 1:
            path = ""
        else:
            a = path[:-1].rindex('/')
            path = path[:a + 1]
        Catalog.path = path


    # Создание
    @staticmethod
    def create_new_folder(new_folder_name:str) -> bool:
        try:
            CodeExecuter.create_new_folder(Catalog.path, new_folder_name)
        except Exception:
            return False # похоже такая папка уже существует
        return True # все ок


    # Удаление
    @staticmethod
    def delete_folder(path: str, delete_folder_name: str) -> bool:
        return CodeExecuter.delete_folder(path, delete_folder_name)
    @staticmethod
    def delete_file(path: str, delete_ffile_name: str) -> bool:
        return CodeExecuter.delete_file(path, delete_ffile_name)