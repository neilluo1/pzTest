# coding: utf-8

import paramiko
from libs.log_obj import LogObj
from utils.decorator import retry
import traceback
from paramiko.ssh_exception import SSHException
from utils.decorator import lock

logger = LogObj().get_logger()


class SSHObj(object):
    _ssh = None
    _sftp = None

    def __init__(self, ip, username, password, key_file=None, port=22, conn_timeout=60):
        self.ip = ip
        self.username = username
        self.password = password
        self.key_file = key_file
        self.port = port
        self.conn_timeout = conn_timeout

    @property
    @lock
    @retry(tries=120, delay=5)
    def ssh(self):
        if self._ssh is None or self._ssh.get_transport() is None or not self._ssh.get_transport().is_active():
            logger.info('Init ssh for {0}'.format(self.ip))
            self._ssh = paramiko.SSHClient()
            self._ssh.load_system_host_keys()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                if self.key_file is not None:
                    if self.ip == '10.203.14.41' or self.ip == '10.203.14.175' or self.ip == '10.203.14.163' or self.ip == '10.203.14.7' or \
                            self.ip == '10.203.14.65' or self.ip == '10.203.14.216':
                        self.key_file = '/root/key/oregon-centos-20181008.pem'

                    pkey = paramiko.RSAKey.from_private_key_file(self.key_file)
                    self._ssh.connect(self.ip, self.port, self.username, self.password, timeout=self.conn_timeout,
                                      pkey=pkey)
                else:
                    self._ssh.connect(self.ip, self.port, self.username, self.password, timeout=self.conn_timeout)
            except SSHException as e:
                logger.warning('{ip} ssh session exception occured!'.format(ip=self.ip))
                self._ssh = None
                raise e
            except Exception as e:
                logger.warning('SSH connect {0} fail!'.format(self.ip))
                raise e

        return self._ssh

    @property
    def sftp(self):
        #         if self._sftp is None:
        #             self._sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        self._sftp = self.ssh.open_sftp()

        return self._sftp

    def run_cmd(self, cmd, sudo=False, timeout=None):
        rtn_dict = {}
        if self.key_file is not None:
            self.password = None

        logger.debug('ssh run {cmd} on {ip}'.format(cmd=cmd, ip=self.ip))
        try:
            if sudo and self.password is not None:
                stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True, timeout=timeout)
                stdin.write(self.password + '\n')
                stdin.flush()
            else:
                stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)

            rtn_dict['stdout'] = stdout.read().decode("utf8", "ignore")
            rtn_dict['stderr'] = stderr.read().decode("utf8", "ignore")
            rtn_dict['rc'] = stdout.channel.recv_exit_status()
        except Exception as e:
            logger.warning('Run cmd fail!')
            raise e

        return rtn_dict

    @retry(tries=20, delay=10)
    def remote_scp_put(self, local_path, remote_path):
        """
        scp put --paramiko
        @params:
          (char) host_ip
          (char) remote_path
          (char) local_path
          (char) username
          (char) password
        @output:
          (void)
        """
        logger.debug('scp %s %s@%s:%s' % (local_path, self.username, self.ip, remote_path))

        try:
            self.sftp.put(local_path, remote_path)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        finally:
            self.sftp.close()
            self.ssh.close()

    @retry(tries=20, delay=10)
    def remote_scp_get(self, local_path, remote_path):
        """
        scp put --paramiko
        @params:
          (char) host_ip
          (char) remote_path
          (char) local_path
          (char) username
          (char) password
        @output:
          (void)
        """
        logger.debug('scp %s@%s:%s %s' % (self.username, self.ip, remote_path, local_path))

        try:
            self.sftp.get(remote_path, local_path)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        finally:
            self.sftp.close()
            self.ssh.close()


if __name__ == '__main__':
    ssh_obj = SSHObj('10.25.116.11', 'root', 'password')
    print(ssh_obj.run_cmd('sleep 10', timeout=9))

