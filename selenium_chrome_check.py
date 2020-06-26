from selenium import webdriver
from collections import Counter
from common_web_elements import *
import time


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")
    return webdriver.Chrome(chrome_options=options)


def find_most_frequent_word(data_set):
    split_it = data_set.split()
    counter = Counter(split_it)
    most_occur = counter.most_common(1)
    print(most_occur)


def get_most_frequent_word(driver, class_name):
    headlines = driver.find_elements_by_class_name(class_name)
    headlines_text = map(get_text_web_element, headlines)
    all_text = " ".join(headlines_text)
    find_most_frequent_word(all_text)


def main():
    driver = get_chrome_driver()
    driver.get("http://www.metsystems.com.au/")
    get_most_frequent_word(driver, 'summary-info')
    driver.find_element_by_xpath("//*[text()=' Products ']").click()
    elements = driver.find_elements_by_class_name('dropdown-item-title')
    click_web_elements_by_name(elements, 'MI CORE')
    get_most_frequent_word(driver, 'content')


def click_nav_link(driver, nav_text):
    els = driver.find_elements_by_class_name('nav-link')
    time.sleep(2)
    click_web_elements_by_name(els, nav_text)


def test_links():
    driver = get_chrome_driver()
    driver.get("http://www.metsystems.com.au/")
    driver.find_element_by_xpath("//*[text()=' Products ']").click()
    elements = driver.find_elements_by_class_name('dropdown-item-title')
    click_web_elements_by_name(elements, 'MI CORE')
    nav_links = ['SERVICES', 'CASE STUDIES', 'NEWS', 'FAQ', 'ABOUT']
    [click_nav_link(driver, nav_link) for nav_link in nav_links]


class TestResult:
    def __init__(self, test_result, exception):
        self.result = test_result
        self.exception = exception


def create_failed_test():
    try:
        driver = get_chrome_driver()
        driver.get("http://www.metsystems.com.au/")
        el = driver.find_element_by_xpath("//*[text()=' Productsss ']")
        return TestResult('PASS', '')
    except Exception as e:
        return TestResult('FAIL', e)


def cba_test(title):
    try:
        driver = get_chrome_driver()
        driver.get("https://www.commbank.com.au/")
        el = driver.find_element_by_css_selector('.banner-content h1')
        test_result = 'The banner text is: [' + el.text + ']'
        time.sleep(5)
        driver.close()
        return TestResult('Pass', test_result)
    except Exception as e:
        driver.close()
        return TestResult('Fail', e)


def click_by_css_selector(driver, css_selector):
    el = driver.find_element_by_css_selector(css_selector)
    time.sleep(2)
    el.click()


def cba_links(title):
    try:
        driver = get_chrome_driver()
        driver.get("https://www.commbank.com.au/")
        css_menu_list = ['a[data-target="#products"]', 'a[data-target="#support"]', 'a[data-target="#rates"]',
                         'a[data-target="#tools"]']
        [click_by_css_selector(driver, link) for link in css_menu_list]
        driver.close()
        return TestResult('Pass', '')
    except Exception as e:
        driver.close()
        return TestResult('Fail', e)


if __name__ == '__main__':
    result = cba_links('')
    m = 2
