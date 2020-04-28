import os
import time
from helium import *
from selenium.webdriver import ChromeOptions

TD_URL = os.getenv('TD_URL')
TD_LOGIN = os.getenv('TD_LOGIN')
TD_PASSWORD = os.getenv('TD_PASSWORD')

AMEX_URL = os.getenv('AMEX_URL')
AMEX_LOGIN = os.getenv('AMEX_LOGIN')
AMEX_PASSWORD = os.getenv('AMEX_PASSWORD')


options = ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument('--disable-notifications')
# https://stackoverflow.com/questions/38684175/how-to-click-allow-on-show-notifications-popup-using-selenium-webdriver
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-notifications")
# driver = webdriver.Chrome(options=chrome_options)
# set_driver(driver)
# get_driver()

#
# TD
#
# start_chrome(TD_URL)
# time.sleep(2)
# write(TD_LOGIN)
# press(TAB)
# write(TD_PASSWORD)
# press(ENTER)

#
# Amex
#
start_chrome(AMEX_URL, options=options)
time.sleep(1)
#click(Text('User ID'))
write(AMEX_LOGIN, into='User ID')
press(TAB)
write(AMEX_PASSWORD, into='Password')
press(ENTER)
time.sleep(2)
click('View All Recent Activity')
time.sleep(2)
click('Date Range')

# Select the next range after "Latest Transactions"
press(TAB)
press(TAB)
press(TAB)
press(ENTER)
click(Button('Download'))
click('MS Excel')
click('Include all additional transaction details.')
press(TAB)
press(ENTER)

# Download "Latest Transactions"
# start_chrome(AMEX_URL)
# time.sleep(1)
# #click(Text('User ID'))
# write(AMEX_LOGIN, into='User ID')
# press(TAB)
# write(AMEX_PASSWORD, into='Password')
# press(ENTER)
# time.sleep(2)
# click('View All Recent Activity')
# time.sleep(2)
# click('Date Range')

time.sleep(1)
click('Date Range')
press(TAB)
press(ENTER)
click(Button('Download'))
click('MS Excel')
# Already unchecked by previous step
#click('Include all additional transaction details.')
press(TAB)
press(TAB)
press(ENTER)
