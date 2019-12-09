import sys
import pexpect
import socket
import csv
from pykeepass import PyKeePass
from getpass import getpass


# Init vars 
sep = '\n===================================================\n'

# Class 
class Host():
    ''' 
        Instance host 
    '''

    def __init__(self, host, users_ssh, port=22):
        self.host = host
        self.users_ssh = users_ssh
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

        client_ssh = ClientSsh(self.host, self.users_ssh)
        if client_ssh.test_account() is True:
            self.set_account(client_ssh.ssh_user(),client_ssh.ssh_pass())
            return True
        else: 
            return False

    def set_account(self, ssh_user, ssh_pass):
        '''
            Set user and pass
        '''
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass
    
    def get_account(self):
        '''
            Get user and pass 
        '''

        return self.ssh_user, self.ssh_pass


class ClientSsh():
    '''
        Instance SSH
    '''
    def __init__(self, host, users_ssh, port=22):
        self.host = host
        self.port = port
        self.users_ssh = users_ssh

    def test_account(self):
        '''
            Check multiple account
        '''
        for account in self.users_ssh.listuser:
            i = 0
            keepass_finduser = self.users_ssh.db.find_entries(username=account)
            while i < len(keepass_finduser):
                try:
                    ssh = pexpect.pxssh.pxssh()
                    ssh.login(self.host, keepass_finduser[i].username, keepass_finduser[i].password)
                    ssh.sendline('ls')
                    ssh.prompt()
                    print(ssh.before)
                    self.ssh_user = keepass_finduser[i].username
                    self.ssh_pass = keepass_finduser[i].password
                    return True

                except pexpect.pxssh.ExceptionPxssh:
                    print("Login failed with {0}".format(account['ssh_user']))
                    break

class Keepass:
    '''
        Instance keepass base
    '''

    def __init__(self):
        self.path = input('Emplacement du fichier keepass : ')
        self.password = getpass('Mot de passe du fichier keepass : ')

    def init_kpdb(self):
        '''
            init vars for Keepass
        '''

        self.listuser = []
        self.searchuser = []
        nb_user = int(input('Combien de compte à rechercher ? : '))
        i = 0
        while i < nb_user:
            '''
                Create a list user 
            '''

            user = input('Renseigner le nom de votre utilisateur : ')
            self.searchuser.append(user)
            i += 1 
        try: 
            ''' 
                Check and add user to list 
            '''

            self.db = PyKeePass(self.path, password=self.password)
            for user in self.searchuser:
                print('Recherche dans la base l\'utilisateur : {0}'.format(user))
                if self.db.find_entries(username=user, first=True):
                    self.listuser.append(user)
                    print('L\'utilisateur : {0} a été ajouté à la liste !'.format)
                else: 
                    print('L\'utilisateur : {0} n\'a pas été trouvé !'.format(user))
        except FileNotFoundError: 
            print('Le fichier n\'a pas été trouvé !')

class InventoryCSV:
    '''
        Instance file CSV
    '''
    def __init__(self):
       self.file = input('Renseigner le fichier CSV à utilister : ')
       with open(self.file, 'r') as csvfile:
           reader = csv.reader(csvfile, delimiter=";")
           self.content = list(reader)


def main():
    '''
        main program
    '''
    print(sep)
    inventaire = InventoryCSV()
    print(sep)
    users_ssh = Keepass()
    users_ssh.init_kpdb()
    print(sep)
    for line in inventaire.content:
        i = 0 
        while i < len(line):
            host = Host(line[i], users_ssh)
            host.check_net()
            host.check_ssh()
    print(sep)

main()
