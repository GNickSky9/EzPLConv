from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()
browser.get("https://www.youtube.com")

f1 = open("/Users/g9/Desktop/songTest.txt", "r")
songQueue = []

for x in f1:
    songQueue.append(x)

f1.close()

f2 = open("/Users/g9/Desktop/urls.txt", "w")

for song in songQueue:
    searchBar = browser.find_element_by_name("search_query")
    searchBar.send_keys(song)
    searchBar.send_keys(Keys.ENTER)
    time.sleep(2)
    video = browser.find_element_by_class_name("yt-simple-endpoint.style-scope.ytd-video-renderer")
    url = video.get_attribute("href")
    f2.write(url + "\n")
    time.sleep(2)
    browser.get("https://www.youtube.com")


f2.close()



