from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

import httplib2

from apiclient import discovery
from oauth2client.file import Storage

import pandas as pd

#import num2words
#from num2words import num2words

import requests, json
import os, time, platform, sys
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def getContacts():
	Contacts_file_name= [file for file in os.listdir(os.curdir)
							 if file.endswith(".csv")]

	Contacts_file_path= os.path.join(dir_path, Contacts_file_name[0])  

	return Contacts_file_path

def getImage():
	Image_file_name= [file for file in os.listdir( os.curdir ) 
						if file.endswith((".jpg", ".png", ".mp4"))]
	if len(Image_file_name)>0:
		Image_file_path= os.path.join(dir_path, Image_file_name[0])
		return Image_file_path
	else:
		return None

def getDoc():
	Doc_file_name= [file for file in os.listdir( os.curdir ) 
						if file.endswith((".doc", ".pdf"))]
	if len(Doc_file_name)>0:
		Doc_file_path= os.path.join(dir_path, Doc_file_name[0])
		return Doc_file_path
	else:
		return None

def getChromeDriverPath():
    chrome_path= dir_path + "\Support\chromedriver.exe"  
    return chrome_path


class Whatsapp:
    whatsAppWeb = 'http://web.whatsapp.com'
    userSearchBoxXpath = '//*[@id="side"]/div[2]/div/label/input'
    resultXpath = '//*[@id="pane-side"]/div/div/div/div[2]/div/div/div[2]/div/div/span'
    resultCsspath = '#pane-side > div > div > div > div:nth-child(2) > div > div > div.chat-body > div > div > span'

    submitButtonXpath = '//*[@id="app"]/div/div[3]/div[1]/span[2]/span/div/div[2]/div[2]/span/div/button'

    def launchChrome(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option("excludeSwitches", ['ignore-certificate-errors'])
        self.driver = webdriver.Chrome(executable_path= getChromeDriverPath(), chrome_options=chromeOptions)
        self.driver.maximize_window()

    def openUrl(self):
        self.driver.get(self.whatsAppWeb)
        
    def read_csv(self):
        self.contacts= pd.read_csv(getContacts())
    
    
    def read_contacts(self, n):
        #self.Proprietor_name= self.contacts["Proprietor_Name"][n]
        #self.Amount = self.contacts["Pre-Approved Amount"][n]
        self.Contact_name= str(self.contacts["Contact Name"][n])
        self.Message= self.contacts["Message"][n]

    def selectUser(self):
        try:
        	time.sleep(0.5)
        	WebDriverWait(self.driver, 8).until(
        		expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, self.resultCsspath)))
        	WebDriverWait(self.driver, 8).until(
                expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, self.resultCsspath))).click()
        except TimeoutException:
        	time.sleep(0.5)
        	WebDriverWait(self.driver, 8).until(
               expected_conditions.visibility_of_element_located((By.XPATH, self.resultXpath)))
        	WebDriverWait(self.driver, 8).until(
               expected_conditions.element_to_be_clickable((By.XPATH, self.resultXpath))).click()
           
    def openUser(self):
        WebDriverWait(self.driver, 100).until(
            expected_conditions.visibility_of_element_located((By.XPATH, self.userSearchBoxXpath)))
        userSearchBox = self.driver.find_element_by_xpath(self.userSearchBoxXpath)
        userSearchBox.click()
        userSearchBox.clear()

        userSearchBox.send_keys(self.Contact_name)

        return self.selectUser()
            
            
    def quit(self):
        self.driver.quit()

    def sendMessage(self):
        
        try:
            messageXpath = '//*[@id="main"]/footer/div[1]/div/div/div[2]'
            submitButtonXpath = '//*[@id="main"]/footer/div[1]/button[2]'
            WebDriverWait(self.driver, 100).until(
                expected_conditions.visibility_of_element_located((By.XPATH, messageXpath)))
            messageBox = self.driver.find_element_by_xpath(messageXpath)
            messageBox.clear()
            lines = self.Message.split("$")
            for line in lines:
            	messageBox.send_keys(line)
            	messageBox.send_keys(Keys.SHIFT+ Keys.ENTER)
            '''
            messageBox.send_keys("Hello, ")
            messageBox.send_keys(self.Proprietor_name)
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys("Greetings from *Indifi*")
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys("We are the *lending partner of TBO*")
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys("We provide working capital facility(OD/Term Loan).")
            messageBox.send_keys("TBO has given your reference.")
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys("You have a pre-approved offer of about *")
            messageBox.send_keys(num2words(self.Amount, lang='en_IN'))
            messageBox.send_keys("* from us.")
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys("*Reply Yes if interested*")
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys("Our team will get back to you")
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys(Keys.SHIFT, Keys.ENTER)
            messageBox.send_keys("Team Indifi")
            '''
            messageBox.send_keys(Keys.ENTER)
        
        except Exception as e:
            print(e)

        
    def send_image(self):
        submitButton_path1 = "div.pane-chat-controls>div.menu>div.menu-item"
        submitButton_path2= "span>div>div.menu-icons>ul>li"
        send_image_path= ('#app > div > div > div.drawer-manager > span.pane.pane-two > div >'
        	' span > div > div > div.drawer-body > span:nth-child(3) > div > button')
        
        try:
            WebDriverWait(ws.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.ID, "main")))
            Button1 = ws.driver.find_elements_by_css_selector(submitButton_path1)
            Button1[1].click()
            ws.driver.execute_script("arguments[0].setAttribute('class', 'menu-item active')", Button1[1])
            Button2 = Button1[1].find_elements_by_css_selector(submitButton_path2)
            elem= Button2[0].find_element_by_css_selector("input")
            elem.send_keys(getImage())
            WebDriverWait(ws.driver, 100).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, send_image_path)))
            Button3= ws.driver.find_element_by_css_selector(send_image_path)
            Button3.click()
        
        except Exception as e:
            print(e)

    def send_doc(self):
        submitButton_path1 = "div.pane-chat-controls>div.menu>div.menu-item"
        submitButton_path2= "span>div>div.menu-icons>ul>li"
        send_doc_path= ('#app > div > div > div.drawer-manager > span.pane.pane-two > div >'
        	' span > div > div > div.drawer-body > span:nth-child(3) > div > button')
        
        try:
            WebDriverWait(ws.driver, 10).until(
            expected_conditions.visibility_of_element_located((By.ID, "main")))
            Button1 = ws.driver.find_elements_by_css_selector(submitButton_path1)
            Button1[1].click()
            ws.driver.execute_script("arguments[0].setAttribute('class', 'menu-item active')", Button1[1])
            Button2 = Button1[1].find_elements_by_css_selector(submitButton_path2)
            elem= Button2[2].find_element_by_css_selector("input")
            elem.send_keys(getDoc())
            WebDriverWait(ws.driver, 100).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, send_image_path)))
            Button3= ws.driver.find_element_by_css_selector(send_doc_path)
            Button3.click()
        
        except Exception as e:
            print(e)


def getCredentials():
	support_dir= os.path.join(dir_path, "Support")
	credential_dir= os.path.join(support_dir, '.credentials')

	credential_path= os.path.join(credential_dir,
	    	                               'sheets.googleapis.com-idifi.json')
	print(credential_path)
	
	store= Storage(credential_path)
	credentials= store.get()
	
	return credentials  


def get_name():
	y= input("name and teamc: ")
	return y


def Sheets(temp):
	credentials= getCredentials()
	http= credentials.authorize(httplib2.Http())
	discoveryUrl= ('https://sheets.googleapis.com/$discovery/rest?'
		'version=v4')
	service= discovery.build('sheets', 'v4', http=http,
    	                        discoveryServiceUrl=discoveryUrl)
	
	spreadsheetID= "1vrRX_jeBdVjnSqZIA7rWzXt09ZAcYxj8bmdR-_r8yC0"
	rangeName = "Sheet1"
	values= [ 
		temp["Contact Name"].tolist(),
		temp["Phone Number"].tolist(),
		temp["status"].tolist(),			
		pd.Series(get_name() for n in range(0, len(temp))).tolist()
	]
	
	body={
	"majorDimension": "COLUMNS",
	"values":values
	}

	result = service.spreadsheets().values().append(
		spreadsheetId=spreadsheetID, range=rangeName,
		valueInputOption="USER_ENTERED", body=body).execute()
	return(print("Sheet Updated"))      



status=[]	
ws = Whatsapp()

try:
    ws.launchChrome()
except WebDriverException:
    print("Retry")
    
ws.openUrl()
print("If QR code is scanned, type Yes")
y= input()

if y=="Yes":
    temp= pd.read_csv(getContacts())
        
    for n in range(0, len(temp)):
        ws.read_csv()
        ws.read_contacts(n)
        try:
            ws.openUser()
        except TimeoutException:
            status.append("User_not_found")
            continue
        except Exception as e:
        	print(e)
        	status.append("Script error")
        	continue
        ws.sendMessage()
        if getImage()!=None:
        	ws.send_image()
        if getDoc()!=None:
        	ws.send_doc()
        status.append("Successful")
        time.sleep(0.5)
        
    temp["status"]= status
    temp.to_csv(getContacts(), index= False)

    Sheets(temp)
    
else:
    print("Scan QR code")
