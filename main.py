import time
from selenium import webdriver
import requests
import json
import sys
import os
import stdiomask

clear = lambda:os.system("cls")

# You can download the chrome driver from https://chromedriver.chromium.org/
# Example: "D:\Programming\chromedriver.exe"
SPATH = ""

clear()

username = ""
password = ""

class colors():
    reset = '\033[0m'
    green = '\033[92m'
    red = '\033[91m'
    cyan = '\033[96m'
    yellow = '\033[93m'

print(f"Stripcode auto answer made by {colors.green}cytmean{colors.reset}.")

if username == "":
    print(f"{colors.yellow}Github username was not found in the file. If you don't want to write in your username every time please put your username into the \"usearname\" variable.{colors.reset}")
    username = input("Username:")
if password == "":
    print(f"{colors.yellow}Github password was not found in the file. If you don't want to write in your password every time please put your password into the \"password\" variable.{colors.reset}")
    password = stdiomask.getpass("Password:", "*")

try:
    driver = webdriver.Chrome(SPATH)
except:
    sys.exit(f"{colors.red}Chromedriver was not found. Please download it from https://chromedriver.chromium.org/ and change the path to the driver in the code.{colors.reset}")
print("\nAccessing page...")
driver.get("https://stripcode.dev/ranked")
print("\nLogging in with GitHub...")
driver.find_element_by_xpath('//*[@id="login_field"]').send_keys(username)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="login"]/div[3]/form/input[14]').click()

time.sleep(1)
b1xpath = '/html/body/div/div/div/div[2]/div[1]/div[2]/button'
b2xpath = '/html/body/div/div/div/div[2]/div[1]/div[3]/button'
b3xpath = '/html/body/div/div/div/div[2]/div[1]/div[4]/button'
b4xpath = '/html/body/div/div/div/div[2]/div[1]/div[5]/button'
b5xpath = '/html/body/div/div/div/div[2]/div[1]/div[6]/button'
titlexpath = '/html/body/div/div/div/div[2]/div[2]/h1'
nextquestion = '/html/body/div/div/div/div[2]/div[1]/button'

time.sleep(2.5)
try:
    driver.find_element_by_xpath("/html/body/div[4]/main/div/div[2]/div[1]/div[2]/div[1]/form/div/button[2]").click()
except:
    pass

time.sleep(2)

try:
    driver.find_element_by_xpath(titlexpath)
except:
    sys.exit(f"{colors.red}The credentials are probably wrong!{colors.reset}")

print(f"{colors.green}Succesfully logged in!{colors.reset}")


while True:
    print("")
    time.sleep(1.5)
    button1 = driver.find_element_by_xpath(b1xpath + "/span[1]").text
    button2 = driver.find_element_by_xpath(b2xpath + "/span[1]").text
    button3 = driver.find_element_by_xpath(b3xpath + "/span[1]").text
    button4 = driver.find_element_by_xpath(b4xpath + "/span[1]").text
    button5 = driver.find_element_by_xpath(b5xpath + "/span[1]").text
    title = driver.find_element_by_xpath(titlexpath).text

    def searchinrepo(repo, name: str):
        name.replace(" ", "%20")
        print(f"\n{colors.cyan}Trying to find \"{name}\" in {repo}{colors.reset}")
        response = requests.get(f"https://api.github.com/search/code?q=repo:{repo}+filename:{name}")
        response = response.json()

        try:
            if response["documentation_url"] == "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting":
                print(f"{colors.yellow}\nGot rate limited while trying to find {name} in {repo}! Waiting for 150 seconds.{colors.reset}")
                time.sleep(150)
                ratelimited = True
                while ratelimited:
                    try:
                        if response["documentation_url"] == "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting":
                            print(f"{colors.yellow}\nGot rate limited again while trying to find {name} in {repo}! Waiting for another 150 seconds.{colors.reset}")
                            time.sleep(150)
                        else:
                            ratelimited = False
                    except:
                        ratelimited = False
        except:
            pass
        
        try:
            if response["total_count"] > 0:
                time.sleep(6)
                print(f"\n{colors.green}Found \"{name}\" in {repo}!{colors.reset}")
                return True
            else:
                time.sleep(6)
                print(f"\n{colors.red}\"{name}\" is not in {repo}.{colors.reset}")
                return False
        except:
            time.sleep(1)
            return False

    print(f"{colors.green}\nNext question: file title:{title}{colors.reset}")
    print(f"{colors.green}Possible answers: \"{button1}\", \"{button2}\", \"{button3}\", \"{button4}\", \"{button5}\"{colors.reset}")

    if searchinrepo(button1, title):
        driver.find_element_by_xpath(b1xpath).click()

    elif searchinrepo(button2, title):
        driver.find_element_by_xpath(b2xpath).click()

    elif searchinrepo(button3, title):
        driver.find_element_by_xpath(b3xpath).click()

    elif searchinrepo(button4, title):
        driver.find_element_by_xpath(b4xpath).click()

    elif searchinrepo(button5, title):
        driver.find_element_by_xpath(b5xpath).click()

    else:
        print(f"\n{colors.yellow}{title} was not found, picking the first one.{colors.reset}")
        driver.find_element_by_xpath(b1xpath).click()

    print(f"\n{colors.green}Going to next question in 1 second!{colors.reset}")
    time.sleep(1)
    try:
        driver.find_element_by_xpath(nextquestion).click()
    except:
        print(f"{colors.yellow}The next question button was not found. Retrying in 5 seconds.{colors.reset}")
        time.sleep(5)
        try:
            driver.find_element_by_xpath(nextquestion).click()
            print(f"{colors.green}The next question button was found! Going to the next question.{colors.reset}")
        except:
            print(f"{colors.yellow}The next question button was not found. Retrying to pick the right answer.{colors.reset}")