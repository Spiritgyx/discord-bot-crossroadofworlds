import os
import sqlite3
from mylogger import MyLogger
from typing import List, Tuple, Union


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
                      "channel_id integer PRIMARY KEY,"
                      "guild_id integer NOT NULL,"
                      # "channel_id integer NOT NULL,"
                      "channel_name text NOT NULL,"
                      "FOREIGN KEY (guild_id) REFERENCES list_guilds (guild_id)"
                      ");"),
    "list_react_msg": ("CREATE TABLE IF NOT EXISTS list_react_msg ("
                       "message_id integer PRIMARY KEY,"
                       "guild_id integer NOT NULL,"
                       "channel_id integer NOT NULL,"
                       "FOREIGN KEY (guild_id) REFERENCES list_guilds (guild_id),"
                       "FOREIGN KEY (channel_id) REFERENCES list_channels (channel_id)"
                       ");"),
    "list_emojis": ("CREATE TABLE IF NOT EXISTS list_emojis ("
                    "emoji_id integer PRIMARY KEY,"
                    "guild_id integer NOT NULL,"
                    "emoji_name text NOT NULL,"
                    "emoji_anim integer NOT NULL,"
                    "FOREIGN KEY (guild_id) REFERENCES list_guilds (guild_id)"
                    ");"),
    "list_reactions": ("CREATE TABLE IF NOT EXISTS list_reactions ("
                       "message_id integer NOT NULL,"
                       "emoji_id integer NOT NULL,"
                       "reaction_type text NOT NULL,"
                       "reaction_argument text NOT NULL,"
                       "FOREIGN KEY (emoji_id) REFERENCES list_emojis (emoji_id),"
                       "FOREIGN KEY (message_id) REFERENCES list_react_msg (message_id),"
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


    def get_emojis(self, guild_id: int = None):
        """
        Return all emojis or emojis in selected guild from SQL DataBase.

        Parameters
        -----------
        guild_id: :class:`int`
            optional integer Guild ID

        Returns
        --------
        :class:`List[Tuple[int, int, str, int]]`
            Emoji ID, Guild ID, Emoji name, Emoji animated
        """
        c = self.conn.cursor()
        if guild_id is None:
            c.execute((
                f"SELECT * FROM list_emojis;"
            ))
        else:
            c.execute((
                f"SELECT * FROM list_emojis "
                f"WHERE guild_id={guild_id};"
            ))
        emojis = c.fetchall()
        return emojis

    def add_emojis(self, emojis):
        """
        Add emojis to SQL DataBase.

        Parameters
        -----------
        emojis: :class:`List[Tuple[int, int, str, int]]`
            Emoji ID, Guild ID, Emoji name, Emoji animated
        """
        if len(emojis) == 0:
            self.logger.info(f"All emojis in DB.")
            return 0
        c = self.conn.cursor()
        for emoji in emojis:
            self.logger.debug(f"Add new emoji: {emoji}")
            c.execute((
                "INSERT INTO list_emojis ("
                "emoji_id, guild_id, emoji_name, emoji_anim"
                ") VALUES (?, ?, ?, ?);"
            ), emoji)
        self.conn.commit()
        self.logger.info(f"Added {len(emojis)} emoji in DB.")
