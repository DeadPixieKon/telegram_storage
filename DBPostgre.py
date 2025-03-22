import psycopg2
import configparser


class DBWork:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="bot_storage",
            user="piton",
            password="$uper_pA$S"
        )
        self.cur: psycopg2.cursor = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()


    @staticmethod
    def parse_path(path: str) -> list:
        return [i for i in path.split('\\') if i.strip()]


    # Функция для вставки файла в базу данных
    def insert_file(self, file_name: str, folder_id: int, file_path: str):
        self.cur.execute(
            "INSERT INTO files (folder_id, file_name, file_link) VALUES (%s, %s, %s)",
            (folder_id, file_name, file_path, )
        )
        self.conn.commit()

    # Функция для извлечения файла из базы данных
    def retrieve_file(self, file_id) -> str:
        self.cur.execute("SELECT file_link FROM files WHERE id = %s", (file_id,))
        file_path = self.cur.fetchone()
        if file_path is None:
            raise Exception("no such file")
        return str(file_path[0])


    ## Гэттеры
    def get_how_many(self, folder_id: int) -> int:
        self.cur.execute(
            "SELECT count(*) FROM folders WHERE parrent_id = %s", (folder_id,))
        # fch = lambda x: int(x[0]) if x is not None else 0
        # return fch(self.cur.fetchone())
        return int(self.cur.fetchone()[0])

    def get_folders_list(self, folder_id: int) -> list:
        self.cur.execute(
            "SELECT id, name FROM folders WHERE parrent_id = %s", (folder_id,))
        s = list()
        for i in range(self.cur.rowcount):
            s.append(self.cur.fetchone())
        return s

    def get_files_list(self, folder_id: int) -> list:
        self.cur.execute(
            "SELECT id, file_name, folder_id FROM files WHERE folder_id = %s", (folder_id,))
        s = list()
        for i in range(self.cur.rowcount):
            s.append(self.cur.fetchone())
        return s

    def get_parrent_id(self, folder_id: int) -> int:
        self.cur.execute(
            "SELECT parrent_id FROM folders WHERE id = %s",
            (folder_id,)
        )
        response = self.cur.fetchone()
        if response is None:
            return -1
        return response[0]

    def get_folder_id(self, path: str) -> int:
        def get_folder_id_by_name_and_id(cur, parrent_id: int, folder_name: str) -> int:
            cur.execute(
                "SELECT id FROM folders WHERE parrent_id = %s AND name = %s", (parrent_id, folder_name,))
            response = cur.fetchone()
            if response is None:
                return -1
            return response[0]


        parrent_id = 0
        for i in DBWork.parse_path(path):
            parrent_id = get_folder_id_by_name_and_id(self.cur, parrent_id, i)
        return parrent_id

    def get_file_id(self, path: str, file_name: str) -> (int, int):
        folder_id = self.get_folder_id(path)
        if folder_id == -1:
            return -1, folder_id
        self.cur.execute(
            "SELECT id FROM files WHERE file_name = %s AND folder_id = %s", (file_name, folder_id, ))
        response = self.cur.fetchone()
        if response is None:
            return -1, folder_id
        return response[0], folder_id

    ## Создание
    def create_new_folder(self, parrent_folder_id: int, new_folder_name: str) -> bool:
        self.cur.execute(
            "UPDATE folders SET count_of_subfoldes = count_of_subfoldes + 1 WHERE id = %s;\n"
            "INSERT INTO folders (name, parrent_id) VALUES (%s, %s)",
            (parrent_folder_id, new_folder_name, parrent_folder_id,)
        )
        self.conn.commit()
        return True

    ## Удаление
    def delete_file(self, file_id: int, folder_id: int) -> bool:
        self.cur.execute(
            "UPDATE folders SET count_of_subfoldes = count_of_subfoldes - 1 WHERE id = %s",
            (folder_id,)
        )
        self.conn.commit()
        self.cur.execute(
            "DELETE FROM files WHERE id = %s",
            (file_id,)
        )
        self.conn.commit()
        return True

    def delete_folder(self, folder_id: int) -> bool:
        if self.get_how_many(folder_id): # значит папка не пустая
            print("not empty")
            return False
        self.cur.execute(
            "UPDATE folders SET count_of_subfoldes = count_of_subfoldes - 1 WHERE id = %s",
            (self.get_parrent_id(folder_id),)
        )
        self.conn.commit()
        self.cur.execute(
            "DELETE FROM folders WHERE id = %s",
            (folder_id,)
        )
        self.conn.commit()
        return True


bd = DBWork()