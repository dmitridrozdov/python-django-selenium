from django.shortcuts import render
from selenium import webdriver
from collections import Counter
from .models import *
from .TestResult import *
import time


# Create your views here.


def get_text_web_element(web_element):
    return web_element.text


def find_index_web_elements_list(web_elements, name):
    return [element.text for element in web_elements].index(name)


def click_web_elements_by_name(web_elements, name):
    index = find_index_web_elements_list(web_elements, name)
    web_elements[index].click()


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--kiosk")
    return webdriver.Chrome(chrome_options=options)


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


def calculate_words(title):
    driver = get_chrome_driver()
    driver.get("http://www.metsystems.com.au/")
    test_result = get_most_frequent_word(title, driver, 'summary-info')
    driver.close()
    return test_result


def test_links(title):
    driver = get_chrome_driver()
    driver.get("http://www.metsystems.com.au/")
    driver.find_element_by_xpath("//*[text()=' Products ']").click()
    elements = driver.find_elements_by_class_name('dropdown-item-title')
    click_web_elements_by_name(elements, 'MI CORE')
    nav_links = ['SERVICES', 'CASE STUDIES', 'NEWS', 'FAQ', 'ABOUT']
    result_list = [click_verify_nav_link(driver, nav_link) for nav_link in nav_links]
    driver.close()
    return TestResult(title, 'Pass', "|".join(result_list))


def create_failed_passed_test(title):
    driver = get_chrome_driver()
    try:
        driver.get("http://www.metsystems.com.au/")
        driver.find_element_by_xpath("//*[text()=' Productsss ']")
        return TestResult(title, 'PASS', '')
    except Exception as e:
        driver.close()
        return TestResult(title, 'Fail', str(e))


def cba_test(title):
    try:
        driver = get_chrome_driver()
        driver.get("https://www.commbank.com.au/")
        el = driver.find_element_by_css_selector('.banner-content h1')
        test_result = 'The banner text is: [' + el.text + ']'
        time.sleep(5)
        driver.close()
        return TestResult(title, 'Pass', test_result)
    except Exception as e:
        driver.close()
        return TestResult(title, 'Fail', e)


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
        return TestResult(title, 'Pass', 'Links verified:|' + "|".join(css_menu_list))
    except Exception as e:
        driver.close()
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


def big_commerce_request_demo(title):
    try:
        driver = get_chrome_driver()
        driver.get("https://www.bigcommerce.com/")
        el = driver.find_element_by_css_selector('.menuItem--hasThirdLevelChildren')
        el.click()
        click_web_element_by_class_name_and_name(driver, 'subMenu-item', 'Headless Commerce')
        time.sleep(3)
        click_web_element_by_css_selector_and_name(driver, 'a[role=button]', 'REQUEST A DEMO')
        time.sleep(2)
        input_ids = ['FirstName', 'LastName', 'Email', 'Company', 'Projected_Annual_Revenue__c', 'Phone', 'Country']
        input_values = ['Dmytro', 'Drozdov', 'dm.drozdov@gmail.com', 'BigCommerce', "I'm not sure", '041234567', 'Australia']
        [input_text_by_id(driver, el_id, value) for el_id, value in zip(input_ids, input_values)]
        driver.close()
        return TestResult(title, 'Pass', 'Requested Demo from BigCommerce web site')
    except Exception as e:
        driver.close()
        return TestResult(title, 'Fail', str(e))


def wikipedia(title):
    try:
        driver = get_chrome_driver()
        driver.get("https://www.wikipedia.org/")
        input_el = driver.find_element_by_id('searchInput')
        input_el.send_keys('Federer')
        time.sleep(3)
        driver.find_element_by_css_selector('[data-jsl10n=search-input-button]').click()
        css_header = 'firstHeading'
        heading = driver.find_element_by_id(css_header).text
        expected_value = 'Roger Federer11'
        driver.close()
        if heading != expected_value:
            return TestResult(title, 'Fail', 'Incorrect header. Expected: ' + expected_value + ' got: ' + heading)
        return TestResult(title, 'Pass', 'The header ' + css_header + ' is correct')
    except Exception as e:
        driver.close()
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


def runtest1(request):
    title = Task.objects.get(test_name='runtest1').title
    test_result = calculate_words(title)
    update_tests('runtest1', test_result)
    return test_result


def runtest2(request):
    title = Task.objects.get(test_name='runtest2').title
    test_result = test_links(title)
    update_tests('runtest2', test_result)
    return test_result


def runtest3(request):
    title = Task.objects.get(test_name='runtest3').title
    test_result = create_failed_passed_test(title)
    update_tests('runtest3', test_result)
    return test_result


def runtest4(request):
    title = Task.objects.get(test_name='runtest4').title
    test_result = cba_test(title)
    update_tests('runtest4', test_result)
    return test_result


def runtest5(request):
    title = Task.objects.get(test_name='runtest5').title
    test_result = cba_links(title)
    update_tests('runtest5', test_result)
    return test_result


def runtest6(request):
    title = Task.objects.get(test_name='runtest6').title
    test_result = big_commerce_request_demo(title)
    update_tests('runtest6', test_result)
    return test_result


def runtest7(request):
    title = Task.objects.get(test_name='runtest7').title
    test_result = wikipedia(title)
    update_tests('runtest7', test_result)
    return test_result


def run_all(request):
    runtest1(request)
    runtest2(request)
    runtest3(request)
    runtest4(request)
    runtest5(request)
    runtest6(request)
    return runtest7(request)


def index(request):
    tasks = Task.objects.all()
    test_result = TestResult('', '', '')

    if request.GET.get('runall'):
        test_result = run_all(request)

    if request.GET.get('runtest1'):
        test_result = runtest1(request)

    if request.GET.get('runtest2'):
        test_result = runtest2(request)

    if request.GET.get('runtest3'):
        test_result = runtest3(request)

    if request.GET.get('runtest4'):
        test_result = runtest4(request)

    if request.GET.get('runtest5'):
        test_result = runtest5(request)

    if request.GET.get('runtest6'):
        test_result = runtest6(request)

    if request.GET.get('runtest7'):
        test_result = runtest7(request)

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

    context = {'tasks': tasks, 'test_result': test_result}
    return render(request, 'tasks/list.html', context)
