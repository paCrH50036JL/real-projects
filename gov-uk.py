# coding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
import time
import difflib

# 定义调试函数
def screenshot_debug(num, timeout = 0):
    OUT_DIR = 'output/gov-uk'
    time.sleep(timeout)
    driver.save_screenshot("%s/debug-%s.png" % (OUT_DIR, num))

if __name__ == "__main__":
    TM = {'编号': 'APP', '国家': '21'}

    ### 进行搜索
    # 进入搜索页面
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=960,1500')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-proxy-server')
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    ua = '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) ' + \
         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    chrome_options.add_argument(ua)
    chrome_options.add_argument('--start-maximized')
    executable_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)
    driver.maximize_window()
    url = 'https://trademarks.ipo.gov.uk/ipo-tmtext'
    driver.get(url)
    screenshot_debug(1, 20)
    # 输入搜索内容
    driver.find_element_by_xpath('/html/body/main/form/div[2]/div[2]/select').click()
    driver.find_element_by_xpath('/html/body/main/form/div[2]/div[2]/select/option[3]').click()
    driver.find_element_by_xpath('/html/body/main/form/div[2]/div[4]/input').send_keys(TM['编号'])
    driver.find_element_by_xpath('/html/body/main/form/div[4]/div[2]/div/ul').click()
    driver.find_element_by_xpath('/html/body/main/form/div[4]/div[2]/div/div/ul/li[21]').click()
    driver.find_element_by_xpath('/html/body/main/form/div[5]/div[3]/div[1]/select').click()
    driver.find_element_by_xpath('/html/body/main/form/div[5]/div[3]/div[1]/select/option[2]').click()
    screenshot_debug(2)
    # 点击搜索
    driver.find_element_by_xpath('/html/body/main/form/div[6]/button').click()
    screenshot_debug(3, 20)
    ### 处理搜索结果
    print(driver.find_element_by_xpath('/html/body/main/form/div[1]/div/div[1]/h2').text)
    print(driver.find_element_by_xpath('/html/body/main/form/div[2]/div/div[1]/p/a').text)
