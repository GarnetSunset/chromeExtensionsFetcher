from bs4 import BeautifulSoup
from selenium import webdriver
from six.moves.urllib.request import urlretrieve
import os
import socket
import sys
import time
import zipfile

localappdata = os.getenv('LocalAPPDATA')
dir = localappdata+"\Google\Chrome\User Data\Default\Extensions"
dragNDrop = ''.join(sys.argv[1:])
names = None
owd = os.getcwd()
searchURL = "https://chrome.google.com/webstore/search/"

if os.path.isfile('chrome.ini'):
    ini = open('chrome.ini', 'r')
    locationString = ini.read()
elif os.path.isfile('chromedriver.exe'):
    locationString = 'chromedriver.exe'
else:
    response = urlretrieve('https://chromedriver.storage.googleapis.com/2.35/chromedriver_win32.zip','chromedriver.zip')

    zip_ref = zipfile.ZipFile("chromedriver.zip", 'r')
    zip_ref.extractall(owd)
    zip_ref.close

    locationString = 'chromedriver.exe'

if dragNDrop == "":
    directory_list = list()
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in dirs:
            if len(name) == 32:
                directory_list.append(name)
else:
    directory_list = []
    with open(dragNDrop) as f:
        for line in f:
            line = line.replace('\n', '')
            if len(line) == 32:
                directory_list.append(line)
    extension = dragNDrop.index(".")
    fileName = dragNDrop[:extension]

if os.path.isfile(socket.gethostname()+"-extensions.txt") and dragNDrop == "":
    os.remove(socket.gethostname()+"-extensions.txt")
if dragNDrop != "":
    os.remove(fileName+"-extensions.txt")

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
    if names == None:
	names = "Unknown ID: " + x
    names = names + "\n"
    if dragNDrop == "":
        text_file = open(socket.gethostname()+"-extensions.txt", "a")
    else:
        text_file = open(fileName+"-extensions.txt", "a")
    text_file.write(names)
    text_file.close()

driver.close()

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

print("All Done")
