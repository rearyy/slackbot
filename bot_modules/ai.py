import aiml
import os, logging, json
from util import Util


class AIModule:
    def __call__(self, messenger): #dac ifa na warunek
        event = messenger.event
        if messenger.isEspeciallyForMe() or messenger.isPrivateMessage():
            message = event["text"].replace(self.pretty_slack_user_id, "").replace("  "," ").strip()
            messenger.response = self.kernel.respond(message, event["channel"])
            Util.log_info(event["login"] + "  told: " + event["text"])
            Util.log_info("Bot respond to user "+ event["login"] + " this: "+ messenger.response)
    
    def __init__(self):
        self.kernel = aiml.Kernel()
        if os.path.isfile("bot_brain.brn"):
            self.kernel.bootstrap(brainFile = "bot_brain.brn")
        else:
            self.kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
            self.kernel.saveBrain("bot_brain.brn")
        config = Util.get_config()
        self.pretty_slack_user_id = '<@' + config["main"]["SLACK_USER_ID"] + '>'
