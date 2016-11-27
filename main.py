from bot_modules import *
from slackclient import SlackClient
from util import Util


class SlackBot:
    def __init__(self):
        config = Util.get_config()
        self.handlers = self.read_modules_config(config)
        self.slack_client = SlackClient(config["main"]["SLACK_TOKEN"])
        self.slack_user_id = config["main"]["SLACK_USER_ID"]
        self.users = self.list_users()
        self.channels = self.list_channels()
        
    def handle_message(self, messenger):
        if hasattr(messenger, "event"):
            for handler in self.handlers:
                if not messenger.response : handler(messenger)
            
    def read_modules_config(self, config):
        handlers = []
        for module in config["modules"]:
           if module["isOn"]:
              handlers.append(self.get_method_by(module["name"])())
        return handlers
            
    def get_method_by(self, name):
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(name)
        if not method:
           raise NotImplementedError("Method %s not implemented" % name)
        return method;
        
    def send_message(self, channel_id, message):
        self.slack_client.api_call(
            "chat.postMessage",
            as_user="true:",
            channel=channel_id,
            text=message,
            parse="true"
        )
        
    def list_channels(self):
        channel_hashmap = {}
        channels_call = self.slack_client.api_call("channels.list")
        if channels_call.get('ok'):
            Util.log_debug("===CHANNELS===\n" + str(channels_call) + "\n===CHANNELS===")
            for channel in channels_call['channels']:
                channel_hashmap[channel["id"]] = channel["name"]
        return channel_hashmap

    def list_users(self):
        user_hashmap = {}
        users_call = self.slack_client.api_call("users.list")
        if users_call.get('ok'):
            Util.log_debug("===USERS===\n" + str(users_call) + "\n===USERS===")
            for user in users_call['members']:
                user_hashmap[user["id"]] = user["name"]
        return user_hashmap

class Messenger:
    def __init__(self, event, slack_bot):
        self.slack_user_id = slack_bot.slack_user_id
        if not "user" in event or (event["user"] != slack_bot.slack_user_id) :
            self.event = event
            if "channel" in event and event["channel"] in slack_bot.channels : self.event["channel_name"] = slack_bot.channels[event["channel"]]
            if "user" in event : self.event["login"] = slack_bot.users[event["user"]]
        self.response = ""
        
    def isMessage(self):
        return self.event["type"] == "message" and not "subtype" in self.event

    def isFromRandom(self):
        return self.isMessage() and "channel_name" in self.event and self.event["channel_name"] == "random"

    def isPrivateMessage(self):
        return self.isMessage() and "channel_name" not in self.event
  
    def isEspeciallyForMe(self):
        return self.isFromRandom() and self.slack_user_id in event["text"]


if __name__ == '__main__':
    slack_bot = SlackBot()
    if slack_bot.slack_client.rtm_connect():
        while True:
            new_events = slack_bot.slack_client.rtm_read()
            for event in new_events:
               Util.log_debug("Event: " + str(event))
               messenger = Messenger(event, slack_bot)
               slack_bot.handle_message(messenger)
               if messenger.response:
                    slack_bot.send_message(messenger.event["channel"], messenger.response)
    else:
        print("Connection Failed, invalid token?")