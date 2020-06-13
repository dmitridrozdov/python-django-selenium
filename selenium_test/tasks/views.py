from django.shortcuts import render
from selenium import webdriver
from collections import Counter
from .models import *
import time
from .TestResult import *


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
    return most_occur


def get_most_frequent_word(driver, class_name):
    headlines = driver.find_elements_by_class_name(class_name)
    headlines_text = map(get_text_web_element, headlines)
    all_text = " ".join(headlines_text)
    return TestResult('Pass', find_most_frequent_word(all_text))


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
    driver.close()
    return TestResult('Pass', '')


def create_failed_passed_test():
    driver = get_chrome_driver()
    try:
        driver.get("http://www.metsystems.com.au/")
        driver.find_element_by_xpath("//*[text()=' Productsss ']")
        return TestResult('PASS', '')
    except Exception as e:
        driver.close()
        return TestResult('Fail', e)


def cleartests(request):
    Task.objects.all().update(result='', log='')
    return render(request, 'tasks/list.html', {'tasks': Task.objects.all()})


def update_tests(test_name, test_result):
    Task.objects.filter(test_name=test_name).update(result=test_result.result, log=test_result.log)


def index(request):
    tasks = Task.objects.all()
    if request.GET.get('runtest1'):
        driver = get_chrome_driver()
        driver.get("http://www.metsystems.com.au/")
        test_result = get_most_frequent_word(driver, 'summary-info')
        driver.close()
        update_tests('runtest1', test_result)
    if request.GET.get('runtest2'):
        test_result = test_links()
        update_tests('runtest2', test_result)
    if request.GET.get('runtest3'):
        test_result = create_failed_passed_test()
        update_tests('runtest3', test_result)
    context = {'tasks': tasks}
    return render(request, 'tasks/list.html', context)
