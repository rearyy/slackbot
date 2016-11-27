# slackbot
Python slack bot with ssh and jenkins integration. Also has some AI

# First run

1. Ensure, that you have installed all dependencies:
pip install python-jenkins
pip install paramiko
pip install slackclient

2. Configure it:
- main config file is config.json
- AIML files for AIModule goes to localization given in std-startup.xml

3. Run it:
python main.python

# Writing new modules
1. Add new module file to ./bot_modules. Mention it in ./bot_modules/__init__.py 
2. Implement class __call__() method
3. Add its configuration to config.json. Configuration name should be same as class name.
