import paramiko
from paramiko import SSHClient
from scp import SCPClient


def transfer():
    ssh = SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target_host = '127.0.0.1'   #replace by address of processing unit
    target_port = 22            # not sure which port number to use

    ssh.connect( hostname = target_host , username = 'Capstones', password = 'AutoGrade' )
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('my_file.txt', 'my_file2.txt') # Copy my_file.txt to the server
        scp.get('my_file2.txt')  # gets the copy of myfile 


REMOTE_HOST_IP = '127.0.0.1'  #replace by address of processing unit
USERNAME = 'autograde'
PASSWORD = 'autograde'

def transfer(source_path, destination_path):
    """Copy remote source_path to local destination_path."""
    ssh = SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target_host = REMOTE_HOST_IP

    ssh.connect(hostname=target_host, username=USERNAME, password=PASSWORD)
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(source_path, destination_path)  # gets the copy of the file
