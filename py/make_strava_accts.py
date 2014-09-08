#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Creates the strava accounts in the strava_accts table in the accts_and_users
        database
     """

__author__ = "ccwilliams"
__date__   = "2014-09-06"

from selenium import webdriver
import pymysql as mdb
import time

NUM_ACCTS  = 100
DB_NAME    = "accts_and_apps"
TABLE_NAME = "strava_accts"
PRIM_KEY   = "id_strava_acct"
REG_URL    = "https://www.strava.com/register/free?utm_source=home-page"

def get_field_vals(conn, id_strava_acct):
    """Returns id, first name, last name, email, and pwd for a specific id
    """
    statement = "SELECT * FROM %s WHERE %s = %i;" % \
                (TABLE_NAME, PRIM_KEY, id_strava_acct)
    cur = conn.cursor()
    cur.execute(statement)
    result = cur.fetchall()[0]
    return result

def logout(driver):
    menu   = driver.find_element_by_css_selector("li.user-menu") 
    logout = driver.find_element_by_xpath("//a[@href='/session']")
    webdriver.ActionChains(driver).move_to_element(menu).click(logout).perform()
    return

#..............................................................................
# SCRIPT

conn   = mdb.connect('localhost', 'root', '', DB_NAME)
driver = webdriver.Firefox()

with conn:
    cur = conn.cursor()

    for i in range(21, NUM_ACCTS + 1): # did several manually
        if i % 10 == 0:
            print "pausing ..."
            time.sleep(5)
        try:
            s_id, first_name, last_name, email, pwd = get_field_vals(conn, i)
        except Exception, e:
            print "Error with id %i, skipping" % i
            print e
            continue

        driver.get(REG_URL)
        if "Home" in driver.title: # logout, wrong page
            logout(driver)
            while True:
                try:
                    driver.find_element_by_css_selector("a.btn-login.button")
                except:
                    time.sleep(1)
                    continue
                break
            driver.get(REG_URL) # back to registration page

        driver.find_element_by_id("firstname").send_keys(first_name)
        driver.find_element_by_id("lastname").send_keys(last_name)
        driver.find_element_by_id("email").send_keys(email)
        driver.find_element_by_id("password").send_keys(pwd)
        driver.find_element_by_id("password_confirmation").send_keys(pwd)
        driver.find_element_by_id("receive_newsletter").click()
        
        driver.find_element_by_id("signup-button").click()
        time.sleep(1)
        if "Home" not in driver.title:
            print "Error with id %i, skipping" % i

        logout(driver)
        while True:
            try:
                driver.find_element_by_css_selector("a.btn-login.button")
            except:
                time.sleep(1)
                continue
            break
        print "Made account with %s successfully" % email
        


