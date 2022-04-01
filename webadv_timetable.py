# Zoë, Kayleigh, Jordan
#
# Python Project
#
# CS371 Scripting Languages
# Spring 2022
#


# Webadvisor: https://www2.monmouth.edu/muwebadv/wa3/search/SearchClassesV2.aspx
# Current term: <option value="22/SP">22/SP - 2022 Spring</option>
'''All terms:
    <option value="22/SP">22/SP - 2022 Spring</option>
    <option value="22/SU">22/SU - All Summer 2022</option>
    <option value="22/SA">22/SA - Summer A 2022</option>
    <option value="22/SB">22/SB - Summer B 2022</option>
    <option value="22/SC">22/SC - Summer C 2022</option>
    <option value="22/SD">22/SD - Summer D 2022</option>
    <option value="22/SE">22/SE - Summer E 2022</option>
    <option value="22/FA">22/FA - 2022 Fall</option>
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import select       # dropdown
from selenium.webdriver.common.by import By     # for finding elements
import time
import sys
import re
import bs4
import requests
from selenium.webdriver.chrome.options import Options
from datetime import date   # for current term


# Getting URL of WebAdvisor for soup
url = requests.get('https://www2.monmouth.edu/muwebadv/wa3/search/SearchClassesV2.aspx')
# Turning it into text
html = url.text
# Soup object
webadvisor_soup = bs4.BeautifulSoup(html, 'html.parser')
# list of dropdowns
dropdowns = webadvisor_soup.find_all('select')

# terms list
terms = webadvisor_soup.find(id = "MainContent_ddlTerm")
terms = re.findall("value=\"([0-9]{2}/[A-Z]{2})", str(terms))
term_id = webadvisor_soup.find(id = "MainContent_ddlTerm")
term_names = re.findall(">(.+?)</option>", str(term_id))

# subjects list
subjects = webadvisor_soup.find(id = "MainContent_ddlSubj_1")
subjects = re.findall("value=\"([\w]+)\">", str(subjects))
subject_id = webadvisor_soup.find(id = "MainContent_ddlSubj_1")
subject_names = re.findall(">(.+?)</option>", str(subject_id))

# arguments list
arguments_string = ""
for arg in sys.argv:
    arguments_string += arg + ","

if(re.search('-help', arguments_string)):
    print( """
        * -open         : show open classes only
        * -help         : display a help screen and sample usage
        * -terms        : list all currently available Terms
        * -subjects     : list all currently available Subjects
    """)
    sys.exit()

# -terms: list all currently available Terms
# (no browser will be opened)
elif(re.search('-terms', arguments_string)):
    # 1. find the correct <select> with id="MainContent_ddlTerm"
    # 2. create a list of terms all under <option>
    #terms = webadvisor_soup.find(id = "MainContent_ddlTerm")
    #terms = re.findall("value=\"([0-9]{2}/[A-Z]{2})", str(terms))
    print("Terms:")
    for term in term_names:
        print(term)
    sys.exit() 

# -subjects: list all currently available Subjects
# (no browser will be opened)
elif(re.search('-subjects', arguments_string)):
    #subjects = webadvisor_soup.find(id = "MainContent_ddlSubj_1")
    #subjects = re.findall("value=\"([A-Z]{2})", str(subjects))
    print("Subjects:")
    for subject in subject_names:
        print(subject)
    sys.exit()

# current term
today_date = date.today()       # format: 2019-12-11
today_month = int(str(today_date)[5:7])
today_year = str(today_date)[0:4]
if(today_month >= 9 and today_month <= 12):
    # fall term
    current_term = str(today_year)[2:] + "/FA"
elif(today_month >= 1 and today_month <= 5):
    # spring term
    current_term = today_year[2:] + "/SP"
elif(today_month >= 5 or today_month <= 8):
    # summer term
    current_term = today_year[2:] + "/SU"

# check if Term given in command line args
if(re.search('[0-9]{2}/[A-Z]{2}', arguments_string)):
    # term = user-given term
    term = re.findall('([0-9]{2}/[A-Z]{2})', arguments_string)
    term = term[0]
else:
    # term = current_term (default)
    term = current_term
# print(term)
# check user-term given is valid (in the term list from website)
term_string = ''
for t in terms:
    term_string += t
if not(re.search(term, term_string)):
    # if user-given term is not valid
    print('Invalid Term, please redo command and select one of the valid terms: ')
    for term in term_names:
        print(term)
    sys.exit() 

# check if Subject given in command line args
if(re.search(',[A-Z]{2}', arguments_string)):
    # subject = user-given subject
    subject = re.findall(',([A-Z]{3}|[A-Z]{2})', arguments_string)
    subject = subject[0]
else:
    # set subject for debugging
    subject = 'N/A'
    print('Forgot to add Subject. Options are: ')
    for subject in subject_names:
        print(subject)
    sys.exit()
# print(subject)
# check user-subject given is valid (in the subjects list from website)
subjects_string = ''
for s in subjects:
    subjects_string += s + ","
if not(re.search(subject, subjects_string)):
    # if user-given subject is not valid
    print('Invalid Subject, please redo command and select one of the valid subjects: ')
    for subject in subject_names:
        print(subject)
    sys.exit()

# webdriver
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www2.monmouth.edu/muwebadv/wa3/search/SearchClassesV2.aspx')
#driver.fullscreen_window()
assert 'Search for Classes Version 2' in driver.page_source
time.sleep(1)

if(re.search('-open', arguments_string)):
    # set term
    term_dropdown = driver.find_element(by=By.XPATH, value="//select[@name='_ctl0:MainContent:ddlTerm']")
    all_options = term_dropdown.find_elements(by=By.TAG_NAME, value="option")
    for option in all_options:
        #print("Value is: %s" % option.get_attribute("value"))
        if option.get_attribute("value") == term:
            option.click()
    time.sleep(1)

    # set open status
    status_dropdown = driver.find_element(by=By.XPATH, value="//select[@name='_ctl0:MainContent:ddlStatus']")
    all_options = status_dropdown.find_elements(by=By.TAG_NAME, value="option")
    for option in all_options:
        #print("Value is: %s" % option.get_attribute("value"))
        if option.get_attribute("value") == 'Open':
            option.click()
    
    time.sleep(1)

# submit form normally - term, subject, submit
# set term
term_dropdown = driver.find_element(by=By.XPATH, value="//select[@name='_ctl0:MainContent:ddlTerm']")
all_options = term_dropdown.find_elements(by=By.TAG_NAME, value="option")
for option in all_options:
    # print("Value is: %s" % option.get_attribute("value"))
    if option.get_attribute("value") == term:
        option.click()
time.sleep(1)

# set subject
subject_dropdown = driver.find_element(by=By.XPATH, value="//select[@name='_ctl0:MainContent:ddlSubj_1']")
all_options = subject_dropdown.find_elements(by=By.TAG_NAME, value="option")
for option in all_options:
    # print("Value is: %s" % option.get_attribute("value"))
    if option.get_attribute("value") == subject:
        option.click()
time.sleep(3)

# submit form
button = driver.find_element(by=By.ID, value="MainContent_btnSubmit")
button.click()
driver.refresh()
assert "Search Result Version 2" in driver.page_source
#time.sleep(2)
#time.sleep(99999999999999999)
# fix: second site goes away after 3 seconds
# current fix: big number for sleep - can improve this
# chrome can detach to keep browser open after running all functions, what option is there for safari?

#driver.quit()