from django.shortcuts import render
from selenium import webdriver
from collections import Counter
from .models import *
from .TestResult import *
import time
from webdriver_manager.chrome import ChromeDriverManager


# Create your views here.


def get_text_web_element(web_element):
    return web_element.text


def find_index_web_elements_list(web_elements, name):
    return [element.text for element in web_elements].index(name)


def click_web_elements_by_name(web_elements, name):
    index = find_index_web_elements_list(web_elements, name)
    time.sleep(1)
    web_elements[index].click()
    time.sleep(1)


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    # return webdriver.Chrome()
    return driver


def find_most_frequent_word(data_set):
    split_it = data_set.split()
    counter = Counter(split_it)
    most_occur = counter.most_common(1)
    word, num_times = most_occur[0]
    return 'The most frequent word is [ %s ] which occur %d times' % (word, num_times)


def get_most_frequent_word(title, driver, class_name):
    headlines = driver.find_elements_by_class_name(class_name)
    headlines_text = map(get_text_web_element, headlines)
    all_text = " ".join(headlines_text)
    return TestResult(title, 'Pass', find_most_frequent_word(all_text))


def click_verify_nav_link(driver, nav_text):
    els = driver.find_elements_by_class_name('nav-link')
    time.sleep(2)
    click_web_elements_by_name(els, nav_text)
    return "Verified link: %s" % nav_text


def calculate_words(title, driver):
    driver.get("http://www.metsystems.com.au/")
    test_result = get_most_frequent_word(title, driver, 'summary-info')
    return test_result


def test_links(title, driver):
    driver.get("http://www.metsystems.com.au/")
    driver.find_element_by_xpath("//*[text()=' Products ']").click()
    elements = driver.find_elements_by_class_name('dropdown-item-title')
    click_web_elements_by_name(elements, 'MI CORE')
    nav_links = ['SERVICES', 'CASE STUDIES', 'NEWS', 'FAQ', 'ABOUT']
    result_list = [click_verify_nav_link(driver, nav_link) for nav_link in nav_links]
    return TestResult(title, 'Pass', "|".join(result_list))


def create_failed_passed_test(title, driver):
    try:
        driver.get("http://www.metsystems.com.au/")
        driver.find_element_by_xpath("//*[text()=' Productsss ']")
        return TestResult(title, 'PASS', '')
    except Exception as e:
        return TestResult(title, 'Fail', str(e))


def cba_test(title, driver):
    try:
        driver.get("https://www.commbank.com.au/")
        el = driver.find_element_by_css_selector('.banner-content h1')
        test_result = 'The banner text is: [' + el.text + ']'
        time.sleep(5)
        return TestResult(title, 'Pass', test_result)
    except Exception as e:
        return TestResult(title, 'Fail', e)


def click_by_css_selector(driver, css_selector):
    el = driver.find_element_by_css_selector(css_selector)
    time.sleep(2)
    el.click()


def cba_links(title, driver):
    try:
        driver.get("https://www.commbank.com.au/")
        css_menu_list = ['a[data-target="#products"]', 'a[data-target="#support"]', 'a[data-target="#rates"]',
                         'a[data-target="#tools"]']
        [click_by_css_selector(driver, link) for link in css_menu_list]
        return TestResult(title, 'Pass', 'Links verified:|' + "|".join(css_menu_list))
    except Exception as e:
        return TestResult(title, 'Fail', e)


def click_web_element_by_class_name_and_name(driver, css_selector, name):
    els = driver.find_elements_by_class_name(css_selector)
    click_web_elements_by_name(els, name)


def click_web_element_by_css_selector_and_name(driver, css_selector, name):
    els = driver.find_elements_by_css_selector(css_selector)
    click_web_elements_by_name(els, name)


def input_text_by_id(driver, id, text):
    time.sleep(1)
    driver.find_element_by_id(id).send_keys(text)


def big_commerce_request_demo(title, driver):
    try:
        driver.get("https://www.bigcommerce.com/")
        driver.find_element_by_css_selector('.menuItem--hasThirdLevelChildren').click()
        click_web_element_by_class_name_and_name(driver, 'subMenu-item', 'Headless Commerce')
        click_web_element_by_css_selector_and_name(driver, 'a[role=button]', 'REQUEST A DEMO')
        input_ids = ['FirstName', 'LastName', 'Email', 'Company', 'Projected_Annual_Revenue__c', 'Phone', 'Country']
        input_values = ['Dmytro', 'Drozdov', 'dm.drozdov@gmail.com', 'BigCommerce', "I'm not sure", '041234567', 'Australia']
        [input_text_by_id(driver, el_id, value) for el_id, value in zip(input_ids, input_values)]
        return TestResult(title, 'Pass', 'Requested Demo from BigCommerce web site')
    except Exception as e:
        return TestResult(title, 'Fail', str(e))


def wikipedia(title, driver):
    try:
        driver.get("https://www.wikipedia.org/")
        input_el = driver.find_element_by_id('searchInput')
        input_el.send_keys('Federer')
        time.sleep(3)
        driver.find_element_by_css_selector('[data-jsl10n=search-input-button]').click()
        css_header = 'firstHeading'
        heading = driver.find_element_by_id(css_header).text
        expected_value = 'Roger Federer'
        if heading != expected_value:
            return TestResult(title, 'Fail', 'Incorrect header. Expected: ' + expected_value + ' got: ' + heading)
        return TestResult(title, 'Pass', 'The header ' + css_header + ' is correct')
    except Exception as e:
        return TestResult(title, 'Fail', str(e))


def cleartests(request):
    Task.objects.all().update(result='', log='', active=False)
    return render(request, 'tasks/list.html', {'tasks': Task.objects.all()})


def update_tests(test_name, test_result):
    Task.objects.all().update(active=False)
    Task.objects.filter(test_name=test_name).update(result=test_result.result, log=test_result.log, active=True)


def show_log(test_name):
    Task.objects.all().update(active=False)
    Task.objects.filter(test_name=test_name).update(active=True)
    return Task.objects.get(test_name=test_name)


def run_all(test_list, func_list):
    web_driver = get_chrome_driver()
    [execute_test(web_driver, test_name, func) for test_name, func in zip(test_list, func_list)]
    web_driver.close()


def execute_test(web_driver, test_name, func):
    title = Task.objects.get(test_name=test_name).title
    test_result = func(title, web_driver)
    update_tests(test_name, test_result)
    return test_result


def execute_test_by_request(request, test_name, func):
    if request.GET.get(test_name):
        web_driver = get_chrome_driver()
        execute_test(web_driver, test_name, func)
        web_driver.close()


def add_log_suffix(name):
    return name + 'Log'


def index(request):
    test_result = TestResult('', '', '')

    tests = ['runtest1', 'runtest2', 'runtest3', 'runtest4', 'runtest5', 'runtest6', 'runtest7']
    logs = [add_log_suffix(name) for name in tests]
    funcs = [calculate_words, test_links, create_failed_passed_test, cba_test, cba_links, big_commerce_request_demo, wikipedia]

    test_result = [execute_test_by_request(request, test_name, func) for test_name, func in zip(tests, funcs)]
    # test_result = [show_log(request, log_name, test_name) for log_name, test_name in zip(logs, tests)]

    if request.GET.get('runall'):
        run_all(tests, funcs)

    if request.GET.get('runtest1Log'):
        test_result = show_log('runtest1')

    if request.GET.get('runtest2Log'):
        test_result = show_log('runtest2')

    if request.GET.get('runtest3Log'):
        test_result = show_log('runtest3')

    if request.GET.get('runtest4Log'):
        test_result = show_log('runtest4')

    if request.GET.get('runtest5Log'):
        test_result = show_log('runtest5')

    if request.GET.get('runtest6Log'):
        test_result = show_log('runtest6')

    if request.GET.get('runtest7Log'):
        test_result = show_log('runtest7')

    if request.GET.get('clear'):
        cleartests(request)

    tasks = Task.objects.all()
    context = {'tasks': tasks, 'test_result': test_result}
    return render(request, 'tasks/list.html', context)
