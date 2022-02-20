from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from pathlib import Path
from plyer import notification
import os
# from amazonses import sendEmail

#setup webdriver
driver = webdriver.Chrome(executable_path='./chromedriver')

#dont want to give up if element not immediatnly avaialble
driver.implicitly_wait(10)

driver.get('https://dumpor.com/v/rachaelsmathew/followers/')
if driver.current_url != 'https://dumpor.com/v/rachaelsmathew/followers/':
    print("Not on correct URL")
    driver.implicitly_wait(1)
    driver.get("https://dumpor.com/v/rachaelsmathew/followers/")
    
driver.implicitly_wait(4)

instagram_count = driver.find_elements(By.XPATH, "//a[@href='https://dumpor.com/v/rachaelsmathew/followers']")[0].text

#scroll to bottom of page
SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
element = driver.find_element_by_xpath("//div[@class='spinner']")
print(element.get_attribute('style')=="")

start_time = time.time()
while True:
    
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    
    if driver.find_element_by_xpath("//div[@class='spinner']").get_attribute('style') != "":
        break
    end_time = time.time()
    if end_time - start_time > 20:
        break




print(element.get_attribute('style')=="")
    
followers = []
#get username
followers = driver.find_elements(By.XPATH, "//div[@class='media-body']//h6")
print(instagram_count)
print("My folllowers")
for follower in followers:
    print(follower.text)

#create currentFollowers.txt file if not exist
currentFollowers = Path('currentFollowers.txt')
currentFollowers.touch(exist_ok=True)
f = open(currentFollowers)

#erase all contents of currentFollowers file
file = open("currentFollowers.txt","r+")
file.truncate(0)
file.close()

#append to currentFollowers file
file = open("currentFollowers.txt", "a")  # append mode
for follower in followers:
    file.write(follower.text+"\n")
file.close()

followersLost = []
#see what followers I have lost
currentFollowers = open("currentFollowers.txt", "r")
readCurrent = currentFollowers.read()

with open("oldFollowers.txt", "r") as old_file:
  for line in old_file:
    stripped_line = line.strip()
    # checking condition for string found or not
    if stripped_line not in readCurrent:
        print(stripped_line , 'Unfollowed You')
        followersLost.append(stripped_line)

# closing a file
currentFollowers.close()

if len(followersLost) == 0:
    notification.notify(title = "No one has unfollowed", message= "guess ur not a loser.", app_icon=None, timeout= 10, toast=False)
    
followersLost_noDup = []
for i in followersLost:
    if i not in followersLost_noDup:
            followersLost_noDup.append(i)
        
for follower in followersLost_noDup:
    print(follower)
    notification.notify(title = follower, message= "UNFOLLOWED YOU", app_icon=None, timeout= 10, toast=False)
    time.sleep(2)
    
#send email if lost followers
#if len(followersLost_noDup) != 0:
    #subprocess.run(["./ses-script.sh", ""], shell=True)
    #sendEmail(followersLost_noDup)
    
#remove old followers
os.remove("oldFollowers.txt")
#rename new followers to old
os.rename("currentFollowers.txt", "oldFollowers.txt")
