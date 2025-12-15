""" MySQLStorage """

import time
import datetime
import os
import random
import threading
import mysql.connector
from datacollector.logger.log import LOGGER
from datacollector.storage.abstract_storage import AbstractStorage


class MySQLStorage(AbstractStorage):
    """ MySQLStorage """

    def __init__(self):
        self.connection = None
        self.mysql_host = "172.17.0.1"
        self.mysql_port = "3306"
        self.mysql_db = "sibasng"
        self.mysql_user = "myuser"
        self.mysql_pass = "mysecret"
        self.last_time = 0
        self.msg_log = {}
        super(MySQLStorage, self).__init__()

    def _init_from_env(self):
        """ Get env variables """
        env_mysql_host = os.getenv('STORAGE_MYSQL_HOST')
        env_mysql_port = os.getenv('STORAGE_MYSQL_PORT')
        env_mysql_db = os.getenv('STORAGE_MYSQL_DB')
        env_mysql_user = os.getenv('STORAGE_MYSQL_USER')
        env_mysql_pass = os.getenv('STORAGE_MYSQL_PASS')

        if env_mysql_host is not None:
            self.mysql_host = str(env_mysql_host)

        if env_mysql_port is not None:
            self.mysql_port = str(env_mysql_port)

        if env_mysql_db is not None:
            self.mysql_db = str(env_mysql_db)

        if env_mysql_user is not None:
            self.mysql_user = str(env_mysql_user)

        if env_mysql_pass is not None:
            self.mysql_pass = str(env_mysql_pass)

    def connect(self):
        #we open a thread who tries to connect
        thread = threading.Thread(target=self._connect)
        thread.start()

    def _check_table(self):
        mycursor = self.connection.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS data (id MEDIUMINT NOT NULL AUTO_INCREMENT, topic VARCHAR(255), message VARCHAR(255), PRIMARY KEY (id))")


    def _connect(self):
        while True:
            try:
                self.connection = mysql.connector.connect(host=self.mysql_host,
                                                          port=self.mysql_port,
                                                          database=self.mysql_db,
                                                          user=self.mysql_user,
                                                          passwd=self.mysql_pass)
            except Exception as exc:
                LOGGER.error("Connection to MYSQL at failed with: %s", exc)
                time.sleep(5)
                continue
            break
        self._check_table()
        return True

    def store(self, topic, key, value):
        LOGGER.info("%s:%s:%s", topic, key, value)
        mycursor = self.connection.cursor()

        sql = "INSERT INTO data (topic, message) VALUES (%s, %s)"
        val = (topic+'/'+key, value)
        mycursor.execute(sql, val)

        self.connection.commit()
