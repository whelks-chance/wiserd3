import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

display = Display(visible=0, size=(1024, 768))
display.start()

delay = 5
search_uuid = 'aaaaa'
filename = 'map_{}.png'.format(search_uuid)

# enable browser logging
# d = DesiredCapabilities.FIREFOX
# d['loggingPrefs'] = {'browser': 'ALL', 'service_log_path': './firefox_log'}

# p = webdriver.FirefoxProfile()
# p.set_preference("webdriver.log.file", "/tmp/firefox_console")

# firefox_capabilities = DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True
# firefox_capabilities['binary'] = '/usr/bin/firefox'

driver = webdriver.Firefox()

# chromium_capabilities = DesiredCapabilities.CHROME
# chromium_capabilities['binary'] = '/usr/lib/chromium-browser/chromedriver'
# driver = webdriver.Chrome(desired_capabilities=chromium_capabilities)


driver.get('http://localhost:8000/map?use_template=False')

for entry in driver.get_log('browser'):
    print entry

try:

    time.sleep(delay)
    driver.save_screenshot(filename)

except Exception as e32564:
    print type(e32564), e32564

driver.quit()
display.stop()

