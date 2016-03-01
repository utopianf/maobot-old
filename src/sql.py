#!/usr/local/bin/env python3
#-*- coding=utf-8 -*-

import configparser
import pymysql

class sql:
    """A class for connection to mysql and operation"""
    
    select_str = "SELECT %s FROM irclog WHERE %s=%s"

    def __init__(self):
        self.con = None
        self.cur = None

    def __enter__(self):
        config = configparser.ConfigParser()
        config.read("../../../../sql.ini")
        default = config["DEFAULT"]
        self.con = pymysql.connect(host=default['server'],
                user=default['user'],
                passwd=default['passwd'],
                db=default['db'],
                charset='utf8')
        self.cur = self.con.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.con = None
            self.cur = None
            return False
        self.con.commit()
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None
        return True

    def insert_log(self, user_name, logtype, channel, content):
        """insert the log into the mysql"""
        self.cur.execute("INSERT INTO irclog (user, type, channel, content) VALUES (%s, %s, %s, %s)", 
                (user_name, logtype, channel, content))

    def select_id(self, log_id, colume=None):
        result = None
        if colume == None:
            self.cur.execute(select_str, ("*", "id", log_id))
        else:
            self.cur.execute(select_str, (colume, "id", log_id))
        result = self.cur.fetchone()
        return result
    
    def select_channel(self, channel, colume=None):
        result = None
        if colume == None:
            self.cur.execute(select_str, ("*", "channel", channel))
        else:
            self.cur.execute(select_str, (colume, "channel", channel))
        result = self.cur.fetchall()
        return result

    def select_all(self):
        result = None
        self.cur.execute("SELECT * FROM irclog")
        result = self.cur.fetchall()
        return result

    def find_user(self,user):
        result = None
        self.cur.execute("SELECT * FROM irclog WHERE username=%s", user)
        result = self.cur.fetchall()
        if result != None:
            return True
        else:
            return False
        return False

    def show_channels(self):
        result = None
        self.cur.execute("SELECT * FROM channel")
        result = self.cur.fetchall()
        return result

    def insert_channel(self, channel):
        self.cur.execute("SELECT * FROM channel WHERE name=%s", channel)
        result = self.cur.fetchall()
        for row in result:
            if row[1] == channel:
                return
        self.cur.execute("INSERT INTO channel (name) VALUES (%s)", channel)

if __name__ == "__main__":
    sql = sql()
    with sql:
        sql.insert_log("test", "test", "test", "test from sql.py")
        for row in sql.select_all():
            print(row)

