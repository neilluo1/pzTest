from libs.mysql_obj import MysqlObj
from common.common import get_io_stats
import json
from settings.global_settings import MYSQL_USER, MYSQL_HOST, MYSQL_PASSWORD
from libs.log_obj import LogObj

logger = LogObj().get_logger()


class CollectVolumeData(object):
    _mysql_obj = None

    def __init__(self, device, ip, username, password):
        self.device = device
        self.ip = ip
        self.username = username
        self.password = password
        self.db_name = 'storage'
        self.table_name = '{ip}_{name}'.format(ip=self.ip.replace('.', '_'), name=self.device.split('/')[-1])

        create_db_cmd = 'create database if not exists {db}'.format(db=self.db_name)
        self.mysql_obj.run_sql_cmd(create_db_cmd)

    @property
    def mysql_obj(self):
        if self._mysql_obj is None:
            self._mysql_obj = MysqlObj(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD)
        return self._mysql_obj

    def create_volume_table(self):
        create_table = """create table if not exists {db}.{table_name} (
            io_stat JSON,
            c_time datetime)""".format(db=self.db_name, table_name=self.table_name)
        self.mysql_obj.run_sql_cmd(create_table)

    def insert_volume_data(self):
        try:
            for c_time, io_stat in get_io_stats(self.device, self.ip, self.username, self.password).items():
                sql_cmd = """INSERT INTO {db}.{table_name} (
                                    io_stat,
                                    c_time)
                                    VALUES (
                                    '{io_stat}',
                                    '{c_time}')""".format(db=self.db_name,
                                                          table_name=self.table_name,
                                                          io_stat=json.dumps(io_stat),
                                                          c_time=c_time)
                self.mysql_obj.run_sql_cmd(sql_cmd)
        except Exception as e:
            logger.error('Exception occured, error is {err}!'.format(err=e))
