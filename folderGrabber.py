from bs4 import BeautifulSoup
from six.moves.urllib.request import urlretrieve
import csv, ctypes, os, re, socket, subprocess, sys, time, zipfile

userfolder = os.getenv('USERNAME')
dldir = "C:\Users\\" + userfolder +"\Downloads"
pfdir = "C:\Program Files"
pfdir86 = "C:\Program Files (x86)"
names = ""
owd = os.getcwd()
dlEnum = 0
pfEnum = 0
pf86Enum = 0
done1 = 0
done2 = 0
done3 = 0

if not os.path.exists("Machines"):
    os.makedirs("Machines")

def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

choice = raw_input("1. Your machine or 2. Someone else's?\n>")

if choice == "2":
    hostnameIP = raw_input("Input hostname or IP\n>")
    username = raw_input("Input username\n>")
else:
    hostnameIP = socket.gethostname()

def makedirlocal(bazinga, choice, dldir, pfdir, pfdir86):
    global directory_list
    directory_list = list()
    dirLoc = 0
    if choice == "1":
        for x in os.listdir(bazinga):
            print(x)
            path = os.path.join(bazinga, x)
            if os.path.isdir(path):
                directory_list.append(x+"/")
            if os.path.isfile(path):
                directory_list.append(x)

    if choice == "2":
        if admin():
            if bazinga == dldir:
                batcmd = "dir \"\\\\" + hostnameIP + "\c$\Users\\" + username + "\Downloads\""
            if bazinga == pfdir:
                batcmd = "dir \"\\\\" + hostnameIP + "\c$\Program Files\""
            if bazinga == pfdir86:
                batcmd = "dir \"\\\\" + hostnameIP + "\c$\Program Files (x86)\""
            result = subprocess.check_output(batcmd, shell=True)
            directory_list = list()
            while(len(result)>30):
                result = result[dirLoc+40:]
                newLine = result.find("\n")
                name = result[:newLine]
                name.rstrip()
                name = name[:-1]
                dirLoc = result.find("\n")
                if len(name) > 2:
                    directory_list.append(name)
                
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        del directory_list[0:2]
        directory_list.sort()
        del directory_list[0:3]


open("Machines/" + hostnameIP + "-dirsnfiles.txt", 'w').close()
open("Machines/" + hostnameIP + "-dirsnfiles.csv", 'w').close()

text_file = open("Machines/" + hostnameIP + "-dirsnfiles.txt", "a")

with open("Machines/" + hostnameIP + "-dirsnfiles.csv", 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    
    text_file.write("------------Downloads------------\n")
    makedirlocal(bazinga=dldir, choice=choice, dldir=dldir, pfdir=pfdir, pfdir86=pfdir86)
    dlList = directory_list
    for x in directory_list:
        names = names + x
        names=names.decode('utf-8','ignore').encode("utf-8")
        text_file.write(names+"\n")
        names = ""

    text_file.write("------------ProgramFiles------------\n")
    makedirlocal(bazinga=pfdir, choice=choice, dldir=dldir, pfdir=pfdir, pfdir86=pfdir86)
    pfList = directory_list
    for x in directory_list:
        names = names + x
        names=names.decode('utf-8','ignore').encode("utf-8")
        text_file.write(names+"\n")
        names = ""
        
    text_file.write("------------ProgramFilesx86------------\n")
    makedirlocal(bazinga=pfdir86, choice=choice, dldir=dldir, pfdir=pfdir, pfdir86=pfdir86)
    for x in directory_list:
        names = names + x
        names=names.decode('utf-8','ignore').encode("utf-8")
        text_file.write(names+"\n")
        names = ""
    wr.writerow(['Downloads', 'ProgramFiles', 'ProgramFilesx86'])
    dlLength = len(dlList)
    pfLength = len(pfList)
    pf86Length = len(directory_list)
    while(done1 != 1 or done2 != 1 or done3 != 1):
        wr.writerow([dlList[dlEnum],pfList[pfEnum],directory_list[pf86Enum]])
        dlEnum += 1
        pfEnum += 1
        pf86Enum += 1
        if(dlEnum == dlLength):
            dlList = [""]
            dlEnum = 0
            dlLength = 1
            done1 = 1
        if(pfEnum == pfLength):
            pfList = [""]
            pfEnum = 0
            pfLength = 1
            done2 = 1
        if(pf86Enum == pf86Length):
            directory_list = [""]
            pf86Enum = 0
            pf86Length = 1
            done3 = 1
        

text_file.close()

with open("Machines/" + hostnameIP + "-dirsnfiles.txt", 'r') as myfile:
        data=myfile.read().replace('\n\n', '\n')
        data=data.replace('\n\n', '\n')
        myfile.close()
        with open("Machines/" + hostnameIP + "-dirsnfiles.txt", 'w') as newfile:
            newfile.write(data)
            newfile.close()

print("All Done")
