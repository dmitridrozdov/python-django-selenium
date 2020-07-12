import time


def get_text_web_element(web_element):
    return web_element.text


def find_index_web_elements_list(web_elements, name):
    return [element.text for element in web_elements].index(name)


def click_web_elements_by_name(web_elements, name):
    index = find_index_web_elements_list(web_elements, name)
    web_elements[index].click()


def click_web_element_by_class_name_and_name(driver, css_selector, name):
    els = driver.find_elements_by_class_name(css_selector)
    click_web_elements_by_name(els, name)


def click_web_element_by_css_selector_and_name(driver, css_selector, name):
    els = driver.find_elements_by_css_selector(css_selector)
    click_web_elements_by_name(els, name)


def input_text_by_id(driver, id, text):
    time.sleep(1)
    driver.find_element_by_id(id).send_keys(text)
