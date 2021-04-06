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
    OUT_DIR = 'output/europa-eu'
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
    url = 'https://euipo.europa.eu/eSearch/#advanced/trademarks'
    driver.get(url)
    screenshot_debug(1, 20)
    driver.find_element_by_xpath('//*[@id="advancedPage"]/div/div/div/div[1]/div[2]/ul/li[2]/a').click()
    screenshot_debug(2)
    # 输入搜索内容
    xpath = '/html/body/div[1]/div/div/div/section[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/span[3]/select[1]'
    driver.find_element_by_xpath(xpath).click()
    xpath = '/html/body/div[1]/div/div/div/section[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/span[3]/select[1]/option[2]'
    driver.find_element_by_xpath(xpath).click()
    xpath = '/html/body/div[1]/div/div/div/section[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/span[4]/input'
    driver.find_element_by_xpath(xpath).send_keys(TM['编号'])
    xpath = '/html/body/div[1]/div/div/div/section[2]/div/div/div/div[2]/div[1]/div[2]/div[3]/span[4]/input'
    driver.find_element_by_xpath(xpath).click()
    xpath = '/html/body/div[1]/div/div/div/section[2]/div/div/div/div[2]/div[1]/div[2]/div[3]/div/ol/li[%s]' % TM['国家']
    driver.find_element_by_xpath(xpath).click()
    screenshot_debug(3)
    # 点击搜索
    driver.find_element_by_xpath('//*[@id="advancedPage"]/div/div/div/div[2]/nav/ul/li[3]/a').click()
    screenshot_debug(4, 20)
    ### 处理搜索结果
    print(driver.find_element_by_xpath('//*[@id="advancedPage"]/div/div/div/div[4]/div[1]/div[1]/div[2]').text)
    print(driver.find_element_by_xpath('//*[@id="advancedPage"]/div/div/div/div[4]/div[3]/div[1]/div/header/div/div[1]/h3/a').text)
