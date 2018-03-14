from bs4 import BeautifulSoup
from six.moves.urllib.request import urlretrieve
import ctypes, os, re, socket, subprocess, sys, time, zipfile

userfolder = os.getenv('USERPROFILE')
dldir = userfolder+"\Downloads"
pfdir = "C:\Program Files"
pfdir86 = "C:\Program Files (x86)"
names = ""
owd = os.getcwd()
hostnameIP = socket.gethostname()

if not os.path.exists("Machines"):
    os.makedirs("Machines")

def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

choice = raw_input("1. Your machine or 2. Someone else's?\n>")

def makedirlocal(bazinga, choice, dldir, hostnameIP):
    global directory_list
    if choice == "1":
        directory_list = list()
        for x in os.listdir(bazinga):
            path = os.path.join(bazinga, x)
            if os.path.isdir(path):
                directory_list.append(x+"/")
            if os.path.isfile(path):
                directory_list.append(x)

if choice == "2":
    hostnameIP = raw_input("Input hostname or IP\n>")
    username = raw_input("Input username\n>")
    if admin():
        batcmd = "dir \"\\\\"+hostnameIP+"\c$\Users\\"+username+"\Downloads\""
        result = subprocess.check_output(batcmd, shell=True)
        directory_list = list()
        while("<DIR>" in result):
            dirLoc = result.find("\n")
            result = result[dirLoc+40:]
            newLine = result.find("\n")
            name = result[:newLine]
            name.rstrip()
            name = name[:-1]
            if len(name) > 2:
                directory_list.append(name)
            
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

open("Machines/" + hostnameIP + "-dirsnfiles.txt", 'w').close()

text_file = open("Machines/" + hostnameIP + "-dirsnfiles.txt", "a")

text_file.write("------------Downloads------------\n")

makedirlocal(bazinga=dldir, choice=choice, dldir=dldir, hostnameIP=hostnameIP)
directory_list.sort()
for x in directory_list:
    names = names + x
    text_file.write(names.encode('utf-8')+"\n")
    names = ""

text_file.write("------------ProgramFiles------------\n")

makedirlocal(bazinga=pfdir, choice=choice, dldir=dldir, hostnameIP=hostnameIP)
directory_list.sort()
for x in directory_list:
    names = names + x
    text_file.write(names.encode('utf-8')+"\n")
    names = ""
    
text_file.write("------------ProgramFilesx86------------\n")

makedirlocal(bazinga=pfdir86, choice=choice, dldir=dldir, hostnameIP=hostnameIP)
directory_list.sort()
for x in directory_list:
    names = names + x
    text_file.write(names.encode('utf-8')+"\n")
    names = ""

text_file.close()

with open("Machines/" + hostnameIP + "-dirsnfiles.txt", 'r') as myfile:
        data=myfile.read().replace('\n\n', '\n')
        data=data.replace('\n\n', '\n')
        myfile.close()
        with open("Machines/" + hostnameIP + "-dirsnfiles.txt", 'w') as newfile:
            newfile.write(data)
            newfile.close()

print("All Done")
