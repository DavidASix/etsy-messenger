from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login(d):
    # Get Credentials
    c = open("private", "r").read().split()
    [u, p] = [c[0], c[1]]
    # Navigate to login page and fill out form
    d.get('https://www.etsy.com/signin')
    username = d.find_element(By.ID, 'join_neu_email_field')
    password = d.find_element(By.ID, 'join_neu_password_field')
    username.clear()
    password.clear()
    username.send_keys(u)
    password.send_keys(p)
    # Find and click login button
    submit = d.find_element(By.XPATH, "//*[@type='submit'][contains(@value, 'sign-in')]")
    submit.click()

def add_cookies(d):
    cs = open('cookies', 'r')
    lines = 0
    for cookie in cs:
        c = cookie.strip()
        c= c.split('=')
        d.add_cookie({'name': c[0], 'value': c[1]})
        lines += 1
    print('Added', lines/2, 'cookies')
    return d

def get_order_ids(d):
    # elements = d.find_elements(By.XPATH, "//a[contains(@href, '?order_id')]")
    orders = d.find_elements(By.XPATH, "//div[contains(@class, 'panel-body-row')]")
    print('Found', len(orders), 'Orders')
    # Iterate through the elements and print their tag names
    print(orders)
    for order in orders:
        order_id = order.find_element(By.XPATH, "//a[contains(@href, '?order_id')]")
        completed = order.find_element(By.XPATH, "div/div/div/div/div[@class='text-body-smaller']")
        print(order_id.get_attribute('innerText'), completed.get_attribute('innerText'))

def main():
    # Initialize the web browser
    driver = webdriver.Firefox()
    # Initially load a page to to avoid cookie aversion error
    driver.get('https://www.etsy.com')
    driver.set_window_position(0, 0, windowHandle='current')
    driver.set_window_size(900, 1000)
    # Load Auth cookies
    driver = add_cookies(driver)
    # Navigate to orders page
    driver.get("https://www.etsy.com/your/orders/sold/completed")
    try:
        print('Waiting for JS')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@href, '?order_id')]")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    get_order_ids(driver)
    # Close the web browser
    #driver.quit()

main()


