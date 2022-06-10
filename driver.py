from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
def create__tor_driver():
    binary = FirefoxBinary(r"C:\Users\bench\Desktop\Tor Browser\Browser\firefox.exe")
    profile = FirefoxProfile(r"C:\Users\bench\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', '127.0.0.1')
    profile.set_preference('network.proxy.socks_port', 9150)
    profile.set_preference("network.proxy.socks_remote_dns", False)
    profile.update_preferences()
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Firefox(profile, binary,options = options)
    return driver

def create_chrome_driver():
    driver = webdriver.Chrome('./chromedriver.exe')
    return driver