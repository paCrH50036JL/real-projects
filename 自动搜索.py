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
    ### 定义常用变量
    OUT_DIR = 'output'
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
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-proxy-server')
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument(ua)
    chrome_options.add_argument('--start-maximized')
    executable_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

    ### 获取点击位置
    # 打开网页
    driver.get("https://www3.wipo.int/branddb/en/#")
    # 取得国家与点击位置对应关系
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'source_filter')))
    except:
        pass
    contry_elements = []
    for i in range(1, 70):
        xpath = "//*[@id='source_filter']/div[1]/div/div[6]/div/a[%d]/div[1]/label" % i
        element = driver.find_element_by_xpath(xpath).text
        contry_element = [element, xpath]
        contry_elements.append(contry_element)
    # print(contry_elements)
    # 取得点击位置
    if ('WO' not in X['国家']):  # WO包含三个,需要单独处理
        for i in range(1, 70):
            if X['国家'] in contry_elements[i][0]:
                contry_click = contry_elements[i][1]
                break
    else:
        if X['国家'] == 'WO AO (LIS)':
            contry_click = contry_elements[66][1]
        if X['国家'] == 'WO TM':
            contry_click = contry_elements[67][1]
        if X['国家'] == 'WO 6TER':
            contry_click = contry_elements[68][1]
    print(contry_click)

    ### 获取数据
    test_cnts = 0
    while True:
        print('#####进行第%d次测试#####' % test_cnts)
        point1 = time.time()
        driver.get("https://www3.wipo.int/branddb/en/#")
        point2 = time.time()
        ### 进行操作
        # 点击'FILTER BY'一侧
        print('1')
        driver.save_screenshot("%s/debug1-%d.png" % (OUT_DIR, test_cnts))
        click_element(driver, "//*[@id='source_filter']/div[1]/div/div[6]/div/a[60]/div[1]/label")
        click_element(driver, "//*[@id='ui-id-10']/span")
        click_element(driver, "//label[@for='ACT_check']")
        click_element(driver, "//label[@for='PEND_check']")
        click_element(driver, "//*[@id='status_filter']/a/span")
        point3 = time.time()
        # 点击'SEARCH BY'一侧
        print('2')
        driver.save_screenshot("%s/debug2-%d.png" % (OUT_DIR, test_cnts))
        click_element(driver, "//*[@id='brand_search_line_0']/div[2]/ul/li/a/span[2]")
        click_element(driver, "//*[@id='brand_search_line_0']/div[2]/ul/li/ul/li[2]/a/div")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BRAND_input")))
        driver.find_element_by_id("BRAND_input").send_keys(X['编号'])
        driver.find_element_by_id("BRAND_input").send_keys(Keys.ENTER)
        # 点击太快网页会出现弹窗提示:Sorry, the page is busy processing another request,导致回车失败
        xpath = "//*[@id='search_pane']/form/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/h4"
        while True:
            try:
                element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                if element.text == "CURRENT SEARCH":  # 特别注意: 此处不是Current Search而是CURRENT SEARCH
                    break
            except:
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BRAND_input")))
                    driver.find_element_by_id("BRAND_input").send_keys(Keys.ENTER)
                except:
                    pass
        point4 = time.time()
        print('3')
        driver.save_screenshot("%s/debug3-%d.png" % (OUT_DIR, test_cnts))
        results = []
        for i in range(0, 30, 1):
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='%d']/td[7]" % i)))
            result = driver.find_element_by_xpath("//*[@id='%d']/td[7]" % i).get_attribute("title")
            results.append(result)
        print(results)
        point5 = time.time()
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
        click_element(driver, "//*[@id='%d']/td[7]/em" % shot_index)
        WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "documentContent")))
        driver.save_screenshot("%s/%s-%d.png" % (OUT_DIR, X['编号'], test_cnts))
        point6 = time.time()

        ### 进行下一次测试
        print("打开网页用时:%s,自动操作浏览器用时%s" % ((point2 -point1), (point6 -point2)))
        print('各阶段用时:%s-%s-%s-%s-%s' % ((point2 -point1), (point3 -point2),
                        (point4 -point3), (point5 -point4), (point6 -point5)))
        test_cnts = test_cnts + 1
        time.sleep(1)

