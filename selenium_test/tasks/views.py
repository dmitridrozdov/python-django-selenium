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


def run_all(request):
    runtest1(request)
    runtest2(request)
    return runtest3(request)


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

    if request.GET.get('runtest1Log'):
        test_result = show_log('runtest1')

    if request.GET.get('runtest2Log'):
        test_result = show_log('runtest2')

    if request.GET.get('runtest3Log'):
        test_result = show_log('runtest3')

    if request.GET.get('clear'):
        cleartests(request)

    context = {'tasks': tasks, 'test_result': test_result}
    return render(request, 'tasks/list.html', context)
