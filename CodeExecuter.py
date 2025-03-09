import subprocess


class CodeExecuter:
    @staticmethod
    def cover(path:str):
        if path.__contains__(' ') and not path.__contains__('"'):
            return '"' + path + '"'
        return path

    @staticmethod
    def execute(command:str) -> str:
        try:
            return subprocess.check_output(command, shell=True).decode().strip()
        except Exception:
            return ''

    @staticmethod
    def check_how_many(path: str) -> int:
        path = CodeExecuter.cover(path)
        command = "ls " + path + " | wc -l"
        return int(subprocess.check_output(command, shell=True).decode().strip())

    @staticmethod
    def chеck_existane(path: str, file_name:str="") -> bool:
        reply: int = 1
        if not bool(file_name.strip()):
            path = CodeExecuter.cover(path)
            command = "[ -d " + path + " ] && echo $? || echo $?"
            reply = int(subprocess.check_output(command, shell=True).decode().strip())
            # print(str(reply) + "|" + command)
        else:
            full: str = CodeExecuter.cover(path + file_name)
            command = "[ -f " + full + " ] && echo $? || echo $?"
            reply = int(subprocess.check_output(command, shell=True).decode().strip())
            # print(str(reply) + "|" + command)
        return reply == 0

    ## Гэттеры
    @staticmethod
    def get_folders_list(path:str='') -> list:
        path = CodeExecuter.cover(path)
        command = 'ls -F ' + path + ' | grep /'
        try:
            return subprocess.check_output(command, shell=True).decode().strip().split('\n')
        except Exception: # значит что нет подобного
            return list()
    @staticmethod
    def get_files_list(path:str='') -> list:
        path = CodeExecuter.cover(path)
        command =  'ls -F ' + path + ' | grep -v /'
        try:
            return subprocess.check_output(command, shell=True).decode().strip().split('\n')
        except Exception: # значит что нет подобного
            return list()

    @staticmethod
    def get_working_path() -> str:
        return 'storage/'
    @staticmethod
    def get_working_fullpath() -> str:
        command = 'echo $PWD'
        return subprocess.check_output(command, shell=True).decode().strip() + '/'


    ## Создание
    @staticmethod
    def create_new_folder(path:str, new_folder_name:str) -> None:
        full: str = CodeExecuter.cover(path + new_folder_name)
        command = 'mkdir ' + full
        subprocess.check_output(command, shell=True)


    ## Удаление
    @staticmethod
    def delete_file(path: str, delete_ffile_name: str) -> bool:
        try:
            full: str = CodeExecuter.cover(path + delete_ffile_name)
            command = 'rm ' + full
            subprocess.check_output(command, shell=True)
        except Exception:
            print("Не удалось удалить файл")
            print(path + delete_ffile_name)
            print(Exception)
            return False
        return True
    @staticmethod
    def delete_folder(path: str, delete_folder_name: str) -> bool:
        full: str = CodeExecuter.cover(path + delete_folder_name)
        if (CodeExecuter.check_how_many(full) != 0):
            return False
        command = 'rm -r ' + full
        subprocess.check_output(command, shell=True)
        return True
