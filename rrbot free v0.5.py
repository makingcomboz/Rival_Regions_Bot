import selenium.webdriver.chrome.options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import re
import sys
import datetime

class Botclass():

    def __init__(self):
        self.version = "v0.5"
        self.skillmethodes = ["Strenght","Education","Endurance","Equal"]
        self.BotLoop()
        
        #THis calls all the methodes
    def BotLoop(self):
        self.Ui()
        self.variables()
        self.Driver()
        self.Login(self.loginmethod)
        while True:
            print("Starting Run")
            self.update_account_data()
            self.print_account_data()
            self.go_skill()
            self.update_account_data()
            self.print_account_data()
            self.Pause()

            #UI to get account data and what to skill etc
    def Ui(self):
        print("Hello and Welcome to the RR Bot free version ",self.version)
        print("This is the free version of the RRBot. It only includes Auto Perk/Skill")
        print("Currently only google and facebook are supported as an auto-login-method.")
        print("")
        print("Official Discord of the Bot: https://discord.gg/qU7CW2w")
        print("Join the Discord for support, announcments, new releases and the premium version")
        print("My Telegram username: @lauxenz")
        print('Telegram only for questions around the bot or "business" requests. NOT for Bot Support')
        print("")
        print("")
        print("Now starting with Logging in:")
        self.loginmethod = input('Which Login Method do you use? Type in "g" for google or "f" for facebook or "manual" for manual login')
        if self.loginmethod == ("f" or "F" or "facebook" or "Facebook"):
            self.loginmethod = "facebook"
        elif self.loginmethod == ("g" or "G" or "google" or "Google"):
            self.loginmethod = "google"
        elif self.loginmethod == "manual":
            self.loginmethod == "manual"
        else:
            print("Login Methode not supported or Input is invalid")
            time.sleep(2)
            sys.exit()
        if self.loginmethod != "manual":
            self.username=input("Please type in your username/Email:")
            self.password=input("Please Type in your Password:")
            print("")
            print("Are these correct?")
            print("Login Methode = ", self.loginmethod)
            print("Username = ",self.username)
            print("Password = ",self.password)
            if input("Please type in yes or no") =="yes":
                pass
            else:
                print("Input not valid, resarting")
                time.sleep(2)
                sys.exit()
        else:
            print("Skippping Logindata")
        index = 1
        for x in self.skillmethodes:
            print("["+str(index)+"] | "+str(x))
            index+=1
        x = input("Please type in the number of the skillmethod:")
        self.skillmethod = self.skillmethodes[int(x)-1]
        print("")
        print("Skillmethod =",self.skillmethod)
        print("")
        if input("Do you want to skill fast? (skill with gold): Please type in yes or no") == "yes":
            self.skillfast = True
        else:
            self.skillfast = False

        print("")
        print("")
        print("")
        print("Finished process")
        print("Starting with the Bot")
        return True

    #unnessescary Def to set some variables, may add it into __init__?
    def variables(self):
        print("Setting Variables")
        self.url = "https://rivalregions.com/"

        self.account_data = {
                             "General": {"Level":0, "Energy": 0,"Money": 0, "Gold": 0, "RemainingSkillTime": "00:00"},
                             "Skills":{"Strenght":0,"Education":0,"Endurance":0},
                             }
        return True

    #starting the chromedriver
    def Driver(self):
        print("Initialing Driver")
        chrome_options = selenium.webdriver.chrome.options.Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--no-sandbox')
        #remove headless to see the driver working and to see xpath etc, thn add it so the bot can run without a chrometab open
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.3945.79 Safari/537.36')

        self.driver = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver.exe")
        self.driver.get(self.url)
        return True

        #Login method, loggin into the rivalregions account
        #Google not working, Facebook has to accept cookies i think
    def Login(self, loginmethod):
        print("Starting Login")
        if loginmethod == "google":
            #Press Google
            print("Logging in using google")
            self.driver.find_element_by_xpath('//*[@class="sa_sn float_left imp gogo"]').click()
            time.sleep(5)
            print("Sending Email")
            x = self.driver.find_element_by_xpath('//*[@type="email"]')
            x.send_keys(self.username)
            x.send_keys(Keys.RETURN)
            time.sleep(5)
            print("Sending Password")
            x = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
            x.send_keys(self.password)
            x.send_keys(Keys.RETURN)
            time.sleep(5)
            print("Logged in")
            return True
        elif loginmethod =="facebook":
            print("Logging in using Facebook")
            self.driver.find_element_by_xpath('//*[@id="sa_add2"]/div[2]/a[1]/div').click()
            time.sleep(8)
            print("Sending Email")
            self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(self.username)
            time.sleep(8)
            print("Sending Password")
            self.driver.find_element_by_xpath('//*[@id="pass"]').send_keys(self.password)
            time.sleep(8)
            self.driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
            time.sleep(8)
            print("Logged in")
            return True
        elif loginmethod == "manual":
            print('Please Login with your Login-Data and then type in "start"')
            if input() == "start":
                return True
        else:
            sys.exit()

        #getting all the account information
    def update_account_data(self):
        print("Getting Account Data")
        self.driver.find_element_by_xpath('//*[@id="header_menu"]/div[5]').click()
        time.sleep(6)
        #Genral
        #Level
        x = self.driver.find_element_by_xpath('//*[@id="index_exp_level"]').text
        self.account_data["General"]["Level"] = int(x.replace(".",""))
        #Energy
        x = self.driver.find_element_by_xpath('//*[@id="s_index"]').text
        self.account_data["General"]["Energy"] = int(x)

        #Skills
        #Strenght
        x = self.driver.find_element_by_xpath('//*[@id="index_perks_list"]/div[4]/div[2]').text
        self.account_data["Skills"]["Strenght"] = int(x.replace(".",""))
        #Education
        x = self.driver.find_element_by_xpath('//*[@id="index_perks_list"]/div[5]/div[2]').text
        self.account_data["Skills"]["Education"] = int(x.replace(".",""))
        #Endurance
        x = self.driver.find_element_by_xpath('//*[@id="index_perks_list"]/div[6]/div[2]').text
        self.account_data["Skills"]["Endurance"] = int(x.replace(".",""))
        #Check if currently something is skilling
        try:
            x = self.driver.find_element_by_xpath('//*[@id="perk_counter_2"]').text
            self.account_data["General"]["RemainingSkillTime"] = str(x)
        except:
            self.account_data["General"]["RemainingSkillTime"] = "00:00"

            #just a function to print the account data to the user
    def print_account_data(self):
        print("Account data:")
        print("Skills:",self.account_data["Skills"])
        return True

    #skilling the thing which needs to be skilled
    def go_skill(self):
        if not self.account_data["General"]["RemainingSkillTime"] == "00:00":
            print("Still skilling. Remaining:",self.account_data["General"]["RemainingSkillTime"])
            return False
        print("Refreshing Page (takes 10 seconds)")
        self.driver.refresh()
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="header_menu"]/div[5]').click()
        time.sleep(5)
        if self.skillmethod == "Equal":
            skillmethod = min(self.account_data["Skills"], key=self.account_data["Skills"].get)
        else:
            skillmethod = self.skillmethod
        print("Going to Skill:",skillmethod)
        if skillmethod == "Strenght":
            skillmethod = 1
        elif skillmethod == "Education":
            skillmethod = 2
        elif skillmethod == "Endurance":
            skillmethod = 3
        if self.skillfast:
            way = 2
        else:
            way = 1
        with requests.Session() as s:
            sessid = self.driver.get_cookie("PHPSESSID")
            self.cookie = sessid.get('value', None)
            expires = sessid.get('expiry', None)
            sessid.pop('expiry', None)
            sessid.pop('httpOnly', None)
            sessid['expires'] = expires
            s.cookies.set(**sessid)
            #get cookie
            r = s.get('http://rivalregions.com/#overview')
            lines = r.text.split("\n")
            for line in lines:
                if re.match("(.*)var c_html(.*)", line):
                    c = line.split("'")[-2]

            s.get("https://rivalregions.com/perks/up/"+str(skillmethod)+"/"+str(way)+"?c="+str(c))
            s.close()
        return True

    #getting how long the skilltime is, then merging it into seconds so itll wait untill the slkill is finished to start again
    def Pause(self):

        # how many digits
        zeit = self.account_data["General"]["RemainingSkillTime"]
        ftr = [3600, 60, 1]
        t = sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(zeit.split(":"))))
        self.ti = int(t)
        self.ti+=10

        print("Starting Pausetime, skilling will be finished at around:",datetime.datetime.utcnow() + datetime.timedelta(seconds=int(self.ti)),"Notice: Timezone = UTC, Hours may vary")
        if int(self.ti) > 600:
            self.driver.quit()
            print("Driver wil reopen after finishing the Pausetime")
            time.sleep(int(self.ti))
            self.Driver()
            self.Login(self.loginmethod)
        else:
            time.sleep(int(self.ti))
        return True
Botclass()
