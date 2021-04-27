from pydash import map_, find
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException


def main():
    landing_elements = {
        "store": (By.CSS_SELECTOR, "a[title='Tienda']"),
        'packs': (By.CSS_SELECTOR, "a[title='Packs Ya']"),
        'change': (By.CSS_SELECTOR, "a[title='Pasate a Claro']"),
        'footer_links': (By.CSS_SELECTOR, "li[class*='footer__item__links__item'] a")
    }
    driver = create_chrome_driver()
    navigate_to(driver, 'https://www.claro.com.ar/personas')
    wait_until_all_elements_visible(driver, landing_elements['footer_links'])
    footer_link_texts = get_all_text_elements(driver, landing_elements['footer_links'])
    print(footer_link_texts)


def create_chrome_driver(headless=False):
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")

    if headless:
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1300,1080')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    return webdriver.Chrome(desired_capabilities=options.to_capabilities())


def navigate_to(driver, url):
    driver.get(url)


def get_element(driver, selector, wait_located=True, timeout=30):
    selector_type = selector[0]
    selector_value = selector[1]

    try:
        if wait_located:
            return WebDriverWait(driver, timeout).until(
                ec.presence_of_element_located(selector))
        else:
            return driver.find_element(selector_type, selector_value)
    except NoSuchElementException:
        raise NoSuchElementException(f"Could not find element by the locator: {str(selector)}")


def get_elements(driver, selector, wait_located=True, timeout=30):
    selector_type = selector[0]
    selector_value = selector[1]

    try:
        if wait_located:
            return WebDriverWait(driver, timeout).until(
                ec.presence_of_all_elements_located(selector))
        else:
            return driver.find_elements(selector_type, selector_value)
    except NoSuchElementException:
        raise NoSuchElementException(f"Could not find element by the locator: {str(selector)}")


# WAIT UNTIL ALL ELEMENTS EXISTS
def wait_until_exist_all_elements(driver, selector, timeout=20):
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.presence_of_all_elements_located(selector))


# WAIT UNTIL ALL ELEMENTS VISIBLE
def wait_until_all_elements_visible(driver, selector, timeout=20):
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.visibility_of_all_elements_located(selector))


# WAIT UNTIL ALL ELEMENTS NOT VISIBLE
def wait_until_all_element_not_visible(driver, selector, timeout=20):
    wait = WebDriverWait(driver, timeout)
    return wait.until(not ec.presence_of_all_elements_located(selector))


# GET ALL TEXT ELEMENTS
def get_all_text_elements(driver, selector, text_sanitize=True, exist_only=False):
    if exist_only:
        elements = driver.find_elements(selector[0], selector[1])
    else:
        elements = wait_until_all_elements_visible(driver, selector)
    return map_(elements, lambda x: x.text.lower().strip() if text_sanitize else x.text)


# FROM ARRAY OF ELEMENTS
def click_with_index(driver, selector, index):
    elements = wait_until_all_elements_visible(driver, selector)
    elements[index].click()


# FROM ARRAY OF ELEMENTS
def click_with_text(driver, selector, text, exist_only=False, *args):
    if exist_only:
        elements = driver.find_elements(selector[0], selector[1])
    else:
        elements = wait_until_exist_all_elements(driver, selector)
    element = find(elements, lambda x: _sanitize_text(x.text) == _sanitize_text(text))
    if element is not None:
        element.click()
    else:
        raise Exception('not exist element')


# FROM ELEMENT
def wait_until_is_visible(driver, selector, timeout=20):
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.visibility_of(selector))


# FROM ELEMENT
def wait_until_is_not_visible(driver, selector, timeout=20):
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.invisibility_of_element(selector))


def wait_until_exist(driver, selector, timeout=20):
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.presence_of_element_located(selector))


# FROM ELEMENT
def wait_until_not_exist(driver, selector, timeout=20):
    wait = WebDriverWait(driver, timeout)
    return wait.until_not(ec.presence_of_element_located(selector))


def get_element_into_view(driver, timeout=10):
    element = wait_until_exist(driver, timeout)
    if element:
        driver.execute_script('arguments[0].scrollIntoView(true);', element)


# FROM ELEMENT
def _sanitize_text(text):
    return text.lower().strip()


def take_screenshot(driver, screen_shot_name):
    driver.save_screenshot(f'temp/{screen_shot_name}')


if __name__ == '__main__':
    main()

main()
