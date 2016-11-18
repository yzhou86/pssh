#!/usr/bin/env python2.7

import sys
import pexpect
import os
from os.path import expanduser

sys.path.append("")
_CONFIG_FILE_ = expanduser("~")+"/.pssh_config"
os.system("touch "+_CONFIG_FILE_)
_ACTION_LIST_ = ["add", "remove", "list"]

class ssh_item :
    hostip = ""
    port = "22"
    user = ""
    password = ""
    name = ""

    def __init__(self, list):
        self.hostip = list[0].strip()
        self.port = list[1].strip()
        self.user = list[2].strip()
        self.password = list[3].strip().replace("\n","")
        if (len(list) > 4):
            self.name = list[4].strip().replace("\n","")
        else :
            self.name = list[0].strip()

    def toLine(self):
        return self.hostip+","+self.port+","+self.user+","+self.password+","+self.name

    def display(self):
        return self.hostip+","+self.port+","+self.user+",******,"+self.name


def saveConfig(data) :
    if not os.path.exists(_CONFIG_FILE_) :
        print "config file not exist, will create it"
        open(_CONFIG_FILE_, 'a').close()
    file = open(_CONFIG_FILE_, "w+")
    for oneItem in data :
        oneItemLine = oneItem.toLine()
        file.write(oneItemLine+"\n")
    file.close()

def loadConfig() :
    configList = []
    with open(_CONFIG_FILE_) as data_file:
        lines = data_file.readlines()
        for line in lines :
            list = line.split(",")
            data = ssh_item(list)
            configList.append(data)
        data_file.close()

    return configList

def list() :
    config_data = loadConfig()
    for item in config_data :
        print item.display()

def new(args) :
    config_data = loadConfig()
    item = ssh_item(args)
    for one in config_data :
        if one.hostip == item.hostip :
            return None
    config_data.append(item)
    saveConfig(config_data)

def remove(hostip) :
    config_data = loadConfig()
    new_config = []
    for one in config_data:
        if one.hostip != hostip:
            new_config.append(one)
    saveConfig(new_config)

def connect(key) :
    config_data = loadConfig()
    for one in config_data:
        if one.hostip == key or one.name == key:
            ssh_connect(one)

def ssh_connect(server) :
    child = pexpect.spawn("ssh -p "+server.port+" "+server.user+"@"+server.hostip)
    index = child.expect(['password:', 'continue connecting (yes/no)?', pexpect.EOF, pexpect.TIMEOUT])
    if index == 0:
        child.sendline(server.password)
        child.interact()
    elif index == 1:
        child.sendline('yes')
        child.expect(['password:'])
        child.sendline(server.password)
        child.interact()
    elif index == 2:
        print "error"
        child.close()
    elif index == 3:
        print "timeout"

def printUsage():
    print """
        ########################################################################################
        ####################################### Usage  #########################################
        pssh.py add [hostname or ip] [port] [user] [password] [tag or alias]
        pssh.py add 10.224.243.20 22 root Slim2012 200
        pssh.py remove 10.224.243.20
        pssh.py list
        pssh.py 10.224.243.20
        pssh.py 200
        ########################################################################################
    """
def __main__(args) :

    if (len(args) < 2) :
        printUsage()
        exit(0)
    action = args[1]

    if action == "help" :
        printUsage()
        exit(0)

    if action not in _ACTION_LIST_ :
        connect(action)

    if (action == _ACTION_LIST_[0]) :
        new(args[2:])

    if (action == _ACTION_LIST_[1]):
        remove(args[2])

    if (action == _ACTION_LIST_[2]):
        list()

__main__(sys.argv)
