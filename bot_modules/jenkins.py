from util import Util
import jenkins

class JenkinsModule:
    def __call__(self, messenger): #not tested yet!
        event = messenger.event
        if messenger.isEspeciallyForMe() or messenger.isPrivateMessage():
            Util.log_error("IMPLEMENT ME!")
            
    
    def __init__(self):
        config = Util.get_module_config("JenkinsModule")
        self.server=jenkins.Jenkins(config["host"], username=config["username"], password=config["password"])

