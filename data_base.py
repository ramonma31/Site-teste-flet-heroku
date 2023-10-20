import sqlite3 as db
from abc import ABC, abstractmethod


class DataBase(ABC):

    @abstractmethod
    def connectdb(self): pass

    @abstractmethod
    def disconnectdb(self): pass

    @abstractmethod
    def insert_into(self, command: str) -> None: pass

    @abstractmethod
    def select_from(self, command: str | bool) -> list[tuple]: pass

    @abstractmethod
    def update_from(self, column: str) -> None: pass

    @abstractmethod
    def delete_data(self, command: str) -> None: pass


class DataBaseUser(DataBase):
    def __init__(self) -> None:
        self.connect = db.connect("data_base.db")
        self.cursor = self.connect.cursor()

    def connectdb(self):
        self.connect = db.connect("data_base.db")
        self.cursor = self.connect.cursor()
        return

    def disconnectdb(self):
        self.cursor.close()
        self.connect.close()
        return

    def update_from(self, command: str) -> None:
        self.connectdb()
        self.cursor.execute(f"UPDATE userprofile SET {command}")
        self.connect.commit()
        self.disconnectdb()
        return

    def insert_into(self, command: str) -> None:
        self.connectdb()
        self.cursor.execute(f"INSERT INTO userprofile {command}")
        self.connect.commit()
        self.disconnectdb()
        return

    def select_from(self, command: str | bool) -> list[tuple]:
        self.connectdb()
        if command:
            try:
                data = self.cursor.execute(
                    f"SELECT * FROM userprofile {command}"
                )
                return data.fetchall()
            except Exception:
                return []
        try:
            query = self.cursor.execute("SELECT * FROM userprofile")
            data = query.fetchall()
            self.disconnectdb()
            return data
        except Exception:
            return []

    def delete_data(self, command: str) -> None:
        self.connectdb()
        self.cursor.execute(f"UPDATE userprofile SET {command}")
        self.connect.commit()
        self.disconnectdb()
        return


class DataBaseOptions(DataBase):
    def __init__(self) -> None:
        self.connect = db.connect("data_base.db")
        self.cursor = self.connect.cursor()

    def connectdb(self):
        self.connect = db.connect("data_base.db")
        self.cursor = self.connect.cursor()
        return

    def disconnectdb(self):
        self.cursor.close()
        self.connect.close()
        return

    def update_from(self, command: str) -> None:
        self.connectdb()
        self.cursor.execute(f"UPDATE gameconfig SET {command}")
        self.connect.commit()
        self.disconnectdb()
        return

    def insert_into(self, command: str) -> None:
        self.connectdb()
        self.cursor.execute(f"INSERT INTO gameconfig {command}")
        self.connect.commit()
        self.disconnectdb()
        return

    def select_from(self, command: str | bool) -> list[tuple]:
        self.connectdb()
        if command:
            data = self.cursor.execute(f"SELECT * FROM gameconfig {command}")
            return data.fetchall()
        query = self.cursor.execute("SELECT * FROM gameconfig")
        data = query.fetchall()
        self.disconnectdb()
        return data

    def delete_data(self, command: str) -> None:
        self.connectdb()
        self.cursor.execute(f"UPDATE gameconfig SET {command}")
        self.connect.commit()
        self.disconnectdb()
        return
