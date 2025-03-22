import sqlite3
import _sqlite3


class DBWork:
    def __init__(self, db_path="bot_storage.db"):
        self.conn: _sqlite3.Connection = sqlite3.connect(db_path)
        self.cur: _sqlite3.Cursor = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    @staticmethod
    def parse_path(path: str) -> list:
        return [i for i in path.strip(".").split('/') if i.strip()]

    # Создание
    def create_new_folder(self, parent_folder_id: int, new_folder_name: str):
        self.cur.execute(
            "UPDATE folders SET count_of_subfolders = count_of_subfolders + 1 WHERE id = ?",
            (parent_folder_id,)
        )
        self.conn.commit()
        self.cur.execute(
            "INSERT INTO folders (name, parent_id) VALUES (?, ?)",
            (new_folder_name, parent_folder_id)
        )
        self.conn.commit()

    # Удаление
    def delete_folder(self, folder_id: int):
        if folder_id == 1:
            raise Exception("Can't delete root catalog")
        elif self.get_how_many(folder_id):  # значит папка не пустая
            raise Exception("folder is not empty")
        self.cur.execute(
            "UPDATE folders SET count_of_subfolders = count_of_subfolders - 1 WHERE id = ?",
            (self.get_parent_id(folder_id),)
        )
        self.conn.commit()
        self.cur.execute(
            "DELETE FROM folders WHERE id = ?",
            (folder_id,)
        )
        self.conn.commit()

    # Функция для вставки файла в базу данных
    def insert_file(self, file_name: str, folder_id: int, file_path: str):
        self.cur.execute(
            "INSERT INTO files (folder_id, file_name, file_link) VALUES (?, ?, ?)",
            (folder_id, file_name, file_path)
        )
        self.conn.commit()
        self.cur.execute(
            "UPDATE folders SET count_of_subfiles = count_of_subfiles + 1 WHERE id = ?",
            (folder_id,)
        )
        self.conn.commit()

    # Функция для извлечения файла из базы данных
    def retrieve_file(self, file_id: int) -> str:
        self.cur.execute(
            "SELECT file_link FROM files WHERE id = ?",
            (file_id,)
        )
        file_path = self.cur.fetchone()
        if file_path is None:
            raise Exception("no such file")
        return str(file_path[0])

    # удаление файла
    def delete_file(self, file_id: int):
        self.cur.execute(
            "SELECT folder_id FROM files WHERE id = ?",
            (file_id,)
        )
        folder_id = int(self.cur.fetchone()[0])
        self.cur.execute(
            "UPDATE folders SET count_of_subfiles = count_of_subfiles - 1 WHERE id = ?",
            (folder_id,)
        )
        self.conn.commit()
        self.cur.execute(
            "DELETE FROM files WHERE id = ?",
            (file_id,)
        )
        self.conn.commit()

    # Гэттеры
    def get_how_many(self, folder_id: int) -> int:
        self.cur.execute(
            "SELECT count_of_subfiles + count_of_subfolders FROM folders WHERE id = ?",
            (folder_id,)
        )
        try:
            return int(self.cur.fetchone()[0])
        except Exception:
            raise Exception("no such folder")

    def get_folders_list(self, folder_id: int) -> list:
        self.cur.execute(
            "SELECT id, name FROM folders WHERE parent_id = ?",
            (folder_id,)
        )
        return self.cur.fetchall()

    def get_files_list(self, folder_id: int) -> list:
        self.cur.execute(
            "SELECT id, file_name FROM files WHERE folder_id = ?",
            (folder_id,)
        )
        return self.cur.fetchall()

    def get_parent_id(self, folder_id: int) -> int:
        self.cur.execute(
            "SELECT parent_id FROM folders WHERE id = ?",
            (folder_id,)
        )
        response = self.cur.fetchone()
        if response is None:
            return -1
        return response[0]

    def get_folder_id(self, path: str) -> int:
        # like "storage\"
        def get_folder_id_by_name_and_id(cur: _sqlite3.Cursor, folder_name: str) -> int:
            cur.execute(
                "SELECT id FROM folders WHERE parent_id = ? AND name = ?",
                (parent_id, folder_name)
            )
            response = cur.fetchone()
            if response is None:
                return -1
            return response[0]

        parent_id = 0
        for i in DBWork.parse_path(path):
            parent_id = get_folder_id_by_name_and_id(self.cur, i)
        return parent_id

    def get_file_id(self, path: str, file_name: str = None) -> int:
        if file_name is None:
            parsed_path = DBWork.parse_path(path)
            path, file_name = '/'.join(parsed_path[:-1]), parsed_path[-1]
        folder_id = self.get_folder_id(path)
        if folder_id == -1:
            return -1, folder_id
        self.cur.execute(
            "SELECT id FROM files WHERE file_name = ? AND folder_id = ?",
            (file_name, folder_id)
        )
        response = self.cur.fetchone()
        if response is None:
            return -1
        return response[0]

    def get_tree(self) -> str:
        def draw_pre_symbols(which_levels: list) -> str:
            pre_symbols = ""
            # print(which_levels)
            for i in which_levels:
                if i == 0:
                    pre_symbols += "|   "
                elif i == 1:
                    # pre_symbols += "|   "
                    pre_symbols += "|---"
                elif i == 2:
                    pre_symbols += "    "
            return pre_symbols


        def add_files(folder_id: int, which_levels: list):
            nonlocal tree
            for id, file_name in self.get_files_list(folder_id):
                tree += draw_pre_symbols(which_levels=which_levels) + file_name + "\n"


        def add_folder(folder_id: int, which_levels: list):
            nonlocal tree
            for id, folder_name in self.get_folders_list(folder_id):
                tree += draw_pre_symbols(which_levels=which_levels) + folder_name + "/\n"
                current_levels = which_levels[:]
                # print("which_levels=", which_levels, "current_levels=", current_levels, "folder_name=", folder_name)
                current_levels[len(which_levels)-1] = 1
                current_levels.append(0)
                add_files(folder_id=id, which_levels=current_levels)
                add_folder(folder_id=id, which_levels=current_levels)



        tree: str = "./storage\n"

        which_levels = list()
        which_levels.append(0)
        add_files(folder_id=1, which_levels=which_levels)
        add_folder(folder_id=1, which_levels=which_levels)
        # print("-" * 30, "RESULT", "-" * 30)
        return tree


db = DBWork()
# db.create_new_folder(parent_folder_id=9, new_folder_name="third level")
# db.delete_folder(folder_id=3)
# db.insert_file(file_name="lol.txt", folder_id=3, file_path="storage/file2")
# db.insert_file(file_name="kak.txt", folder_id=8, file_path="storage/file1")
# print(db.retrieve_file(2))
# db.delete_file(file_id=6)
# print(db.get_how_many(folder_id=3))
# print(db.get_folders_list(folder_id=1))
# print(db.get_files_list(folder_id=3))
# print(db.get_parent_id(folder_id=3))
# print(db.get_folder_id("storage/first level"))
# print(db.get_file_id("storage/first level", "lol.txt"))
# print(db.get_file_id("storage/first level/lol.txt"))
print(db.get_tree())
# print("-" * 30, "RESULT", "-" * 30)
# print(db.get_folder_id("storage/first level/second level third"))