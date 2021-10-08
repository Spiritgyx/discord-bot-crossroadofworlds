import os
import sqlite3
from bot.mylogger import MyLogger


SQL_CREATE_TABLES = {
    "list_guilds": ("CREATE TABLE IF NOT EXISTS list_guilds ("
                    "guild_id integer PRIMARY KEY,"
                    "guild_name text NOT NULL"
                    ");"),
    "list_members": ("CREATE TABLE IF NOT EXISTS list_members ("
                     "id integer PRIMARY KEY AUTOINCREMENT,"
                     "guild_id integer NOT NULL,"
                     "member_id integer NOT NULL,"
                     "member_tag text NOT NULL,"
                     "member_nickname text NOT NULL,"
                     "FOREIGN KEY (guild_id) REFERENCES list_guilds (guild_id)"
                     ");"),
    "list_channels": ("CREATE TABLE IF NOT EXISTS list_channels ("
                      "id integer PRIMARY KEY AUTOINCREMENT,"
                      "guild_id integer NOT NULL,"
                      "channel_id integer NOT NULL,"
                      "channel_name text NOT NULL,"
                      "FOREIGN KEY (guild_id) REFERENCES list_guilds (guild_id)"
                      ");")
}


class Sql:
    def __init__(self, db_path: str='database.db', level=20):
        self.logger = MyLogger('sql', filename='sql.log', levels=(level, 20))
        if not os.path.exists(db_path):
            self.conn = self.create_db(db_path)
            if self.conn is None:
                return
            self.create_tables()


    def create_db(self, db_path='database.db'):
        try:
            conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            self.logger.error(e)
            return None
        return conn

    def create_tables(self):
        c = self.conn.cursor()
        for k, v in SQL_CREATE_TABLES.items():
            try:
                c.execute(v)
            except sqlite3.Error as e:
                self.logger.error(f"Table [{k}] create failed.")
            else:
                self.logger.info(f"Table [{k}] created.")
        self.conn.commit()

