import paramiko
from paramiko import SSHClient
from transfer_file import REMOTE_HOST_IP, USERNAME, PASSWORD


FILE = 'test1'



START_COMMAND = 'cd capstone-ag/autograde; ./our_python autograde_toplevel.py'


ssh = SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(REMOTE_HOST_IP, username=USERNAME, password=PASSWORD)
stdin, stdout, stderr = ssh.exec_command(START_COMMAND)

while True:
    print(stderr.readline())
