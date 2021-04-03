# coding=utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys #键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
import time
import difflib

def click_element(driver, element_by_xpath, timeout = 10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, element_by_xpath)))
        element.click()
    except:
        pass

if __name__ == "__main__":
    ### 定义标量
    X = {'编号': 'SNOOPY', '国家': 'US'}
    ### 打开网页
    # https://stackoverflow.com/questions/55479056/headless-chrome-getting-blank-page-source
    # 无界面模式通过截图会看到返回空内容,推测被反爬虫过滤了
    # driver.save_screenshot("debug.png")  # 可用于无界面模式调试
    ua = '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) ' + \
         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    chrome_options = webdriver.ChromeOptions()
    # # 获取页面长度、高度方式如下: 本页面为2157 951
    # page_height = driver.execute_script('return document.documentElement.scrollHeight')
    # page_width = driver.execute_script('return document.documentElement.scrollWidth')
    # print(page_height, page_width)
    chrome_options.add_argument('--window-size=960,1500')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(ua)
    chrome_options.add_argument('--start-maximized')
    executable_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)
    driver.get("https://www3.wipo.int/branddb/en/#")
    ### 进行操作
    # 点击'FILTER BY'一侧
    print('1')
    driver.save_screenshot("debug1.png")
    click_element(driver, "//*[@id='source_filter']/div[1]/div/div[6]/div/a[60]/div[1]/label")
    click_element(driver, "//*[@id='ui-id-10']/span")
    click_element(driver, "//label[@for='ACT_check']")
    click_element(driver, "//label[@for='PEND_check']")
    click_element(driver, "//*[@id='status_filter']/a/span")
    # 点击'SEARCH BY'一侧
    print('2')
    driver.save_screenshot("debug2.png")
    click_element(driver, "//*[@id='brand_search_line_0']/div[2]/ul/li/a/span[2]")
    click_element(driver, "//*[@id='brand_search_line_0']/div[2]/ul/li/ul/li[2]/a/div")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BRAND_input")))
    driver.find_element_by_id("BRAND_input").send_keys(X['编号'])
    time.sleep(5)  # 操作太快会有弹窗,一段时间后自动消失
    driver.find_element_by_id("BRAND_input").send_keys(Keys.ENTER)
    time.sleep(10)
    # 提取第一页内容
    print('3')
    driver.save_screenshot("debug3.png")
    results = []
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='0']/td[7]")))
    for i in range(0, 30, 1):
        result = driver.find_element_by_xpath("//*[@id='%d']/td[7]" % i).get_attribute("title")
        results.append(result)
    print(results)
    # 判断匹配程度，并排名
    ranks = []
    for result in results:
        xsd = difflib.SequenceMatcher(None, result, X['编号']).quick_ratio()
        ranks.append(xsd)
        print(result, xsd)
    shot_index = ranks.index(max(ranks))
    print(max(ranks), shot_index, type(shot_index))
    # 设置屏幕尺寸,并截取整个屏幕
    # driver.set_window_size(1920, 3000)
    click_element(driver, "//*[@id='%d']/td[7]/em" % shot_index, timeout=10)
    time.sleep(20)
    driver.save_screenshot("%s.png" % X['编号'])
