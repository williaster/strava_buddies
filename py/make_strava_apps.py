#!/Users/christopherwilliams/dotfiles/virtualenvs/.virtualenvs/lighttable/bin/python
info="""Creates the strava apps in the strava_apps table in the accts_and_users
        database
     """

__author__ = "ccwilliams"
__date__   = "2014-09-06"

from selenium import webdriver
import pymysql as mdb
import time

FILE_OUT   = "acct_app_info.backup" # in case lose SQL table
NUM_ACCTS  = 100
DB_NAME    = "accts_and_apps"

APP_TABLE  = "strava_apps"
ACCT_TABLE = "strava_accts"
ACCT_PK    = "id_strava_acct"

API_URL    = "http://www.strava.com/developers"

def get_acct_vals(conn, id_strava_acct):
    """Returns id, first name, last name, email, and pwd for a specific id
    """
    statement = "SELECT * FROM %s WHERE %s = %i;" % \
                (ACCT_TABLE, ACCT_PK, id_strava_acct)
    cur = conn.cursor()
    cur.execute(statement)
    result = cur.fetchall()[0]
    return result

def set_app_vals(conn, id_strava_app, client_id, client_secret, access_token):
    """Populates one row of the APP_TABLE
    """
    statement = "INSERT INTO %s VALUES (%i, %i, '%s', '%s')" % \
        (APP_TABLE, id_strava_app, client_id, client_secret, access_token)
    cur  = conn.cursor()
    cur.execute(statement)
    print "SQL data entered for app_id %i" % id_strava_app
    return

def logout(driver):
    menu   = driver.find_element_by_css_selector("li.user-menu") 
    logout = driver.find_element_by_xpath("//a[@href='/session']")
    webdriver.ActionChains(driver).move_to_element(menu).click(logout).perform()

    while True:
        try:
            driver.find_element_by_xpath("//a[@href='https://www.strava.com/login']")
        except:
            time.sleep(1)
            continue
        break
    return

#..............................................................................
# SCRIPT

f_out  = open(FILE_OUT, "a")
conn   = mdb.connect('localhost', 'root', '', DB_NAME)
driver = webdriver.Firefox()

with conn:
    cur = conn.cursor()

    for i in range(61, NUM_ACCTS + 1): # did several manually

        if i % 5 == 0:
            print "pausing ..."
            time.sleep(5)
        
        # get login credentials
        s_id, first_name, last_name, email, pwd = get_acct_vals(conn, i)

        while True: # login
            driver.get(API_URL)
            try: 
                driver.find_element_by_xpath("//div[@class='instructions panel-content']//a[@href='/login']").click()
                time.sleep(1.5)
                driver.find_element_by_id("email").send_keys(email)
                driver.find_element_by_id("password").send_keys(pwd)
                driver.find_element_by_id("login-button").click()
                break

            except:
                print "unsuccessful login for account %s ..." % email
                logout(driver)
                continue

        try: # create api
            time.sleep(1.5)
            driver.find_element_by_xpath("//div[@class='instructions panel-content']//a[@href='/settings/api']").click()
            driver.find_element_by_id("app-name").send_keys("test application")
            driver.find_element_by_id("app-user_support_url").send_keys("NA")
            driver.find_element_by_id("app-description").send_keys("todo: update")
            driver.find_element_by_id("app-domain").send_keys("williaster.com")
            driver.find_element_by_id("tos").click()
            driver.find_element_by_xpath("//input[@value='Create']").click()

            try: # fetch values and add to DB/out file
                print "API made with account %s" % email
                driver.find_element_by_id("show-secret").click()
                driver.find_element_by_id("show-token").click()
                
                client_id     = int(driver.find_element_by_xpath("//div[@id='API']/table/tbody/tr[1]/td[2]").text.split("\n")[1])
                client_secret = driver.find_element_by_xpath("//div[@id='API']/table/tbody/tr[2]/td[2]/span").text.encode("ascii")
                my_token      = driver.find_element_by_xpath("//div[@id='API']/table/tbody/tr[3]/td[2]/span").text.encode("ascii")

                f_out.write("%s\t%i, %i, '%s', '%s'\n" % \
                    (email, i, client_id, client_secret, my_token))
                 
                set_app_vals(conn, i, client_id, client_secret, my_token)

            except Exception, e:
                print e
                raise Exception("Error parsing API information")
                
        except Exception, e:
            print e
            print "Error with account %s, continuing" % email
            logout(driver)
            continue

        logout(driver)
        print "Full app made with %s successfully" % email
        
f_out.close()
print "done"
