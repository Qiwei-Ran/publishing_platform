#!/usr/bin/env python
# -*- coding:utf-8 -*-

from paramiko import SSHClient, AutoAddPolicy, RSAKey
from scp import SCPClient


# noinspection SpellCheckingInspection
def push_war(war_location, target_address, purpose_directory, user='root', key_location='/root/.ssh/id_rsa'):
    """
    this is a function of translation .war file through scp and paramiko.
    """
    private_key = RSAKey.from_private_key_file(key_location)
    if not war_location[-4:] == '.war':
        return None

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    try:
        ssh.connect(hostname=target_address, username=user, pkey=private_key)
        # scp use the ssh session
        scp = SCPClient(ssh.get_transport())
    except Exception as e:
        ssh.close()
        raise e
    else:
        scp.put(war_location, purpose_directory)
        scp.close()
        ssh.close()
        return True


'''
if __name__ == '__main__':
    # key_place = '/home/super/.ssh/id_rsa'
    push_war('/root/test.war', '2.2.2.102', '/root', 'root',)
'''
