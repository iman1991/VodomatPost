#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql.cursors
# import sqlite3
# conn = sqlite3.connect('Vodm.db')
# c = conn.cursor()

def connect():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='7087',
                                 db='vodomat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def update_user(**kwargs):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET score = '{}' WHERE IDT = {}".format(kwargs.get('score'), kwargs.get('idT')))

    connection.commit()
    cursor.close()
    connection.close()