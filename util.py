import os, logging, json

CONFIG_FILE = 'config.json'

class Util:
    config = {}
    with open(CONFIG_FILE) as config_file:    
            config = json.load(config_file)
    logging.basicConfig(filename='log/bot.log', format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    
    
    def log_debug(message):
        logging.debug(message)
        
    def log_info(message):
        logging.info(message);
        
    def log_error(message):
        logging.error(message);
        
    def get_module_config(module):
        configurations = Util.get_modules_config()
        for conf in configurations :
            if conf["name"] == module : return conf
        return None
        
    def get_config():
        return Util.config
        
    def get_modules_config():
        return Util.config["modules"]