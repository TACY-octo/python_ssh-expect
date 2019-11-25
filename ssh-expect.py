import sys
import pexpect
import socket 
import csv
from access import accounts

class Host(): 
    def __init__(self, host, port=22): 
        self.host = host

    def check_net(self): 
        '''
            Check network flow 'SSH'
        '''
        try:
            net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            net.settimeout(2)
            net.connect((self.ip, self.port))
            net.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            net.close()

    def check_ssh(self):
        '''
            Check access with ssh 
        '''
        client_ssh = ClientSsh(self.host)
        if client_ssh.test_account() is True: 
            self.ssh_user = client_ssh.ssh_user()
            self.ssh_pass = client_ssh.ssh_pass()



    def set_account(self, ssh_user, ssh_pass):
        '''
            Set user andd pass
        '''
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass 


class ClientSsh():
    def __init__(self, host, port=22):
        self.host = host
        self.port = port

    def test_account(self):
        '''
            Check multiple account
        '''
        for account in accounts: 
            try:
                ssh = pexpect.pxssh.pxssh()
                ssh.login(self.host, account['ssh_user'], account['ssh_pass'])
                ssh.sendline('ls')
                ssh.prompt()
                print(ssh.before)
                self.ssh_user = account['ssh_user']
                self.ssh_pass = account['ssh_pass']
                return True

            except pexpect.pxssh.ExceptionPxssh:
                print("Login failed with {0}".format(account['ssh_user']))
                break
        return 
