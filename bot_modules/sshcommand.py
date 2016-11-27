from util import Util
from os import walk
import paramiko
import re

class SSHCommandModule:
    def __call__(self, messenger):
        event = messenger.event
        if messenger.isEspeciallyForMe() or messenger.isPrivateMessage():
            commands = self.get_availible_commands()
            for command in commands :
                if(re.match(self.pretty_command(command), event["text"], re.I)):
                        command_value = open(self.command_folder + command, 'r').read()
                        self.exec_command(command_value)
                        messenger.response = "Done."
    
    def __init__(self):
        config = Util.get_module_config("SSHCommandModule")
        self.host = config["host"]
        self.username = config["username"]
        self.password = config["password"]
        self.command_folder = config["command_folder"]
    
    def get_availible_commands(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.command_folder):
            Util.log_debug("Commands found: "+ str(filenames))
            f.extend(filenames)
            break
        return f
        
    def pretty_command(self, command):
        match_all = "(.*)"
        return match_all + command.replace(" ", match_all) + match_all
        
    def exec_command(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        try:
            Util.log_info("Creating ssh connection for host: "+ self.host + " user: " + self.username)
            ssh.connect(self.host, username=self.username, password=self.password)
            ssh.exec_command(command)
            #yield ssh
        finally:
            Util.log_info("Closing ssh connection...")
            ssh.close()
