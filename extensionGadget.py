from bs4 import BeautifulSoup
from selenium import webdriver
from six.moves.urllib.request import urlretrieve
import ctypes, os, re, json, socket, subprocess, sys, time, zipfile

localappdata = os.getenv('LocalAPPDATA')
dir = localappdata+"\Google\Chrome\User Data\Default\Extensions"
dragNDrop = ''.join(sys.argv[1:])
local = False
names = None
owd = os.getcwd()
returnMan = []
searchURL = "https://chrome.google.com/webstore/search/"

if not os.path.exists("Machines"):
    os.makedirs("Machines")

def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if os.path.isfile('chrome.ini'):
    ini = open('chrome.ini', 'r')
    locationString = ini.read()
elif os.path.isfile('chromedriver.exe'):
    locationString = 'chromedriver.exe'
else:
    response = urlretrieve('https://chromedriver.storage.googleapis.com/2.38/chromedriver_win32.zip','chromedriver.zip')

    zip_ref = zipfile.ZipFile("chromedriver.zip", 'r')
    zip_ref.extractall(owd)
    zip_ref.close

    locationString = 'chromedriver.exe'

if dragNDrop == "":
    pass
else:
    directory_list = []
    with open(dragNDrop) as f:
        for line in f:
            line = line.replace('\n', '')
            if len(line) == 32:
                directory_list.append(line)
    extension = dragNDrop.index(".")
    fileName = dragNDrop[:extension]
    open("Machines/" + fileName + "-extensions.txt", 'w').close()

choice = raw_input("1. Your machine or 2. Someone else's?\n>")
if choice == "1" and dragNDrop == "":
    directory_list = list()
    hostnameIP = socket.gethostname()
    open("Machines/" + hostnameIP + "-extensions.txt", 'w').close()
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if len(name) == 32:
                directory_list.append(name)

if choice == "2" and dragNDrop == "":
    hostnameIP = raw_input("Input hostname or IP\n>")
    username = raw_input("Input username\n>")
    open("Machines/" + hostnameIP + "-extensions.txt", 'w').close()
    if admin():
        batcmd = "dir \"\\\\"+hostnameIP+"\c$\Users\\"+username+"\AppData\Local\Google\Chrome\User Data\Default\Extensions\""
        result = subprocess.check_output(batcmd, shell=True)
        directory_list = list()
        while("<DIR>" in result):
            dirLoc = result.find("<DIR>")
            result = result[dirLoc+15:]
            newLine = result.find("\n")
            name = result[:newLine]
            name.rstrip()
            name = name[:-1]
            if len(name) == 32:
                directory_list.append(name)

    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
if choice == "2":
    driver = webdriver.Chrome(executable_path=(locationString))
    driver.set_window_position(4000, 651)
    driver.set_page_load_timeout(600)

    for x in directory_list:
        driver.get(searchURL+x)
        time.sleep(2)
        requestRec = driver.page_source
        soup = BeautifulSoup(requestRec, 'lxml')
        soup.prettify()
        for tagStuff in soup.find_all('div', {'class': 'a-na-d-w'}):
            names = tagStuff.text
            print(tagStuff.text.encode('utf-8'))
        if names == None:
    	       names = "Unknown ID: " + x
        if dragNDrop == "":
            text_file = open("Machines/" + hostnameIP + "-extensions.txt", "a")
        else:
            text_file = open("Machines/" + fileName + "-extensions.txt", "a")
        text_file.write(names.encode('utf-8')+"\n")
        text_file.close()
        names = ""

    driver.close()
else:
    local = True
    for dirpath, subdirs, files in os.walk(dir):
        for x in files:
            if x == "manifest.json":
                with open(dirpath+"\manifest.json") as f:
                    herewego = json.load(f)
                if("__MSG_appName__" != herewego["name"]):
                    if("__MSG_APP_NAME__" != herewego["name"]):
                        if("__MSG_extName__" != herewego["name"]):
                                returnMan.append(herewego["name"])

if os.path.isfile("debug.log"):
    try:
        os.remove("debug.log")
    except:
        print("")

if os.path.isfile("chromedriver.zip"):
    try:
        os.remove("chromedriver.zip")
    except:
        print("")

if dragNDrop == "":
        with open("Machines/" + hostnameIP + "-extensions.txt", 'r') as myfile:
            data=myfile.read().replace('\n\n', '\n')
            data=data.replace('\n\n', '\n')
            myfile.close()
            with open("Machines/" + hostnameIP + "-extensions.txt", 'w') as newfile:
                if(local == True):
                    for x in returnMan:
                        newfile.write(x+"\n")
                else:
                    newfile.write(data)
                newfile.close()
else:
    with open("Machines/" + fileName + "-extensions.txt", 'r') as myfile:
        data=myfile.read().replace('\n\n', '\n')
        data=data.replace('\n\n', '\n')
        myfile.close()
        with open("Machines/" + fileName + "-extensions.txt", 'w') as newfile:
            newfile.write(data)
            newfile.close()

print("All Done")
