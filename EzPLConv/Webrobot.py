from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# Find duration of each song and store it - use this if your file of songs doesn't contain durations
def findDuration():
    browser = webdriver.Firefox()
    f1 = open("songTest.txt")
    songQueue = []
    for x in f1:
        songQueue.append(x)
    f1.close()
    browser.get("https://www.google.com")
    loadDelay = 3
    for song in songQueue:
        searchBar = WebDriverWait(browser,loadDelay).until(EC.presence_of_element_located((By.NAME,"q")))
        searchBar.send_keys(song + " spotify track")
        searchBar.send_keys(Keys.ENTER)
        time.sleep(2)
        browser.find_element(By.XPATH, '(//h3)[1]/../../a').click()
        names = browser.find_elements_by_class_name("tracklist-name ellipsis-one-line")
                         # presence_of_all_elements_located_located((By.CLASS_NAME,"tracklist-name ellipsis-one-line")))
        durations = browser.find_elements_by_tag_name("span")
            #WebDriverWait(browser,loadDelay).until(EC.presence_of_all_elements_located_located((By.TAG_NAME,"span")))

        time.sleep(2)

        for elem in names:
            print(elem.get_attribute("value"))
        time.sleep(2)
        browser.get("https://www.google.com")



# Heuristic for determining which video is most similar to desired song
def goodVid(video):
    return

def main():
    browser = webdriver.Firefox()
    browser.get("https://www.youtube.com")

    f1 = open("songTest.txt", "r")
    songQueue = []

    for x in f1:
        songQueue.append(x)

    f1.close()

    f2 = open("urls.txt", "w")

    loadDelay = 3

    try:
        for song in songQueue:
            searchBar = WebDriverWait(browser,loadDelay).until(EC.presence_of_element_located((By.NAME,"search_query")))
            searchBar.send_keys(song)
            searchBar.send_keys(Keys.ENTER)
            #time.sleep(2)
            video = WebDriverWait(browser,loadDelay)\
            .until(EC.presence_of_element_located((By.CLASS_NAME,"yt-simple-endpoint.style-scope.ytd-video-renderer")))
            url = video.get_attribute("href")
            f2.write(url + "\n")
            #time.sleep(2)
            browser.get("https://www.youtube.com")
    except TimeoutException:
        print("Failure - Loading Took Too Long")

    f2.close()
    browser.quit()

    print("Successful")


if __name__ == "__main__":
    main()