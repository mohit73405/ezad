from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--lang=en')
# chrome_options.add_argument("--enable-file-cookies")
browser1 = webdriver.Chrome(chrome_options=chrome_options)

user_name = 'spidey_try@hotmail.com'
password = 'ironman9@123786'

browser1.get("https://www.instagram.com/accounts/login/")

browser1.find_element_by_name("username").send_keys(user_name)
browser1.find_element_by_name("password").send_keys(password)

browser1.find_element_by_xpath("//button/div[ text()='Log in' ]").click()
cookies = browser1.get_cookies()
print(cookies)
for item in cookies:
    print(item)

# browser2 = webdriver.Chrome(chrome_options=chrome_options)

browser1.get("https://www.instagram.com")
for cookie in cookies:
    print(cookie)
    browser1.add_cookie(cookie)
browser1.get("https://www.instagram.com/blowek5/?__a=1")

# cookies = browser2.get_cookies()
# print(cookies)
# print(data)
