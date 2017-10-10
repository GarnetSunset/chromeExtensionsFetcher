from bs4 import BeautifulSoup
from selenium import webdriver
from six.moves.urllib.request import urlretrieve
import os
import socket
import time
import zipfile

owd = os.getcwd()
localappdata = os.getenv('LocalAPPDATA')
dir = localappdata+"\Google\Chrome\User Data\Default\Extensions"
searchURL = "https://chrome.google.com/webstore/search/"

if os.path.isfile(socket.gethostname()+"-extensions.txt"):
    os.remove(socket.gethostname()+"-extensions.txt")

if os.path.isfile('chrome.ini'):
    ini = open('chrome.ini', 'r')
    locationString = ini.read()
elif os.path.isfile('chromedriver.exe'):
    locationString = 'chromedriver.exe'
else:
    response = urlretrieve('https://chromedriver.storage.googleapis.com/2.33/chromedriver_win32.zip','chromedriver.zip')

    zip_ref = zipfile.ZipFile("chromedriver.zip", 'r')
    zip_ref.extractall(owd)
    zip_ref.close

    locationString = 'chromedriver.exe'

driver = webdriver.Chrome(executable_path=(locationString))
driver.set_window_position(4000, 651)
driver.set_page_load_timeout(600)

directory_list = list()
for root, dirs, files in os.walk(dir, topdown=False):
    for name in dirs:
        if len(name) == 32:
            directory_list.append(name)

for x in directory_list:
    driver.get(searchURL+x)
    time.sleep(2)
    requestRec = driver.page_source
    soup = BeautifulSoup(requestRec, 'lxml')
    soup.prettify()
    for tagStuff in soup.find_all('div', {'class': 'a-na-d-w'}):
        names = tagStuff.text
    names = names + "\n"
    text_file = open(socket.gethostname()+"-extensions.txt", "a")
    text_file.write(names)
    text_file.close()

driver.close()
try:
    os.remove("chromedriver.zip")
    print("All Done")
except:
    print("All Done")
