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
