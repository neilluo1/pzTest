import pymysql
from utils.decorator import print_for_call
from libs.log_obj import LogObj


logger = LogObj().get_logger()


class MysqlObj(object):
    def __init__(self, host, username, password, port=3306, database=None, autocommit=True):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.autocommit = autocommit

        logger.info("Init conn for {host}:{port} ->> {db}".format(host=self.host, port=self.port, db=self.database))
        self.conn = pymysql.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            port=self.port,
            database=self.database,
            autocommit=self.autocommit,
            cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.conn.cursor()

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            logger.error('Exception occured, error is {err}!'.format(err=e))

    @print_for_call
    def run_sql_cmd(self, sql_cmd):
        logger.debug(sql_cmd)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql_cmd)

    def commit(self):
        self.conn.commit()

    @property
    def fetchall(self):
        rows = self.cursor.fetchall()
        return rows

    @property
    def fetchone(self):
        return self.cursor.fetchone()


if __name__ == '__main__':
    username = 'root'
    password = 'password'
    vbos_node_ip = '10.180.116.23'
    device = '/dev/dpl1'
    host = '10.199.116.1'

    mysql_obj = MysqlObj(host, username, password)
    use_db_cmd = 'use vbos10_180_116_11'
    mysql_obj.run_sql_cmd(use_db_cmd)