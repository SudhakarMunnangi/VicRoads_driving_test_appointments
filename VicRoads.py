#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 22:31:43 2020

@author: sudhakarmunnangi
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://billing.vicroads.vic.gov.au/bookings/Manage/Details")
#inputElement = driver.find_element_by_id("ClientID")
inputElement = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("ClientID"))
inputElement.send_keys('--VicRoads Customer number--')
inputElement = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("FamilyNameOne"))
#inputElement = driver.find_element_by_id("")
inputElement.send_keys('Munnangi')
inputElement.send_keys(Keys.ENTER)
#WebDriverWait(driver, 40).until(lambda x: x.find_element_by_id("FamilyNameOne"))
element = WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="TransferDiv"]/label')))
driver.find_element_by_xpath("//input[@type='radio' and @value='change']").click()
driver.find_element_by_xpath("//input[@type='submit' and @value='Next']").click()
driver.find_element_by_xpath("//input[@type='submit' and @value='Next']").click()


VicRoadsLoc = [
'Ararat'
,'Ballarat'
,'Benalla'
,'Bendigo'
,'Broadmeadows'
,'Bundoora'
,'Burwood East'
,'Carlton'
,'Colac'
,'Dandenong'
,'Dromana'
,'Frankston'
,'Geelong'
,'Heatherton'
,'Hoppers Crossing'
,'Hub@Exhibition (Melbourne CBD)'
,'Hub@Sunshine'
,'Kyneton'
,'Leongatha'
,'Maryborough'
,'Melton'
,'Mooroolbark'
,'Morwell'
,'Pakenham'
,'Seymour'
,'Shepparton'
,'Sunbury'
,'Warragul'
,'Werribee']



if os.path.exists("----path----/appointmentsfile.txt"):
    os.remove("----path----/appointmentsfile.txt")
f = open("----path----/appointmentsfile.txt", "a+")
f.write("slots"+"\n")


for each in VicRoadsLoc:
 driver.find_element_by_xpath("//select[@name='officeid']/option[text()='{}']".format(each)).click()
#driver.find_element_by_xpath("//select[@name='officeid']/option[@value='3']").click()
 driver.find_element_by_id("NextAvailableAppointment").click()
 driver.find_element_by_xpath("//input[@type='submit' and @value='Search']").click()
 try:
     element = WebDriverWait(driver,40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="monday"]/div[1]')))
 except:
    print("not of any help")
 appointments = driver.find_element_by_xpath('/html/body/div/div[2]/div[9]').text
 driver.find_element_by_xpath('/html/body/div/div[2]/div[11]/div[1]/div[2]/a').click()
 f.write("\n"+each)
 f.write("\n"+appointments+"\n")
f.close()
driver.close()
#### file processing 

#reading .csv file into pandas dataframe for further computation
df = pd.read_csv("----path----/appointmentsfile.txt")

#dropping the rows(slots) which have "No appointments"
df.drop(index = df[df['slots']=="No appointments"].index.values -1,inplace = True)
df.drop(index = df[df['slots']=="No appointments"].index.values,inplace = True)
df.reset_index(drop=True, inplace=True)

#finding latest appointment

VicRoadsLoc_index = []
for index, row in df.iterrows():
   if row['slots'] in VicRoadsLoc:
       VicRoadsLoc_index.append(index)
       

VicRoads_loc = []
VicRoads_loc_eairliest_date_day = []
VicRoads_loc_eairliest_date_month = []
VicRoads_loc_eairliest_time = []
for each in VicRoadsLoc_index:
    VicRoads_loc.append(''.join(df.iloc[each].values))
    VicRoads_loc_eairliest_date_day.append((''.join(df.iloc[each + 1]))[4:6])
    VicRoads_loc_eairliest_date_month.append((''.join(df.iloc[each + 1]))[7:])
    VicRoads_loc_eairliest_time.append(''.join(df.iloc[each + 2]))
    
zippedlists = list(zip(VicRoads_loc, VicRoads_loc_eairliest_date_month, VicRoads_loc_eairliest_date_day, VicRoads_loc_eairliest_time))
df2 = pd.DataFrame(zippedlists, columns = ['location', 'month', 'date', 'time'])
df2 = df2.sort_values(['month', 'date'],ascending=True)


#sending email

msg = MIMEMultipart('alternative')
msg['To'] = email.utils.formataddr(('Sudhakar', '--from email id--'))
msg['From'] = email.utils.formataddr(('Your Name', '--to email id--'))
msg['Subject'] = "Earliest Hazard slots available are:"
html = df2.to_html()
part1 = MIMEText(html, 'plain')
part2 = MIMEText(html, 'html')
msg.attach(part1)
msg.attach(part2)
EMAIL_USE_TLS = True   
server = smtplib.SMTP('smtp.office365.com')
server.connect ('smtp.office365.com', 25)
server.ehlo()
server.starttls()
server.login('--from email id--', "--password--")
server.sendmail('--from email id--', ['--to email id--'], msg.as_string())
server.quit()
