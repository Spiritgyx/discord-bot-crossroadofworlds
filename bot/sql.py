import os
import sqlite3
from mylogger import MyLogger


SQL_CREATE_TABLES = {
    "list_guilds": ("CREATE TABLE IF NOT EXISTS list_guilds ("
                    "guild_id integer PRIMARY KEY,"
                    "guild_name text NOT NULL"
                    ");"),
    "list_members": ("CREATE TABLE IF NOT EXISTS list_members ("
                     "id integer PRIMARY KEY,"
                     "guild_id integer NOT NULL,"
                     "member_id integer NOT NULL,"
                     "member_tag text NOT NULL,"
                     "member_nickname text NOT NULL,"
                     "FOREIGN KEY (guild_id) REFERENCES list_guilds (guild_id)"
                     ");"),
    "list_channels": ("CREATE TABLE IF NOT EXISTS list_channels ("
                      "id integer PRIMARY KEY,"
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
        else:
            try:
                self.conn = sqlite3.connect(db_path)
            except sqlite3.Error as e:
                self.logger.error(e)
                return

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

    def get_guilds(self) -> list:
        c = self.conn.cursor()
        c.execute((
            "SELECT guild_id FROM list_guilds;"
        ))
        guilds = c.fetchall()

        return guilds

    def add_guilds(self, guilds: list):
        c = self.conn.cursor()
        for guild in guilds:
            c.execute((
                "INSERT INTO list_guilds (guild_id, guild_name) VALUES (?, ?);"
            ), guild)
        self.conn.commit()
        self.logger.info(f"Added {len(guilds)} guilds in DB.")

    def get_members(self, guild_id):
        c = self.conn.cursor()
        c.execute((
            f"SELECT * FROM list_members WHERE guild_id={guild_id};"
        ))
        members = c.fetchall()
        return members

    def add_members(self, members: list):
        c = self.conn.cursor()
        for member in members:
            self.logger.debug(f"Add new member: {member}")
            c.execute((
                "INSERT INTO list_members (guild_id, member_id, member_tag, member_nickname) VALUES (?, ?, ?, ?);"
            ), member)
        self.conn.commit()
        self.logger.info(f"Added {len(members)} members in DB.")
